# PCPartPicker GPU Dataset QA Report

**Audit date:** 2026-10-22
**Production file:** `Monthly_Scraped_Data\pcpartpicker_gpu_trends_final.json`

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

The original backup is `920BFC9BD9F93DB05EC25D64598E4037D132D411B6B32CEA01C4DB38C105D2A1` and the current production hash is `773F35F2BCA7081DFCF80D2F09CDE56914A0E8FEE1F1AFFA17B0A4CD044A9D16`. The comparison report lists every semantic change. The only price/quality additions are August and September 2026; earlier price values and unrelated record identities were preserved. Review-reason additions are limited to patch and target-evidence metadata. The 46 positions reconcile to the approved register with no mismatch.

## Price-data QA

The statistical screen flagged 39 large month-to-month transitions using a data-derived IQR rule. These are warnings only, not confirmed defects; GPU prices can move sharply and no values were automatically changed. The detailed findings are in `qa_findings.csv`. The 12 target N/A positions were retained conservatively. The 34 target numeric values remain review-required and traceable to the official asset manifest and diagnostic files.

## Pipeline QA

PASS: `gpu_trends_image_extraction.py` now defines the 27-month schema and preserves observed/estimated/N/A parsing. PASS: `backup_and_write` creates a unique backup and writes through a temporary file followed by replacement, deleting the temporary file on failure. PASS: the coordinate runner isolates expected image/calibration failures per record and emits N/A values rather than fabricating prices. PASS: calibration validation rejects incomplete/contradictory geometry. WARNING: the working tree contains an unrelated modified spider and many untracked historical/experimental artifacts; none were staged or changed by this audit.

## Automated validation

Command: `\.venv\Scripts\python.exe -m unittest discover -s tests -q`
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
- Tests: `\.venv\Scripts\python.exe -m unittest discover -s tests -q`
- Working-tree check: `git status --short`
- Diff check: `git diff --check`

No production prices, pipeline thresholds, unrelated files, staging area, commits, or remote state were changed by this QA audit.
