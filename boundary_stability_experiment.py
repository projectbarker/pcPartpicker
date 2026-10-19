"""Isolated post-boundary-stability experiment for RTX 4090 June 2025.

This script intentionally does not call the production extraction function or
write any pilot output. It compares the existing component median with a
candidate post-boundary stable-run rule on one frozen source image.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw

from coordinate_calibration import Calibration, _is_black, _line_candidates, _select_candidate, price_from_y


ROOT = Path(__file__).parent
SOURCE = ROOT / "diagnostics" / "controlled_validation_sources" / "geforce_rtx_4090.png"
DIAGNOSTIC = ROOT / "diagnostics" / "step12_rtx4090_june2025_boundary.png"
COMPARISON = ROOT / "diagnostics" / "step12_rtx4090_june2025_boundary.json"
MONTH = "2025-06-01"
BOUNDARY_X = 599

# Defined before evaluation: inspect only a short post-boundary window, require
# a contiguous run, and reject ambiguity rather than selecting a best-looking
# pixel. The chosen constants are experiment settings, not production policy.
POST_OFFSET_START = 3
POST_OFFSET_END = 20
MIN_STABLE_COLUMNS = 8
MAX_COLUMN_SPREAD = 4
MAX_RUN_MEDIAN_SPREAD = 4


def load_calibration() -> Calibration:
    data = json.loads((ROOT / "diagnostics" / "step9_seven_gpu_pilot" / "geforce_rtx_4090.calibration.json").read_text(encoding="utf-8"))
    return Calibration(
        plot_left=data["plot_bounds"][0], plot_right=data["plot_bounds"][2],
        plot_top=data["plot_bounds"][1], plot_bottom=data["plot_bounds"][3],
        x_gridlines=tuple(data["x_gridlines"]), y_gridlines=tuple(data["y_gridlines"]),
        y_values=tuple(data["y_tick_values"]), anchor_date=data["anchor_date"], anchor_x=data["anchor_x"],
    )


def column_black_band(image: Image.Image, x: int, y_min: int, y_max: int) -> list[int]:
    rgb = image.convert("RGB")
    return [y for y in range(y_min, y_max + 1) if _is_black(rgb.getpixel((x, y)))]


def stable_post_boundary(image: Image.Image, calibration: Calibration, boundary_x: int, source_bounds: tuple[int, int]) -> dict[str, object]:
    y_min = max(calibration.plot_top + 2, source_bounds[0] - 8)
    y_max = min(calibration.plot_bottom - 2, source_bounds[1] + 8)
    columns = []
    for x in range(boundary_x + POST_OFFSET_START, boundary_x + POST_OFFSET_END + 1):
        ys = column_black_band(image, x, y_min, y_max)
        columns.append({"x": x, "ys": ys, "median_y": float(sorted(ys)[(len(ys) - 1) // 2]) if ys else None})

    runs: list[list[dict[str, object]]] = []
    current: list[dict[str, object]] = []
    for column in columns:
        ys = column["ys"]
        if ys and max(ys) - min(ys) <= MAX_COLUMN_SPREAD:
            current.append(column)
        else:
            if current:
                runs.append(current)
            current = []
    if current:
        runs.append(current)

    eligible = []
    for run in runs:
        medians = [column["median_y"] for column in run]
        if len(run) >= MIN_STABLE_COLUMNS and max(medians) - min(medians) <= MAX_RUN_MEDIAN_SPREAD:
            eligible.append(run)

    if len(eligible) != 1:
        return {"status": "ambiguous_or_missing", "window": [columns[0]["x"], columns[-1]["x"]], "columns": columns, "runs": [[column["x"] for column in run] for run in runs], "selected_y": None}
    run = eligible[0]
    values = [column["median_y"] for column in run]
    selected_y = float(sorted(values)[(len(values) - 1) // 2])
    return {"status": "stable", "window": {"x": [columns[0]["x"], columns[-1]["x"]], "y": [y_min, y_max]}, "columns": columns, "runs": [[column["x"] for column in item] for item in runs], "stable_run": [run[0]["x"], run[-1]["x"]], "selected_y": selected_y}


def make_diagnostic(image: Image.Image, current_y: float, experimental_y: float | None, stability: dict[str, object], calibration: Calibration) -> None:
    crop_box = (510, 240, 690, 330)
    crop = image.crop(crop_box)
    draw = ImageDraw.Draw(crop)
    def cx(x: int) -> int:
        return x - crop_box[0]
    def cy(y: float) -> int:
        return round(y) - crop_box[1]
    draw.rectangle((cx(BOUNDARY_X + POST_OFFSET_START), 0, cx(BOUNDARY_X + POST_OFFSET_END), crop.height - 1), outline=(255, 165, 0), width=1)
    draw.line((cx(BOUNDARY_X), 0, cx(BOUNDARY_X), crop.height - 1), fill=(255, 0, 0), width=1)
    draw.line((0, cy(current_y), crop.width - 1, cy(current_y)), fill=(255, 0, 0), width=1)
    draw.text((cx(BOUNDARY_X) + 2, 2), "June x=599", fill=(255, 0, 0))
    draw.text((2, cy(current_y) + 2), "current y=289", fill=(255, 0, 0))
    if experimental_y is not None:
        draw.line((0, cy(experimental_y), crop.width - 1, cy(experimental_y)), fill=(0, 150, 0), width=1)
        draw.text((2, cy(experimental_y) + 2), f"stable y={experimental_y:g}", fill=(0, 150, 0))
    draw.line((0, 294 - crop_box[1], crop.width - 1, 294 - crop_box[1]), fill=(0, 0, 255), width=1)
    draw.text((2, 294 - crop_box[1] + 2), "grid y=294 ($2000)", fill=(0, 0, 255))
    zoom = crop.resize((crop.width * 4, crop.height * 4), Image.Resampling.NEAREST)
    DIAGNOSTIC.parent.mkdir(parents=True, exist_ok=True)
    zoom.save(DIAGNOSTIC)


def main() -> int:
    image = Image.open(SOURCE).convert("RGB")
    calibration = load_calibration()
    current_candidates = _line_candidates(image, BOUNDARY_X, calibration)
    current_y, current_quality, current_reason, current_detail = _select_candidate(current_candidates)
    assert current_y is not None
    # The production diagnostic stores component span but not its absolute
    # bounds. Reconstruct a conservative local band around the selected
    # component for this experiment; this does not alter production sampling.
    source_bounds = (current_y - current_detail["y_span"], current_y + current_detail["y_span"])
    stability = stable_post_boundary(image, calibration, BOUNDARY_X, (int(source_bounds[0]), int(source_bounds[1])))
    experimental_y = stability["selected_y"]
    experimental_price = price_from_y(float(experimental_y), calibration) if experimental_y is not None else None
    current_price = price_from_y(current_y, calibration)
    make_diagnostic(image, current_y, float(experimental_y) if experimental_y is not None else None, stability, calibration)
    result = {
        "source_image": str(SOURCE), "image_dimensions": list(image.size), "month": MONTH, "boundary_x": BOUNDARY_X,
        "rule": {"post_boundary_window": [BOUNDARY_X + POST_OFFSET_START, BOUNDARY_X + POST_OFFSET_END], "minimum_stable_columns": MIN_STABLE_COLUMNS, "max_column_y_spread": MAX_COLUMN_SPREAD, "max_run_median_y_spread": MAX_RUN_MEDIAN_SPREAD, "failure_outcome": "ambiguous_or_missing; do not replace the current value or fabricate a value"},
        "current_median": {"y": current_y, "quality": current_quality, "reason": current_reason, "price_usd": round(current_price, 2), "candidate": current_detail},
        "post_boundary_stability": {**stability, "price_usd": round(experimental_price, 2) if experimental_price is not None else None},
        "conservative_fallback": {"behavior": "retain current result if stability is not uniquely established", "price_usd": round(current_price, 2)},
        "diagnostic_image": str(DIAGNOSTIC),
    }
    COMPARISON.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"current_y": current_y, "current_price": round(current_price, 2), "stability_status": stability["status"], "stable_run": stability.get("stable_run"), "experimental_y": experimental_y, "experimental_price": round(experimental_price, 2) if experimental_price is not None else None, "diagnostic": str(DIAGNOSTIC)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
