import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from gpu_trends_image_extraction import (
    EXPECTED_MONTHS,
    backup_and_write,
    extract_one,
    load_gpu_records,
    parse_model_output,
    safe_parse_json,
    summarize,
)


def complete_payload(value="150.00"):
    return json.dumps({month: value for month in EXPECTED_MONTHS})


def fake_client(content):
    return SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(
                create=lambda **kwargs: SimpleNamespace(
                    choices=[SimpleNamespace(message=SimpleNamespace(content=content))]
                )
            )
        )
    )


class PipelineTests(unittest.TestCase):
    def test_month_keys_are_complete_and_ordered(self):
        values, status = safe_parse_json(complete_payload())
        self.assertEqual(list(values), EXPECTED_MONTHS)
        self.assertEqual(len(values), len(EXPECTED_MONTHS))
        self.assertEqual(EXPECTED_MONTHS[-1], "2026-07-01")
        self.assertEqual(status, "success")

    def test_partial_and_all_missing_are_not_success(self):
        partial = {month: ("150.00" if month == EXPECTED_MONTHS[0] else "N/A") for month in EXPECTED_MONTHS}
        values, status = safe_parse_json(json.dumps(partial))
        self.assertEqual(values[EXPECTED_MONTHS[0]], "150.00")
        self.assertEqual(status, "partial")
        values, status = safe_parse_json(json.dumps({month: "N/A" for month in EXPECTED_MONTHS}))
        self.assertEqual(len(values), len(EXPECTED_MONTHS))
        self.assertEqual(status, "failed")

    def test_estimated_values_round_and_require_review(self):
        payload = {month: {"value": "132.6", "quality": "estimated", "reason": None} for month in EXPECTED_MONTHS}
        values, quality, reasons, status = parse_model_output(json.dumps(payload))
        self.assertEqual(values[EXPECTED_MONTHS[0]], "133.00")
        self.assertEqual(quality[EXPECTED_MONTHS[0]], "estimated")
        self.assertIn("estimated_values_present", reasons)
        self.assertEqual(status, "needs_review")

    def test_mixed_quality_and_missing_history(self):
        payload = {month: {"value": "N/A", "quality": "N/A", "reason": "outside_visible_history"} for month in EXPECTED_MONTHS}
        payload[EXPECTED_MONTHS[0]] = {"value": "150.00", "quality": "observed", "reason": None}
        values, quality, reasons, status = parse_model_output(json.dumps(payload))
        self.assertEqual(values[EXPECTED_MONTHS[0]], "150.00")
        self.assertEqual(quality[EXPECTED_MONTHS[0]], "observed")
        self.assertEqual(status, "partial")
        self.assertIn("outside_visible_history", reasons)

    def test_invalid_quality_becomes_missing_and_failed(self):
        payload = {month: {"value": "150.00", "quality": "certain", "reason": None} for month in EXPECTED_MONTHS}
        values, quality, reasons, status = parse_model_output(json.dumps(payload))
        self.assertTrue(all(value == "N/A" for value in values.values()))
        self.assertTrue(all(value == "N/A" for value in quality.values()))
        self.assertEqual(status, "failed")
        self.assertIn("axis_unclear", reasons)

    def test_suspicious_uniform_sequence_requires_review(self):
        payload = {month: {"value": str(1000 - (index * 50 if index < 7 else 300 - (index - 6) * 50)), "quality": "observed", "reason": "Directly readable at gridline."} for index, month in enumerate(EXPECTED_MONTHS)}
        _values, _quality, reasons, status = parse_model_output(json.dumps(payload))
        self.assertIn("suspicious_sequence", reasons)
        self.assertEqual(status, "needs_review")

    def test_malformed_and_invalid_prices_fail_safely(self):
        self.assertEqual(safe_parse_json("not json"), ({}, "failed"))
        values, status = safe_parse_json(json.dumps({month: "-1" for month in EXPECTED_MONTHS}))
        self.assertEqual(status, "failed")
        self.assertTrue(all(value == "N/A" for value in values.values()))

    def test_input_validation_deduplicates_and_skips_invalid(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input.json"
            source.write_text(json.dumps([
                {"gpu_model": "A", "image_url": "https://example/a.png"},
                {"gpu_model": "A", "image_url": "https://example/a2.png"},
                {"gpu_model": "", "image_url": "https://example/b.png"},
                {"gpu_model": "B", "image_url": "not-a-url"},
            ]), encoding="utf-8")
            self.assertEqual(load_gpu_records(source), [{"gpu_model": "A", "image_url": "https://example/a.png"}])

    def test_api_response_and_status_are_recorded(self):
        result = extract_one({"gpu_model": "A", "image_url": "https://example/a.png"}, fake_client(complete_payload()), retries=0)
        self.assertEqual(result["extraction_status"], "success")
        self.assertEqual(len(result["price_trend"]), len(EXPECTED_MONTHS))
        self.assertIn("price_quality", result)
        self.assertFalse(result["review_required"])

    def test_api_estimate_sets_review_fields(self):
        payload = json.dumps({month: {"value": "100.4", "quality": "estimated", "reason": None} for month in EXPECTED_MONTHS})
        result = extract_one({"gpu_model": "A", "image_url": "https://example/a.png"}, fake_client(payload), retries=0)
        self.assertEqual(result["extraction_status"], "needs_review")
        self.assertTrue(result["review_required"])
        self.assertIn("estimated_values_present", result["review_reasons"])

    def test_api_failure_does_not_retry_forever(self):
        calls = []

        def fail(**kwargs):
            calls.append(1)
            raise RuntimeError("temporary failure")

        client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=fail)))
        result = extract_one({"gpu_model": "A", "image_url": "https://example/a.png"}, client, retries=2, sleep=lambda _: None)
        self.assertEqual(result["extraction_status"], "failed")
        self.assertEqual(len(calls), 3)

    def test_backup_and_atomic_write(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "result.json"
            output.write_text("old", encoding="utf-8")
            backup = backup_and_write([{"x": 1}], output)
            self.assertIsNotNone(backup)
            self.assertTrue(backup.exists())
            self.assertEqual(json.loads(output.read_text(encoding="utf-8")), [{"x": 1}])

    def test_repeated_write_replaces_without_duplicate_records(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "result.json"
            first = [{"gpu_model_name": "A"}]
            second = [{"gpu_model_name": "A"}, {"gpu_model_name": "B"}]
            backup_and_write(first, output)
            backup_and_write(second, output)
            self.assertEqual(json.loads(output.read_text(encoding="utf-8")), second)

    def test_backup_names_do_not_collide_with_same_second_timestamp(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "result.json"
            output.write_text(json.dumps([{"version": "old"}]), encoding="utf-8")
            with patch("gpu_trends_image_extraction.time.strftime", return_value="20261017_120000"):
                first_backup = backup_and_write([{"version": "one"}], output)
                second_backup = backup_and_write([{"version": "two"}], output)
            self.assertNotEqual(first_backup, second_backup)
            self.assertEqual(json.loads(first_backup.read_text(encoding="utf-8")), [{"version": "old"}])
            self.assertEqual(json.loads(second_backup.read_text(encoding="utf-8")), [{"version": "one"}])
            self.assertEqual(json.loads(output.read_text(encoding="utf-8")), [{"version": "two"}])

    def test_serialization_failure_preserves_output_and_cleans_temp_file(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "result.json"
            output.write_text(json.dumps([{"version": "stable"}]), encoding="utf-8")
            with self.assertRaises(TypeError):
                backup_and_write([{"bad": object()}], output)
            self.assertEqual(json.loads(output.read_text(encoding="utf-8")), [{"version": "stable"}])
            backups = list(Path(directory).glob("result.backup_*.json"))
            self.assertEqual(len(backups), 1)
            self.assertEqual(json.loads(backups[0].read_text(encoding="utf-8")), [{"version": "stable"}])
            self.assertEqual({path.name for path in Path(directory).iterdir()}, {"result.json", backups[0].name})

    def test_summary_counts_values_and_missing_values(self):
        records = [{"gpu_model_name": "A", "extraction_status": "partial", "price_trend": {month: ("1.00" if month == EXPECTED_MONTHS[0] else "N/A") for month in EXPECTED_MONTHS}}]
        result = summarize(records)
        self.assertEqual(result["input_gpus"], 1)
        self.assertEqual(result["numeric_monthly_values"], 1)
        self.assertEqual(result["missing_monthly_values"], len(EXPECTED_MONTHS) - 1)
        self.assertEqual(result["partial"], 1)


if __name__ == "__main__":
    unittest.main()
