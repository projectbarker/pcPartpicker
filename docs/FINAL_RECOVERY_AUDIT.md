# Final Recovery Audit

## Current result

The repository now contains 23 GPU records with 27 monthly fields each. The dataset has 425 numeric values and 196 `N/A` values. Numeric quality is 35 `observed` and 390 `estimated`; all 23 records remain review-required and no record is marked failed.

The pre-cached baseline had 307 numeric values. The cached July source run added 97 values, and the independently validated manual-axis recovery added 21 more, for 118 additions. No previously numeric value was overwritten.

The machine-readable audit is [`FINAL_RECOVERY_BASELINE_AUDIT.json`](FINAL_RECOVERY_BASELINE_AUDIT.json), and the complete 196-position register is [`FINAL_RECOVERY_REGISTER.json`](FINAL_RECOVERY_REGISTER.json).

## Remaining missing positions

Every remaining `N/A` is accounted for:

| Reason | Count | Treatment |
|---|---:|---|
| `out_of_history` | 85 | The cached chart has no visible position for the month. |
| `missing_line_segment` | 54 | No connected black price-line segment supports a value. |
| `isolated_spike` | 11 | The only candidate is a rejected vertical/isolated spike. |
| `source_unavailable_chart_not_visible` | 46 | August and September 2026 are not represented in the cached July source. |

No missing value was interpolated, copied from a neighboring month, extrapolated, or replaced with MSRP/retail data.

## Source and calibration evidence

All 23 cached July 3, 2026 chart images were retrieved as 1176×484 PNGs. The contact sheet and representative full-resolution charts confirm the rolling visible range is approximately February 2025 through July 2026. Live PCPartPicker page access remains Cloudflare-blocked; no newer authorized August/September source was found in the repository or cached artifacts.

The six former automatic calibration failures were investigated individually. Explicit in-bounds, monotonic gridline coordinates were accepted only after visual verification of the labeled axis and chart geometry. The default automatic seven-gridline check remains unchanged. The calibration evidence is in [`CACHED_JULY_2026_MANUAL_CALIBRATION.json`](CACHED_JULY_2026_MANUAL_CALIBRATION.json).

## Numeric audit

The 307 pre-existing numeric values were preserved as inherited baseline values. The 118 recovered values were checked against the cached source identity, 1176×484 image, calibrated month positions, pixel-to-price mapping, diagnostic status, numeric formatting, and review metadata. The 21 manual-axis values are still estimates/review-required unless directly aligned to a calibrated tick. No universal accuracy threshold is claimed, and this audit does not establish transaction-level ground truth.

## Validation and integrity

- Full test suite: 44 passed.
- Schema: 23 unique models, 27 unique month keys per record, 621 positions.
- Count reconciliation: `425 + 196 = 621`; `35 + 390 = 425`.
- Final SHA-256: `A001249CE23B0537FA475F24AE7B5BF8DDE18FF896449EA10AF1CEBD37BE66E2`.
- Pre-cached baseline SHA-256: `FBD1F9126A899F57D01A41BC46E54897DA515B37C42E4FBE9CDB33CF32CE5459`.
- Latest atomic-write backup: `Monthly_Scraped_Data/pcpartpicker_gpu_trends_final.backup_20261022_161515.json`.

## Remaining blocker

The remaining limitation is source coverage, not a failed record: August and September 2026 require a newer authorized PCPartPicker chart source. Historical gaps and rejected spikes remain `N/A` until a readable source segment is available. Production use still requires human review of estimated values and the monthly-boundary interpretation.
