"""Hold the framework launch lock for an isolated, manually reviewed MTS cell.

This launcher only reports process state. Acceptance results are recorded
separately from game logs, saved state and reviewed screenshots.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import threading
import time

from migrate_to_ck3_1_20 import MOD, ROOT, framework_tools
from validate_and_build import build, validate


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--framework", type=Path, required=True)
    parser.add_argument("--game", type=Path, required=True)
    parser.add_argument("--warm-userdir", type=Path, required=True)
    parser.add_argument("--attempt", type=Path, required=True)
    parser.add_argument("--bus-cli", type=Path, required=True)
    parser.add_argument("--screen-task", required=True)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    framework_tools(args.framework)
    sys.path.insert(0, str(args.framework / "ck3_autonomous_player/src"))
    import psutil
    import win32con
    import win32gui
    import win32process
    from xar_autoplayer.locking import exclusive_launch_lock

    validate(args.framework, args.game)
    args.attempt.mkdir(parents=True, exist_ok=False)
    userdir = args.attempt.resolve() / "userdir"
    userdir.mkdir()
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    built = build(args.framework, userdir / "production", revision)
    (userdir / "mod").mkdir()
    target = userdir / "production/more_tenets_slots_xa_dev"
    (userdir / "mod/mts.mod").write_text(
        (target / "descriptor.mod").read_text(encoding="utf-8-sig")
        + f'\npath="{target.as_posix()}"\n', encoding="utf-8", newline="\n")
    (userdir / "dlc_load.json").write_text(json.dumps(
        {"enabled_mods": ["mod/mts.mod"], "disabled_dlcs": []}), encoding="utf-8")
    settings = (args.warm_userdir / "pdx_settings.txt").read_text(encoding="utf-8-sig")
    settings = re.sub(r'("language"\s*=\s*{\s*version=\d+\s*value=)"[^"\n]+"',
                      r'\1"l_english"', settings)
    (userdir / "pdx_settings.txt").write_text(settings, encoding="utf-8", newline="\n")
    for filename in ("shadercache", "shadercache.cache", "cache", "pops_gdpr.dat"):
        source = args.warm_userdir / filename
        if source.is_file():
            shutil.copy2(source, userdir / filename)
        elif source.is_dir():
            shutil.copytree(source, userdir / filename)
    bus = [sys.executable, str(args.bus_cli), "--bus-dir", str(args.bus_cli.parent.parent),
           "--expected-cli-sha256",
           hashlib.sha256(args.bus_cli.read_bytes()).hexdigest().upper()]

    def call_bus(*argv: str) -> dict:
        result = subprocess.run(bus + list(argv), capture_output=True, text=True, encoding="utf-8")
        if result.returncode:
            raise RuntimeError(result.stdout + result.stderr)
        return json.loads(result.stdout)

    call_bus("poll", "--task", args.screen_task, "--ack")
    taskset = call_bus("list")["tasks"]
    owners = [t["task_id"] for t in taskset if t.get("state") == "running"
              and "ck3-screen:acquired" in t.get("resources", []) and not t.get("stale")]
    if owners != [args.screen_task]:
        raise RuntimeError(f"screen owners differ: {owners}")
    stop = threading.Event()

    def control() -> None:
        for line in sys.stdin:
            if line.strip() == "stop":
                stop.set()
                return

    threading.Thread(target=control, daemon=True).start()
    exe = args.game / "binaries/ck3.exe"
    command = [str(exe), "-debug_mode", "-gdpr-compliant", f"-userdir={userdir}"]
    with exclusive_launch_lock(exe):
        if any((p.info["name"] or "").lower() == "ck3.exe"
               for p in psutil.process_iter(["name"])):
            raise RuntimeError("CK3 already running")
        process = subprocess.Popen(command, cwd=exe.parent)
        record = {"run_id": args.run_id, "pid": process.pid, "command": command,
                  "source_commit": revision, "production": built,
                  "launched_at_utc": datetime.now(timezone.utc).isoformat(),
                  "status": "launched-unverified"}
        receipt = args.attempt / "session.json"
        receipt.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"pid": process.pid, "userdir": str(userdir),
                          "run_id": args.run_id}), flush=True)
        deadline = time.monotonic() + 1800
        heartbeat = time.monotonic()
        try:
            while process.poll() is None and not stop.wait(1):
                if time.monotonic() >= deadline or (args.attempt / "STOP").exists():
                    stop.set()
                if time.monotonic() - heartbeat > 30:
                    tasks = call_bus("list")["tasks"]
                    owner = next(t for t in tasks if t["task_id"] == args.screen_task)
                    call_bus("heartbeat", "--task", args.screen_task,
                             "--expected-sequence", str(owner["last_sequence"]))
                    heartbeat = time.monotonic()
        finally:
            # A failed lease renewal must also stop our own game process.
            if process.poll() is None:
                def close(hwnd: int, _: object) -> None:
                    if win32process.GetWindowThreadProcessId(hwnd)[1] == process.pid:
                        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                win32gui.EnumWindows(close, None)
                try:
                    process.wait(timeout=30)
                except subprocess.TimeoutExpired:
                    process.terminate()
                    process.wait(timeout=15)
            record.update(status="process-exited-unverified", exit_code=process.returncode,
                          ended_at_utc=datetime.now(timezone.utc).isoformat())
            receipt.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            print(json.dumps({"exit_code": process.returncode}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
