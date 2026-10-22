import json
import unittest
from pathlib import Path

from gpu_trends_image_extraction import EXPECTED_MONTHS


class ExtendedDatasetTests(unittest.TestCase):
    def test_month_range_is_july_2024_through_july_2026(self):
        self.assertEqual(len(EXPECTED_MONTHS), 25)
        self.assertEqual(EXPECTED_MONTHS[0], "2024-07-01")
        self.assertEqual(EXPECTED_MONTHS[-1], "2026-07-01")

    def test_extended_final_dataset_has_complete_structure(self):
        path = Path("Monthly_Scraped_Data/pcpartpicker_gpu_trends_final.json")
        records = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(len(records), 23)
        self.assertEqual(len({record["gpu_model_name"] for record in records}), 23)
        for record in records:
            self.assertEqual(list(record["price_trend"]), EXPECTED_MONTHS)
            self.assertEqual(list(record["price_quality"]), EXPECTED_MONTHS)
            self.assertNotIn("2026-08-01", record["price_trend"])
            self.assertNotIn("2026-09-01", record["price_trend"])
