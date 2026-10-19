"""Run the calibrated extraction prototype for a small, explicit sample."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import requests
from PIL import Image, UnidentifiedImageError
from io import BytesIO

from coordinate_calibration import calibrate_chart, extract_calibrated_prices, save_overlay
from gpu_trends_image_extraction import EXPECTED_MONTHS, backup_and_write, load_gpu_records


def _short_error(error: Exception, limit: int = 240) -> str:
    detail = str(error).splitlines()[0].strip() or type(error).__name__
    return f"{type(error).__name__}: {detail}"[:limit]


def _failure_record(item: dict[str, str], stage: str, reason_code: str, error: Exception | str) -> dict[str, object]:
    reason = _short_error(error) if isinstance(error, Exception) else str(error)[:240]
    return {
        "gpu_model_name": item["gpu_model"],
        "image_url": item["image_url"],
        "price_trend": {month: "N/A" for month in EXPECTED_MONTHS},
        "price_quality": {month: "N/A" for month in EXPECTED_MONTHS},
        "review_required": True,
        "review_reasons": [reason_code],
        "extraction_status": "failed",
        "failure_stage": stage,
        "failure_reason": reason,
        "extraction_skipped": True,
    }


def _safe_name(model: str) -> str:
    return "".join(character.lower() if character.isalnum() else "_" for character in model).strip("_")


def process_record(item: dict[str, str], config: dict[str, object] | None, artifact_dir: Path) -> dict[str, object]:
    """Process one record, isolating expected record-level failures."""
    if not config:
        return _failure_record(item, "calibration", "calibration_failed", "missing calibration configuration")
    try:
        response = requests.get(item["image_url"], timeout=30, headers={"User-Agent": "GPU-PCPartPicker-calibration/1.0"})
        response.raise_for_status()
        image = Image.open(BytesIO(response.content)).convert("RGB")
    except (requests.RequestException, UnidentifiedImageError, OSError) as error:
        return _failure_record(item, "source_image", "image_validation_failed", error)
    try:
        calibration = calibrate_chart(image, config)
    except ValueError as error:
        return _failure_record(item, "calibration", "calibration_failed", error)
    try:
        values, qualities, reasons, positions, pixel_positions, diagnostics = extract_calibrated_prices(image, calibration, EXPECTED_MONTHS, return_diagnostics=True)
        review_reasons = set(reasons)
        numeric = sum(value != "N/A" for value in values.values())
        review = review_reasons & {"estimated_values_present", "ambiguous_month_boundary", "missing_line_segment", "isolated_spike", "ambiguous_line_candidate", "axis_unclear"}
        status = "failed" if numeric == 0 else "needs_review" if review else "partial" if numeric < len(EXPECTED_MONTHS) else "success"
        safe_name = _safe_name(item["gpu_model"])
        overlay_path = artifact_dir / f"{safe_name}.overlay.png"
        save_overlay(image, calibration, positions, pixel_positions, overlay_path, diagnostics)
        (artifact_dir / f"{safe_name}.calibration.json").parent.mkdir(parents=True, exist_ok=True)
        (artifact_dir / f"{safe_name}.calibration.json").write_text(json.dumps({
            "image_size": image.size,
            "plot_bounds": [calibration.plot_left, calibration.plot_top, calibration.plot_right, calibration.plot_bottom],
            "x_gridlines": calibration.x_gridlines,
            "y_gridlines": calibration.y_gridlines,
            "y_tick_values": calibration.y_values,
            "anchor_date": calibration.anchor_date,
            "anchor_x": calibration.anchor_x,
            "monthly_x_positions": positions,
            "monthly_pixel_y_positions": pixel_positions,
            "monthly_sampling_diagnostics": diagnostics,
        }, indent=2), encoding="utf-8")
        return {
            "gpu_model_name": item["gpu_model"],
            "image_url": item["image_url"],
            "price_trend": values,
            "price_quality": qualities,
            "review_required": bool(review),
            "review_reasons": sorted(review_reasons),
            "extraction_status": status,
            "calibration_artifact": str(overlay_path),
            "failure_stage": None,
            "failure_reason": None,
            "extraction_skipped": False,
        }
    except Exception as error:
        # Keep the concise reason in JSON while retaining the full traceback in logs.
        import logging
        logging.getLogger(__name__).exception("Unexpected processing error for %s", item["gpu_model"])
        return _failure_record(item, "processing", "unexpected_processing_error", error)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("sample_input.json"))
    parser.add_argument("--calibration", type=Path, default=Path("sample_calibration.json"))
    parser.add_argument("--output", type=Path, default=Path("Monthly_Scraped_Data/pcpartpicker_gpu_trends_coordinate_sample.json"))
    parser.add_argument("--artifact-dir", type=Path, default=Path("diagnostics/coordinate_sample"))
    args = parser.parse_args()
    records = load_gpu_records(args.input)
    configs = json.loads(args.calibration.read_text(encoding="utf-8"))
    results = []
    for item in records:
        results.append(process_record(item, configs.get(item["gpu_model"]), args.artifact_dir))
    backup_and_write(results, args.output)
    print(json.dumps({"records": len(results), "statuses": {status: sum(r["extraction_status"] == status for r in results) for status in ("success", "partial", "needs_review", "failed")}}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
