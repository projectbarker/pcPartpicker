import unittest

from coverage_audit import build_audit_records
from coverage_config import EXPECTED_MONTHS, ORIGINAL_MONTHS


class CoverageAuditTests(unittest.TestCase):
    def test_authoritative_range_and_legacy_range(self):
        self.assertEqual(len(ORIGINAL_MONTHS), 19)
        self.assertEqual(ORIGINAL_MONTHS[-1], "2026-01-01")
        self.assertEqual(len(EXPECTED_MONTHS), 27)
        self.assertEqual(EXPECTED_MONTHS[-1], "2026-09-01")

    def test_audit_has_one_row_per_gpu_month_and_no_validated_rows(self):
        rows = build_audit_records()
        self.assertEqual(len(rows), 23 * 27)
        self.assertEqual(len({row["gpu_model_name"] for row in rows}), 23)
        self.assertTrue(all(row["json_field_exists"] == "true" for row in rows))
        self.assertTrue(all(row["review_required"] == "true" for row in rows))
        self.assertFalse(any(row["final_coverage_classification"] == "validated" for row in rows))

    def test_historical_warning_rows_remain_unresolved(self):
        rows = {(row["gpu_model_name"], row["month"]): row for row in build_audit_records()}
        for key in (
            ("GeForce RTX 4080", "2024-11-01"),
            ("GeForce RTX 4080", "2024-12-01"),
            ("GeForce RTX 4080", "2025-01-01"),
            ("GeForce RTX 4090", "2024-10-01"),
        ):
            self.assertEqual(rows[key]["qa_status"], "unresolved_historical_qa_warning")
            self.assertEqual(rows[key]["value_classification"], "estimated")


if __name__ == "__main__":
    unittest.main()
