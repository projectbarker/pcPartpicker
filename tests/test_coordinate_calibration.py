import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from datetime import date

from PIL import Image, ImageDraw

from coordinate_calibration import (
    calibrate_chart,
    detect_gridlines,
    extract_calibrated_prices,
    month_x_positions,
    price_from_y,
    sample_black_line,
    save_overlay,
)


def synthetic_chart():
    image = Image.new("RGB", (140, 120), (240, 240, 240))
    draw = ImageDraw.Draw(image)
    for y in (10, 50, 90):
        draw.line((20, y, 120, y), fill=(150, 150, 150), width=1)
    for x in (20, 60, 100, 120):
        draw.line((x, 10, x, 90), fill=(150, 150, 150), width=1)
    draw.line((20, 60, 120, 60), fill=(0, 0, 0), width=2)
    draw.line((80, 60, 100, 40), fill=(0, 0, 0), width=2)
    return image


class CoordinateCalibrationTests(unittest.TestCase):
    def test_gridline_detection_and_calibration(self):
        image = synthetic_chart()
        horizontal, vertical = detect_gridlines(image)
        self.assertEqual(horizontal, [10, 50, 90])
        self.assertEqual(vertical, [20, 60, 100, 120])
        calibration = calibrate_chart(image, {"anchor_date": "2024-08-01", "anchor_x": 60, "y_tick_values": [100, 50, 0]})
        self.assertEqual(calibration.plot_left, 20)
        self.assertEqual(calibration.plot_bottom, 90)

    def test_month_mapping_uses_anchor_and_detected_grid(self):
        calibration = calibrate_chart(synthetic_chart(), {"anchor_date": "2024-08-01", "anchor_x": 60, "y_tick_values": [100, 50, 0]})
        positions = month_x_positions(calibration, ["2024-07-01", "2024-08-01", "2024-09-01", "2024-12-01"])
        self.assertEqual(positions["2024-07-01"], 20)
        self.assertEqual(positions["2024-08-01"], 60)
        self.assertEqual(positions["2024-09-01"], 100)
        self.assertIsNone(positions["2024-12-01"])

    def test_pixel_to_price_interpolates_calibrated_ticks(self):
        calibration = calibrate_chart(synthetic_chart(), {"anchor_date": "2024-08-01", "anchor_x": 60, "y_tick_values": [100, 50, 0]})
        self.assertAlmostEqual(price_from_y(30, calibration), 75)

    def test_black_line_sampling_and_estimation(self):
        calibration = calibrate_chart(synthetic_chart(), {"anchor_date": "2024-08-01", "anchor_x": 60, "y_tick_values": [100, 50, 0]})
        y, quality, reason = sample_black_line(synthetic_chart(), 60, calibration)
        self.assertIsNotNone(y)
        self.assertEqual(quality, "estimated")
        self.assertIsNone(reason)
        values, qualities, reasons, positions, pixels = extract_calibrated_prices(synthetic_chart(), calibration, ["2024-07-01", "2024-08-01", "2024-09-01", "2024-12-01"])
        self.assertEqual(values["2024-08-01"], "38.00")
        self.assertEqual(qualities["2024-12-01"], "N/A")
        self.assertIn("outside_visible_history", reasons)

    def test_missing_black_line_returns_review_reason(self):
        image = Image.new("RGB", (140, 120), (240, 240, 240))
        draw = ImageDraw.Draw(image)
        for y in (10, 50, 90):
            draw.line((20, y, 120, y), fill=(150, 150, 150), width=1)
        for x in (20, 60, 100, 120):
            draw.line((x, 10, x, 90), fill=(150, 150, 150), width=1)
        calibration = calibrate_chart(image, {"anchor_date": "2024-08-01", "anchor_x": 60, "y_tick_values": [100, 50, 0]})
        y, quality, reason = sample_black_line(image, 60, calibration)
        self.assertIsNone(y)
        self.assertEqual(quality, "N/A")
        self.assertEqual(reason, "missing_line_segment")

    def test_calibration_rejects_mismatched_axis_ticks(self):
        with self.assertRaises(ValueError):
            calibrate_chart(synthetic_chart(), {"anchor_date": "2024-08-01", "anchor_x": 60, "y_tick_values": [100, 50]})

    def test_calibration_rejects_incomplete_gridline_set(self):
        image = Image.new("RGB", (140, 120), (240, 240, 240))
        draw = ImageDraw.Draw(image)
        for y in (10, 50):
            draw.line((20, y, 120, y), fill=(150, 150, 150))
        for x in (20, 60, 100, 120):
            draw.line((x, 10, x, 50), fill=(150, 150, 150))
        with self.assertRaisesRegex(ValueError, "horizontal gridlines"):
            calibrate_chart(image, {"anchor_date": "2024-08-01", "anchor_x": 60, "y_tick_values": [100, 50, 0]})

    def test_calibration_rejects_contradictory_tick_order(self):
        with self.assertRaisesRegex(ValueError, "strictly decrease"):
            calibrate_chart(synthetic_chart(), {"anchor_date": "2024-08-01", "anchor_x": 60, "y_tick_values": [0, 50, 100]})

    def test_invalid_calibration_cannot_produce_trusted_prices(self):
        with self.assertRaises(ValueError):
            calibration = calibrate_chart(synthetic_chart(), {"anchor_date": "2024-08-01", "anchor_x": 60, "y_tick_values": [100, 100, 0]})
            price_from_y(30, calibration)

    def _calibration(self):
        return calibrate_chart(synthetic_chart(), {"anchor_date": "2024-08-01", "anchor_x": 60, "y_tick_values": [100, 50, 0]})

    def test_vertical_spike_is_rejected_without_displacing_line(self):
        image = Image.new("RGB", (140, 120), (240, 240, 240))
        draw = ImageDraw.Draw(image)
        for y in (10, 50, 90):
            draw.line((20, y, 120, y), fill=(150, 150, 150))
        for x in (20, 60, 100, 120):
            draw.line((x, 10, x, 90), fill=(150, 150, 150))
        draw.line((25, 60, 95, 60), fill=(0, 0, 0), width=2)
        draw.line((60, 20, 60, 40), fill=(0, 0, 0), width=1)
        y, quality, reason, detail = sample_black_line(image, 60, self._calibration(), return_diagnostics=True)
        self.assertEqual(y, 60)
        self.assertIsNone(reason)
        self.assertTrue(any(candidate["vertical_spike"] for candidate in detail["candidates"]))

    def test_wider_tall_spike_is_rejected_by_shape_ratio(self):
        image = Image.new("RGB", (140, 120), (240, 240, 240))
        draw = ImageDraw.Draw(image)
        draw.rectangle((58, 20, 62, 40), fill=(0, 0, 0))
        y, quality, reason, detail = sample_black_line(image, 60, self._calibration(), return_diagnostics=True)
        self.assertIsNone(y)
        self.assertEqual(quality, "N/A")
        self.assertEqual(reason, "isolated_spike")
        self.assertTrue(detail["candidates"][0]["vertical_spike"])

    def test_month_boundary_spike_does_not_override_continuous_line(self):
        image = Image.new("RGB", (140, 120), (240, 240, 240))
        draw = ImageDraw.Draw(image)
        draw.line((25, 60, 95, 60), fill=(0, 0, 0), width=2)
        draw.line((60, 20, 60, 40), fill=(0, 0, 0), width=1)
        y, _, reason = sample_black_line(image, 60, self._calibration(), previous_y=60)
        self.assertEqual(y, 60)
        self.assertIsNone(reason)

    def test_genuine_steep_change_is_retained_when_horizontally_supported(self):
        image = Image.new("RGB", (140, 120), (240, 240, 240))
        draw = ImageDraw.Draw(image)
        draw.line((48, 75, 72, 35), fill=(0, 0, 0), width=2)
        y, _, reason, detail = sample_black_line(image, 60, self._calibration(), return_diagnostics=True)
        self.assertIsNotNone(y)
        self.assertIsNone(reason)
        self.assertTrue(detail["accepted"]["horizontal_support"] >= 3)

    def test_multiple_disconnected_candidates_remain_ambiguous(self):
        image = Image.new("RGB", (140, 120), (240, 240, 240))
        draw = ImageDraw.Draw(image)
        draw.line((54, 40, 66, 40), fill=(0, 0, 0), width=1)
        draw.line((54, 70, 66, 70), fill=(0, 0, 0), width=1)
        y, quality, reason = sample_black_line(image, 60, self._calibration())
        self.assertIsNone(y)
        self.assertEqual(quality, "N/A")
        self.assertEqual(reason, "ambiguous_line_candidate")

    def test_disconnected_segment_is_missing_not_interpolated(self):
        image = Image.new("RGB", (140, 120), (240, 240, 240))
        draw = ImageDraw.Draw(image)
        draw.line((25, 60, 45, 60), fill=(0, 0, 0), width=2)
        draw.line((75, 60, 95, 60), fill=(0, 0, 0), width=2)
        y, quality, reason = sample_black_line(image, 60, self._calibration())
        self.assertIsNone(y)
        self.assertEqual(quality, "N/A")
        self.assertEqual(reason, "missing_line_segment")

    def test_overlay_marks_rejected_and_ambiguous_candidates(self):
        image = synthetic_chart()
        calibration = self._calibration()
        positions = {"2024-08-01": 60, "2024-09-01": 100}
        pixel_positions = {"2024-08-01": None, "2024-09-01": None}
        diagnostics = {
            "2024-08-01": {
                "reason": "isolated_spike",
                "candidates": [{"y": 30.0, "vertical_spike": True}],
            },
            "2024-09-01": {
                "reason": "ambiguous_line_candidate",
                "candidates": [
                    {"y": 40.0, "vertical_spike": False},
                    {"y": 70.0, "vertical_spike": False},
                ],
            },
        }
        with TemporaryDirectory() as directory:
            output = Path(directory) / "overlay.png"
            save_overlay(image, calibration, positions, pixel_positions, output, diagnostics)
            rendered = Image.open(output).convert("RGB")
            colors = {rendered.getpixel((x, y)) for x in range(50, 111) for y in range(20, 81)}
        self.assertIn((255, 140, 0), colors)
        self.assertIn((255, 210, 0), colors)


if __name__ == "__main__":
    unittest.main()
