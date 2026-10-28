#!/usr/bin/env python3
"""Create a new active log and update CURRENT_LOG.txt.

This is a thin wrapper used to create a new log file via the repo's script.
"""

from pathlib import Path
from subprocess import run

repo_root = Path(__file__).resolve().parents[1]
script = repo_root / "tools" / "create_active_log.py"

# Use the current real timestamp at runtime.
cmd = [
    "python",
    str(script),
    "--commander", "F1NE",
    "--scope", "Account:F1NE",
    "--description", "Current strategic state, event timing, and near-term build priorities for F1NE.",
    "--vip-level", "11",
    "--vip-points", "380,560 / 500,000",
    "--vip-timer", "81d 23:00",
    "--hq", "33",
    "--tank-center", "33",
    "--wall", "33 in progress",
    "--wall-timer", "24d 07:14",
    "--goal", "finish Wall 33, then trigger HQ 34",
    "--coin-available", "38.0M",
    "--coin-inventory", "900.9M",
    "--construction-speedups", "250d 05:53",
    "--research-speedups", "245d 07:50",
    "--training-speedups", "271d 19:03",
    "--healing-speedups", "065d 06:51",
    "--note", "Do not spend Coin on tank hero upgrades while the tank heroes are capped at 165.",
    "--note", "Hold Coin for the HQ 34 unlock.",
    "--note", "Use construction speedups on the Wall 33 build unless a stronger event window materially improves the value of waiting.",
]

result = run(cmd, cwd=str(repo_root), capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print(result.stderr)
