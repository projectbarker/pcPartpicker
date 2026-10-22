# PCPartPicker Human Review Action Plan

Review-only checklist prepared from the existing QA reports and August–September review artifacts. This document does not change production data, quality flags, review flags, or historical evidence.

## Scope and reconciliation

- Production dataset: 23 GPUs, 27 months per GPU, 621 GPU-month positions.
- Unresolved August–September positions: 12, all currently `N/A`.
- Statistical transition warnings: 39, all marked `UNVERIFIED` by the QA screen.
- Distinct checklist rows: 51. Exact GPU/month comparison found no overlap between the 12 unresolved positions and the 39 statistical warnings.
- Source files checked: `reports/qa_20261022/PCPARTPICKER_DATASET_QA_REPORT.md`, `reports/qa_20261022/QA_EXECUTIVE_SUMMARY.md`, `reports/qa_20261022/qa_findings.csv`, `experimental/aug_sep_2026_full_review_20261022/manual_review_queue.json`, `experimental/aug_sep_2026_full_review_20261022/final_review_register.csv`, and the referenced overlay/diagnostic files.

The review register's automated dispositions are provisional. A reviewer must inspect the native chart evidence before recording a decision. Do not treat a statistical warning as proof of an extraction error.

## Prioritized review order

1. Resolve the 12 `N/A` positions first. These are the only rows where the current package explicitly lacks a usable numeric reading or rejected the candidate for missing/ambiguous line evidence.
2. Review the highest-magnitude statistical warnings next, beginning with RTX 5090 February 2026 (+$437), RTX 5070 Ti February 2026 (+$376), RTX 5090 March 2026 (+$273), RTX 5090 September 2026 (+$253), RTX 4080 February 2025 (+$307), and other warnings in descending absolute change.
3. Review the remaining statistical warnings grouped by GPU so one chart calibration can be checked consistently across its flagged months.
4. Re-run the integrity checks only after decisions are recorded. Do not edit a price merely to remove a warning.

## How to inspect a chart

Open the exact overlay and diagnostic JSON listed for the row. Use the overlay to locate the monthly sample and the diagnostic JSON to confirm the x-coordinate, y-coordinate, sampling status, reason code, and calibration context. Compare the selected point with the black actual-price line, not with the colored diagnostic marker alone.

For each point, check:

- The month position is aligned to the visible date/gridline axis.
- The selected pixel lies on the black actual-price trace rather than a gridline, border, legend, vertical spike, or unrelated dark mark.
- The y-coordinate maps monotonically to the readable USD tick labels.
- The neighboring line supports a genuine step or steep movement; a single isolated pixel or disconnected fragment is not enough.
- A missing or ambiguous segment is retained as `N/A`; never interpolate, extrapolate, smooth, or borrow a neighboring month's value.

## Decision recording rules

- `visually_supported`: direct chart evidence supports the existing numeric value and month alignment.
- `estimated_needs_review`: the trace supports a rounded visual estimate, but it remains an estimate and must keep `price_quality=estimated` and `review_required=true`.
- `ambiguous_keep_na`: competing candidates, unclear calibration, a spike, or an unreadable transition prevents a defensible value; retain `N/A` and its review reason.
- `missing_keep_na`: the target month is outside visible history or the black trace is absent/disconnected; retain `N/A`.
- `suspected_extraction_error`: the selected point is demonstrably inconsistent with the chart. Record the evidence and proposed correction separately; do not edit production in this review.

Observed values require direct, clearly traceable chart support. Estimated values must never be upgraded to observed based only on plausibility or continuity. A reviewer should record the decision and evidence in the blank fields below, leaving the production JSON unchanged.

## Checklist A — unresolved August–September positions

These 12 rows are all currently `N/A`. The listed reason is the existing automated review reason, not a new conclusion.

| Priority | GPU model | Month | Current value | Existing reason | Overlay to inspect | Diagnostic JSON to inspect | Decision | Evidence / notes |
|---:|---|---|---|---|---|---|---|---|
| 1 | GeForce RTX 4070 Ti | 2026-08-01 | `N/A` | `missing_line_segment` | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_4070_ti.overlay.png` | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_4070_ti.diagnostic.json` | __________________ | __________________ |
| 2 | GeForce RTX 4070 Ti | 2026-09-01 | `N/A` | `missing_line_segment` | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_4070_ti.overlay.png` | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_4070_ti.diagnostic.json` | __________________ | __________________ |
| 3 | GeForce RTX 4070 Ti SUPER | 2026-08-01 | `N/A` | `missing_line_segment` | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_4070_ti_super.overlay.png` | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_4070_ti_super.diagnostic.json` | __________________ | __________________ |
| 4 | GeForce RTX 4070 Ti SUPER | 2026-09-01 | `N/A` | `missing_line_segment` | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_4070_ti_super.overlay.png` | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_4070_ti_super.diagnostic.json` | __________________ | __________________ |
| 5 | GeForce RTX 4090 | 2026-08-01 | `N/A` | `missing_line_segment` | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_4090.overlay.png` | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_4090.diagnostic.json` | __________________ | __________________ |
| 6 | GeForce RTX 4090 | 2026-09-01 | `N/A` | `missing_line_segment` | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_4090.overlay.png` | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_4090.diagnostic.json` | __________________ | __________________ |
| 7 | Radeon RX 7600 XT | 2026-08-01 | `N/A` | `ambiguous` / no accepted numeric candidate | `experimental/aug_sep_2026_full_review_20261022/radeon_rx_7600_xt.overlay.png` | `experimental/aug_sep_2026_full_review_20261022/radeon_rx_7600_xt.diagnostic.json` | __________________ | __________________ |
| 8 | Radeon RX 7600 XT | 2026-09-01 | `N/A` | `isolated_spike` | `experimental/aug_sep_2026_full_review_20261022/radeon_rx_7600_xt.overlay.png` | `experimental/aug_sep_2026_full_review_20261022/radeon_rx_7600_xt.diagnostic.json` | __________________ | __________________ |
| 9 | Radeon RX 7800 XT | 2026-08-01 | `N/A` | `missing_line_segment` | `experimental/aug_sep_2026_full_review_20261022/radeon_rx_7800_xt.overlay.png` | `experimental/aug_sep_2026_full_review_20261022/radeon_rx_7800_xt.diagnostic.json` | __________________ | __________________ |
| 10 | Radeon RX 7800 XT | 2026-09-01 | `N/A` | `missing_line_segment` | `experimental/aug_sep_2026_full_review_20261022/radeon_rx_7800_xt.overlay.png` | `experimental/aug_sep_2026_full_review_20261022/radeon_rx_7800_xt.diagnostic.json` | __________________ | __________________ |
| 11 | Radeon RX 7900 XTX | 2026-08-01 | `N/A` | `ambiguous` / no accepted numeric candidate | `experimental/aug_sep_2026_full_review_20261022/radeon_rx_7900_xtx.overlay.png` | `experimental/aug_sep_2026_full_review_20261022/radeon_rx_7900_xtx.diagnostic.json` | __________________ | __________________ |
| 12 | Radeon RX 7900 XTX | 2026-09-01 | `N/A` | `isolated_spike` | `experimental/aug_sep_2026_full_review_20261022/radeon_rx_7900_xtx.overlay.png` | `experimental/aug_sep_2026_full_review_20261022/radeon_rx_7900_xtx.diagnostic.json` | __________________ | __________________ |

For this section, retain `N/A` unless the exact month position has clear black-line support. Do not use the neighboring month as a substitute.

## Checklist B — statistical transition warnings

These are statistical screening warnings, not confirmed defects. Each row records the current value at the flagged month and the QA evidence. Inspect the same chart's neighboring months and decide whether the transition is a genuine visible movement or an extraction/calibration problem.

| # | GPU model | Month | Current value | Quality | QA warning | Overlay / diagnostic to inspect | Decision | Evidence / notes |
|---:|---|---|---:|---|---|---|---|---|
| 1 | Arc A770 | 2026-08-01 | 240.00 | estimated | +$194; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/arc_a770.overlay.png` / `arc_a770.diagnostic.json` | __________ | __________ |
| 2 | GeForce RTX 4070 SUPER | 2025-12-01 | 633.00 | estimated | +$182; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_4070_super.overlay.png` / `geforce_rtx_4070_super.diagnostic.json` | __________ | __________ |
| 3 | GeForce RTX 4070 Ti | 2025-04-01 | 767.00 | estimated | +$114; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_4070_ti.overlay.png` / `geforce_rtx_4070_ti.diagnostic.json` | __________ | __________ |
| 4 | GeForce RTX 4070 Ti | 2025-08-01 | 688.00 | estimated | +$112; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_4070_ti.overlay.png` / `geforce_rtx_4070_ti.diagnostic.json` | __________ | __________ |
| 5 | GeForce RTX 4080 | 2024-11-01 | 1104.00 | estimated | +$232; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_4080.overlay.png` / `geforce_rtx_4080.diagnostic.json` | __________ | __________ |
| 6 | GeForce RTX 4080 | 2024-12-01 | 1403.00 | estimated | +$299; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_4080.overlay.png` / `geforce_rtx_4080.diagnostic.json` | __________ | __________ |
| 7 | GeForce RTX 4080 | 2025-01-01 | 1291.00 | estimated | +$112; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_4080.overlay.png` / `geforce_rtx_4080.diagnostic.json` | __________ | __________ |
| 8 | GeForce RTX 4080 | 2025-02-01 | 1598.00 | estimated | +$307; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_4080.overlay.png` / `geforce_rtx_4080.diagnostic.json` | __________ | __________ |
| 9 | GeForce RTX 4090 | 2024-10-01 | 1940.00 | estimated | +$254; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_4090.overlay.png` / `geforce_rtx_4090.diagnostic.json` | __________ | __________ |
| 10 | GeForce RTX 4090 | 2025-02-01 | 1866.00 | estimated | +$134; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_4090.overlay.png` / `geforce_rtx_4090.diagnostic.json` | __________ | __________ |
| 11 | GeForce RTX 4090 | 2025-06-01 | 2075.00 | estimated | +$209; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_4090.overlay.png` / `geforce_rtx_4090.diagnostic.json` | __________ | __________ |
| 12 | GeForce RTX 4090 | 2025-07-01 | 1866.00 | estimated | +$209; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_4090.overlay.png` / `geforce_rtx_4090.diagnostic.json` | __________ | __________ |
| 13 | GeForce RTX 5070 | 2026-02-01 | 776.00 | estimated | +$109; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_5070.overlay.png` / `geforce_rtx_5070.diagnostic.json` | __________ | __________ |
| 14 | GeForce RTX 5070 | 2026-08-01 | 856.00 | estimated | +$111; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_5070.overlay.png` / `geforce_rtx_5070.diagnostic.json` | __________ | __________ |
| 15 | GeForce RTX 5070 | 2026-09-01 | 1000.00 | observed | +$144; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_5070.overlay.png` / `geforce_rtx_5070.diagnostic.json` | __________ | __________ |
| 16 | GeForce RTX 5070 Ti | 2026-02-01 | 560.00 | estimated | +$376; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_5070_ti.overlay.png` / `geforce_rtx_5070_ti.diagnostic.json` | __________ | __________ |
| 17 | GeForce RTX 5080 | 2025-03-01 | 1373.00 | estimated | +$157; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_5080.overlay.png` / `geforce_rtx_5080.diagnostic.json` | __________ | __________ |
| 18 | GeForce RTX 5080 | 2025-05-01 | 1545.00 | estimated | +$135; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_5080.overlay.png` / `geforce_rtx_5080.diagnostic.json` | __________ | __________ |
| 19 | GeForce RTX 5080 | 2026-02-01 | 1659.00 | estimated | +$249; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_5080.overlay.png` / `geforce_rtx_5080.diagnostic.json` | __________ | __________ |
| 20 | GeForce RTX 5080 | 2026-08-01 | 1750.00 | estimated | +$121; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_5080.overlay.png` / `geforce_rtx_5080.diagnostic.json` | __________ | __________ |
| 21 | GeForce RTX 5080 | 2026-09-01 | 1894.00 | estimated | +$144; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_5080.overlay.png` / `geforce_rtx_5080.diagnostic.json` | __________ | __________ |
| 22 | GeForce RTX 5090 | 2025-03-01 | 2687.00 | estimated | +$314; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_5090.overlay.png` / `geforce_rtx_5090.diagnostic.json` | __________ | __________ |
| 23 | GeForce RTX 5090 | 2025-04-01 | 2851.00 | estimated | +$164; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_5090.overlay.png` / `geforce_rtx_5090.diagnostic.json` | __________ | __________ |
| 24 | GeForce RTX 5090 | 2025-05-01 | 3076.00 | estimated | +$225; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_5090.overlay.png` / `geforce_rtx_5090.diagnostic.json` | __________ | __________ |
| 25 | GeForce RTX 5090 | 2025-06-01 | 3258.00 | estimated | +$182; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_5090.overlay.png` / `geforce_rtx_5090.diagnostic.json` | __________ | __________ |
| 26 | GeForce RTX 5090 | 2025-09-01 | 2910.00 | estimated | +$166; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_5090.overlay.png` / `geforce_rtx_5090.diagnostic.json` | __________ | __________ |
| 27 | GeForce RTX 5090 | 2026-02-01 | 3333.00 | estimated | +$437; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_5090.overlay.png` / `geforce_rtx_5090.diagnostic.json` | __________ | __________ |
| 28 | GeForce RTX 5090 | 2026-03-01 | 3606.00 | estimated | +$273; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_5090.overlay.png` / `geforce_rtx_5090.diagnostic.json` | __________ | __________ |
| 29 | GeForce RTX 5090 | 2026-06-01 | 3879.00 | estimated | +$121; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_5090.overlay.png` / `geforce_rtx_5090.diagnostic.json` | __________ | __________ |
| 30 | GeForce RTX 5090 | 2026-07-01 | 4149.00 | estimated | +$270; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_5090.overlay.png` / `geforce_rtx_5090.diagnostic.json` | __________ | __________ |
| 31 | GeForce RTX 5090 | 2026-08-01 | 4284.00 | estimated | +$135; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_5090.overlay.png` / `geforce_rtx_5090.diagnostic.json` | __________ | __________ |
| 32 | GeForce RTX 5090 | 2026-09-01 | 4537.00 | estimated | +$253; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_5090.overlay.png` / `geforce_rtx_5090.diagnostic.json` | __________ | __________ |
| 33 | Radeon RX 7900 XT | 2026-02-01 | 800.00 | observed | +$121; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/radeon_rx_7900_xt.overlay.png` / `radeon_rx_7900_xt.diagnostic.json` | __________ | __________ |
| 34 | Radeon RX 7900 XTX | 2025-03-01 | 1146.00 | estimated | +$165; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/radeon_rx_7900_xtx.overlay.png` / `radeon_rx_7900_xtx.diagnostic.json` | __________ | __________ |
| 35 | Radeon RX 7900 XTX | 2025-12-01 | 890.00 | estimated | +$110; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/radeon_rx_7900_xtx.overlay.png` / `radeon_rx_7900_xtx.diagnostic.json` | __________ | __________ |
| 36 | Radeon RX 7900 XTX | 2026-01-01 | 1000.00 | observed | +$110; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/radeon_rx_7900_xtx.overlay.png` / `radeon_rx_7900_xtx.diagnostic.json` | __________ | __________ |
| 37 | Radeon RX 7900 XTX | 2026-02-01 | 1168.00 | estimated | +$168; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/radeon_rx_7900_xtx.overlay.png` / `radeon_rx_7900_xtx.diagnostic.json` | __________ | __________ |
| 38 | Radeon RX 9070 XT | 2025-06-01 | 928.00 | estimated | +$107; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/radeon_rx_9070_xt.overlay.png` / `radeon_rx_9070_xt.diagnostic.json` | __________ | __________ |
| 39 | Radeon RX 9070 XT | 2026-08-01 | 712.00 | estimated | +$145; IQR flag $106.50 | `experimental/aug_sep_2026_full_review_20261022/radeon_rx_9070_xt.overlay.png` / `radeon_rx_9070_xt.diagnostic.json` | __________ | __________ |

## After-review validation

Record decisions outside the production JSON first. After a reviewer has completed the checklist:

1. Confirm all 12 unresolved positions have an explicit decision; retain `N/A` unless direct evidence supports a value.
2. Confirm all 39 statistical warnings have a disposition: visually supported, estimated-needs-review, ambiguous, missing, or suspected extraction error.
3. Preserve `price_quality`, `review_required`, `review_reasons`, and `extraction_status` unless a separately approved data change is made.
4. Re-run the full test suite and dataset integrity checks: 23 unique GPUs, 27 month keys per record, 621 total positions, valid numeric formatting, and numeric/`N/A` reconciliation.
5. Recalculate the production SHA-256 and compare it with the pre-review hash. If no approved data change was made, it must remain `773F35F2BCA7081DFCF80D2F09CDE56914A0E8FEE1F1AFFA17B0A4CD044A9D16`.
6. Review the diff before any future production edit. Human review alone does not authorize changing prices or clearing review flags.

## First review action

Start with **GeForce RTX 4070 Ti — August 2026**. Open:

`experimental/aug_sep_2026_full_review_20261022/geforce_rtx_4070_ti.overlay.png`

Then inspect the matching `geforce_rtx_4070_ti.diagnostic.json`. The current value is `N/A` with `missing_line_segment`; retain `N/A` unless the native chart clearly supports a traceable August point.
