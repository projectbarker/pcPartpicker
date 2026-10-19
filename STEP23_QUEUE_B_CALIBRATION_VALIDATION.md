# Step 23 — Queue B Calibration Validation

**Date:** 2026-10-19  
**Scope:** Six Queue B charts; geometry validation only. No price extraction, OCR, API, or 23-GPU processing.

## Validation performed

The six Step 22 proposed artifacts were copied into a new validation record set under `diagnostics/step23_queue_b_validation/`. Each was checked for:

- 1176×484 image bounds.
- Plot bounds `[55, 27, 1149, 427]`.
- Seven monotonic y gridlines `[27, 94, 161, 227, 294, 361, 427]`.
- Matching top-to-bottom USD tick mappings.
- October 2024 date anchor at x=113.
- In-bounds, ordered vertical gridline coordinates.
- Monthly x mapping from the anchor without extrapolating outside the visible gridline list.

All six passed these geometry checks. The y=427/$0 boundary is the manually accepted Step 22 boundary; the production detector was not weakened and was not changed.

## Per-GPU outcome

| GPU | Geometry | Overall status | Visible-history finding |
|---|---|---|---|
| RTX 4070 Ti SUPER | Valid | `manual_review_required` | Line is visible through much of the chart, but the late drop/zero overlap is unresolved. |
| RTX 5060 Ti | Valid | `manual_review_required` | Black trace leaves the bottom region around January 2025; early requested months are unsupported. |
| RTX 5070 Ti | Valid | `manual_review_required` | Readable line begins around February–March 2025; earlier structures are disconnected/unsupported. |
| RX 9060 XT | Valid | `manual_review_required` | Readable line begins around February 2025; earlier months are unsupported. |
| RX 9070 | Valid | `manual_review_required` | Readable line begins around March 2025 after early disconnected structures. |
| RX 9070 XT | Valid | `manual_review_required` | Readable line begins around March 2025; earlier structures are unsupported. |

No record is `blocked` because all source images and axis evidence are available. No record is overall `calibration_verified` because the requested monthly extraction range includes unresolved or unsupported black-line history, and the policy requires missing/disconnected segments to remain `N/A` and reviewed.

## Counts

- Overall `calibration_verified`: 0
- Overall `manual_review_required`: 6
- Overall `blocked`: 0
- Geometry validated: 6

RX 7600 XT remains separately blocked and was not processed.

## Tests and preservation

The six new JSON artifacts and the manifest were parsed and checked for bounds, monotonicity, anchor consistency, and monthly mapping. Existing calibration tests were run unchanged:

```text
python -m unittest tests.test_coordinate_calibration -v
Ran 16 tests
OK
```

No existing artifact, Step 19 output, detector threshold, production code, or extraction policy was modified.

## Next action

Perform a supervised line-history review for the six charts, explicitly marking unsupported early months and late disconnected regions as `N/A`; only after that review should any controlled price pilot be considered.

