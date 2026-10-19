"""Extract monthly PCPartPicker GPU prices from trend-chart images."""

from __future__ import annotations

import argparse
import json
import logging
import os
import shutil
import tempfile
import time
from pathlib import Path
from typing import Any, Callable
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

import requests
from dotenv import load_dotenv
from openai import OpenAI

LOGGER = logging.getLogger(__name__)
DEFAULT_MODEL = "gpt-4o-mini"
EXPECTED_MONTHS = [
    f"{year}-{month:02d}-01"
    for year in range(2024, 2027)
    for month in range(1, 13)
    if (year, month) >= (2024, 7) and (year, month) <= (2026, 1)
]


def load_gpu_records(path: Path) -> list[dict[str, Any]]:
    """Load valid, unique GPU model/image records from JSON."""
    with path.open("r", encoding="utf-8") as handle:
        records = json.load(handle)
    if not isinstance(records, list):
        raise ValueError("Input JSON must contain a list of GPU records.")
    clean: list[dict[str, Any]] = []
    seen_models: set[str] = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            LOGGER.warning("Skipping record %d: expected an object", index)
            continue
        model = record.get("gpu_model")
        image_url = record.get("image_url")
        if not isinstance(model, str) or not model.strip():
            LOGGER.warning("Skipping record %d: missing gpu_model", index)
            continue
        if not isinstance(image_url, str) or not image_url.startswith(("http://", "https://")):
            LOGGER.warning("Skipping %s: invalid image_url", model)
            continue
        model = model.strip()
        if model in seen_models:
            LOGGER.warning("Skipping duplicate GPU model: %s", model)
            continue
        seen_models.add(model)
        clean.append({"gpu_model": model, "image_url": image_url.strip()})
    return clean


def validate_image_url(image_url: str, timeout: int = 20) -> tuple[bool, str]:
    """Check that a URL returns a non-empty PNG/JPEG-like image."""
    try:
        response = requests.get(image_url, timeout=timeout, headers={"User-Agent": "GPU-PCPartPicker-turnover/1.0"})
        response.raise_for_status()
        content = response.content
        content_type = response.headers.get("Content-Type", "").lower()
        signature_ok = content.startswith(b"\x89PNG\r\n\x1a\n") or content.startswith(b"\xff\xd8\xff")
        if not content or not (signature_ok or "image/" in content_type):
            return False, "response is not a recognized image"
        return True, "ok"
    except requests.RequestException as exc:
        return False, str(exc)


def feature_extraction_prompt_template(item: dict[str, Any]) -> str:
    return f"""Analyze this PCPartPicker GPU price-trend chart.

GPU model: {item['gpu_model']}
Image URL: {item['image_url']}

Extract the price at the start of each month from July 2024 through January
2026, inclusive. Use only the thick, solid black actual-price line. Ignore
blue lines, shaded ranges, projections, markers, annotations, and watermarks.
Treat the line as a step function and read the first stable value immediately
after each month boundary. Read the USD y-axis and interpolate only when the
chart supports a reasonable visual reading. Do not average, extrapolate,
smooth, or invent values. Use "N/A" when a value cannot be read confidently.

Return exactly one JSON object with these 19 date keys:
{', '.join(EXPECTED_MONTHS)}
For each date return an object with "value", "quality", and "reason".
Quality must be "observed", "estimated", or "N/A". Use "observed" when the
line is directly readable at a gridline/step level. Use "estimated" only when
the axes and line position are clear but interpolation is required. Use "N/A"
for missing history, gaps, ambiguous points, or unclear axes. Return JSON only."""


SYSTEM_PROMPT = """You are a careful GPU price-chart analyst.
First identify the plot area, visible month/date axis, USD y-axis, gridlines,
and thick black actual-price line. Map each requested month to the black line
immediately after its month boundary. Never fabricate, extrapolate, smooth, or
fill gaps. Return valid JSON only, without Markdown or commentary."""

VALID_QUALITIES = {"observed", "estimated", "N/A"}
VALID_REASONS = {
    "estimated_values_present", "ambiguous_month_boundary", "missing_line_segment",
    "axis_unclear", "outside_visible_history", "suspicious_sequence",
}


def normalize_reason(reason: Any) -> str | None:
    """Map common model prose to the controlled review reason vocabulary."""
    if not isinstance(reason, str):
        return None
    text = reason.strip().lower()
    if text in VALID_REASONS:
        return text
    if "missing history" in text or "outside" in text or "not available" in text:
        return "outside_visible_history"
    if "ambiguous" in text or "unclear" in text:
        return "ambiguous_month_boundary"
    if "gap" in text or "missing line" in text:
        return "missing_line_segment"
    if "axis" in text or "scale" in text:
        return "axis_unclear"
    if "estimate" in text or "interpolat" in text:
        return "estimated_values_present"
    return None


def parse_model_output(result: str | None) -> tuple[dict[str, str], dict[str, str], list[str], str]:
    """Normalize model output and return values, quality, reasons, and status."""
    if not result:
        return {}, {}, [], "failed"
    try:
        parsed = json.loads(result)
    except (json.JSONDecodeError, TypeError) as exc:
        LOGGER.error("Model response was not valid JSON: %s", exc)
        return {}, {}, [], "failed"
    if not isinstance(parsed, dict):
        LOGGER.error("Model response was not a JSON object")
        return {}, {}, [], "failed"
    cleaned: dict[str, str] = {}
    quality: dict[str, str] = {}
    reasons: set[str] = set()
    numeric_count = 0
    for month in EXPECTED_MONTHS:
        entry = parsed.get(month, {"value": "N/A", "quality": "N/A", "reason": "outside_visible_history"})
        if isinstance(entry, dict):
            value = entry.get("value", "N/A")
            item_quality = entry.get("quality", "N/A")
            reason = entry.get("reason")
        else:
            value = entry
            item_quality = "observed" if entry != "N/A" else "N/A"
            reason = None
        if item_quality not in VALID_QUALITIES:
            LOGGER.warning("Invalid quality for %s: %r; using N/A", month, item_quality)
            value, item_quality, reason = "N/A", "N/A", "axis_unclear"
        reason = normalize_reason(reason)
        if reason:
            reasons.add(reason)
        if isinstance(value, str) and value.strip().upper() == "N/A":
            cleaned[month] = "N/A"
            quality[month] = "N/A"
            continue
        try:
            if isinstance(value, str):
                value = value.strip().replace("$", "").replace(",", "")
            price = Decimal(str(value))
            if price < 0 or price > 10000:
                raise ValueError("price outside validation bounds")
            if item_quality == "estimated":
                price = price.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
            cleaned[month] = f"{price:.2f}"
            quality[month] = item_quality
            numeric_count += 1
            if item_quality == "estimated":
                reasons.add("estimated_values_present")
        except (TypeError, ValueError, InvalidOperation):
            LOGGER.warning("Invalid price for %s: %r; using N/A", month, value)
            cleaned[month] = "N/A"
            quality[month] = "N/A"
    unexpected = set(parsed) - set(EXPECTED_MONTHS)
    if unexpected:
        LOGGER.warning("Ignoring unexpected month keys: %s", sorted(unexpected))
    numeric_values = [Decimal(value) for value in cleaned.values() if value != "N/A"]
    if len(numeric_values) >= 4:
        deltas = [numeric_values[index + 1] - numeric_values[index] for index in range(len(numeric_values) - 1)]
        if len(set(abs(delta) for delta in deltas)) == 1 and len(set(deltas)) <= 2 and abs(deltas[0]) >= 25:
            reasons.add("suspicious_sequence")
    if numeric_count == 0:
        return cleaned, quality, sorted(reasons), "failed"
    review_reasons = reasons & {"estimated_values_present", "ambiguous_month_boundary", "missing_line_segment", "axis_unclear", "suspicious_sequence"}
    if review_reasons:
        return cleaned, quality, sorted(reasons), "needs_review"
    if numeric_count < len(EXPECTED_MONTHS):
        return cleaned, quality, sorted(reasons), "partial"
    return cleaned, quality, sorted(reasons), "success"


def safe_parse_json(result: str | None) -> tuple[dict[str, str], str]:
    """Backward-compatible value/status parser for simple callers."""
    values, _quality, _reasons, status = parse_model_output(result)
    return values, status


def extract_one(
    item: dict[str, Any],
    client: OpenAI,
    model: str = DEFAULT_MODEL,
    max_completion_tokens: int = 5000,
    retries: int = 2,
    sleep: Callable[[float], None] = time.sleep,
    raw_response_path: Path | None = None,
) -> dict[str, Any]:
    """Extract one chart, retrying API exceptions a bounded number of times."""
    record = {
        "gpu_model_name": item.get("gpu_model"),
        "image_url": item.get("image_url"),
        "price_trend": {month: "N/A" for month in EXPECTED_MONTHS},
        "price_quality": {month: "N/A" for month in EXPECTED_MONTHS},
        "review_required": False,
        "review_reasons": [],
        "extraction_status": "failed",
    }
    for attempt in range(retries + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                temperature=0,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": [
                        {"type": "text", "text": feature_extraction_prompt_template(item)},
                        {"type": "image_url", "image_url": {"url": item["image_url"], "detail": "high"}},
                    ]},
                ],
                max_completion_tokens=max_completion_tokens,
            )
            content = response.choices[0].message.content
            if raw_response_path:
                raw_response_path.parent.mkdir(parents=True, exist_ok=True)
                raw_response_path.write_text(content or "", encoding="utf-8")
            trend, quality, reasons, status = parse_model_output(content)
            record["price_trend"] = trend or record["price_trend"]
            record["price_quality"] = quality or record["price_quality"]
            record["review_reasons"] = reasons
            record["review_required"] = status == "needs_review"
            record["extraction_status"] = status
            if status == "failed":
                LOGGER.error("No usable monthly prices extracted for %s", item["gpu_model"])
            return record
        except Exception as exc:
            if attempt >= retries:
                LOGGER.error("API extraction failed for %s: %s", item["gpu_model"], exc)
                return record
            delay = 2 ** attempt
            LOGGER.warning("API attempt %d failed for %s; retrying in %ss", attempt + 1, item["gpu_model"], delay)
            sleep(delay)
    return record


def backup_and_write(records: list[dict[str, Any]], output_path: Path) -> Path | None:
    """Back up an existing output and atomically write JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    backup_path: Path | None = None
    if output_path.exists():
        stamp = time.strftime("%Y%m%d_%H%M%S")
        backup_path = output_path.with_name(f"{output_path.stem}.backup_{stamp}{output_path.suffix}")
        suffix = 1
        while backup_path.exists():
            backup_path = output_path.with_name(
                f"{output_path.stem}.backup_{stamp}_{suffix}{output_path.suffix}"
            )
            suffix += 1
        shutil.copy2(output_path, backup_path)
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=output_path.parent, delete=False) as handle:
            temp_path = Path(handle.name)
            json.dump(records, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        temp_path.replace(output_path)
    except Exception:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)
        raise
    return backup_path


def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    statuses = {status: sum(r.get("extraction_status") == status for r in records) for status in ("success", "partial", "needs_review", "failed")}
    missing_by_gpu = {r.get("gpu_model_name", "unknown"): sum(v == "N/A" for v in r.get("price_trend", {}).values()) for r in records}
    numeric = sum(v != "N/A" for r in records for v in r.get("price_trend", {}).values())
    return {"input_gpus": len(records), "unique_gpu_models": len({r.get("gpu_model_name") for r in records}), **statuses, "numeric_monthly_values": numeric, "missing_monthly_values": len(records) * len(EXPECTED_MONTHS) - numeric, "missing_by_gpu": missing_by_gpu}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("pcpartpicker_gpu_trends.json"))
    parser.add_argument("--output", type=Path, default=Path("Monthly_Scraped_Data/pcpartpicker_gpu_trends_latest.json"))
    parser.add_argument("--limit", type=int, default=None, help="Process only the first N records for a controlled test")
    parser.add_argument("--skip-image-check", action="store_true", help="Skip HTTP image validation")
    parser.add_argument("--diagnostic-dir", type=Path, default=None, help="Save raw model JSON responses here")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    args = parser.parse_args()
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is missing; set it in the environment or .env file")
    records = load_gpu_records(args.input)
    selected = records[: args.limit] if args.limit is not None else records
    LOGGER.info("Loaded %d unique GPU records; processing %d", len(records), len(selected))
    client = OpenAI(api_key=api_key)
    results = []
    for item in selected:
        if not args.skip_image_check:
            valid, reason = validate_image_url(item["image_url"])
            if not valid:
                LOGGER.error("Skipping %s: image validation failed: %s", item["gpu_model"], reason)
                results.append({"gpu_model_name": item["gpu_model"], "image_url": item["image_url"], "price_trend": {m: "N/A" for m in EXPECTED_MONTHS}, "price_quality": {m: "N/A" for m in EXPECTED_MONTHS}, "review_required": False, "review_reasons": ["image_validation_failed"], "extraction_status": "failed"})
                continue
        diagnostic_path = None
        if args.diagnostic_dir:
            safe_name = "".join(character.lower() if character.isalnum() else "_" for character in item["gpu_model"]).strip("_")
            diagnostic_path = args.diagnostic_dir / f"{safe_name}.response.json"
        results.append(extract_one(item, client, model=args.model, raw_response_path=diagnostic_path))
    backup = backup_and_write(results, args.output)
    LOGGER.info("Summary: %s", json.dumps(summarize(results), sort_keys=True))
    if backup:
        LOGGER.info("Previous output backed up to %s", backup)
    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    raise SystemExit(main())
