"""Validate MTS against its reviewed native inputs and build a production ZIP."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

from migrate_to_ck3_1_20 import CONTRACT, MOD, ROOT, framework_tools, generate
from selector_padding import LANGUAGES, generated_files

PRODUCT = "more_tenets_slots_xa_dev"
WORKSHOP_ID = "3182367229"
RELEASE_FILES = (
    "descriptor.mod", "thumbnail.png",
    "common/defines/More tradition slots.txt",
    "common/script_values/zz_mts_core_tenets_cap.txt",
    "gui/window_faith.gui", "gui/window_rite_creation.gui",
) + tuple(f"localization/{language}/religion/MTS_religion_confucianism_l_{language}.yml"
          for language in LANGUAGES) + tuple(sorted(generated_files()))
DEVELOPMENT_FILES = {"original_author_said_it_ok.png"}


def validate_localization(game: Path) -> dict:
    from translate_localization_minimax import assert_protected_tokens, parse_ck3_localization

    layout = game / "launcher/settings-layout.json"
    provider = json.loads(layout.read_text(encoding="utf-8-sig"))
    language_options = []

    def collect(value: object) -> None:
        if isinstance(value, dict):
            if value.get("name") == "language" and value.get("provider") == "lang":
                language_options.extend(option["value"] for option in value["options"])
            for child in value.values():
                collect(child)
        elif isinstance(value, list):
            for child in value:
                collect(child)

    collect(provider)
    if sorted(language_options) != sorted(f"l_{language}" for language in LANGUAGES):
        raise ValueError(f"native launcher language options changed: {language_options}")
    translated_keys = {"shangru" + suffix for suffix in
                       ("", "_adj", "_adherent", "_adherent_plural", "_desc")}
    baseline = None
    for language in LANGUAGES:
        native = game / "game/localization" / language
        if not native.is_dir():
            raise ValueError(f"native localization directory missing: {language}")
        entries = {}
        for path in sorted((MOD / "localization" / language).rglob("*.yml")):
            if path.read_text(encoding="utf-8-sig").splitlines()[0] != f"l_{language}:":
                raise ValueError(f"wrong language header: {path}")
            family = parse_ck3_localization(path)
            if entries.keys() & family.keys():
                raise ValueError(f"duplicate localization keys across files: {language}")
            entries.update(family)
        expected = translated_keys | {
            key for key in parse_ck3_localization(
                MOD / f"localization/english/religion/mts_selector_l_english.yml")}
        if entries.keys() != expected:
            raise ValueError(f"localization key coverage differs: {language}")
        for key, value in entries.items():
            if (key in translated_keys) != bool(value):
                raise ValueError(f"localization empty/value contract differs: {language} {key}")
        if baseline is None:
            baseline = entries
        assert_protected_tokens(baseline, entries)
    return {"status": "format-certified", "languages": list(LANGUAGES),
            "files": 2 * len(LANGUAGES), "keys_per_language": len(expected),
            "translated_keys_per_language": len(translated_keys),
            "intentionally_empty_keys_per_language": len(expected - translated_keys),
            "native_language_layout_sha256": hashlib.sha256(layout.read_bytes()).hexdigest(),
            "live_verified": False}


def validate(framework: Path, game: Path) -> dict:
    framework_tools(framework)
    from ck3_text_projection import blocks, masked

    projection = generate(framework, game, check=True)
    actual = {p.relative_to(MOD).as_posix() for p in MOD.rglob("*") if p.is_file()}
    if actual - DEVELOPMENT_FILES != set(RELEASE_FILES):
        raise ValueError(f"release allowlist differs: {sorted(actual ^ set(RELEASE_FILES))}")
    descriptor = (MOD / "descriptor.mod").read_text(encoding="utf-8-sig")
    if 'supported_version="1.20.0.3"' not in descriptor or 'version="10"' not in descriptor:
        raise ValueError("descriptor differs from the migrated product identity")
    if "remote_file_id" in descriptor:
        raise ValueError("inner descriptor must not contain Workshop ID")
    for relative in RELEASE_FILES:
        path = MOD / relative
        if path.suffix in {".mod", ".txt", ".gui", ".yml"}:
            if not path.read_bytes().startswith(b"\xef\xbb\xbf"):
                raise ValueError(f"UTF-8 BOM missing: {relative}")
            source = path.read_text(encoding="utf-8-sig")
            if path.suffix != ".yml":
                blocks(source)
            for old in ("tenet_zz_empty_", "doctrine_core_tenets", "FaithCreationWindow",
                        "faith_creation_clean", "on_mts_faith_creation"):
                if old in source:
                    raise ValueError(f"retired dependency {old}: {relative}")
    defines = masked((MOD / RELEASE_FILES[2]).read_text(encoding="utf-8-sig"))
    values = masked((MOD / RELEASE_FILES[3]).read_text(encoding="utf-8-sig"))
    for pattern in (r"FAITH_CORE_TENETS_CAP\s*=\s*100\b",
                    r"DEFAULT_MAX_TRADITIONS\s*=\s*10000\b"):
        if len(re.findall(pattern, defines)) != 1:
            raise ValueError("native cap contract differs")
    if not re.search(r"pam_faith_core_tenets_cap_value\s*=\s*{\s*value\s*=\s*100\s*}", values):
        raise ValueError("council cap differs from native cap")
    # Script-value IDs are merged across filenames; the native pam_values.txt
    # otherwise wins over the old mts_ filename. This guards our reviewed
    # single-mod cell; effective values still require native runtime readback.
    cap_id = "pam_faith_core_tenets_cap_value"
    native_cap_files = sorted(
        p.name for p in (game / "game/common/script_values").glob("*.txt")
        if re.search(r"(?m)^" + cap_id + r"\s*=", masked(p.read_text(encoding="utf-8-sig")))
    )
    if native_cap_files != ["pam_values.txt"]:
        raise ValueError(f"native cap definition owners changed: {native_cap_files}")
    if Path(RELEASE_FILES[3]).name <= native_cap_files[-1]:
        raise ValueError("product script-value override must load after native definition")
    localization = validate_localization(game)
    return {"status": "static-ready", "native_projection": projection,
            "localization": localization,
            "checks": ["exact-native-inputs", "reversible-native-gui", "native-controls-preserved",
                       "native-and-council-cap-100", "script-value-override-order",
                       "traditions-cap-10000", "BOM-and-braces",
                       "no-retired-dependencies", "localization-structure", "release-allowlist"],
            "release_file_count": len(RELEASE_FILES), "live_verified": False}


def build(framework: Path, destination: Path, revision: str) -> dict:
    framework_tools(framework)
    from build_release import create_manifest, manifest_bytes, write_deterministic_zip

    # The caller provides a new build directory; old attempts are preserved.
    destination.mkdir(parents=True, exist_ok=False)
    staging = destination / PRODUCT
    for relative in RELEASE_FILES:
        target = staging / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(MOD / relative, target)
    manifest = create_manifest(staging, revision, "10")
    manifest["workshop_item_id"] = WORKSHOP_ID
    (destination / f"{PRODUCT}.manifest.json").write_bytes(manifest_bytes(manifest))
    archive = destination / f"{PRODUCT}.zip"
    write_deterministic_zip(staging, archive, manifest)
    return {"manifest": manifest, "zip_sha256": hashlib.sha256(archive.read_bytes()).hexdigest()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--framework", type=Path, required=True)
    parser.add_argument("--game", type=Path, required=True)
    parser.add_argument("--output", type=Path, help="new build directory; omit for validation only")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        result = validate(args.framework, args.game)
        revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        with tempfile.TemporaryDirectory(prefix="mts-build-") as temp:
            first = build(args.framework, Path(temp) / "a", revision)
            second = build(args.framework, Path(temp) / "b", revision)
            if first != second:
                raise ValueError("two production builds differ")
        result["reproducible_build"] = first
        result["input_contract"] = json.loads(CONTRACT.read_text(encoding="utf-8"))
        result["framework_commit"] = subprocess.check_output(
            ["git", "-C", str(args.framework), "rev-parse", "HEAD"], text=True).strip()
        if args.output:
            result["output"] = str(args.output.resolve())
            build(args.framework, args.output, revision)
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({k: v for k, v in result.items()
                          if k not in {"input_contract", "reproducible_build"}}, indent=2))
        return 0
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"RED: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
