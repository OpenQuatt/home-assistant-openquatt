from __future__ import annotations

import builtins
from datetime import date
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parent.parent
EXPORTER_PATH = (
    ROOT
    / "tools"
    / "quatt-insights-export"
    / "openquatt_quatt_insights_export.py"
)


class FakeService:
    def __init__(self):
        self.calls = []
        self.response = {"graph": []}

    def __call__(self, *args, **kwargs):
        return lambda function: function

    def has_service(self, domain, name):
        return (domain, name) == ("quatt", "get_cic_insights")

    def call(self, domain, name, **kwargs):
        self.calls.append((domain, name, kwargs))
        return self.response


class FakeTask:
    def sleep(self, seconds):
        return None


class FakeState:
    def __init__(self):
        self.calls = []

    def set(self, *args):
        self.calls.append(args)


class FakeLog:
    def info(self, message):
        return None


class QuattInsightsExportTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original_builtins = {}
        cls.fake_service = FakeService()
        injected = {
            "pyscript_executor": lambda function: function,
            "service": cls.fake_service,
            "task": FakeTask(),
            "state": FakeState(),
            "log": FakeLog(),
        }
        for name, value in injected.items():
            cls.original_builtins[name] = getattr(builtins, name, None)
            setattr(builtins, name, value)

        spec = importlib.util.spec_from_file_location("quatt_insights_export", EXPORTER_PATH)
        cls.exporter = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.exporter)

    @classmethod
    def tearDownClass(cls):
        for name, original in cls.original_builtins.items():
            if original is None:
                delattr(builtins, name)
            else:
                setattr(builtins, name, original)

    def setUp(self):
        self.fake_service.calls.clear()
        self.fake_service.response = {"graph": []}

    def test_day_source_uses_importable_top_level_totals(self):
        raw = {
            "from": "2024-01-01T00:00:00Z",
            "to": "2024-01-02T00:00:00Z",
            "totalHpElectric": 1200,
            "totalHpHeat": 4200,
            "totalBoilerHeat": 300,
            "graph": [{"timestamp": "2024-01-01T12:00:00Z", "hpHeat": 4200}],
        }

        day = self.exporter._normalise_day_from_totals(raw, "2024-01-01", True)

        self.assertEqual(
            {
                "date": "2024-01-01",
                "energy_hp_electric": 1200,
                "energy_hp_heat": 4200,
                "energy_boiler_heat": 300,
                "raw_sample": raw,
            },
            day,
        )

    def test_month_source_maps_utc_timestamp_to_local_day(self):
        raw = {
            "graph": [
                {
                    "timestamp": "2024-01-01T23:30:00Z",
                    "hpElectric": 100,
                    "hpHeat": 400,
                    "boilerHeat": 20,
                }
            ]
        }

        days = self.exporter._normalise_days_from_month(
            raw,
            date(2024, 1, 1),
            date(2024, 1, 31),
            False,
            "Europe/Amsterdam",
        )

        self.assertEqual(
            [
                {
                    "date": "2024-01-02",
                    "energy_hp_electric": 100,
                    "energy_hp_heat": 400,
                    "energy_boiler_heat": 20,
                }
            ],
            days,
        )

    def test_month_source_ignores_rows_without_required_energy_values(self):
        raw = {
            "outsideTemperatureGraph": [
                {"timestamp": "2024-01-01", "temperatureOutside": 5.5}
            ]
        }

        days = self.exporter._normalise_days_from_month(
            raw,
            date(2024, 1, 1),
            date(2024, 1, 31),
            False,
            "Europe/Amsterdam",
        )

        self.assertEqual([], days)

    def test_naive_timestamp_is_interpreted_in_selected_timezone(self):
        self.assertEqual(
            "2024-01-01",
            self.exporter._local_date_from_timestamp(
                "2024-01-01T00:30:00", "Europe/Amsterdam"
            ),
        )

    def test_upstream_error_response_fails_export(self):
        with self.assertRaisesRegex(RuntimeError, "Failed to fetch insights data"):
            self.exporter._get_response_data(
                {"service_response": {"error": "Failed to fetch insights data"}}
            )

    def test_unknown_timezone_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unknown local_timezone"):
            self.exporter._validate_timezone("Not/A_Timezone")

    def test_invalid_delay_is_rejected(self):
        for value in (-1, 5001, float("nan"), "not-a-number"):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "day_delay_ms"):
                    self.exporter._validate_delay_ms(value)

    def test_excessive_call_count_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "split the export"):
            self.exporter._validate_call_count(367, 366, "day")

    def test_call_counts_do_not_require_building_date_ranges(self):
        self.assertEqual(
            367,
            self.exporter._inclusive_day_count(date(2024, 1, 1), date(2025, 1, 1)),
        )
        self.assertEqual(
            13,
            self.exporter._inclusive_month_count(
                date(2024, 1, 1), date(2025, 1, 1)
            ),
        )

    def test_default_end_date_uses_selected_timezone_today(self):
        original_today = self.exporter._today
        self.exporter._today = lambda timezone: date(2024, 1, 31)
        try:
            with tempfile.TemporaryDirectory() as output_dir:
                result = self.exporter.openquatt_export_quatt_insights(
                    from_date="2024-01-01",
                    daily=True,
                    output_dir=output_dir,
                    base_name="timezone-default",
                    day_delay_ms=0,
                    local_timezone="Europe/Amsterdam",
                )
        finally:
            self.exporter._today = original_today

        self.assertEqual(1, len(self.fake_service.calls))
        self.assertEqual("2024-01-01", self.fake_service.calls[0][2]["from_date"])
        self.assertEqual(31, result["missing_day_count"])

    def test_future_range_does_not_make_future_api_calls(self):
        original_today = self.exporter._today
        self.exporter._today = lambda timezone: date(2024, 1, 31)
        try:
            with tempfile.TemporaryDirectory() as output_dir:
                result = self.exporter.openquatt_export_quatt_insights(
                    from_date="2024-02-01",
                    to_date="2024-02-29",
                    daily=True,
                    output_dir=output_dir,
                    base_name="future-range",
                    day_delay_ms=0,
                    local_timezone="Europe/Amsterdam",
                )
        finally:
            self.exporter._today = original_today

        self.assertEqual([], self.fake_service.calls)
        self.assertEqual(0, result["missing_day_count"])

    def test_file_writer_outputs_flat_csv_and_cleans_temporary_files(self):
        payload = {
            "schema": "openquatt.quatt_insights_daily.v1",
            "days": [
                {
                    "date": "2024-01-01",
                    "energy_hp_electric": 100,
                    "energy_hp_heat": 400,
                    "raw_sample": {"token": "not-in-csv"},
                }
            ],
        }

        with tempfile.TemporaryDirectory() as output_dir:
            files = self.exporter._write_export_files(output_dir, "../unsafe name", payload)
            json_path = Path(files["json_path"])
            csv_path = Path(files["csv_path"])

            self.assertEqual("unsafe_name.json", json_path.name)
            self.assertEqual(payload, json.loads(json_path.read_text(encoding="utf-8")))
            csv_text = csv_path.read_text(encoding="utf-8")
            self.assertIn("date,energy_hp_electric,energy_hp_heat", csv_text)
            self.assertNotIn("raw_sample", csv_text)
            self.assertEqual([], list(Path(output_dir).glob("*.tmp")))

    def test_file_writer_rejects_relative_output_directory(self):
        with self.assertRaisesRegex(ValueError, "absolute path"):
            self.exporter._write_export_files("relative/path", "export", {"days": []})


if __name__ == "__main__":
    unittest.main()
