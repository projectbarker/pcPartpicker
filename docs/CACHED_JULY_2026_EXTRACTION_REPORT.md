# Cached July 2026 GPU Extraction Report

## Result

The 23 cached CDN chart images dated `2026.07.03` were retrieved successfully into a separate diagnostics directory. All were `1176×484` PNGs and were screened in a contact sheet against the GPU identities from the cached HTML page. The rolling x-axis shows February 2025 through June 2026 labels, with the right edge representing approximately July 2026. August and September 2026 are not represented.

The existing calibrated Pillow pipeline was run against local cached images with a separate experimental calibration set. The visible February 2025 date anchor was used for this July chart layout; the older October 2024 anchor was not reused. The detector's duplicate right border was excluded from monthly sampling so August was not falsely mapped to the border.

## Dataset update

Only newly supported February–July 2026 positions were added. July 2024–January 2026 values were compared with the timestamped pre-update backup and were unchanged. August and September remain `N/A`. No interpolation, extrapolation, smoothing, or OpenAI API extraction was used.

| Measure | Result |
|---|---:|
| GPU records | 23 |
| Monthly positions | 621 |
| Numeric values | 425 |
| `N/A` values | 196 |
| `observed` values | 35 |
| `estimated` values | 390 |
| Records requiring review | 23 |
| Failed records | 0 |
| New numeric values relative to the pre-cached baseline | 118 |

New numeric coverage by month is February 19, March 17, April 18, May 19, June 20, and July 18. August and September remain zero numeric values.

## Calibration and review

All 23 charts produced at least some numeric values, and all records remain marked for review because the readings are raster-derived and mostly estimated. Six charts initially failed the automatic seven-gridline calibration check: GeForce RTX 4070, GeForce RTX 4070 Ti, GeForce RTX 4070 Ti SUPER, GeForce RTX 4090, Radeon RX 9060 XT, and Radeon RX 7600 XT. Direct chart evidence supported an explicit in-bounds manual gridline configuration for each; the automatic detector threshold was not changed. Unsupported segments remain `N/A`.

Representative overlays were inspected for Arc A380 and Radeon RX 9070; the accepted markers followed the black line, while spike/missing-line diagnostics remained visible. The GeForce RTX 4070 source visibly lacks a detector-complete horizontal gridline set, so it remains failed rather than receiving fabricated prices.

No universal accuracy threshold was claimed. The extraction is a controlled, review-required update, not proof that every price is within the manager's reported 1–5% range. The full audit is `docs/CACHED_JULY_2026_COMPLETION_AUDIT.md`.

## Integrity and artifacts

- Final dataset: `Monthly_Scraped_Data/pcpartpicker_gpu_trends_final.json`
- Backup: `Monthly_Scraped_Data/pcpartpicker_gpu_trends_final.backup_20261022_160047.json`
- Final SHA-256: `902198B7FFE5F0258FC020D93906C91C0091F4B683F8C21A7475E9B964603779`
- Validation manifest: `docs/CACHED_JULY_2026_VALIDATION.json`
- Retrieved images: `diagnostics/cached_july_2026_sources/`
- Overlays and diagnostics: `diagnostics/cached_july_2026_extraction/`

The prior final SHA-256 was `FBD1F9126A899F57D01A41BC46E54897DA515B37C42E4FBE9CDB33CF32CE5459`. Historical months were verified unchanged. The live PCPartPicker page remains Cloudflare-blocked; the source is the cached July 3 CDN set, not a live August/September source.
