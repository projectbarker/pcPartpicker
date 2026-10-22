# Cached July 2026 Completion and Missing-Value Audit

## Outcome

This execution audited all 23 cached July 3, 2026 chart images, repaired the six calibration failures only where the visible axis supported a manual gridline configuration, and merged newly supported values through atomic writes. No live Cloudflare-blocked page, OCR, API batch, interpolation, extrapolation, or third-party price source was used.

| Measure | Result |
|---|---:|
| GPU records | 23 |
| Monthly positions | 575 |
| Numeric values | 425 |
| `N/A` values | 150 |
| `observed` values | 35 |
| `estimated` values | 390 |
| Records requiring review | 23 |
| Failed records | 0 |

The pre-cached baseline had 307 numeric values. The first cached-source update added 97 values; the manual-axis recovery added 21 more, for 118 additions in total. Existing numeric values were not overwritten. August and September are excluded because the cached charts do not show those months.

## Source and calibration evidence

All 23 cached images were retrieved as 1176×484 PNGs and inspected in the source contact sheet and full-resolution representative charts. The rolling axis supports approximately February 2025 through July 2026. Live PCPartPicker page access remains Cloudflare-blocked.

The six former calibration failures were resolved with explicit `verified_y_gridlines` coordinates `[27, 94, 161, 227, 294, 361, 427]`, validated as in-bounds and monotonic. The default automatic seven-gridline check was not relaxed. The GeForce RTX 4070 `$600` gridline was visibly obscured by the black line but visible on both sides; the other five charts show the bottom `$0` boundary directly.

| GPU | New values merged | Remaining evidence issue |
|---|---:|---|
| GeForce RTX 4070 | 6 | missing segments and rejected spikes remain `N/A` where applicable |
| GeForce RTX 4070 Ti | 0 | missing segments and rejected spikes remain `N/A` where applicable |
| GeForce RTX 4070 Ti SUPER | 0 | missing segments and rejected spikes remain `N/A` where applicable |
| GeForce RTX 4090 | 0 | missing segments and rejected spikes remain `N/A` where applicable |
| Radeon RX 9060 XT | 6 | missing segments and rejected spikes remain `N/A` where applicable |
| Radeon RX 7600 XT | 9 | missing segments and rejected spikes remain `N/A` where applicable |

## Per-GPU coverage matrix

`Y` is numeric and `N` is `N/A`. The reason lists identify every remaining `N/A` position.

| GPU | 2024-07 | 2024-08 | 2024-09 | 2024-10 | 2024-11 | 2024-12 | 2025-01 | 2025-02 | 2025-03 | 2025-04 | 2025-05 | 2025-06 | 2025-07 | 2025-08 | 2025-09 | 2025-10 | 2025-11 | 2025-12 | 2026-01 | 2026-02 | 2026-03 | 2026-04 | 2026-05 | 2026-06 | 2026-07 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Arc A380 | N | N | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | N | Y | Y | Y | Y |
| Arc A750 | N | N | N | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| Arc A770 | N | N | N | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | N | N | Y | Y | Y |
| GeForce RTX 4070 | N | N | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| GeForce RTX 4070 SUPER | N | N | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | N | Y | Y | Y | Y | Y | Y | Y | Y | N |
| GeForce RTX 4070 Ti | N | N | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | N | Y | N | N | N | N | N | N | N |
| GeForce RTX 4070 Ti SUPER | N | N | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | N | N | N | N | N | N | N | N | N | N |
| GeForce RTX 4080 | N | N | N | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| GeForce RTX 4080 SUPER | N | N | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | N | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| GeForce RTX 4090 | N | N | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | N | N | N | N | N | N | N | N | N | N |
| GeForce RTX 5060 Ti | N | N | N | N | N | N | N | N | N | N | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| GeForce RTX 5070 | N | N | N | N | N | N | N | N | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| GeForce RTX 5070 Ti | N | N | N | N | N | N | N | N | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| GeForce RTX 5080 | N | N | N | N | N | N | N | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| GeForce RTX 5090 | N | N | N | N | N | N | N | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| Radeon RX 7600 XT | N | N | N | N | N | N | N | Y | Y | Y | Y | Y | Y | Y | N | N | N | N | N | N | N | N | N | Y | Y |
| Radeon RX 7700 XT | N | N | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| Radeon RX 7800 XT | N | N | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | N |
| Radeon RX 7900 XT | N | N | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| Radeon RX 7900 XTX | N | N | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| Radeon RX 9060 XT | N | N | N | N | N | N | N | N | N | N | N | N | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| Radeon RX 9070 | N | N | N | N | N | N | N | Y | N | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| Radeon RX 9070 XT | N | N | N | N | N | N | N | Y | N | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |

## Remaining `N/A` classifications

| Reason | Count |
|---|---:|
| `out_of_history` | 85 |
| `missing_line_segment` | 54 |
| `isolated_spike` | 11 |
| `source_unavailable_chart_not_visible` | 0 |

## Exact remaining `N/A` positions

- **Arc A380**: `out_of_history`: 2024-07-01, 2024-08-01; `isolated_spike`: 2026-03-01
- **Arc A750**: `out_of_history`: 2024-07-01, 2024-08-01, 2024-09-01
- **Arc A770**: `out_of_history`: 2024-07-01, 2024-08-01, 2024-09-01; `missing_line_segment`: 2026-03-01, 2026-04-01
- **GeForce RTX 4070**: `out_of_history`: 2024-07-01, 2024-08-01
- **GeForce RTX 4070 SUPER**: `out_of_history`: 2024-07-01, 2024-08-01; `isolated_spike`: 2025-10-01, 2026-07-01
- **GeForce RTX 4070 Ti**: `out_of_history`: 2024-07-01, 2024-08-01; `missing_line_segment`: 2025-11-01, 2026-01-01, 2026-02-01, 2026-03-01, 2026-04-01, 2026-05-01, 2026-06-01, 2026-07-01
- **GeForce RTX 4070 Ti SUPER**: `out_of_history`: 2024-07-01, 2024-08-01; `isolated_spike`: 2025-10-01, 2026-05-01; `missing_line_segment`: 2025-11-01, 2025-12-01, 2026-01-01, 2026-02-01, 2026-03-01, 2026-04-01, 2026-06-01, 2026-07-01
- **GeForce RTX 4080**: `out_of_history`: 2024-07-01, 2024-08-01, 2024-09-01
- **GeForce RTX 4080 SUPER**: `out_of_history`: 2024-07-01, 2024-08-01; `isolated_spike`: 2025-10-01
- **GeForce RTX 4090**: `out_of_history`: 2024-07-01, 2024-08-01; `isolated_spike`: 2025-10-01; `missing_line_segment`: 2025-11-01, 2025-12-01, 2026-01-01, 2026-02-01, 2026-03-01, 2026-04-01, 2026-05-01, 2026-06-01, 2026-07-01
- **GeForce RTX 5060 Ti**: `out_of_history`: 2024-07-01, 2024-08-01, 2024-09-01, 2024-10-01, 2024-11-01, 2024-12-01; `missing_line_segment`: 2025-01-01, 2025-02-01, 2025-03-01, 2025-04-01
- **GeForce RTX 5070**: `out_of_history`: 2024-07-01, 2024-08-01, 2024-09-01, 2024-10-01, 2024-11-01, 2024-12-01; `missing_line_segment`: 2025-01-01; `isolated_spike`: 2025-02-01
- **GeForce RTX 5070 Ti**: `out_of_history`: 2024-07-01, 2024-08-01, 2024-09-01, 2024-10-01, 2024-11-01, 2024-12-01; `missing_line_segment`: 2025-01-01; `isolated_spike`: 2025-02-01
- **GeForce RTX 5080**: `out_of_history`: 2024-07-01, 2024-08-01, 2024-09-01, 2024-10-01, 2024-11-01, 2024-12-01; `missing_line_segment`: 2025-01-01
- **GeForce RTX 5090**: `out_of_history`: 2024-07-01, 2024-08-01, 2024-09-01, 2024-10-01, 2024-11-01, 2024-12-01; `missing_line_segment`: 2025-01-01
- **Radeon RX 7600 XT**: `out_of_history`: 2024-07-01, 2024-08-01, 2024-09-01, 2024-10-01, 2024-11-01, 2024-12-01; `missing_line_segment`: 2025-01-01, 2025-11-01, 2025-12-01, 2026-01-01, 2026-02-01, 2026-03-01, 2026-04-01, 2026-05-01; `isolated_spike`: 2025-09-01, 2025-10-01
- **Radeon RX 7700 XT**: `out_of_history`: 2024-07-01, 2024-08-01
- **Radeon RX 7800 XT**: `out_of_history`: 2024-07-01, 2024-08-01; `missing_line_segment`: 2026-07-01
- **Radeon RX 7900 XT**: `out_of_history`: 2024-07-01, 2024-08-01
- **Radeon RX 7900 XTX**: `out_of_history`: 2024-07-01, 2024-08-01
- **Radeon RX 9060 XT**: `out_of_history`: 2024-07-01, 2024-08-01, 2024-09-01, 2024-10-01, 2024-11-01, 2024-12-01; `missing_line_segment`: 2025-01-01, 2025-02-01, 2025-03-01, 2025-04-01, 2025-05-01, 2025-06-01
- **Radeon RX 9070**: `out_of_history`: 2024-07-01, 2024-08-01, 2024-09-01, 2024-10-01, 2024-11-01, 2024-12-01; `missing_line_segment`: 2025-01-01, 2025-03-01
- **Radeon RX 9070 XT**: `out_of_history`: 2024-07-01, 2024-08-01, 2024-09-01, 2024-10-01, 2024-11-01, 2024-12-01; `missing_line_segment`: 2025-01-01, 2025-03-01

## Validation

- The prior 97 cached-source values were rechecked against source identity, axis configuration, monthly x-positions, diagnostics, numeric conversion, and review metadata; none was removed by the evidence audit.
- The manual-axis pass added 21 further values; all are estimated/review-required unless aligned to a calibrated tick.
- Remaining `N/A` values are not fabricated or interpolated.
- Final dataset writes used timestamped backups and the existing atomic-write helper.
- Raw images and diagnostics remain local under ignored directories; compact source validation remains in `docs/CACHED_JULY_2026_VALIDATION.json`.
