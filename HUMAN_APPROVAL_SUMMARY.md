# Human Approval Summary — Historical QA Warnings

This summary covers four historical QA warnings tracked separately from the 46 August–September 2026 patch positions. All four remain `unresolved` and `pending_human_approval`.

## Items requiring review

| GPU and month | Existing price | Warning reason | Source evidence |
|---|---:|---|---|
| GeForce RTX 4080 — November 2024 | `$1,104.00` | Statistical change: `$232.00` versus IQR flag `$106.50`; diagnostic status `out_of_history`. | Chart: `diagnostics/cached_july_2026_sources/geforce_rtx_4080.png`<br>Overlay: `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_4080.overlay.png`<br>Diagnostic: `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_4080.diagnostics.json` |
| GeForce RTX 4080 — December 2024 | `$1,403.00` | Statistical change: `$299.00` versus IQR flag `$106.50`; diagnostic status `out_of_history`. | Same RTX 4080 chart, overlay, and diagnostic paths above. |
| GeForce RTX 4080 — January 2025 | `$1,291.00` | Statistical change: `$112.00` versus IQR flag `$106.50`; diagnostic status `rejected_missing_line_segment` at the left-edge coordinate. | Same RTX 4080 chart, overlay, and diagnostic paths above. |
| GeForce RTX 4090 — October 2024 | `$1,940.00` | Statistical change: `$254.00` versus IQR flag `$106.50`; diagnostic status `out_of_history`. | Chart: `diagnostics/cached_july_2026_sources/geforce_rtx_4090.png`<br>Overlay: `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_4090.overlay.png`<br>Diagnostic: `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_4090.diagnostics.json` |

The exact QA tracking IDs are `QA-20261022-L15`, `QA-20261022-L16`, `QA-20261022-L17`, and `QA-20261022-L19` in `reports/qa_20261022/HISTORICAL_QA_WARNING_REGISTER.csv`.

## Why the prices are not fully verified

The retained RTX 4080 and RTX 4090 chart images begin around January/February 2025. Therefore, the October–December 2024 points are outside the visible source history and cannot be checked directly. For RTX 4080 January 2025, the chart begins near the boundary, but the diagnostic rejected the exact monthly coordinate as a missing line segment. The existing number is therefore preserved but not confirmed by the retained evidence.

These are evidence limitations, not proof that the prices are wrong. The statistical detector identifies unusually large changes; it does not establish an extraction defect by itself.

## Decision options for each item

For each of the four rows, the reviewer may choose one of these documented paths:

1. **Retain provisionally:** keep the existing price unchanged, retain `review_required`, and leave the row marked `unresolved` / `pending_human_approval`. This requires no production edit.
2. **Obtain additional evidence:** request or recover a historical chart image that visibly covers the target month, verify the month coordinate and y-axis mapping, then reassess the price. No value should be changed until that evidence is available.

For RTX 4080 January 2025 specifically, additional evidence may also be a separately verified correction to the left-edge month coordinate. The current evidence does not justify changing `$1,291.00` or replacing it with `N/A`.

## Validation versus approval

Technical validation passed:

- 44 automated tests passed.
- Dataset integrity passed: 23 unique GPUs, 27 months per GPU, 621 positions.
- Production SHA-256: `773F35F2BCA7081DFCF80D2F09CDE56914A0E8FEE1F1AFFA17B0A4CD044A9D16`.
- Backup SHA-256: `920BFC9BD9F93DB05EC25D64598E4037D132D411B6B32CEA01C4DB38C105D2A1`.
- `git diff --check` passed.

Passing tests and unchanged hashes confirm structural and technical integrity; they do not approve the accuracy of these four prices. No human approval has been recorded, no production price or review flag was changed, and no commit or push was performed.

## Exact reviewer decisions needed

- RTX 4080 November 2024: retain `$1,104.00` provisionally, or request historical chart evidence.
- RTX 4080 December 2024: retain `$1,403.00` provisionally, or request historical chart evidence.
- RTX 4080 January 2025: retain `$1,291.00` provisionally pending calibration evidence, or provide a verified replacement coordinate/value.
- RTX 4090 October 2024: retain `$1,940.00` provisionally, or request historical chart evidence.

The dataset remains unsuitable for valuation approval until these decisions and the broader human-review gate are completed.
