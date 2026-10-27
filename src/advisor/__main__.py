from __future__ import annotations

import argparse
from pathlib import Path

from .advisor import Advisor


def main() -> None:
    parser = argparse.ArgumentParser(description="Schema-aware Last War advisor")
    parser.add_argument("--repo-root", type=str, default=".", help="Repository root directory")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    advisor = Advisor(repo_root)
    summary = advisor.summarize()

    print(f"Account: {summary.account}")
    print("Schemas loaded:")
    for schema_name, count in sorted(summary.schema_counts.items()):
        print(f"  - {schema_name}: {count} file(s)")

    print("\nRecommended priorities:")
    for item in advisor.recommend_next_upgrades():
        print(f"  - {item}")


if __name__ == "__main__":
    main()
