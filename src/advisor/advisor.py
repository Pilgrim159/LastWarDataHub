from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List

from .parser import FileParser


@dataclass
class AdvisorSummary:
    account: str
    schema_files: List[str] = field(default_factory=list)
    schema_counts: Dict[str, int] = field(default_factory=dict)
    building_priorities: List[str] = field(default_factory=list)


class Advisor:
    """A lightweight advisor that reads player data files and summarizes state."""

    def __init__(self, repo_root: str | Path):
        self.repo_root = Path(repo_root).resolve()
        self.players_dir = self.repo_root / "players"

    def load_player_files(self) -> List[Dict[str, object]]:
        parsed_files = []
        if not self.players_dir.exists():
            return parsed_files

        for path in sorted(self.players_dir.glob("*.txt")):
            parsed = FileParser.parse_file(path)
            parsed_files.append({
                "path": str(path.relative_to(self.repo_root)),
                "metadata": parsed.metadata,
                "columns": parsed.columns,
                "rows": parsed.rows,
            })
        return parsed_files

    def summarize(self) -> AdvisorSummary:
        player_files = self.load_player_files()
        schema_counts: Dict[str, int] = {}
        schema_files: List[str] = []
        building_priorities: List[str] = []

        for file_info in player_files:
            schema_name = file_info["metadata"].get("Schema")
            if not schema_name:
                continue
            schema_files.append(file_info["path"])
            schema_counts[schema_name] = schema_counts.get(schema_name, 0) + 1

            if schema_name == "BuildingStatus":
                for row in file_info["rows"]:
                    status = row.get("Status", "")
                    name = row.get("BuildingName", "")
                    priority = row.get("Priority", "")
                    if name:
                        building_priorities.append(f"{name}:{status}:{priority}")

        account = "unknown"
        for file_info in player_files:
            scope = file_info["metadata"].get("Scope", "")
            if "Account:" in scope:
                account = scope.split("Account:", 1)[1].strip()
                break

        return AdvisorSummary(
            account=account,
            schema_files=schema_files,
            schema_counts=schema_counts,
            building_priorities=building_priorities,
        )

    def recommend_next_upgrades(self) -> List[str]:
        recommendations: List[str] = []
        for file_info in self.load_player_files():
            if file_info["metadata"].get("Schema") != "BuildingStatus":
                continue

            rows = file_info["rows"]
            for row in rows:
                if row.get("Status") == "Upgrading":
                    recommendations.append(
                        f"{row.get('BuildingName')} is upgrading from {row.get('CurrentLevel')} to {row.get('TargetLevel')}"
                    )
                    continue
                if row.get("TargetLevel") and row.get("CurrentLevel"):
                    if int(row["TargetLevel"]) > int(row["CurrentLevel"]):
                        recommendations.append(
                            f"{row.get('BuildingName')} should be prioritized: current {row.get('CurrentLevel')}, target {row.get('TargetLevel')}, priority {row.get('Priority')}"
                        )

        return recommendations[:10]
