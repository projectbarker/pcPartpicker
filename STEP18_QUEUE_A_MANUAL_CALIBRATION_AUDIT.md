# Step 18 — Queue A Manual-Calibration Audit

**Date:** 2026-10-19  
**Scope:** Nine Queue A charts from the Step 17 manifest. Calibration review only; no monthly price extraction.

## Result

All nine Queue A calibrations are **`calibration_verified`** for axis geometry and date-axis mapping. This means that the chart-specific image, visible tick labels, detected gridline geometry, and October 2024 anchor were consistent with the existing calibration conventions. It does not mean that every monthly black-line position is readable or that numeric prices are approved.

Summary:

| Status | Count |
|---|---:|
| `calibration_verified` | 9 |
| `manual_review_required` | 0 for calibration geometry; all 9 still require normal line/price review before use |
| `blocked` | 0 |

The per-GPU proposed calibration artifacts are in `diagnostics/step18_queue_a_manual_calibration/`. The machine-readable summary is [STEP18_QUEUE_A_CALIBRATION_MANIFEST.json](STEP18_QUEUE_A_CALIBRATION_MANIFEST.json).

## Evidence and method

The exact source image paths and URLs were taken from `STEP17_SOURCE_IMAGE_EVIDENCE_MANIFEST.json`; no GPU image was substituted. Each image was opened and visually inspected. The existing `detect_gridlines()` and `calibrate_chart()` functions were run in memory with the chart-specific tick values read from the visible y-axis labels.

The observed geometry for all nine charts was:

- Image dimensions: `1176×484`.
- Plot bounds: left `55`, top `27`, right `1149`, bottom `427`.
- Horizontal gridlines: `[27, 94, 161, 227, 294, 361, 427]`.
- Vertical gridlines: `[55, 113, 175, 235, 296, 359, 415, 477, 537, 599, 659, 721, 783, 843, 905, 965, 1026, 1089, 1145, 1149]`.
- Visible October 2024 date anchor: `x=113`.

These coordinates are recorded separately in each artifact because they were checked against each image. Their agreement is an observed result, not an assumption that all chart layouts must be identical.

The requested month mapping under the existing anchor convention is:

| Month | x-coordinate | Interpretation |
|---|---:|---|
| 2024-07-01 | `null` | No corresponding detected vertical gridline in the visible chart range |
| 2024-08-01 | `null` | No corresponding detected vertical gridline in the visible chart range |
| 2024-09-01 | 55 | First visible monthly gridline |
| 2024-10-01 | 113 | Verified anchor |
| 2024-11-01 | 175 | Visible monthly gridline |
| 2024-12-01 | 235 | Visible monthly gridline |
| 2025-01-01 | 296 | Visible monthly gridline |
| 2025-02-01 | 359 | Visible monthly gridline |
| 2025-03-01 | 415 | Visible monthly gridline |
| 2025-04-01 | 477 | Visible monthly gridline |
| 2025-05-01 | 537 | Visible monthly gridline |
| 2025-06-01 | 599 | Visible monthly gridline |
| 2025-07-01 | 659 | Visible monthly gridline |
| 2025-08-01 | 721 | Visible monthly gridline |
| 2025-09-01 | 783 | Visible monthly gridline |
| 2025-10-01 | 843 | Visible monthly gridline |
| 2025-11-01 | 905 | Visible monthly gridline |
| 2025-12-01 | 965 | Visible monthly gridline |
| 2026-01-01 | 1026 | Visible monthly gridline |

The `null` values are coordinate-mapping results, not fabricated prices. They preserve the existing outside-visible-history behavior for July and August when no x-gridline is available.

## Per-GPU review

### Intel Arc A770 / inventory name `Arc A770`

- Source: `diagnostics/step17_source_images/arc_a770.png`.
- Visible y-axis: `$600` through `$0` in `$100` steps.
- Calibration: seven gridlines and the October 2024 anchor passed automated checks; visible labels agree with the mapping.
- Chart evidence: the black line is present over much of the range but contains irregular sections and late spikes.
- Status: **`calibration_verified`**.
- Price implication: monthly line candidates still require continuity review; this artifact does not authorize numeric extraction.

### NVIDIA GeForce RTX 4070 SUPER / inventory name `GeForce RTX 4070 SUPER`

- Source: `diagnostics/step17_source_images/geforce_rtx_4070_super.png`.
- Visible y-axis: `$1200` through `$0` in `$200` steps.
- Calibration: seven gridlines, monotonic ticks, and the October anchor passed; labels are readable.
- Chart evidence: broad black-line coverage with a late flat section; this is favorable for calibration but not proof of monthly price accuracy.
- Status: **`calibration_verified`**.
- Price implication: estimated values remain review-required under the existing policy.

### NVIDIA GeForce RTX 4070 Ti / inventory name `GeForce RTX 4070 Ti`

- Source: `diagnostics/step17_source_images/geforce_rtx_4070_ti.png`.
- Visible y-axis: `$1200` through `$0` in `$200` steps.
- Calibration: seven gridlines and the October anchor passed; tick order is strictly decreasing.
- Chart evidence: black line is visible but includes repeated sharp drops and disconnected-looking structures.
- Status: **`calibration_verified`**.
- Price implication: those structures require rejection/review handling; calibration alone does not support interpolation through them.

### NVIDIA GeForce RTX 4080 SUPER / inventory name `GeForce RTX 4080 SUPER`

- Source: `diagnostics/step17_source_images/geforce_rtx_4080_super.png`.
- Visible y-axis: `$1500` through `$0` in `$250` steps.
- Calibration: seven gridlines, readable ticks, and the October anchor passed.
- Chart evidence: the line is broadly visible with a short late peak.
- Status: **`calibration_verified`**.
- Price implication: the peak is a line-review concern; no post-boundary selection rule is introduced.

### NVIDIA GeForce RTX 5070 / inventory name `GeForce RTX 5070`

- Source: `diagnostics/step17_source_images/geforce_rtx_5070.png`.
- Visible y-axis: `$1200` through `$0` in `$200` steps.
- Calibration: seven gridlines and the October anchor passed.
- Chart evidence: black history begins around late 2024/early 2025; the earlier requested months do not visibly contain supported history.
- Status: **`calibration_verified`**.
- Price implication: early unsupported months remain `N/A`; no carry-forward or extrapolation is allowed.

### NVIDIA GeForce RTX 5080 / inventory name `GeForce RTX 5080`

- Source: `diagnostics/step17_source_images/geforce_rtx_5080.png`.
- Visible y-axis: `$3000` through `$0` in `$500` steps.
- Calibration: seven gridlines and the October anchor passed.
- Chart evidence: black history begins around early 2025 and the scale is coarse.
- Status: **`calibration_verified`**.
- Price implication: early unsupported months remain `N/A`; the coarse scale increases estimate/review sensitivity.

### AMD Radeon RX 7700 XT / inventory name `Radeon RX 7700 XT`

- Source: `diagnostics/step17_source_images/radeon_rx_7700_xt.png`.
- Visible y-axis: `$1200` through `$0` in `$200` steps.
- Calibration: seven gridlines and the October anchor passed.
- Chart evidence: the black line spans the chart with local irregularities.
- Status: **`calibration_verified`**.
- Price implication: local spikes or ambiguous candidates must retain the existing review/`N/A` semantics.

### AMD Radeon RX 7800 XT / inventory name `Radeon RX 7800 XT`

- Source: `diagnostics/step17_source_images/radeon_rx_7800_xt.png`.
- Visible y-axis: `$1200` through `$0` in `$200` steps.
- Calibration: seven gridlines and the October anchor passed.
- Chart evidence: broad black-line coverage with several drops and late irregularities.
- Status: **`calibration_verified`**.
- Price implication: visually supported calibration does not justify filling an ambiguous line segment.

### AMD Radeon RX 7900 XT / inventory name `Radeon RX 7900 XT`

- Source: `diagnostics/step17_source_images/radeon_rx_7900_xt.png`.
- Visible y-axis: `$1200` through `$0` in `$200` steps.
- Calibration: seven gridlines, monotonic ticks, and the October anchor passed.
- Chart evidence: noisy actual-price line with local spikes and a late drop.
- Status: **`calibration_verified`**.
- Price implication: candidate continuity and ambiguity review remain necessary; no smoothing is permitted.

## Validation results

The existing calibration implementation accepted all nine chart-specific configurations without changing code or thresholds. For every artifact:

- All plot and anchor coordinates are within the `1176×484` image bounds.
- Seven horizontal gridlines were detected.
- The configured y-axis values are strictly decreasing from top to bottom.
- The October 2024 anchor is within the existing five-pixel acceptance rule of the detected vertical gridline.
- The month mapping follows the existing `month_x_positions()` convention.
- No `extract_calibrated_prices()` call was made.

The validation is split correctly between automated and visual evidence: automated checks establish geometry consistency; visual inspection establishes that the tick labels, date anchor, and plot structure are actually readable. Neither establishes numeric monthly accuracy.

## Preservation and restrictions

- New artifacts were written only under `diagnostics/step18_queue_a_manual_calibration/` and the new Step 18 manifest/report.
- Frozen Step 9 output, previous calibration files, source images, and historical diagnostics were not overwritten.
- Queue B and Radeon RX 7600 XT were not calibrated.
- No production extraction logic, thresholds, or review policy changed.
- No API, scraper, OCR, or 23-GPU extraction batch was run.

## Next action

The nine Queue A charts now have proposed, independently recorded calibration artifacts. The single next action is to review and approve these nine artifacts for a separate supervised extraction pilot, preserving `N/A` for unsupported history and requiring visual review of every numeric line candidate. Do not begin the full 23-GPU batch and do not calibrate Queue B or RX 7600 XT as part of this step.

