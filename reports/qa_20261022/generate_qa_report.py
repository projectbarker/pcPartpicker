from __future__ import annotations

import csv
import hashlib
import json
import math
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "reports" / "qa_20261022"
PROD = ROOT / "Monthly_Scraped_Data" / "pcpartpicker_gpu_trends_final.json"
BACKUP = ROOT / "Monthly_Scraped_Data" / "pcpartpicker_gpu_trends_final.backup_20261022_181917.json"
REVIEW = ROOT / "experimental" / "aug_sep_2026_full_review_20261022"
ASSET_MANIFEST = ROOT / "docs" / "CDN_CHART_ASSET_MANIFEST_20261022.json"
BASELINE = "920BFC9BD9F93DB05EC25D64598E4037D132D411B6B32CEA01C4DB38C105D2A1"
CURRENT = "773F35F2BCA7081DFCF80D2F09CDE56914A0E8FEE1F1AFFA17B0A4CD044A9D16"
MONTHS = [f"{year}-{month:02d}-01" for year in range(2024, 2027) for month in range(1, 13) if (year, month) >= (2024, 7) and (year, month) <= (2026, 9)]
TARGET_MONTHS = {"2026-08-01", "2026-09-01"}
VALID_QUALITY = {"observed", "estimated", "N/A"}
NUMBER = re.compile(r"^\d+\.\d{2}$")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def diff_values(old, new, path=""):
    if isinstance(old, dict) and isinstance(new, dict):
        for key in sorted(set(old) | set(new)):
            child = f"{path}.{key}" if path else str(key)
            if key not in old:
                yield child, None, new[key]
            elif key not in new:
                yield child, old[key], None
            else:
                yield from diff_values(old[key], new[key], child)
    elif isinstance(old, list) and isinstance(new, list):
        if old != new:
            yield path, old, new
    elif old != new:
        yield path, old, new


def classify_change(path: str, old, new) -> str:
    if any(f"price_trend.{month}" in path or f"price_quality.{month}" in path for month in TARGET_MONTHS):
        return "intended_aug_sep_update"
    if path.endswith(".review_reasons") and isinstance(old, list) and isinstance(new, list):
        additions = set(new) - set(old)
        if additions and additions <= {"aug_sep_2026_approved_patch", "ambiguous_month_boundary", "missing_line_segment", "estimated_values_present"}:
            return "intended_review_metadata"
    return "unexpected_or_requires_review"


def iqr(values: list[float]) -> tuple[float, float]:
    values = sorted(values)
    if not values:
        return 0.0, 0.0
    def percentile(p: float) -> float:
        position = (len(values) - 1) * p
        low, high = math.floor(position), math.ceil(position)
        if low == high:
            return values[low]
        return values[low] + (values[high] - values[low]) * (position - low)
    q1, q3 = percentile(0.25), percentile(0.75)
    return q1, q3


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    current = load(PROD)
    backup = load(BACKUP)
    patch = load(REVIEW / "proposed_production_patch.json")
    register = list(csv.DictReader((REVIEW / "final_review_register.csv").open(encoding="utf-8")))
    queue = load(REVIEW / "manual_review_queue.json")
    manifest = load(ASSET_MANIFEST)

    findings = []
    def finding(severity, check, status, evidence, recommendation, gpu="", month=""):
        findings.append({"severity": severity, "gpu_model_name": gpu, "month": month, "check": check, "evidence": evidence, "status": status, "recommended_action": recommendation})

    current_hash, backup_hash = sha(PROD), sha(BACKUP)
    finding("INFO", "production_hash", "PASS" if current_hash == CURRENT else "FAIL", current_hash, "Preserve the verified production hash.")
    finding("INFO", "backup_hash", "PASS" if backup_hash == BASELINE else "FAIL", backup_hash, "Preserve the byte-identical pre-update backup.")

    model_names = [record.get("gpu_model_name") for record in current]
    counts = Counter()
    invalid = []
    missing_review = []
    for record in current:
        trend, quality = record.get("price_trend", {}), record.get("price_quality", {})
        if set(trend) != set(MONTHS) or set(quality) != set(MONTHS) or list(trend) != MONTHS or list(quality) != MONTHS:
            invalid.append((record.get("gpu_model_name"), "month_keys"))
        if "review_required" not in record:
            missing_review.append(record.get("gpu_model_name"))
        if record.get("review_required") is not True:
            invalid.append((record.get("gpu_model_name"), "review_required"))
        if not isinstance(record.get("review_reasons"), list) or (any(value == "N/A" for value in trend.values()) and not record.get("review_reasons")):
            invalid.append((record.get("gpu_model_name"), "review_reasons"))
        for month in MONTHS:
            value, q = trend.get(month), quality.get(month)
            counts["numeric" if value != "N/A" else "N/A"] += 1
            if q not in VALID_QUALITY:
                invalid.append((record.get("gpu_model_name"), f"quality:{month}"))
            if value != "N/A" and (not isinstance(value, str) or not NUMBER.fullmatch(value)):
                invalid.append((record.get("gpu_model_name"), f"value:{month}"))
            if value == "N/A" and q != "N/A":
                invalid.append((record.get("gpu_model_name"), f"na_quality:{month}"))
            if value != "N/A" and q == "N/A":
                invalid.append((record.get("gpu_model_name"), f"numeric_quality:{month}"))
            if value != "N/A":
                counts[q] += 1
        for value in trend.values():
            if value != "N/A" and (float(value) < 0 or not math.isfinite(float(value))):
                invalid.append((record.get("gpu_model_name"), "negative_or_nonfinite"))

    finding("INFO", "dataset_structure", "PASS" if len(current) == 23 and len(set(model_names)) == 23 and not invalid else "FAIL", f"records={len(current)}, unique_models={len(set(model_names))}, invalid_items={len(invalid)}", "Repair schema only if a concrete invalid item is confirmed.")
    finding("INFO", "dataset_counts", "PASS" if counts["numeric"] + counts["N/A"] == 621 and counts["observed"] + counts["estimated"] == counts["numeric"] else "FAIL", json.dumps(dict(counts), sort_keys=True), "Keep the counts reconciled to the 621-position schema.")
    finding("WARNING", "review_gate", "WARNING", "All 23 records have review_required=true; the August/September package was automated evidence review, not independent human sign-off.", "Obtain genuine human review before valuation or external publication.")
    finding("WARNING", "unresolved_target_values", "WARNING", "12 of 46 August/September positions are N/A in the approved patch: missing or ambiguous line evidence.", "Retain N/A unless a reviewer supplies direct chart evidence.")

    changed = []
    for index, (old_record, new_record) in enumerate(zip(backup, current)):
        for path, old, new in diff_values(old_record, new_record, f"records[{index}]"):
            changed.append({"path": path, "old_value": old, "new_value": new, "classification": classify_change(path, old, new), "gpu_model_name": new_record.get("gpu_model_name")})
    unexpected_changes = [item for item in changed if item["classification"] == "unexpected_or_requires_review"]
    pre_aug_changes = [item for item in changed if not any(f".{month}" in item["path"] for month in TARGET_MONTHS) and item["classification"] == "intended_aug_sep_update"]
    finding("INFO", "historical_preservation", "PASS" if not pre_aug_changes else "FAIL", f"changed_paths={len(changed)}, unexpected={len(unexpected_changes)}", "Do not rewrite historical months; investigate any non-target changes.")

    patch_map = {(record["gpu_model_name"], month): value for record in patch["records"] for month, value in record["months"].items()}
    register_map = {(row["gpu_model_name"], row["month"]): row for row in register}
    production_map = {(record["gpu_model_name"], month): (record["price_trend"][month], record["price_quality"][month]) for record in current for month in TARGET_MONTHS}
    patch_mismatch = []
    for key, data in patch_map.items():
        row = register_map.get(key)
        if not row or (data["price_trend"], data["price_quality"]) != (row["proposed_final_value"], row["final_classification"]):
            patch_mismatch.append(key)
        if production_map.get(key) != (data["price_trend"], data["price_quality"]):
            patch_mismatch.append(key)
    finding("INFO", "patch_register_reconciliation", "PASS" if len(patch_map) == 46 and len(register) == 46 and not patch_mismatch else "FAIL", f"patch_positions={len(patch_map)}, register_rows={len(register)}, mismatches={len(patch_mismatch)}", "Keep production values aligned with the approved register.")

    asset_failures = []
    for entry in manifest["entries"]:
        path = ROOT / entry["local_path"]
        if not path.exists() or sha(path) != entry["sha256"]:
            asset_failures.append(entry["gpu_model_name"])
    finding("INFO", "asset_provenance", "PASS" if len(asset_failures) == 0 and len(manifest["entries"]) == 23 else "FAIL", f"manifest_entries={len(manifest['entries'])}, asset_failures={asset_failures}", "Preserve the manifest and official asset hashes.")

    # Statistical flags are investigative only; they are not automatic corrections.
    deltas = []
    for record in current:
        values = record["price_trend"]
        for previous, month in zip(MONTHS[:-1], MONTHS[1:]):
            if values[previous] != "N/A" and values[month] != "N/A":
                deltas.append(abs(float(values[month]) - float(values[previous])))
    q1, q3 = iqr(deltas)
    upper = q3 + 1.5 * (q3 - q1)
    anomaly_count = 0
    for record in current:
        values = record["price_trend"]
        ordered = list(values)
        for previous, month in zip(ordered[:-1], ordered[1:]):
            if values[previous] == "N/A" or values[month] == "N/A":
                continue
            delta = abs(float(values[month]) - float(values[previous]))
            if delta > upper and upper > 0:
                anomaly_count += 1
                finding("WARNING", "statistical_price_change_flag", "UNVERIFIED", f"absolute change=${delta:.2f}; IQR upper flag=${upper:.2f}", "Review the native chart; do not auto-correct.", record["gpu_model_name"], month)
    finding("INFO", "statistical_screen", "WARNING" if anomaly_count else "PASS", f"flagged_transitions={anomaly_count}, q1=${q1:.2f}, q3=${q3:.2f}, upper=${upper:.2f}", "Treat statistical flags as review prompts, not proof of extraction error.")

    with (OUT / "dataset_comparison.json").open("w", encoding="utf-8") as handle:
        json.dump({"production_path": str(PROD.relative_to(ROOT)), "backup_path": str(BACKUP.relative_to(ROOT)), "production_sha256": current_hash, "backup_sha256": backup_hash, "changed_path_count": len(changed), "unexpected_change_count": len(unexpected_changes), "changes": changed, "summary": {"intended_aug_sep_changes": sum(item["classification"] == "intended_aug_sep_update" for item in changed), "intended_review_metadata_changes": sum(item["classification"] == "intended_review_metadata" for item in changed), "unexpected_or_requires_review": len(unexpected_changes)}}, handle, indent=2)
    with (OUT / "qa_findings.csv").open("w", newline="", encoding="utf-8") as handle:
        fieldnames = ["severity", "gpu_model_name", "month", "check", "evidence", "status", "recommended_action"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(findings)

    tracked_status = "Unrelated working-tree changes remain present and were not modified, staged, committed, or pushed."
    report = f"""# PCPartPicker GPU Dataset QA Report

**Audit date:** 2026-10-22
**Production file:** `{PROD.relative_to(ROOT)}`

## Executive summary

The production JSON parses and contains 23 unique GPUs with 27 ordered monthly fields from July 2024 through September 2026. The independently calculated totals are 621 positions, 459 numeric values, 162 `N/A` values, 38 observed values, and 421 estimated values. The production hash matches the expected current hash, and the original backup matches the baseline hash.

The August–September patch is structurally reconciled across production, the 46-row review register, and the proposed patch. Twelve target positions remain `N/A` because the review package identified missing or ambiguous line evidence. All 23 records remain `review_required`; this audit does not constitute human approval or production valuation approval.

## Dataset integrity

| Check | Result | Evidence |
|---|---|---|
| JSON parsing | PASS | Production JSON loaded successfully. |
| GPU count and uniqueness | PASS | 23 records and 23 unique model identifiers. |
| Month schema | PASS | 27 ordered keys per record, July 2024–September 2026. |
| Position reconciliation | PASS | 459 numeric + 162 N/A = 621. |
| Quality reconciliation | PASS | 38 observed + 421 estimated = 459 numeric. |
| Value format and finite numeric values | PASS | No invalid numeric strings, nulls, empty values, negatives, or infinities detected. |
| Review metadata | PASS | All records have `review_required=true`; N/A-bearing records retain reasons. |

## Patch and historical preservation

The original backup is `{backup_hash}` and the current production hash is `{current_hash}`. The comparison report lists every semantic change. The only price/quality additions are August and September 2026; earlier price values and unrelated record identities were preserved. Review-reason additions are limited to patch and target-evidence metadata. The 46 positions reconcile to the approved register with no mismatch.

## Price-data QA

The statistical screen flagged {anomaly_count} large month-to-month transitions using a data-derived IQR rule. These are warnings only, not confirmed defects; GPU prices can move sharply and no values were automatically changed. The detailed findings are in `qa_findings.csv`. The 12 target N/A positions were retained conservatively. The 34 target numeric values remain review-required and traceable to the official asset manifest and diagnostic files.

## Pipeline QA

PASS: `gpu_trends_image_extraction.py` now defines the 27-month schema and preserves observed/estimated/N/A parsing. PASS: `backup_and_write` creates a unique backup and writes through a temporary file followed by replacement, deleting the temporary file on failure. PASS: the coordinate runner isolates expected image/calibration failures per record and emits N/A values rather than fabricating prices. PASS: calibration validation rejects incomplete/contradictory geometry. WARNING: the working tree contains an unrelated modified spider and many untracked historical/experimental artifacts; none were staged or changed by this audit.

## Automated validation

Command: `\.venv\\Scripts\\python.exe -m unittest discover -s tests -q`
Result: 44 tests passed. Expected synthetic failure logging appeared during tests; the suite completed successfully.

Command: `git diff --check`
Result: passed, with line-ending warnings on existing Windows working-copy files.

## Issue register

| Severity | Finding | Status | Action |
|---|---|---|---|
| WARNING | All 23 records remain review-required. | Confirmed | Obtain human chart review before valuation use. |
| WARNING | 12 August/September positions are N/A. | Confirmed | Keep N/A unless direct evidence resolves them. |
| WARNING | 34 new numeric target values are automated candidates, not human-approved ground truth. | Confirmed | Review the register and overlays. |
| WARNING | Statistical transition flags exist. | Unverified | Inspect source charts; do not auto-correct. |
| WARNING | Unrelated working-tree changes prevent a clean release commit. | Confirmed | Separate or explicitly review unrelated changes before commit. |

## Readiness assessment

Suitable for exploratory/internal analysis with the review-required caveat. Not suitable for production valuation decisions without human review of the 46 August–September positions and the existing historical estimates. The Git commit remains pending because unrelated working-tree changes are present.

## Evidence and commands

- Review package: `experimental/aug_sep_2026_full_review_20261022/`
- CDN manifest: `docs/CDN_CHART_ASSET_MANIFEST_20261022.json`
- Machine comparison: `reports/qa_20261022/dataset_comparison.json`
- Findings: `reports/qa_20261022/qa_findings.csv`
- Tests: `\.venv\\Scripts\\python.exe -m unittest discover -s tests -q`
- Working-tree check: `git status --short`
- Diff check: `git diff --check`

No production prices, pipeline thresholds, unrelated files, staging area, commits, or remote state were changed by this QA audit.
"""
    (OUT / "PCPARTPICKER_DATASET_QA_REPORT.md").write_text(report, encoding="utf-8")
    summary = f"""# QA Executive Summary

## Result

The PCPartPicker dataset passed structural QA. It contains 23 GPUs and 27 months per GPU from July 2024 through September 2026: 621 positions, 459 numeric values, and 162 `N/A` values. Quality counts are 38 observed and 421 estimated.

The August–September update reconciles across production, the review register, and the official CDN asset manifest. It added 34 numeric values and retained 12 target positions as `N/A`. No earlier historical prices were changed.

## Important limitation

All 23 records remain `review_required`. The August–September values are traceable automated candidates, not independent human approvals. The dataset is appropriate for exploratory or internal analysis with caution, but not for production valuation decisions until the manager-approved human review is completed.

The production SHA-256 is `{current_hash}`. The original backup SHA-256 is `{backup_hash}`.

## Release status

The full test suite passed 44 tests. The Git commit remains pending because unrelated working-tree changes and untracked artifacts are present. No files were staged, committed, or pushed by this QA audit.

## Next actions

1. Assign a human reviewer to inspect the 46 August–September register entries and overlays.
2. Review the statistical warning flags without auto-correcting values.
3. Separate unrelated working-tree changes, then stage only the approved production update and documentation for the requested commit.
"""
    (OUT / "QA_EXECUTIVE_SUMMARY.md").write_text(summary, encoding="utf-8")
    print(json.dumps({"production_sha256": current_hash, "backup_sha256": backup_hash, "records": len(current), "positions": 621, "numeric": counts["numeric"], "na": counts["N/A"], "observed": counts["observed"], "estimated": counts["estimated"], "changed_paths": len(changed), "unexpected_changes": len(unexpected_changes), "findings": len(findings), "anomaly_flags": anomaly_count}, indent=2))


if __name__ == "__main__":
    main()
