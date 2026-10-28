#!/usr/bin/env python3
"""Create a timestamped active log and update the current active-log pointer.

This script creates a new log under logs/active/ using a local Mountain Time timestamp,
then writes the filename to logs/active/CURRENT_LOG.txt.
It includes the standard sections requested for strategic state, resource snapshot,
weekly schedule, and reset timing, and notes missing values explicitly instead of
inventing data when information is unavailable.
"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

MT = ZoneInfo("America/Denver")


def now_local() -> datetime:
    return datetime.now(MT)


def generate_filename(dt: datetime) -> str:
    return dt.strftime("%Y%m%d_%H%M%S_log")


def ensure_directories(repo_root: Path) -> tuple[Path, Path]:
    active_dir = repo_root / "logs" / "active"
    active_dir.mkdir(parents=True, exist_ok=True)
    current_pointer = active_dir / "CURRENT_LOG.txt"
    return active_dir, current_pointer


def reset_note_for(dt: datetime) -> str:
    if dt.dst() is not None:
        return "Reset occurs at 8:00PM when Daylight Saving Time is active."
    return "Reset occurs at 7:00PM when Standard Time is active."


def format_missing(label: str) -> str:
    return f"Missing data: {label} not available in current repo files or inputs."


def parse_resource_inventory(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values

    in_data = False
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith("Header:Begin") or line.startswith("Header:End"):
                continue
            if line.startswith("Data:Begin"):
                in_data = True
                continue
            if line.startswith("Data:End"):
                break
            if not in_data or "|" not in line:
                continue

            parts = [part.strip() for part in line.split("|")]
            if len(parts) < 6:
                continue

            _, _, item, _, packet_count, _ = parts[:6]
            if not item or item.startswith("#"):
                continue

            normalized = item.strip()
            if normalized in {"Food", "Iron", "Coin", "Oil", "Diamonds", "Hero_EXP", "Stamina"}:
                values[normalized] = packet_count.strip()

    return values


def build_default_strategic_state(cli_values: dict[str, str]) -> list[str]:
    lines: list[str] = []
    lines.append("[1. STRATEGIC STATE]")

    for key, label in [
        ("vip_level", "VIP Level"),
        ("vip_points", "VIP Points"),
        ("vip_timer", "VIP Timer"),
    ]:
        value = cli_values.get(key)
        lines.append(f"- {label}: {value if value else format_missing(label)}")

    for key, label in [
        ("hq", "HQ"),
        ("tank_center", "Tank Center"),
        ("wall", "Wall"),
        ("wall_timer", "Wall Timer"),
    ]:
        value = cli_values.get(key)
        lines.append(f"- {label}: {value if value else format_missing(label)}")

    goal = cli_values.get("goal")
    lines.append(f"- Immediate Goal: {goal if goal else format_missing('Immediate Goal')}")
    return lines


def build_default_resource_snapshot(repo_root: Path, cli_values: dict[str, str]) -> list[str]:
    lines: list[str] = []
    lines.append("[2. RESOURCE SNAPSHOT]")

    resource_inventory = parse_resource_inventory(repo_root / "players" / "F1NE_Resource_Inventory.txt")
    resource_pairs = [
        ("Coin (Available)", "Coin", cli_values.get("coin_available")),
        ("Coin (Inventory)", "Coin", cli_values.get("coin_inventory")),
        ("Iron", "Iron", cli_values.get("iron")),
        ("Food", "Food", cli_values.get("food")),
        ("Oil", "Oil", cli_values.get("oil")),
        ("Diamonds", "Diamonds", cli_values.get("diamonds")),
        ("Hero_EXP", "Hero_EXP", cli_values.get("hero_exp")),
    ]

    for label, key, cli_value in resource_pairs:
        value = cli_value or resource_inventory.get(key)
        lines.append(f"- {label}: {value if value else format_missing(label)}")

    for speedup_label, cli_key in [
        ("Construction Speedups", "construction_speedups"),
        ("Research Speedups", "research_speedups"),
        ("Training Speedups", "training_speedups"),
        ("Healing Speedups", "healing_speedups"),
    ]:
        value = cli_values.get(cli_key)
        lines.append(f"- {speedup_label}: {value if value else format_missing(speedup_label)}")

    return lines


def build_weekly_schedule() -> list[str]:
    lines: list[str] = []
    lines.append("[3. WEEKLY SCHEDULE]")
    for day, activity in [
        ("Monday", "Radar Training"),
        ("Tuesday", "City Building"),
        ("Wednesday", "Tech Research"),
        ("Thursday", "Hero Training"),
        ("Friday", "Total Mobilization"),
        ("Saturday", "Enemy Buster"),
    ]:
        lines.append(f"{day} - {activity}")
    return lines


def build_reset_timing(dt: datetime) -> list[str]:
    lines: list[str] = []
    lines.append("[4. RESET TIMING]")
    if dt.dst() is not None:
        lines.append("- Reset occurs at 8:00PM when Daylight Saving Time is active.")
    else:
        lines.append("- Reset occurs at 7:00PM when Standard Time is active.")
    lines.append("- In 2026, DST ends at 2:00AM MDT on Sunday 01 November 2026.")
    return lines


def build_log_document(repo_root: Path, commander: str, scope: str, description: str, version: str, timezone: str, now: datetime, notes: list[str], cli_values: dict[str, str]) -> list[str]:
    lines: list[str] = [
        "Header:Begin",
        "FileType: Log_File",
        f"Commander: {commander}",
        f"Date: {now.strftime('%Y-%m-%d')}",
        f"Time: {now.strftime('%H:%M:%S')}",
        f"Timezone: {timezone}",
        "Status: Active",
        f"Scope: {scope}",
        f"Version: {version}",
        f"Description: {description}",
        "Header:End",
        "",
        "Data:Begin",
    ]
    lines.extend(build_default_strategic_state(cli_values))
    lines.extend(build_default_resource_snapshot(repo_root, cli_values))
    lines.extend(build_weekly_schedule())
    lines.extend(build_reset_timing(now))
    if notes:
        lines.append("[5. NOTES]")
        for note in notes:
            lines.append(f"- {note}")
    lines.append("Data:End")
    lines.append("")
    return lines


def write_pointer(current_pointer: Path, filename: str) -> None:
    current_pointer.write_text(f"{filename}\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a new active log file and update CURRENT_LOG.txt.")
    parser.add_argument("--commander", default="F1NE")
    parser.add_argument("--scope", default="Account:F1NE")
    parser.add_argument("--description", default="Current strategic state, event timing, and near-term build priorities for F1NE.")
    parser.add_argument("--version", default="1.0")
    parser.add_argument("--timezone", default="MT")
    parser.add_argument("--note", action="append", default=[])
    parser.add_argument("--vip-level")
    parser.add_argument("--vip-points")
    parser.add_argument("--vip-timer")
    parser.add_argument("--hq")
    parser.add_argument("--tank-center")
    parser.add_argument("--wall")
    parser.add_argument("--wall-timer")
    parser.add_argument("--goal")
    parser.add_argument("--coin-available")
    parser.add_argument("--coin-inventory")
    parser.add_argument("--iron")
    parser.add_argument("--food")
    parser.add_argument("--oil")
    parser.add_argument("--diamonds")
    parser.add_argument("--hero-exp")
    parser.add_argument("--construction-speedups")
    parser.add_argument("--research-speedups")
    parser.add_argument("--training-speedups")
    parser.add_argument("--healing-speedups")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    active_dir, current_pointer = ensure_directories(repo_root)
    now = now_local()
    target_name = generate_filename(now)
    target_path = active_dir / target_name

    cli_values = {
        "vip_level": args.vip_level,
        "vip_points": args.vip_points,
        "vip_timer": args.vip_timer,
        "hq": args.hq,
        "tank_center": args.tank_center,
        "wall": args.wall,
        "wall_timer": args.wall_timer,
        "goal": args.goal,
        "coin_available": args.coin_available,
        "coin_inventory": args.coin_inventory,
        "iron": args.iron,
        "food": args.food,
        "oil": args.oil,
        "diamonds": args.diamonds,
        "hero_exp": args.hero_exp,
        "construction_speedups": args.construction_speedups,
        "research_speedups": args.research_speedups,
        "training_speedups": args.training_speedups,
        "healing_speedups": args.healing_speedups,
    }

    if args.dry_run:
        print(f"Would create: {target_path}")
        print(f"Would update: {current_pointer}")
        return

    if target_path.exists():
        raise FileExistsError(f"Target log already exists: {target_path}")

    document = build_log_document(repo_root, args.commander, args.scope, args.description, args.version, args.timezone, now, args.note, cli_values)
    target_path.write_text("\n".join(document), encoding="utf-8")
    write_pointer(current_pointer, target_name)

    print(f"Created active log: {target_path}")
    print(f"Updated current pointer: {current_pointer}")


if __name__ == "__main__":
    main()
