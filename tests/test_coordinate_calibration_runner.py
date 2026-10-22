import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import requests

from coordinate_calibration_runner import process_record
from gpu_trends_image_extraction import EXPECTED_MONTHS


def fake_calibration():
    return SimpleNamespace(
        plot_left=55,
        plot_right=1149,
        plot_top=27,
        plot_bottom=427,
        x_gridlines=(55, 113, 175),
        y_gridlines=(27, 94, 161),
        y_values=(300.0, 150.0, 0.0),
        anchor_date="2024-10-01",
        anchor_x=113,
    )


def fake_image_response():
    return SimpleNamespace(content=b"image-bytes", raise_for_status=lambda: None)


class CoordinateRunnerTests(unittest.TestCase):
    def setUp(self):
        self.item = {"gpu_model": "Test GPU", "image_url": "https://example/test.png"}
        self.values = {month: ("123.00" if month == EXPECTED_MONTHS[0] else "N/A") for month in EXPECTED_MONTHS}
        self.qualities = {month: ("estimated" if month == EXPECTED_MONTHS[0] else "N/A") for month in EXPECTED_MONTHS}

    def run_with_patches(self, extraction=None, calibration=None):
        extraction = extraction or (self.values, self.qualities, ["estimated_values_present"], {}, {}, {})
        calibration = calibration or fake_calibration()
        patches = [
            patch("coordinate_calibration_runner.requests.get", return_value=fake_image_response()),
            patch("coordinate_calibration_runner.Image.open", return_value=SimpleNamespace(convert=lambda _mode: SimpleNamespace(size=(1176, 484)))),
            patch("coordinate_calibration_runner.calibrate_chart", return_value=calibration),
            patch("coordinate_calibration_runner.extract_calibrated_prices", return_value=extraction),
            patch("coordinate_calibration_runner.save_overlay"),
        ]
        return patches

    def test_valid_record_preserves_schema_and_review_status(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.run_with_patches()[0], self.run_with_patches()[1], self.run_with_patches()[2], self.run_with_patches()[3], self.run_with_patches()[4]:
                result = process_record(self.item, {"valid": True}, Path(directory))
        self.assertEqual(result["extraction_status"], "needs_review")
        self.assertTrue(result["review_required"])
        self.assertEqual(len(result["price_trend"]), len(EXPECTED_MONTHS))
        self.assertEqual(result["price_trend"][EXPECTED_MONTHS[0]], "123.00")
        self.assertEqual(result["price_quality"][EXPECTED_MONTHS[0]], "estimated")
        self.assertIn("estimated_values_present", result["review_reasons"])
        self.assertEqual(result["failure_stage"], None)
        self.assertFalse(result["extraction_skipped"])

    def test_calibration_failure_is_recorded_without_numeric_values(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch("coordinate_calibration_runner.requests.get", return_value=fake_image_response()), \
                 patch("coordinate_calibration_runner.Image.open", return_value=SimpleNamespace(convert=lambda _mode: SimpleNamespace(size=(1176, 484)))), \
                 patch("coordinate_calibration_runner.calibrate_chart", side_effect=ValueError("Expected 7 horizontal gridlines, detected 6")), \
                 patch("coordinate_calibration_runner.extract_calibrated_prices") as extract:
                result = process_record(self.item, {"invalid": True}, Path(directory))
        self.assertEqual(result["extraction_status"], "failed")
        self.assertTrue(result["review_required"])
        self.assertEqual(result["failure_stage"], "calibration")
        self.assertIn("calibration_failed", result["review_reasons"])
        self.assertTrue(result["extraction_skipped"])
        self.assertTrue(all(value == "N/A" for value in result["price_trend"].values()))
        self.assertTrue(all(value == "N/A" for value in result["price_quality"].values()))
        self.assertIn("Expected 7 horizontal gridlines", result["failure_reason"])
        extract.assert_not_called()

    def test_one_calibration_failure_does_not_stop_next_valid_record(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch("coordinate_calibration_runner.requests.get", return_value=fake_image_response()), \
                 patch("coordinate_calibration_runner.Image.open", return_value=SimpleNamespace(convert=lambda _mode: SimpleNamespace(size=(1176, 484)))), \
                 patch("coordinate_calibration_runner.calibrate_chart", side_effect=[ValueError("bad grid"), fake_calibration()]), \
                 patch("coordinate_calibration_runner.extract_calibrated_prices", return_value=(self.values, self.qualities, ["estimated_values_present"], {}, {}, {})), \
                 patch("coordinate_calibration_runner.save_overlay"):
                failed = process_record(self.item, {"invalid": True}, Path(directory))
                valid = process_record({"gpu_model": "Valid GPU", "image_url": "https://example/valid.png"}, {"valid": True}, Path(directory))
        self.assertEqual(failed["extraction_status"], "failed")
        self.assertEqual(valid["extraction_status"], "needs_review")
        self.assertEqual(valid["gpu_model_name"], "Valid GPU")

    def test_unreadable_image_is_recorded_as_failed(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch("coordinate_calibration_runner.requests.get", side_effect=requests.RequestException("connection failed")):
                result = process_record(self.item, {"valid": True}, Path(directory))
        self.assertEqual(result["extraction_status"], "failed")
        self.assertEqual(result["failure_stage"], "source_image")
        self.assertIn("image_validation_failed", result["review_reasons"])
        self.assertTrue(result["extraction_skipped"])

    def test_unexpected_processing_error_is_failed_not_success(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch("coordinate_calibration_runner.requests.get", return_value=fake_image_response()), \
                 patch("coordinate_calibration_runner.Image.open", return_value=SimpleNamespace(convert=lambda _mode: SimpleNamespace(size=(1176, 484)))), \
                 patch("coordinate_calibration_runner.calibrate_chart", return_value=fake_calibration()), \
                 patch("coordinate_calibration_runner.extract_calibrated_prices", side_effect=RuntimeError("unexpected parser state")):
                result = process_record(self.item, {"valid": True}, Path(directory))
        self.assertEqual(result["extraction_status"], "failed")
        self.assertEqual(result["failure_stage"], "processing")
        self.assertIn("unexpected_processing_error", result["review_reasons"])
        self.assertNotEqual(result["extraction_status"], "success")

    def test_missing_calibration_configuration_is_explicit_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            result = process_record(self.item, None, Path(directory))
        self.assertEqual(result["extraction_status"], "failed")
        self.assertEqual(result["failure_stage"], "calibration")
        self.assertTrue(result["extraction_skipped"])
        self.assertEqual(json.loads(json.dumps(result))["price_trend"][EXPECTED_MONTHS[0]], "N/A")


if __name__ == "__main__":
    unittest.main()
