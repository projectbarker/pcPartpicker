# Data Quality and Calibration

## Monthly policy

The project uses a verified 25-month schema: `2024-07-01` through `2026-07-01`. The intended interpretation is a chart observation at the monthly sampling position, not a daily average or transaction-level price. Where a boundary transition is ambiguous, the current production decision is to retain the existing sampler, require review, and use `N/A` when the value cannot be determined reliably.

## Quality classes

| Class | Meaning | Review behavior |
|---|---|---|
| `observed` | Directly supported by a clear black-line position and valid calibration. | May be consumed as a clear chart observation. |
| `estimated` | A readable line position mapped to a rounded USD value from the raster. | Always review-required; it is not ground truth. |
| `N/A` | Outside visible history, missing, disconnected, or ambiguous. | Preserve `N/A` and the reason; never fill it. |

Calibration must be supported by the chart's own bounds, date anchor, tick labels, and horizontal gridlines. A detector result alone is not sufficient evidence. The post-boundary stability experiment remains diagnostic-only and is not the production sampler.

## Review and failure reasons

The implementation retains reason codes such as `outside_visible_history`, `missing_line_segment`, `ambiguous_line_candidate`, `isolated_spike`, and calibration/image failure details. A failed record has all 25 monthly values set to `N/A`, `extraction_skipped: true`, and no fabricated numeric values.

## Evidence history

The three-GPU vision sample exposed false missing-history interpretations and suspicious sequences. The continuity-aware coordinate prototype improved selection around spikes but left unstable regions requiring review. The Queue A pilot and Queue B boundary/history reviews supplied the published evidence used for the final integration. The compact `diagnostics/turnover_blocker_attempt/` directory contains the six recovered Queue B calibration artifacts and overlays.

The approximate manual readings in the historical validation work are visual references, not ground truth. No universal accuracy threshold was invented. Future expansion should compare distributed manual references, review all ambiguous points, and preserve the current conservative semantics.

The original chart URLs are dated `2026.03.03`. A controlled follow-up used 23 cached CDN URLs dated `2026.07.03` and retrieved all 23 chart images. Where calibration and line evidence passed, February through July 2026 were extracted conservatively. August and September were not verified and are excluded from the schema; no value was inferred beyond visible history.

The source investigation found `pcpartpicker_debug_page.html`, a saved local page containing 23 CDN references dated `2026.07.03`. All 23 were downloaded and inspected as a controlled cached-source run. The rolling chart axes support approximately July 2026; August and September are unverified and excluded from the dataset. Six records initially failed automatic calibration (`Expected 7 horizontal gridlines, detected 6`), but direct image evidence supported a bounded manual-axis configuration without changing the default threshold. Unsupported segments remain `N/A`. No official public trend-data API or downloadable dataset was found, and unofficial wrappers were not accepted as authoritative sources. See `docs/CACHED_JULY_2026_COMPLETION_AUDIT.md`.

## Remaining limitations

The six former automatic calibration failures now have verified manual-axis geometry, but all records remain review-required. Missing line segments and isolated spikes remain `N/A`; August and September 2026 are not visible in the cached source charts and are excluded from the dataset.

Its visible bottom boundary was not approved as a safe replacement for the missing gridline. The calibration check remains intact and the record remains failed.
