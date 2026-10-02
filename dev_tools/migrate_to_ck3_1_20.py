"""Project the exact CK3 1.20.0.3 GUI with scrollable MTS tenet grids."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "more_tenets_slots_xa_dev"
CONTRACT = ROOT / "dev_tools/ck3_1_20_0_3_sources.json"
HEADER = "# GENERATED FILE - CK3 1.20.0.3 native GUI with MTS scrollable tenet grids\n"


def framework_tools(framework: Path) -> None:
    directory = framework.resolve() / "tools"
    if not (directory / "ck3_text_projection.py").is_file():
        raise ValueError("framework lacks ck3_text_projection; use commit 36a225237 or newer")
    sys.path.insert(0, str(directory))


def scroll_grid(native: str, key: str, name: str, height: int,
                creation: bool = False) -> tuple[str, str]:
    from ck3_text_projection import named_block

    span = named_block(native, key, name)
    original = native[span.start:span.end]
    indent = native[native.rfind("\n", 0, span.start) + 1:span.start]
    body = native[span.opening + 1:span.end - 1]
    visibility = ""
    if not creation:
        # Keep visibility on the scrollbox itself, so the hidden grid uses no space.
        match = re.search(r'\n\s*visible = "[^\n]+"', body)
        if match is None:
            raise ValueError("native tenet grid visibility is missing")
        visibility = "\n" + indent + "\t" + match.group().strip()
        body = body[:match.start()] + body[match.end():]
    else:
        body = body.replace("spacing = 45", "spacing = 20", 1)
        body = body.replace('name = "tenets_grid"',
                            'name = "tenets_grid"\n' + indent + '\twrap_count = 3', 1)
    # Move the unchanged native card data model and controls two levels deeper.
    nested = "\n".join("\t\t" + line if line else line for line in body.split("\n"))
    replacement = (
        "scrollbox = {\n" + indent + '\tname = "mts_' + name + '_scroll"'
        + visibility + "\n" + indent + "\tsize = { 100% " + str(height) + " }"
        + "\n" + indent + "\tlayoutpolicy_horizontal = expanding"
        + "\n" + indent + "\tblockoverride \"scrollbox_content\" {"
        + "\n" + indent + "\t\tflowcontainer = {" + nested
        + "}\n" + indent + "\t}\n" + indent + "}"
    )
    return original, replacement


def changes(native: str, relative: str) -> list[tuple[str, str]]:
    if relative == "gui/window_rite_creation.gui":
        return [scroll_grid(native, "hbox", "tenets_grid", 300, creation=True)]
    return [scroll_grid(native, "flowcontainer", "doctrines_grid_core_tenets", 250),
            scroll_grid(native, "flowcontainer", "doctrines_compact_grid_core_tenets", 130)]


def generate(framework: Path, game: Path, check: bool = False) -> dict:
    framework_tools(framework)
    from ck3_installation import installed_game_version
    from ck3_text_projection import blocks, project, recover

    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    exe = game / "binaries/ck3.exe"
    if installed_game_version(exe) != contract["version"]:
        raise ValueError("installed version differs from the reviewed contract")
    if hashlib.sha256(exe.read_bytes()).hexdigest() != contract["exe_sha256"]:
        raise ValueError("installed executable differs from the reviewed contract")
    for relative, pin in contract["sources"].items():
        if hashlib.sha256((game / "game" / relative).read_bytes()).hexdigest() != pin["sha256"]:
            raise ValueError(f"native input changed: {relative}")
    results = {}
    for relative in ("gui/window_faith.gui", "gui/window_rite_creation.gui"):
        native = (game / "game" / relative).read_text(encoding="utf-8-sig")
        patches = changes(native, relative)
        expected = contract["sources"][relative]["normalized_sha256"]
        body = project(native, expected, patches)
        blocks(body)
        if recover(body, expected, patches) != native:
            raise ValueError(f"native recovery differs: {relative}")
        content = (HEADER + body).encode("utf-8-sig")
        target = MOD / relative
        if check:
            if target.read_bytes() != content:
                raise ValueError(f"generated output differs: {relative}")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        results[relative] = {"sha256": hashlib.sha256(content).hexdigest(),
                             "native_recovery": "PASS", "changes": len(patches)}
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--framework", type=Path, required=True)
    parser.add_argument("--game", type=Path, required=True, help="CK3 installation root")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(generate(args.framework, args.game, args.check), indent=2))
        return 0
    except (OSError, ValueError) as error:
        print(f"RED: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
