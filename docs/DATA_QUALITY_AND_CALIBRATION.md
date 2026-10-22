# Data Quality and Calibration

## Monthly policy

The project uses a fixed 27-month schema: `2024-07-01` through `2026-09-01`. The intended interpretation is a chart observation at the monthly sampling position, not a daily average or transaction-level price. Where a boundary transition is ambiguous, the current production decision is to retain the existing sampler, require review, and use `N/A` when the value cannot be determined reliably.

## Quality classes

| Class | Meaning | Review behavior |
|---|---|---|
| `observed` | Directly supported by a clear black-line position and valid calibration. | May be consumed as a clear chart observation. |
| `estimated` | A readable line position mapped to a rounded USD value from the raster. | Always review-required; it is not ground truth. |
| `N/A` | Outside visible history, missing, disconnected, or ambiguous. | Preserve `N/A` and the reason; never fill it. |

Calibration must be supported by the chart's own bounds, date anchor, tick labels, and horizontal gridlines. A detector result alone is not sufficient evidence. The post-boundary stability experiment remains diagnostic-only and is not the production sampler.

## Review and failure reasons

The implementation retains reason codes such as `outside_visible_history`, `missing_line_segment`, `ambiguous_line_candidate`, `isolated_spike`, `extension_not_validated`, and calibration/image failure details. A failed record has all 27 monthly values set to `N/A`, `extraction_skipped: true`, and no fabricated numeric values.

## Evidence history

The three-GPU vision sample exposed false missing-history interpretations and suspicious sequences. The continuity-aware coordinate prototype improved selection around spikes but left unstable regions requiring review. The Queue A pilot and Queue B boundary/history reviews supplied the published evidence used for the final integration. The compact `diagnostics/turnover_blocker_attempt/` directory contains the six recovered Queue B calibration artifacts and overlays.

The approximate manual readings in the historical validation work are visual references, not ground truth. No universal accuracy threshold was invented. Future expansion should compare distributed manual references, review all ambiguous points, and preserve the current conservative semantics.

The saved chart URLs are dated `2026.03.03`. A local chart inspection showed visible history through approximately February 2026, but no approved extraction was run for the eight requested extension months. They therefore remain `N/A` with `extension_not_validated`; March through September are outside the saved chart history.

## Remaining blocker

Radeon RX 7600 XT still raises:

```text
ValueError: Expected 7 horizontal gridlines, detected 6
```

Its visible bottom boundary was not approved as a safe replacement for the missing gridline. The calibration check remains intact and the record remains failed.
