# RTX 4080 January 2025 Candidate Review

Date: 2026-10-22
Scope: evidence review only. No production values, classifications, review flags, QA findings, thresholds, or source artifacts were changed.

## Decision

The existing `$1,291.00` value remains **indeterminate and unsupported by the retained candidate evidence**. It must remain unchanged, `estimated`, review-required, and unresolved. The evidence does not justify replacing it, marking it observed, or converting it to `N/A`.

## Exact candidate artifacts

| Item | Path / URL | Identity and provenance |
|---|---|---|
| Candidate source chart | `diagnostics/cached_july_2026_sources/geforce_rtx_4080.png` | Local cached July 3, 2026 PCPartPicker CDN chart for GeForce RTX 4080; native 1176×484 PNG; SHA-256 `29C8E601685CD232F62746F0AE802638121CB21E5115614F2C13870221FF6E38`. |
| Candidate CDN reference | `https://cdna.pcpartpicker.com/static/forever/images/trends/2026.07.03.usd.gpu.chipset.geforce-rtx-4080.4bb4ec8ae38fc313e72ec0bf68c1aabd.png` | URL recorded in `Monthly_Scraped_Data/pcpartpicker_gpu_sources_cached_2026.07.03.json`; source metadata identifies it as a local cached-page reference, not a live-verified historical capture. |
| Overlay | `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_4080.overlay.png` | Generated diagnostic overlay for the same source image; 1176×484. |
| Diagnostic | `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_4080.diagnostics.json` | Generated from the same chart/calibration run; records the January position and rejection reason. |
| Calibration implementation | `coordinate_calibration.py` | Existing production calibration and conservative missing-segment handling. |

The original March 3, 2026 URL is also recorded in the source metadata, but no corresponding March image was found to provide an earlier historical view:

`https://cdna.pcpartpicker.com/static/forever/images/trends/2026.03.03.usd.gpu.chipset.geforce-rtx-4080.1a458cb629180b007380226fb7d85212.png`

## Calibration reconstruction

The diagnostic reports:

- Image dimensions: `1176 × 484`.
- Plot bounds: `[55, 27, 1149, 427]`.
- Date anchor: `2025-02-01` at `x=115`.
- January 2025 monthly x-coordinate: `x=55`.
- Horizontal gridlines: `y=[27, 94, 161, 227, 294, 361, 427]`.
- Tick mapping: `y=27 → $3,000`, `94 → $2,500`, `161 → $2,000`, `227 → $1,500`, `294 → $1,000`, `361 → $500`, `427 → $0`.

January `x=55` is therefore inside the recorded plot boundary, but it is the extreme left edge. The diagnostic does not record a supported y-coordinate there.

## January evidence

The January diagnostic entry is exactly:

```json
{"status":"rejected","reason":"missing_line_segment","candidates":[],"accepted":null}
```

The source image shows a black trace entering at or very near the left boundary and then changing rapidly before the February position. The overlay contains no accepted January marker. The first accepted point is February 2025 at `x=115`, `y=214`, corresponding to approximately `$1,598` under the recorded y-axis mapping.

This distinction matters:

- The January coordinate exists geometrically.
- A visible dark feature near the edge is not automatically a valid monthly price point.
- There is no connected candidate accepted by the existing line-selection policy at `x=55`.
- Assigning `$1,291.00` from the nearby edge feature would be an estimate or extrapolation, not a directly supported observation.
- Neighboring February evidence cannot be used to infer January.

## Assessment

| Question | Finding |
|---|---|
| Is January 2025 within the image? | Yes, at the left boundary `x=55`. |
| Is a supported line point present at that coordinate? | No. The diagnostic reports zero candidates and `missing_line_segment`. |
| Is `$1,291.00` directly observed? | No. No accepted y-coordinate or direct monthly point is recorded. |
| Is it a defensible estimate from this artifact? | No. The left-edge feature is not sufficiently separated from the boundary and is not supported by the sampler. Calling it an estimate would require an additional, explicitly verified interpretation. |
| Can current evidence resolve the warning? | No. The candidate is insufficient. |

## Additional evidence required

One of the following is needed before the warning can be resolved:

1. An original or earlier native RTX 4080 chart image whose visible history clearly includes January 2025, with preserved provenance and readable date/tick calibration; or
2. A separately reviewed calibration reconstruction proving that `x=55` is the January monthly position and identifying a connected actual-price line segment at that coordinate, without weakening the existing `missing_line_segment` safeguard.

The additional evidence must establish both the month assignment and the line position. A URL date, a nearby February value, a visual impression of a short edge feature, or an interpolated price is not sufficient.

## Integrity validation

- Production dataset SHA-256: `773F35F2BCA7081DFCF80D2F09CDE56914A0E8FEE1F1AFFA17B0A4CD044A9D16`.
- Original backup SHA-256: `920BFC9BD9F93DB05EC25D64598E4037D132D411B6B32CEA01C4DB38C105D2A1`.
- The full test suite was rerun after this review: 44 tests passed. `git diff --check` also passed. These results do not establish price accuracy or approval.
