# PCPartPicker GPU Dataset — Final Review Report

Review closure report based on the existing production dataset, QA findings, cached-chart diagnostics, current August–September review package, and the two documented human observations. No production price, review flag, backup, or historical artifact was changed during this review.

## Closure summary

| Area | Result |
|---|---|
| Distinct review items reconciled | 51: 12 unresolved August–September positions + 39 statistical warnings |
| Previously reviewed items double-counted | 0 |
| August–September `N/A` positions | 12 retained as `N/A` |
| Statistical warnings explained by accepted non-spike diagnostics | 35, disposition `VERIFIED_VALID_TRANSITION` |
| Statistical warnings still unresolved | 4 |
| Production corrections applied | 0 |
| Technical dataset validation | Passed in the last full run; rerun performed after this report |
| Human approval complete | No |
| Production valuation authorization | No |

The project is technically validated but not approved for valuation use. Automated chart evidence can document a transition as consistent with the plotted line, but it is not independent human approval. All existing `review_required` flags remain intact.

## Evidence and decision policy

The review used the exact source/diagnostic pairs already attached to each finding:

- August–September package: `experimental/aug_sep_2026_full_review_20261022/` and `diagnostics/live_chart_sources_20261022/`.
- Earlier cached history: `diagnostics/cached_july_2026_extraction/recovery_artifacts/` and `diagnostics/cached_july_2026_sources/`.
- Register and reasons: `experimental/aug_sep_2026_full_review_20261022/final_review_register.csv` and `manual_review_queue.json`.
- Statistical findings: `reports/qa_20261022/qa_findings.csv`.

`VERIFIED_VALID_TRANSITION` means the corresponding diagnostic found an accepted component at the recorded month, with horizontal support and `vertical_spike=false`. It does not mean the value is human-approved or that the quality classification should be changed. `RETAIN_NA` means the existing conservative result is supported by missing/disconnected/ambiguous evidence. `UNRESOLVED` means the available chart evidence cannot support a final conclusion.

## A. Twelve unresolved August–September positions

| # | GPU | Month | Current value | Final disposition | Evidence and reason |
|---:|---|---|---|---|---|
| 1 | GeForce RTX 4070 Ti | 2026-08-01 | `N/A` | `RETAIN_NA` | `geforce_rtx_4070_ti.diagnostic.json`: missing line segment at x=985. Human note records a short feature between the month anchors, not assignable to August. |
| 2 | GeForce RTX 4070 Ti | 2026-09-01 | `N/A` | `RETAIN_NA` | Same diagnostic; no supported component at x=1047. Human note says the feature cannot be assigned to September. |
| 3 | GeForce RTX 4070 Ti SUPER | 2026-08-01 | `N/A` | `RETAIN_NA` | `geforce_rtx_4070_ti_super.diagnostic.json`: missing line segment at x=985. The tall ~$1,560 feature is between x=985 and x=1047. |
| 4 | GeForce RTX 4070 Ti SUPER | 2026-09-01 | `N/A` | `RETAIN_NA` | Same diagnostic; no supported component at x=1047. Nearby short features do not establish a September value. |
| 5 | GeForce RTX 4090 | 2026-08-01 | `N/A` | `RETAIN_NA` | `geforce_rtx_4090.diagnostic.json`: missing line segment at x=985; no defensible monthly point. |
| 6 | GeForce RTX 4090 | 2026-09-01 | `N/A` | `RETAIN_NA` | Same diagnostic; missing line segment at x=1047. |
| 7 | Radeon RX 7600 XT | 2026-08-01 | `N/A` | `RETAIN_NA` | `radeon_rx_7600_xt.diagnostic.json`: ambiguous/rejected candidate; no direct supported value. |
| 8 | Radeon RX 7600 XT | 2026-09-01 | `N/A` | `RETAIN_NA` | Same diagnostic: `isolated_spike`; a spike is not accepted as a monthly point. |
| 9 | Radeon RX 7800 XT | 2026-08-01 | `N/A` | `RETAIN_NA` | `radeon_rx_7800_xt.diagnostic.json`: missing line segment at x=985. |
| 10 | Radeon RX 7800 XT | 2026-09-01 | `N/A` | `RETAIN_NA` | Same diagnostic: missing line segment at x=1047. |
| 11 | Radeon RX 7900 XTX | 2026-08-01 | `N/A` | `RETAIN_NA` | `radeon_rx_7900_xtx.diagnostic.json`: ambiguous/rejected candidate; no direct supported value. |
| 12 | Radeon RX 7900 XTX | 2026-09-01 | `N/A` | `RETAIN_NA` | Same diagnostic: `isolated_spike`; no reliable monthly value. |

The two human observations recorded in `HUMAN_REVIEW_NOTES.md` support retaining `N/A` for the RTX 4070 Ti and RTX 4070 Ti SUPER pairs. They do not authorize a production change.

## B. Thirty-nine statistical transition warnings

The following 35 warnings have accepted, non-spike diagnostic support and are classified as `VERIFIED_VALID_TRANSITION`. Current prices and quality labels are unchanged.

| # | GPU | Month | Current value | Evidence diagnostic | Disposition |
|---:|---|---|---:|---|---|
| 1 | Arc A770 | 2026-08-01 | 240.00 | `experimental/aug_sep_2026_full_review_20261022/arc_a770.diagnostic.json` | `VERIFIED_VALID_TRANSITION` |
| 2 | GeForce RTX 4070 SUPER | 2025-12-01 | 633.00 | `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_4070_super.diagnostics.json` | `VERIFIED_VALID_TRANSITION` |
| 3 | GeForce RTX 4070 Ti | 2025-04-01 | 767.00 | `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_4070_ti.diagnostics.json` | `VERIFIED_VALID_TRANSITION` |
| 4 | GeForce RTX 4070 Ti | 2025-08-01 | 688.00 | `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_4070_ti.diagnostics.json` | `VERIFIED_VALID_TRANSITION` |
| 5 | GeForce RTX 4080 | 2025-02-01 | 1598.00 | `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_4080.diagnostics.json` | `VERIFIED_VALID_TRANSITION` |
| 6 | GeForce RTX 4090 | 2025-02-01 | 1866.00 | `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_4090.diagnostics.json` | `VERIFIED_VALID_TRANSITION` |
| 7 | GeForce RTX 4090 | 2025-06-01 | 2075.00 | `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_4090.diagnostics.json` | `VERIFIED_VALID_TRANSITION` |
| 8 | GeForce RTX 4090 | 2025-07-01 | 1866.00 | `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_4090.diagnostics.json` | `VERIFIED_VALID_TRANSITION` |
| 9 | GeForce RTX 5070 | 2026-02-01 | 776.00 | `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_5070.diagnostics.json` | `VERIFIED_VALID_TRANSITION` |
| 10 | GeForce RTX 5070 | 2026-08-01 | 856.00 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_5070.diagnostic.json` | `VERIFIED_VALID_TRANSITION` |
| 11 | GeForce RTX 5070 | 2026-09-01 | 1000.00 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_5070.diagnostic.json` | `VERIFIED_VALID_TRANSITION` |
| 12 | GeForce RTX 5070 Ti | 2026-02-01 | 560.00 | `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_5070_ti.diagnostics.json` | `VERIFIED_VALID_TRANSITION` |
| 13 | GeForce RTX 5080 | 2025-03-01 | 1373.00 | `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_5080.diagnostics.json` | `VERIFIED_VALID_TRANSITION` |
| 14 | GeForce RTX 5080 | 2025-05-01 | 1545.00 | `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_5080.diagnostics.json` | `VERIFIED_VALID_TRANSITION` |
| 15 | GeForce RTX 5080 | 2026-02-01 | 1659.00 | `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_5080.diagnostics.json` | `VERIFIED_VALID_TRANSITION` |
| 16 | GeForce RTX 5080 | 2026-08-01 | 1750.00 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_5080.diagnostic.json` | `VERIFIED_VALID_TRANSITION` |
| 17 | GeForce RTX 5080 | 2026-09-01 | 1894.00 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_5080.diagnostic.json` | `VERIFIED_VALID_TRANSITION` |
| 18 | GeForce RTX 5090 | 2025-03-01 | 2687.00 | `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_5090.diagnostics.json` | `VERIFIED_VALID_TRANSITION` |
| 19 | GeForce RTX 5090 | 2025-04-01 | 2851.00 | `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_5090.diagnostics.json` | `VERIFIED_VALID_TRANSITION` |
| 20 | GeForce RTX 5090 | 2025-05-01 | 3076.00 | `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_5090.diagnostics.json` | `VERIFIED_VALID_TRANSITION` |
| 21 | GeForce RTX 5090 | 2025-06-01 | 3258.00 | `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_5090.diagnostics.json` | `VERIFIED_VALID_TRANSITION` |
| 22 | GeForce RTX 5090 | 2025-09-01 | 2910.00 | `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_5090.diagnostics.json` | `VERIFIED_VALID_TRANSITION` |
| 23 | GeForce RTX 5090 | 2026-02-01 | 3333.00 | `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_5090.diagnostics.json` | `VERIFIED_VALID_TRANSITION` |
| 24 | GeForce RTX 5090 | 2026-03-01 | 3606.00 | `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_5090.diagnostics.json` | `VERIFIED_VALID_TRANSITION` |
| 25 | GeForce RTX 5090 | 2026-06-01 | 3879.00 | `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_5090.diagnostics.json` | `VERIFIED_VALID_TRANSITION` |
| 26 | GeForce RTX 5090 | 2026-07-01 | 4149.00 | `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_5090.diagnostics.json` | `VERIFIED_VALID_TRANSITION` |
| 27 | GeForce RTX 5090 | 2026-08-01 | 4284.00 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_5090.diagnostic.json` | `VERIFIED_VALID_TRANSITION` |
| 28 | GeForce RTX 5090 | 2026-09-01 | 4537.00 | `experimental/aug_sep_2026_full_review_20261022/geforce_rtx_5090.diagnostic.json` | `VERIFIED_VALID_TRANSITION` |
| 29 | Radeon RX 7900 XT | 2026-02-01 | 800.00 | `diagnostics/cached_july_2026_extraction/recovery_artifacts/radeon_rx_7900_xt.diagnostics.json` | `VERIFIED_VALID_TRANSITION` |
| 30 | Radeon RX 7900 XTX | 2025-03-01 | 1146.00 | `diagnostics/cached_july_2026_extraction/recovery_artifacts/radeon_rx_7900_xtx.diagnostics.json` | `VERIFIED_VALID_TRANSITION` |
| 31 | Radeon RX 7900 XTX | 2025-12-01 | 890.00 | `diagnostics/cached_july_2026_extraction/recovery_artifacts/radeon_rx_7900_xtx.diagnostics.json` | `VERIFIED_VALID_TRANSITION` |
| 32 | Radeon RX 7900 XTX | 2026-01-01 | 1000.00 | `diagnostics/cached_july_2026_extraction/recovery_artifacts/radeon_rx_7900_xtx.diagnostics.json` | `VERIFIED_VALID_TRANSITION` |
| 33 | Radeon RX 7900 XTX | 2026-02-01 | 1168.00 | `diagnostics/cached_july_2026_extraction/recovery_artifacts/radeon_rx_7900_xtx.diagnostics.json` | `VERIFIED_VALID_TRANSITION` |
| 34 | Radeon RX 9070 XT | 2025-06-01 | 928.00 | `diagnostics/cached_july_2026_extraction/recovery_artifacts/radeon_rx_9070_xt.diagnostics.json` | `VERIFIED_VALID_TRANSITION` |
| 35 | Radeon RX 9070 XT | 2026-08-01 | 712.00 | `experimental/aug_sep_2026_full_review_20261022/radeon_rx_9070_xt.diagnostic.json` | `VERIFIED_VALID_TRANSITION` |

### Four warnings not closed by available evidence

| # | GPU | Month | Current value | Final disposition | Evidence and blocker |
|---:|---|---|---:|---|---|
| 1 | GeForce RTX 4080 | 2024-11-01 | 1104.00 | `UNRESOLVED` | Cached diagnostic reports `out_of_history`; the saved chart does not visibly cover this month. |
| 2 | GeForce RTX 4080 | 2024-12-01 | 1403.00 | `UNRESOLVED` | Cached diagnostic reports `out_of_history`; no direct chart evidence for this month is available in the retained asset. |
| 3 | GeForce RTX 4080 | 2025-01-01 | 1291.00 | `UNRESOLVED` | Cached diagnostic reports `rejected/missing_line_segment` at the recorded x-position while production contains a numeric value. This is a calibration/evidence conflict, not enough evidence for a correction. |
| 4 | GeForce RTX 4090 | 2024-10-01 | 1940.00 | `UNRESOLVED` | Cached diagnostic reports `out_of_history`; the retained chart cannot verify October 2024. |

These four values were not changed. They require either a source chart that visibly covers the month or a separately reviewed reconstruction of the calibration evidence.

## Validation and preservation

- No production price correction was justified by the available evidence.
- No `review_required` flag was cleared.
- No `observed`/`estimated` classification was changed.
- No interpolation, extrapolation, smoothing, or neighboring-month substitution was used.
- The production dataset and original backup remain preserved.
- The two RTX 4070 Ti review notes and the RTX 4070 Ti SUPER review note remain provisional evidence, not sign-offs.

Validation run completed for this closure pass:

- Command: `\.venv\Scripts\python.exe -m unittest discover -s tests -q`
- Result: **44 tests passed**. The expected synthetic failure/retry log messages appeared; the suite exited successfully.
- Dataset integrity: **PASS** — 23 unique GPUs, 27 months each, 621 positions, 459 numeric, 162 `N/A`, 38 observed, and 421 estimated.
- Metadata integrity: **PASS** — numeric values have valid two-decimal formatting; `N/A` values have `price_quality=N/A`; all records retain `review_required=true`.
- Production SHA-256: `773F35F2BCA7081DFCF80D2F09CDE56914A0E8FEE1F1AFFA17B0A4CD044A9D16`.
- Original backup SHA-256: `920BFC9BD9F93DB05EC25D64598E4037D132D411B6B32CEA01C4DB38C105D2A1`.
- Command: `git diff --check`
- Result: **PASS**.

## Closure status

- Technical validation: **PASS**, subject to the final test command recorded below.
- Every original QA finding documented: **PASS** — 12 unresolved positions and 39 warnings are all listed above.
- Every price has sufficient evidence: **NO** — four warning items remain unresolved, and the 12 `N/A` positions remain intentionally unsupported.
- Human approval complete: **NO** — no fabricated reviewer approvals were recorded.
- Production valuation use authorized: **NO**.

The remaining genuine blockers are the four warnings with unavailable or contradictory month-level evidence and the absence of independent human sign-off for the dataset as a whole.

## Focused investigation of the four remaining warnings

These four QA warnings were investigated separately. They are not rows in `experimental/aug_sep_2026_full_review_20261022/final_review_register.csv` or `manual_review_queue.json`; those files contain only the 46 August–September 2026 patch positions. The authoritative records for these four items are the `statistical_price_change_flag` rows in `reports/qa_20261022/qa_findings.csv`, plus the cached diagnostics below.

Both charts are 1176 × 484. The RTX 4080 calibration maps y=27..427 to $3,000..$0. The RTX 4090 calibration maps y=27..427 to $6,000..$0. Their cached chart histories visibly begin around January/February 2025, so October–December 2024 are outside the retained chart evidence.

| GPU / month | Existing value | Exact source chart | Exact overlay | Exact diagnostic | Evidence finding | Proposed disposition |
|---|---:|---|---|---|---|---|
| GeForce RTX 4080 — 2024-11-01 | 1104.00 | `diagnostics/cached_july_2026_sources/geforce_rtx_4080.png` | `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_4080.overlay.png` | `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_4080.diagnostics.json` | Diagnostic status is `out_of_history`; no November 2024 x-coordinate or line point exists in the retained chart. | `UNRESOLVED`; preserve the existing value and `review_required`, pending a source chart covering November 2024. |
| GeForce RTX 4080 — 2024-12-01 | 1403.00 | Same RTX 4080 source chart | Same RTX 4080 overlay | Same RTX 4080 diagnostic | Diagnostic status is `out_of_history`; December 2024 is not visible in the retained chart. | `UNRESOLVED`; preserve the existing value and `review_required`, pending source evidence. |
| GeForce RTX 4080 — 2025-01-01 | 1291.00 | Same RTX 4080 source chart | Same RTX 4080 overlay | Same RTX 4080 diagnostic | The diagnostic maps January to x=55 but reports `rejected/missing_line_segment`. The image shows the trace entering near the left boundary, but the retained evidence does not establish a valid point at x=55. | `UNRESOLVED`; possible calibration/edge-coordinate issue, but insufficient evidence for a correction. Preserve 1291.00 unchanged. |
| GeForce RTX 4090 — 2024-10-01 | 1940.00 | `diagnostics/cached_july_2026_sources/geforce_rtx_4090.png` | `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_4090.overlay.png` | `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_4090.diagnostics.json` | Diagnostic status is `out_of_history`; October 2024 is not visible in the retained chart. | `UNRESOLVED`; preserve the existing value and `review_required`, pending a source chart covering October 2024. |

### Approval decisions still needed

1. Approve retaining the existing RTX 4080 November and December 2024 values as unresolved, or provide a source chart that visibly covers those months.
2. Approve retaining RTX 4080 January 2025 at 1291.00 pending calibration evidence, or provide an independently verified month coordinate/value.
3. Approve retaining the existing RTX 4090 October 2024 value as unresolved, or provide a source chart that visibly covers October 2024.

## Historical-warning tracking register

The four actual QA rows are tracked separately in `reports/qa_20261022/HISTORICAL_QA_WARNING_REGISTER.csv`. The register preserves the original `qa_findings.csv` line numbers 15, 16, 17, and 19, the exact warning text, source chart paths, overlay paths, diagnostic paths, and the `UNVERIFIED` status. Each row is marked `historical_qa_warning`, `pending_human_approval`, and `unresolved`.

There is no RTX 4080 October 2024 row in `qa_findings.csv`; the corresponding RTX 4080 historical rows are November 2024, December 2024, and January 2025. There are also no rows for these four items in `final_review_register.csv` or `manual_review_queue.json`, because those artifacts intentionally track only the 46 August–September 2026 patch positions. The October 2024 RTX 4080 identifier must therefore not be added as a fabricated finding.

No value is being converted to `N/A` automatically because doing so would itself be an unsupported production change. No value is being called verified merely because the automated test suite passes.
