# Historical Warning Evidence Assessment

Focused senior data-quality assessment of the four historical QA warnings. This review does not change prices, classifications, review flags, source artifacts, or QA findings.

## Evidence inspected

- `HUMAN_APPROVAL_SUMMARY.md`
- `FINAL_REVIEW_REPORT.md`
- `reports/qa_20261022/HISTORICAL_QA_WARNING_REGISTER.csv`
- `reports/qa_20261022/qa_findings.csv`
- `coordinate_calibration.py`, `coordinate_calibration_runner.py`, and `gpu_trends_image_extraction.py`
- RTX 4080 source: `diagnostics/cached_july_2026_sources/geforce_rtx_4080.png`
- RTX 4080 overlay: `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_4080.overlay.png`
- RTX 4080 diagnostic: `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_4080.diagnostics.json`
- RTX 4090 source: `diagnostics/cached_july_2026_sources/geforce_rtx_4090.png`
- RTX 4090 overlay: `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_4090.overlay.png`
- RTX 4090 diagnostic: `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_4090.diagnostics.json`

The source images and overlays were inspected at native chart resolution. Both are 1176 × 484. The RTX 4080 y-axis maps y=27..427 to $3,000..$0. The RTX 4090 y-axis maps y=27..427 to $6,000..$0.

## Assessment table

| QA ID | GPU / month | Existing value and quality | Does the retained chart show the month? | Direct point at the correct monthly coordinate? | Evidence conclusion | Can existing evidence resolve it? | Recommended disposition |
|---|---|---:|---|---|---|---|---|
| `QA-20261022-L15` | GeForce RTX 4080 — 2024-11-01 | `$1,104.00`, `estimated` | No. Diagnostic status is `out_of_history`; the visible chart begins around January/February 2025. | No x-coordinate or y-point exists for November 2024. | The production number is not directly supported by the retained chart; its provenance cannot be established from this source. | No. Resolving it requires a chart asset whose visible history includes November 2024, with verified month and y-axis calibration. | Keep `$1,104.00` unchanged, `estimated`, `review_required=true`, and `unresolved`; or obtain historical evidence and reassess. |
| `QA-20261022-L16` | GeForce RTX 4080 — 2024-12-01 | `$1,403.00`, `estimated` | No. Diagnostic status is `out_of_history`; December 2024 is outside the visible chart history. | No x-coordinate or y-point exists for December 2024. | The production number is not directly supported by the retained chart; its provenance cannot be established from this source. | No. A source chart covering December 2024 is required. | Keep `$1,403.00` unchanged, `estimated`, `review_required=true`, and `unresolved`; or obtain historical evidence and reassess. |
| `QA-20261022-L17` | GeForce RTX 4080 — 2025-01-01 | `$1,291.00`, `estimated` | Only at the left edge. The diagnostic maps January to x=55 but rejects the point as `missing_line_segment`. | No accepted point at x=55. The visible trace enters near the boundary, but the retained evidence does not prove that it represents the January monthly sample. | The value is not a verified observation. It remains an estimated production value with unresolved coordinate/provenance evidence. | Not safely. Existing code intentionally returns `missing_line_segment` when no supported component is found; relaxing that check would be unsafe. | Keep `$1,291.00` unchanged, `estimated`, `review_required=true`, and `unresolved`; or obtain a verified edge-coordinate calibration/source point. |
| `QA-20261022-L19` | GeForce RTX 4090 — 2024-10-01 | `$1,940.00`, `estimated` | No. Diagnostic status is `out_of_history`; the visible chart begins around January/February 2025. | No x-coordinate or y-point exists for October 2024. | The production number is not directly supported by the retained chart; its provenance cannot be established from this source. | No. A chart asset covering October 2024 with verified calibration is required. | Keep `$1,940.00` unchanged, `estimated`, `review_required=true`, and `unresolved`; or obtain historical evidence and reassess. |

## Relevant code behavior

The calibration implementation derives monthly x positions from the anchor date and x-coordinate. Months outside the chart history are recorded as `out_of_history`. At an in-history position, the sampler requires a supported connected black-line component; if none exists it records `missing_line_segment`. Candidate components marked as vertical spikes are rejected rather than converted into prices. These safeguards are consistent with the documented policy and were not relaxed.

## Decision summary

No item is directly verified by the retained evidence. No production correction is justified. The safest current state is to preserve all four existing estimated values, keep their review flags and unresolved status, and obtain additional historical chart evidence before treating any as verified.

Required additional evidence:

1. RTX 4080 November and December 2024: a native chart image showing those months, plus verified x-axis date anchors and y-axis ticks.
2. RTX 4080 January 2025: a source/calibration review that establishes the left-edge monthly coordinate and a connected line point at that coordinate, without weakening missing-segment rejection.
3. RTX 4090 October 2024: a native chart image showing October 2024, plus verified x-axis date anchors and y-axis ticks.

No human or business approval is implied by this assessment.
