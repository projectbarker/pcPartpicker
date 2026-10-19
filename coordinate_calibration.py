"""Lightweight Pillow-based chart calibration and black-line sampling.

The prototype deliberately separates pixel calibration from model interpretation.
Each chart supplies visible axis tick values and one visible date-label anchor;
plot/grid coordinates are detected from that specific image.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw


@dataclass(frozen=True)
class Calibration:
    plot_left: int
    plot_right: int
    plot_top: int
    plot_bottom: int
    x_gridlines: tuple[int, ...]
    y_gridlines: tuple[int, ...]
    y_values: tuple[float, ...]
    anchor_date: str
    anchor_x: int


def _clusters(values: list[int], max_gap: int = 2) -> list[int]:
    if not values:
        return []
    groups: list[list[int]] = [[values[0]]]
    for value in values[1:]:
        if value - groups[-1][-1] <= max_gap:
            groups[-1].append(value)
        else:
            groups.append([value])
    return [round(sum(group) / len(group)) for group in groups]


def detect_gridlines(image: Image.Image) -> tuple[list[int], list[int]]:
    """Detect long neutral-gray horizontal and vertical chart gridlines."""
    rgb = image.convert("RGB")
    width, height = rgb.size
    horizontal: list[int] = []
    vertical: list[int] = []
    for y in range(height):
        count = 0
        for x in range(width):
            r, g, b = rgb.getpixel((x, y))
            mean = (r + g + b) // 3
            if max(r, g, b) - min(r, g, b) <= 8 and 90 <= mean <= 190:
                count += 1
        if count >= int(width * 0.70):
            horizontal.append(y)
    for x in range(width):
        count = 0
        for y in range(height):
            r, g, b = rgb.getpixel((x, y))
            mean = (r + g + b) // 3
            if max(r, g, b) - min(r, g, b) <= 8 and 90 <= mean <= 190:
                count += 1
        if count >= int(height * 0.60):
            vertical.append(x)
    return _clusters(horizontal), _clusters(vertical)


def calibrate_chart(image: Image.Image, config: dict[str, Any]) -> Calibration:
    """Calibrate one image using its visible tick labels and date anchor."""
    y_lines, x_lines = detect_gridlines(image)
    y_values = tuple(float(value) for value in config["y_tick_values"])
    if len(y_lines) != len(y_values):
        raise ValueError(f"Expected {len(y_values)} horizontal gridlines, detected {len(y_lines)}")
    if any(upper <= lower for upper, lower in zip(y_values, y_values[1:])):
        raise ValueError("Y-axis tick values must strictly decrease from top to bottom")
    if len(x_lines) < 3:
        raise ValueError("Too few vertical gridlines detected")
    anchor_x = int(config["anchor_x"])
    nearest = min(x_lines, key=lambda x: abs(x - anchor_x))
    if abs(nearest - anchor_x) > 5:
        raise ValueError(f"Date anchor x={anchor_x} does not match detected gridline")
    return Calibration(
        plot_left=x_lines[0], plot_right=x_lines[-1],
        plot_top=y_lines[0], plot_bottom=y_lines[-1],
        x_gridlines=tuple(x_lines), y_gridlines=tuple(y_lines),
        y_values=y_values, anchor_date=config["anchor_date"], anchor_x=nearest,
    )


def month_x_positions(calibration: Calibration, months: list[str]) -> dict[str, int | None]:
    """Map requested month keys to detected monthly gridline positions."""
    anchor = date.fromisoformat(calibration.anchor_date)
    anchor_index = min(range(len(calibration.x_gridlines)), key=lambda i: abs(calibration.x_gridlines[i] - calibration.anchor_x))
    positions: dict[str, int | None] = {}
    for month in months:
        target = date.fromisoformat(month)
        index = (target.year - anchor.year) * 12 + target.month - anchor.month + anchor_index
        positions[month] = calibration.x_gridlines[index] if 0 <= index < len(calibration.x_gridlines) else None
    return positions


def price_from_y(y: float, calibration: Calibration) -> float:
    """Convert a pixel y position to USD using the calibrated grid."""
    lines = calibration.y_gridlines
    values = calibration.y_values
    if y <= lines[0]:
        return values[0]
    if y >= lines[-1]:
        return values[-1]
    for index in range(len(lines) - 1):
        if lines[index] <= y <= lines[index + 1]:
            fraction = (y - lines[index]) / (lines[index + 1] - lines[index])
            return values[index] + fraction * (values[index + 1] - values[index])
    raise ValueError("Pixel y is outside calibrated plot")


def _is_black(pixel: tuple[int, int, int]) -> bool:
    return max(pixel) < 85 and max(pixel) - min(pixel) < 25


def _line_candidates(image: Image.Image, x: int, calibration: Calibration, radius: int = 6) -> list[dict[str, Any]]:
    """Find connected black components near a month, retaining shape evidence.

    A candidate is deliberately based on a connected component and its horizontal
    support, rather than the darkest or nearest pixel. This makes thin vertical
    spikes visible to the caller as rejected evidence.
    """
    rgb = image.convert("RGB")
    left = max(calibration.plot_left + 2, x - radius)
    right = min(calibration.plot_right - 2, x + radius)
    top = calibration.plot_top + 2
    bottom = calibration.plot_bottom - 2
    pixels = {(px, py) for px in range(left, right + 1) for py in range(top, bottom + 1) if _is_black(rgb.getpixel((px, py)))}
    components: list[set[tuple[int, int]]] = []
    while pixels:
        seed = pixels.pop()
        component = {seed}
        stack = [seed]
        while stack:
            px, py = stack.pop()
            for nx in range(px - 1, px + 2):
                for ny in range(py - 1, py + 2):
                    if (nx, ny) in pixels:
                        pixels.remove((nx, ny))
                        component.add((nx, ny))
                        stack.append((nx, ny))
        components.append(component)
    candidates: list[dict[str, Any]] = []
    for component in components:
        xs = [point[0] for point in component]
        ys = [point[1] for point in component]
        columns = len(set(xs))
        x_span = max(xs) - min(xs)
        y_span = max(ys) - min(ys)
        near_center = min(abs(px - x) for px in xs) <= 2
        if not near_center:
            continue
        ordered_ys = sorted(ys)
        median_y = ordered_ys[(len(ordered_ys) - 1) // 2]
        vertical_spike = y_span >= 5 and (columns <= 2 or y_span > max(8, x_span * 4))
        candidates.append({
            "y": float(median_y), "x_span": x_span, "y_span": y_span,
            "horizontal_support": columns, "area": len(component),
            "vertical_spike": vertical_spike,
        })
    return sorted(candidates, key=lambda item: item["y"])


def _select_candidate(candidates: list[dict[str, Any]], previous_y: float | None = None, next_y: float | None = None) -> tuple[float | None, str, str | None, dict[str, Any] | None]:
    if not candidates:
        return None, "N/A", "missing_line_segment", None
    viable = [candidate for candidate in candidates if not candidate["vertical_spike"]]
    if not viable:
        return None, "N/A", "isolated_spike", None
    for candidate in viable:
        support = candidate["horizontal_support"]
        candidate["score"] = min(support, 5) * 2 + min(candidate["area"], 12) / 12
        neighbors = [value for value in (previous_y, next_y) if value is not None]
        if neighbors:
            candidate["score"] += max(0.0, 6.0 - min(abs(candidate["y"] - value) for value in neighbors))
    viable.sort(key=lambda candidate: candidate["score"], reverse=True)
    best = viable[0]
    tied = [candidate for candidate in viable[1:] if abs(candidate["score"] - best["score"]) < 1.5]
    if tied and all(abs(candidate["y"] - best["y"]) > 4 for candidate in tied):
        return None, "N/A", "ambiguous_line_candidate", None
    distance_to_grid = min(abs(best["y"] - line) for line in []) if False else 0
    return best["y"], "estimated", None, best


def sample_black_line(image: Image.Image, x: int, calibration: Calibration, previous_y: float | None = None, next_y: float | None = None, return_diagnostics: bool = False):
    """Return (pixel_y, quality, reason), with optional candidate diagnostics."""
    candidates = _line_candidates(image, x, calibration)
    y, quality, reason, accepted = _select_candidate(candidates, previous_y, next_y)
    if y is not None:
        distance_to_grid = min(abs(y - line) for line in calibration.y_gridlines)
        quality = "observed" if distance_to_grid <= 2.5 else "estimated"
    if return_diagnostics:
        return y, quality, reason, {"candidates": candidates, "accepted": accepted}
    return y, quality, reason


def extract_calibrated_prices(image: Image.Image, calibration: Calibration, months: list[str], return_diagnostics: bool = False):
    positions = month_x_positions(calibration, months)
    values: dict[str, str] = {}
    qualities: dict[str, str] = {}
    reasons: set[str] = set()
    pixel_positions: dict[str, float | None] = {}
    raw_candidates: dict[str, list[dict[str, Any]]] = {month: _line_candidates(image, x, calibration) for month, x in positions.items() if x is not None}
    previous_y: float | None = None
    diagnostics: dict[str, Any] = {}
    ordered_months = list(positions)
    for month_index, month in enumerate(ordered_months):
        x = positions[month]
        if x is None:
            values[month], qualities[month] = "N/A", "N/A"
            reasons.add("outside_visible_history")
            pixel_positions[month] = None
            diagnostics[month] = {"status": "out_of_history", "candidates": []}
            continue
        next_month = ordered_months[month_index + 1] if month_index + 1 < len(ordered_months) else None
        next_candidates = raw_candidates.get(next_month, []) if next_month else []
        next_viable = [candidate["y"] for candidate in next_candidates if not candidate["vertical_spike"]]
        next_y = next_viable[0] if len(next_viable) == 1 else None
        y, quality, reason, detail = sample_black_line(image, x, calibration, previous_y, next_y, return_diagnostics=True)
        pixel_positions[month] = y
        diagnostics[month] = {"status": "accepted" if y is not None else "rejected", "reason": reason, **(detail or {})}
        if y is None:
            values[month], qualities[month] = "N/A", "N/A"
            if reason:
                reasons.add(reason)
            continue
        previous_y = y
        price = price_from_y(y, calibration)
        if quality == "observed":
            nearest_tick = min(range(len(calibration.y_gridlines)), key=lambda index: abs(y - calibration.y_gridlines[index]))
            price = calibration.y_values[nearest_tick]
        if quality == "estimated":
            price = float(Decimal(str(price)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
            reasons.add("estimated_values_present")
        values[month] = f"{price:.2f}"
        qualities[month] = quality
    numeric = sum(value != "N/A" for value in values.values())
    review = reasons & {"estimated_values_present", "ambiguous_month_boundary", "missing_line_segment", "isolated_spike", "ambiguous_line_candidate", "axis_unclear"}
    if numeric == 0:
        status = "failed"
    elif review:
        status = "needs_review"
    elif numeric < len(months):
        status = "partial"
    else:
        status = "success"
    result = (values, qualities, sorted(reasons), positions, pixel_positions)
    return result + (diagnostics,) if return_diagnostics else result


def save_overlay(image: Image.Image, calibration: Calibration, positions: dict[str, int | None], pixel_positions: dict[str, float | None], output_path: Path, diagnostics: dict[str, Any] | None = None) -> None:
    overlay = image.convert("RGB").copy()
    draw = ImageDraw.Draw(overlay)
    draw.rectangle((calibration.plot_left, calibration.plot_top, calibration.plot_right, calibration.plot_bottom), outline=(255, 0, 255), width=2)
    for x in calibration.x_gridlines:
        draw.line((x, calibration.plot_top, x, calibration.plot_bottom), fill=(0, 180, 0), width=1)
    for y in calibration.y_gridlines:
        draw.line((calibration.plot_left, y, calibration.plot_right, y), fill=(0, 120, 255), width=1)
    for month, x in positions.items():
        y = pixel_positions[month]
        if x is not None and y is not None:
            draw.ellipse((x - 4, y - 4, x + 4, y + 4), outline=(0, 180, 0), width=2)
        detail = (diagnostics or {}).get(month, {})
        for candidate in detail.get("candidates", []):
            cy = candidate["y"]
            if candidate.get("vertical_spike"):
                draw.line((x - 4, cy - 4, x + 4, cy + 4), fill=(255, 140, 0), width=2)
                draw.line((x - 4, cy + 4, x + 4, cy - 4), fill=(255, 140, 0), width=2)
            elif y is None and detail.get("reason") == "ambiguous_line_candidate":
                draw.ellipse((x - 4, cy - 4, x + 4, cy + 4), outline=(255, 210, 0), width=2)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    overlay.save(output_path)

