#!/usr/bin/env python3
"""Calculate hero level-up costs from the canonical HeroLevelCostTable.txt.

The repository defines the table as a step-cost table:
- the cost for a row at Level N is the cost required to advance from Level N-1 to Level N.
- therefore, the cost from StartLevel to EndLevel is the sum of the values for
  StartLevel + 1 through EndLevel.

Examples:
    python tools/hero_level_cost_calculator.py --start 1 --end 5
    python tools/hero_level_cost_calculator.py --start 168 --end 169 --heroes 3
"""

from __future__ import annotations

import argparse
from pathlib import Path


def load_cost_table(table_path: Path) -> dict[int, int]:
    """Parse the canonical HeroLevelCostTable.txt and return {level: step_cost}."""
    if not table_path.exists():
        raise ValueError(
            f"Hero cost table not found: '{table_path}'. "
            "Check that the repository contains the canonical global/HeroLevelCostTable.txt file."
        )

    table: dict[int, int] = {}
    in_data = False

    with table_path.open("r", encoding="utf-8") as handle:
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
            if not in_data:
                continue
            if line.startswith("#"):
                continue
            if line.lower().startswith("level"):
                continue

            parts = line.split()
            if len(parts) < 2:
                continue

            try:
                level = int(parts[0])
                cost = int(parts[1])
            except ValueError:
                continue

            table[level] = cost

    if not table:
        raise ValueError(
            f"No valid level/cost rows were found in '{table_path}'. "
            "The file appears to be empty or malformed."
        )

    return table


def validate_inputs(start_level: int, end_level: int, hero_count: int, cost_table: dict[int, int]) -> None:
    """Validate the requested range and count before calculating totals."""
    if start_level < 1:
        raise ValueError(
            f"Invalid start level {start_level}: hero levels start at 1. "
            "You cannot level a hero below Level 1."
        )

    if end_level <= start_level:
        raise ValueError(
            f"Invalid range {start_level} -> {end_level}: "
            "the end level must be greater than the start level."
        )

    if hero_count < 1:
        raise ValueError(
            f"Invalid hero count {hero_count}: you must level at least 1 hero."
        )

    missing_levels = [
        level
        for level in range(start_level + 1, end_level + 1)
        if level not in cost_table
    ]
    if missing_levels:
        missing = ", ".join(str(level) for level in missing_levels)
        raise ValueError(
            f"Requested range {start_level} -> {end_level} includes level(s) {missing} "
            f"that are not defined in the canonical HeroLevelCostTable. "
            "Check that your start/end levels are valid for this table."
        )


def compute_level_steps(cost_table: dict[int, int], start_level: int, end_level: int) -> list[tuple[int, int]]:
    """Return a list of (target_level, cost_to_reach_target_level) from start to end."""
    steps: list[tuple[int, int]] = []
    for target_level in range(start_level + 1, end_level + 1):
        if target_level not in cost_table:
            raise ValueError(
                f"Missing cost for level {target_level} in the HeroLevelCostTable. "
                f"This usually means the requested range is outside the table's defined levels."
            )
        steps.append((target_level, cost_table[target_level]))
    return steps


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    default_table = repo_root / "global" / "HeroLevelCostTable.txt"

    parser = argparse.ArgumentParser(
        description="Calculate hero level-up cost from a starting level to an ending level."
    )
    parser.add_argument("--start", type=int, required=True, help="Starting hero level")
    parser.add_argument("--end", type=int, required=True, help="Ending hero level")
    parser.add_argument("--heroes", type=int, default=1, help="Number of heroes to level")
    parser.add_argument(
        "--table",
        type=Path,
        default=default_table,
        help="Path to HeroLevelCostTable.txt (defaults to the repo canonical table)",
    )
    args = parser.parse_args()

    try:
        cost_table = load_cost_table(args.table)
        validate_inputs(args.start, args.end, args.heroes, cost_table)
        steps = compute_level_steps(cost_table, args.start, args.end)
    except ValueError as exc:
        raise SystemExit(f"Error: {exc}") from exc

    per_hero_total = sum(cost for _, cost in steps)
    total_for_all = per_hero_total * args.heroes

    print(f"Hero level-up calculation: {args.start} -> {args.end}")
    print(f"Heroes: {args.heroes}")
    print()

    print("Per-level step costs:")
    for target_level, cost in steps:
        print(f"  {args.start} -> {target_level}: {cost}")

    print()
    print(f"Per hero total: {per_hero_total}")
    print(f"Total for {args.heroes} hero(s): {total_for_all}")


if __name__ == "__main__":
    main()
