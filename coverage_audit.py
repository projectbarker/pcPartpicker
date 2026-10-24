"""Build a month-level evidence and coverage audit without extracting prices."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any

from coverage_config import EXPECTED_MONTHS


ROOT = Path(__file__).resolve().parent
PRODUCTION_PATH = ROOT / "Monthly_Scraped_Data" / "pcpartpicker_gpu_trends_final.json"
CACHED_SOURCE_DIR = ROOT / "diagnostics" / "cached_july_2026_sources"
CACHED_DIAGNOSTIC_DIR = ROOT / "diagnostics" / "cached_july_2026_extraction" / "recovery_artifacts"
LIVE_SOURCE_DIR = ROOT / "diagnostics" / "live_chart_sources_20261022"
LIVE_REVIEW_DIR = ROOT / "experimental" / "aug_sep_2026_full_review_20261022"
CACHED_INVENTORY_PATH = ROOT / "Monthly_Scraped_Data" / "pcpartpicker_gpu_sources_cached_2026.07.03.json"
LIVE_MANIFEST_PATH = ROOT / "docs" / "CDN_CHART_ASSET_MANIFEST_20261022.json"
HISTORICAL_REGISTER_PATH = ROOT / "reports" / "qa_20261022" / "HISTORICAL_QA_WARNING_REGISTER.csv"
QA_FINDINGS_PATH = ROOT / "reports" / "qa_20261022" / "qa_findings.csv"
PATCH_REGISTER_PATH = LIVE_REVIEW_DIR / "final_review_register.csv"


AUDIT_FIELDS = [
    "gpu_model_name", "month", "json_field_exists", "json_value", "value_classification",
    "original_chart_evidence_available", "evidence_file_or_source_reference",
    "evidence_retrieval_verification_status", "extraction_status", "review_required",
    "qa_status", "final_coverage_classification", "reason_for_classification",
]


def _slug(model: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "_" for ch in model).strip("_")


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _diagnostic_status(path: Path, month: str) -> tuple[str, str | None]:
    if not path.exists():
        return "not_available", None
    data = _load(path)
    entry = data.get("monthly_sampling_diagnostics", {}).get(month)
    if not entry:
        return "not_recorded", None
    status = entry.get("status", "not_recorded")
    reason = entry.get("reason")
    return status, reason


def _source_maps() -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    cached = {item["gpu_model_name"]: item for item in _load(CACHED_INVENTORY_PATH)["entries"]}
    live = {item["gpu_model_name"]: item for item in _load(LIVE_MANIFEST_PATH)["entries"]}
    return cached, live


def _reference_maps() -> tuple[dict[tuple[str, str], dict[str, str]], dict[tuple[str, str], dict[str, str]], set[tuple[str, str]]]:
    historical = {(row["gpu_model_name"], row["month"]): row for row in _csv_rows(HISTORICAL_REGISTER_PATH)}
    qa = {(row.get("gpu_model_name", ""), row.get("month", "")): row for row in _csv_rows(QA_FINDINGS_PATH) if row.get("gpu_model_name")}
    patch = {(row["gpu_model_name"], row["month"]): row for row in _csv_rows(PATCH_REGISTER_PATH)}
    return historical, patch, set(qa)


def build_audit_records(production_path: Path = PRODUCTION_PATH) -> list[dict[str, str]]:
    records = _load(production_path)
    cached_sources, live_sources = _source_maps()
    historical, patch, qa_keys = _reference_maps()
    result: list[dict[str, str]] = []

    for record in records:
        model = record["gpu_model_name"]
        slug = _slug(model)
        trend = record.get("price_trend", {})
        quality = record.get("price_quality", {})
        cached_diag_path = CACHED_DIAGNOSTIC_DIR / f"{slug}.diagnostics.json"
        cached_diag = _load(cached_diag_path) if cached_diag_path.exists() else {}
        for month in EXPECTED_MONTHS:
            value = trend.get(month, "N/A")
            value_quality = quality.get(month, "N/A")
            is_live_month = month in {"2026-08-01", "2026-09-01"}
            if is_live_month:
                patch_row = patch.get((model, month), {})
                image_path = patch_row.get("evidence_image_path", f"diagnostics/live_chart_sources_20261022/{slug}.png")
                diagnostic_path = patch_row.get("diagnostic_json_path", f"experimental/aug_sep_2026_full_review_20261022/{slug}.diagnostic.json")
                source_url = live_sources.get(model, {}).get("url", "")
                sample_status = patch_row.get("sampling_status", "not_recorded")
                sample_reason = patch_row.get("sampling_reason") or ""
                image_available = (ROOT / image_path.replace("\\", "/")).exists()
                evidence_status = "asset_verified_automated_sample" if sample_status == "accepted" else "asset_verified_candidate_rejected"
            else:
                image_path = f"diagnostics/cached_july_2026_sources/{slug}.png"
                diagnostic_path = f"diagnostics/cached_july_2026_extraction/recovery_artifacts/{slug}.diagnostics.json"
                source_url = cached_sources.get(model, {}).get("cached_image_url", "")
                sample_status, sample_reason = _diagnostic_status(cached_diag_path, month)
                image_available = (ROOT / image_path).exists()
                if sample_status == "accepted":
                    evidence_status = "asset_present_automated_candidate"
                elif sample_status == "out_of_history":
                    evidence_status = "asset_present_month_not_visible"
                elif sample_status == "not_available":
                    evidence_status = "asset_or_diagnostic_unavailable"
                else:
                    evidence_status = "asset_present_candidate_rejected"

            key = (model, month)
            if key in historical:
                qa_status = "unresolved_historical_qa_warning"
            elif key in patch and patch[key].get("proposed_final_value") == "N/A":
                qa_status = "unresolved_aug_sep_position"
            elif key in qa_keys:
                qa_status = "statistical_warning_explained_automated_only"
            else:
                qa_status = "not_flagged"

            if sample_status == "out_of_history":
                final_class = "missing_evidence"
                reason = "The retained chart asset exists, but this month is outside its visible history."
            elif sample_status in {"rejected", "missing_line_segment", "ambiguous_line_candidate", "isolated_spike"} or sample_reason:
                final_class = "ambiguous"
                reason = f"The sampler did not accept an unambiguous line point ({sample_reason or sample_status})."
            elif value == "N/A":
                final_class = "missing_evidence"
                reason = "The JSON field is present as N/A and no accepted numeric point is recorded for this month."
            elif record.get("review_required"):
                final_class = "pending_human_review"
                reason = "Numeric value has automated/source support but the record remains review-required; no human validation is recorded."
            else:
                final_class = "validated"
                reason = "No review requirement recorded."

            evidence_reference = "; ".join(filter(None, [image_path, diagnostic_path, source_url]))
            result.append({
                "gpu_model_name": model,
                "month": month,
                "json_field_exists": str(month in trend).lower(),
                "json_value": str(value),
                "value_classification": value_quality,
                "original_chart_evidence_available": "yes" if image_available else "no",
                "evidence_file_or_source_reference": evidence_reference,
                "evidence_retrieval_verification_status": evidence_status,
                "extraction_status": f"{record.get('extraction_status', 'unknown')}:{sample_status}",
                "review_required": str(bool(record.get("review_required"))).lower(),
                "qa_status": qa_status,
                "final_coverage_classification": final_class,
                "reason_for_classification": reason,
            })
    return result


def write_audit(output_path: Path, summary_path: Path) -> dict[str, Any]:
    rows = build_audit_records()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=AUDIT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "dataset_start_month": EXPECTED_MONTHS[0],
        "dataset_end_month": EXPECTED_MONTHS[-1],
        "months_per_gpu": len(EXPECTED_MONTHS),
        "gpu_count": len({row["gpu_model_name"] for row in rows}),
        "total_gpu_month_positions": len(rows),
        "json_fields_present": sum(row["json_field_exists"] == "true" for row in rows),
        "numeric_values": sum(row["json_value"] != "N/A" for row in rows),
        "na_values": sum(row["json_value"] == "N/A" for row in rows),
        "value_classification_counts": dict(Counter(row["value_classification"] for row in rows)),
        "final_coverage_classification_counts": dict(Counter(row["final_coverage_classification"] for row in rows)),
        "qa_status_counts": dict(Counter(row["qa_status"] for row in rows)),
        "source_asset_rows": sum(row["original_chart_evidence_available"] == "yes" for row in rows),
        "all_records_review_required": all(row["review_required"] == "true" for row in rows),
        "validated_rows": sum(row["final_coverage_classification"] == "validated" for row in rows),
    }
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    print(json.dumps(write_audit(ROOT / "reports" / "coverage_audit_20261023.csv", ROOT / "reports" / "coverage_summary_20261023.json"), indent=2))
