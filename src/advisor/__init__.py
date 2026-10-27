from pathlib import Path

from src.advisor import Advisor
from src.advisor.registry import SchemaRegistry


def test_registry_loads_schema_map():
    repo_root = Path(__file__).resolve().parents[1]
    registry = SchemaRegistry(repo_root)
    mapping = registry.load()

    assert "BuildingStatus" in mapping
    assert mapping["BuildingStatus"].endswith("Building_Status_Spec.md")


def test_advisor_summarizes_player_files():
    repo_root = Path(__file__).resolve().parents[1]
    advisor = Advisor(repo_root)
    summary = advisor.summarize()

    assert summary.account == "F1NE"
    assert summary.schema_counts["BuildingStatus"] >= 1
    assert summary.schema_counts["TechTreeStatus"] >= 1


def test_best_next_upgrade_prioritizes_building_and_research():
    repo_root = Path(__file__).resolve().parents[1]
    advisor = Advisor(repo_root)
    recommendations = advisor.recommend_best_next_upgrade()

    assert recommendations
    assert any(item.startswith("BUILDING|") for item in recommendations)
    assert any(item.startswith("RESEARCH|") for item in recommendations)
