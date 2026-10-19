# Step 22 — Queue B Bottom-Boundary Review

**Date:** 2026-10-19  
**Scope:** Six Queue B charts from Step 21. No extraction, OCR, API, or batch run.

## Method

Each exact Step 17 source image was opened and compared with its Step 21 artifact. Pixels at y=427 and neighboring rows were inspected at multiple x positions. The visible `$0` label, plot edge, interior gridline sequence, and the boundary's continuation through regions without black price history were considered together.

The existing detector searches for a long neutral-gray row. It found six interior rows because y=427 is partly overwritten by black chart content or border pixels. The review did not lower that threshold. Instead, it determined whether the row is the chart baseline by its position and axis context.

## Per-GPU decisions

| GPU | Decision | Evidence | Remaining limitation |
|---|---|---|---|
| RTX 4070 Ti SUPER | `accepted` | y=427 is a horizontal boundary aligned with `$0`; gray baseline is visible across the earlier plot and black late zero trace overlaps it. | Late drop/zero trace remains a separate line-support review issue. |
| RTX 5060 Ti | `accepted` | The early black trace lies at y=427, then a gray baseline is visible after the trace leaves zero; it aligns with `$0`. | Early requested months are unsupported. |
| RTX 5070 Ti | `accepted` | The lower edge is aligned with `$0`; gray baseline is visible outside the early black zero-history overlap. | Early history and disconnected structures remain unresolved. |
| RX 9060 XT | `accepted` | The left black zero-history segment overlays the baseline; after the actual line begins, y=427 is visibly gray and aligned with `$0`. | Actual history begins later; no early values may be inferred. |
| RX 9070 | `accepted` | y=427 is the plot bottom and `$0` axis; gray baseline is visible after early black structures. | Early structures require line-support review. |
| RX 9070 XT | `accepted` | y=427 is aligned with the `$0` label and lower plot edge; gray baseline continues outside early black zero-history structures. | Unsupported early history remains N/A. |

## Decision counts

- Accepted: 6
- Rejected: 0
- Inconclusive: 0

This is acceptance of the bottom axis boundary only. All six proposed artifacts retain `overall_calibration_status: manual_review_required`; accepting y=427 does not approve monthly price extraction or resolve missing/ambiguous line segments.

RX 7600 XT remains separate and blocked.

## Artifacts and preservation

New proposed artifacts are in `diagnostics/step22_bottom_boundary_review/`. Step 21 artifacts, the Step 19 pilot output, and historical files were not overwritten.

## Validation

The six proposed JSON files and the Step 22 manifest parse successfully. Existing calibration unit tests were run unchanged:

```text
python -m unittest tests.test_coordinate_calibration -v
Ran 16 tests
OK
```

No extraction or production code change was made.

## Next action

Use the accepted y=427 boundary in a separately reviewed calibration-validation step, while retaining manual review for history coverage and black-line support. Do not start price extraction until that broader review is complete.

