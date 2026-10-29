from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Dict, List, Tuple

from .parser import FileParser


@dataclass
class AdvisorSummary:
    account: str
    schema_files: List[str] = field(default_factory=list)
    schema_counts: Dict[str, int] = field(default_factory=dict)
    building_priorities: List[str] = field(default_factory=list)
    research_priorities: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class DataFreshness:
    path: str
    schema: str
    recorded_date: str | None
    age_days: int | None
    max_age_days: int
    status: str

    def __str__(self) -> str:
        recorded_date = self.recorded_date or "missing"
        age = f"{self.age_days}d" if self.age_days is not None else "unknown"
        return (
            f"{self.status}: {self.path} (schema={self.schema}, "
            f"date={recorded_date}, age={age}, limit={self.max_age_days}d)"
        )


class Advisor:
    """A schema-aware advisor that reads player data files and produces simple upgrade guidance."""

    INVENTORY_MAX_AGE_DAYS = 7
    PLAYER_DATA_MAX_AGE_DAYS = 30

    def __init__(self, repo_root: str | Path):
        self.repo_root = Path(repo_root).resolve()
        self.players_dir = self.repo_root / "players"
        self.schema_dir = self.repo_root / "schema"

        try:
            from .registry import SchemaRegistry
            self.registry = SchemaRegistry(self.repo_root)
            self.registry.load()
        except Exception:
            self.registry = None

    def load_player_files(self) -> List[Dict[str, object]]:
        parsed_files: List[Dict[str, object]] = []
        if not self.players_dir.exists():
            return parsed_files

        for path in sorted(self.players_dir.glob("*.txt")):
            parsed = FileParser.parse_file(path)
            parsed_files.append(
                {
                    "path": str(path.relative_to(self.repo_root)),
                    "metadata": parsed.metadata,
                    "columns": parsed.columns,
                    "rows": parsed.rows,
                }
            )
        return parsed_files

    def data_freshness_report(self, as_of: date | None = None) -> List[DataFreshness]:
        """Report source dates and freshness for each current player file."""
        reference_date = as_of or date.today()
        report: List[DataFreshness] = []

        for file_info in self.load_player_files():
            metadata = file_info["metadata"]
            schema = str(metadata.get("Schema") or "Unknown")
            max_age_days = (
                self.INVENTORY_MAX_AGE_DAYS
                if schema == "ResourceInventory"
                else self.PLAYER_DATA_MAX_AGE_DAYS
            )
            recorded_date_value = metadata.get("Date")
            recorded_date = str(recorded_date_value) if recorded_date_value else None
            age_days = None

            if recorded_date:
                try:
                    source_date = date.fromisoformat(recorded_date)
                except ValueError:
                    status = "UNKNOWN"
                else:
                    age_days = (reference_date - source_date).days
                    if age_days < 0:
                        status = "FUTURE"
                    elif age_days > max_age_days:
                        status = "STALE"
                    else:
                        status = "CURRENT"
            else:
                status = "UNKNOWN"

            report.append(
                DataFreshness(
                    path=str(file_info["path"]),
                    schema=schema,
                    recorded_date=recorded_date,
                    age_days=age_days,
                    max_age_days=max_age_days,
                    status=status,
                )
            )

        return report

    def summarize(self) -> AdvisorSummary:
        player_files = self.load_player_files()
        schema_counts: Dict[str, int] = {}
        schema_files: List[str] = []
        building_priorities: List[str] = []
        research_priorities: List[str] = []

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

            if schema_name == "TechTreeStatus":
                for row in file_info["rows"]:
                    node_id = row.get("NodeID", "")
                    status = row.get("Status", "")
                    current = row.get("CurrentLevel", "")
                    if node_id:
                        research_priorities.append(f"{node_id}:{status}:{current}")

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
            research_priorities=research_priorities,
        )

    def _normalize_int(self, value: object) -> int:
        if value is None:
            return 0
        if isinstance(value, str):
            value = value.strip()
            if value in {"", "-", "None"}:
                return 0
            try:
                return int(value)
            except ValueError:
                return 0
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0

    def recommend_best_next_upgrade(self) -> List[str]:
        recommendations: List[str] = []

        for file_info in self.load_player_files():
            metadata = file_info["metadata"]
            schema_name = metadata.get("Schema")
            rows = file_info["rows"]

            if schema_name == "BuildingStatus":
                for row in rows:
                    name = row.get("BuildingName", "")
                    if not name:
                        continue
                    status = row.get("Status", "")
                    current = self._normalize_int(row.get("CurrentLevel"))
                    target = self._normalize_int(row.get("TargetLevel"))
                    priority = self._normalize_int(row.get("Priority"))

                    if status == "Upgrading":
                        recommendations.append(
                            f"BUILDING|{name}|status={status}|current={current}|target={target}|priority={priority}"
                        )
                    elif target > current:
                        recommendations.append(
                            f"BUILDING|{name}|status={status}|current={current}|target={target}|priority={priority}"
                        )

            elif schema_name == "TechTreeStatus":
                for row in rows:
                    node_id = row.get("NodeID", "")
                    if not node_id:
                        continue
                    status = row.get("Status", "")
                    current = self._normalize_int(row.get("CurrentLevel"))
                    if status == "-" and current < 10:
                        recommendations.append(
                            f"RESEARCH|{node_id}|status={status}|current={current}"
                        )

        recommendations.sort(key=self._sort_key)
        return recommendations[:10]

    def recommend_next_upgrades(self) -> List[str]:
        return self.recommend_best_next_upgrade()

    @staticmethod
    def _sort_key(item: str) -> Tuple[int, str]:
        kind, *rest = item.split("|")
        if kind == "BUILDING":
            priority = 99
            for segment in rest:
                if segment.startswith("priority="):
                    priority = int(segment.split("=", 1)[1])
                    break
            return (0, f"{priority:03d}|{item}")
        return (1, item)

    def load_schemas(self) -> Dict[str, Path]:
        if self.registry is None:
            return {}
        mapping: Dict[str, Path] = {}
        for name, rel_path in self.registry.load().items():
            mapping[name] = (self.repo_root / rel_path).resolve()
        return mapping
