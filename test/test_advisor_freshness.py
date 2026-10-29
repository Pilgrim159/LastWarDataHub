from datetime import date
from pathlib import Path
import tempfile
import unittest

from src.advisor import Advisor


class AdvisorFreshnessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.temp_dir.name)
        (self.repo_root / "players").mkdir()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_player_file(self, name: str, schema: str, recorded_date: str | None) -> None:
        date_line = f"Date: {recorded_date}\n" if recorded_date is not None else ""
        path = self.repo_root / "players" / name
        path.write_text(
            "Header:Begin\n"
            f"Schema: {schema}\n"
            f"{date_line}"
            "Header:End\n"
            "Data:Begin\n"
            "Data:End\n",
            encoding="utf-8",
        )

    def test_inventory_uses_seven_day_threshold(self) -> None:
        self.write_player_file("inventory.txt", "ResourceInventory", "2026-10-22")
        self.write_player_file("buildings.txt", "BuildingStatus", "2026-09-29")

        report = Advisor(self.repo_root).data_freshness_report(date(2026, 10, 29))

        by_path = {Path(item.path).name: item for item in report}
        self.assertEqual("CURRENT", by_path["inventory.txt"].status)
        self.assertEqual("CURRENT", by_path["buildings.txt"].status)
        self.assertEqual(7, by_path["inventory.txt"].age_days)
        self.assertEqual(30, by_path["buildings.txt"].age_days)
        self.assertEqual(7, by_path["inventory.txt"].max_age_days)
        self.assertEqual(30, by_path["buildings.txt"].max_age_days)

    def test_stale_data_is_flagged_past_threshold(self) -> None:
        self.write_player_file("inventory.txt", "ResourceInventory", "2026-10-21")
        self.write_player_file("buildings.txt", "BuildingStatus", "2026-09-28")

        report = Advisor(self.repo_root).data_freshness_report(date(2026, 10, 29))

        self.assertTrue(all(item.status == "STALE" for item in report))

    def test_missing_invalid_and_future_dates_are_not_current(self) -> None:
        self.write_player_file("missing.txt", "BuildingStatus", None)
        self.write_player_file("invalid.txt", "BuildingStatus", "not-a-date")
        self.write_player_file("future.txt", "BuildingStatus", "2026-10-30")

        report = Advisor(self.repo_root).data_freshness_report(date(2026, 10, 29))

        by_path = {Path(item.path).name: item for item in report}
        self.assertEqual("UNKNOWN", by_path["missing.txt"].status)
        self.assertEqual("UNKNOWN", by_path["invalid.txt"].status)
        self.assertEqual("FUTURE", by_path["future.txt"].status)
        self.assertIsNone(by_path["missing.txt"].age_days)
        self.assertIsNone(by_path["invalid.txt"].age_days)
        self.assertEqual(-1, by_path["future.txt"].age_days)


if __name__ == "__main__":
    unittest.main()
