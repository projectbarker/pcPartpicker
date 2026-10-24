"""Authoritative monthly-range definitions for the PCPartPicker dataset."""

from __future__ import annotations

from datetime import date


DATASET_START_MONTH = "2024-07-01"
DATASET_END_MONTH = "2026-09-01"
ORIGINAL_EXTRACTION_END_MONTH = "2026-01-01"
CACHED_JULY_SOURCE_END_MONTH = "2026-07-01"
LIVE_SOURCE_END_MONTH = "2026-09-01"


def month_range(start_month: str, end_month: str) -> list[str]:
    """Return inclusive first-of-month ISO keys."""
    start = date.fromisoformat(start_month)
    end = date.fromisoformat(end_month)
    if start.day != 1 or end.day != 1 or start > end:
        raise ValueError("Month range must contain ordered first-of-month dates")
    result: list[str] = []
    year, month = start.year, start.month
    while (year, month) <= (end.year, end.month):
        result.append(f"{year:04d}-{month:02d}-01")
        month += 1
        if month == 13:
            year += 1
            month = 1
    return result


ORIGINAL_MONTHS = month_range(DATASET_START_MONTH, ORIGINAL_EXTRACTION_END_MONTH)
EXPECTED_MONTHS = month_range(DATASET_START_MONTH, DATASET_END_MONTH)
CACHED_JULY_SOURCE_MONTHS = month_range(DATASET_START_MONTH, CACHED_JULY_SOURCE_END_MONTH)
LIVE_SOURCE_MONTHS = month_range(DATASET_START_MONTH, LIVE_SOURCE_END_MONTH)
