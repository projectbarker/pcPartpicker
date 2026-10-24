"""Extend the original 19-month dataset to the current 27-month field schema."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from coverage_config import EXPECTED_MONTHS, ORIGINAL_MONTHS
from gpu_trends_image_extraction import backup_and_write


LEGACY_MONTHS = ORIGINAL_MONTHS
EXTENSION_MONTHS = EXPECTED_MONTHS[19:]


def extend_dataset(input_path: Path, output_path: Path) -> dict[str, int | str]:
    records = json.loads(input_path.read_text(encoding="utf-8"))
    if not isinstance(records, list) or len(records) != 23:
        raise ValueError("Expected exactly 23 existing GPU records")
    models = [record.get("gpu_model_name") for record in records]
    if len(set(models)) != 23:
        raise ValueError("Existing dataset contains duplicate or missing GPU models")

    for record in records:
        trend = record.get("price_trend")
        quality = record.get("price_quality")
        if list(trend or {}) != LEGACY_MONTHS or list(quality or {}) != LEGACY_MONTHS:
            raise ValueError(f"Historical month keys are not the approved 19-month range for {record.get('gpu_model_name')}")
        for month in EXTENSION_MONTHS:
            trend[month] = "N/A"
            quality[month] = "N/A"
        reasons = set(record.get("review_reasons") or [])
        reasons.add("extension_not_validated")
        record["review_reasons"] = sorted(reasons)
        record["review_required"] = True

    backup = backup_and_write(records, output_path)
    numeric = sum(value != "N/A" for record in records for value in record["price_trend"].values())
    return {
        "records": len(records),
        "months_per_record": len(EXPECTED_MONTHS),
        "total_positions": len(records) * len(EXPECTED_MONTHS),
        "numeric_values": numeric,
        "na_values": len(records) * len(EXPECTED_MONTHS) - numeric,
        "backup_path": str(backup) if backup else "",
        "output_path": str(output_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("Monthly_Scraped_Data/pcpartpicker_gpu_trends_final.json"))
    parser.add_argument("--output", type=Path, default=Path("Monthly_Scraped_Data/pcpartpicker_gpu_trends_final.json"))
    args = parser.parse_args()
    print(json.dumps(extend_dataset(args.input, args.output), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
