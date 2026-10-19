# Step 20 — Queue A Value-Level Human Review

**Audit date:** 2026-10-19  
**Scope:** Existing Step 19 nine-GPU pilot only. No extraction was rerun and no pilot output was changed.

## Scope and evidence

Reviewed the Step 19 pilot output, pilot manifest, nine calibration diagnostics, nine Step 19 overlays, and the nine exact source charts under `diagnostics/step17_source_images/`. The output contains 9 × 19 = 171 monthly cells: 137 numeric values and 34 `N/A` values. The quality metadata reports 11 `observed` and 126 `estimated` numeric values.

The review used the recorded monthly x-position, selected y-position where present, diagnostic status/reason, overlay marker, and the corresponding black actual-price line in the source chart. Visual readings are evidence of line attachment and conservative classification, not independent ground truth for dollar accuracy.

## Results

| Classification | Count | Treatment |
|---|---:|---|
| `visually_supported` | 11 | The 11 values labelled `observed` were visibly aligned with the black line and the calibrated gridline level. They remain `observed` in the frozen output. |
| `estimated_needs_review` | 126 | All estimated numeric values remain estimates and review-required. The markers generally attach to the black line, but the raster chart does not independently establish exact-dollar accuracy. |
| `ambiguous_keep_na` | 4 | Four isolated-spike months remain `N/A`; the chart has a competing short spike at the monthly position, so the conservative rejection is appropriate. |
| `missing_keep_na` | 30 | Eighteen months are outside visible history and twelve have no supported line segment at the sampled position. No history was filled. |
| `suspected_extraction_error` | 0 | No confirmed numeric point was visibly selected from a gridline, legend, or unrelated dark feature. |

All 171 monthly cells are represented in these counts. No value was rewritten.

## Record-level coverage

| GPU | Numeric | N/A | Observed | Estimated | Review reasons |
|---|---:|---:|---:|---:|---|
| Arc A770 | 16 | 3 | 2 | 14 | estimated; isolated spike; outside history |
| GeForce RTX 4070 SUPER | 16 | 3 | 0 | 16 | estimated; isolated spike; outside history |
| GeForce RTX 4070 Ti | 15 | 4 | 5 | 10 | estimated; missing line; outside history |
| GeForce RTX 4080 SUPER | 16 | 3 | 0 | 16 | estimated; isolated spike; outside history |
| GeForce RTX 5070 | 11 | 8 | 0 | 11 | estimated; isolated spike; missing line; outside history |
| GeForce RTX 5080 | 12 | 7 | 0 | 12 | estimated; missing line; outside history |
| Radeon RX 7700 XT | 17 | 2 | 0 | 17 | estimated; outside history |
| Radeon RX 7800 XT | 17 | 2 | 2 | 15 | estimated; outside history |
| Radeon RX 7900 XT | 17 | 2 | 2 | 15 | estimated; outside history |

## Flagged-month review

The following are all 34 `N/A` months. `x` is the recorded monthly sample coordinate; `—` means the month is outside the visible chart history and no x-position was assigned.

| GPU | Months | Recorded x | Diagnostic evidence | Classification and review conclusion |
|---|---|---|---|---|
| Arc A770 | Jul–Aug 2024 | — | `out_of_history`, no candidates | `missing_keep_na`; the source chart begins later than the requested period. |
| Arc A770 | Sep 2024 | 55 | Rejected candidate, `isolated_spike`, vertical-spike flag | `ambiguous_keep_na`; orange overlay marker is at the boundary spike, not an accepted value. |
| RTX 4070 SUPER | Jul–Aug 2024 | — | `out_of_history`, no candidates | `missing_keep_na`. |
| RTX 4070 SUPER | Oct 2025 | 843 | Rejected candidate, `isolated_spike`, vertical-spike flag | `ambiguous_keep_na`; the source chart has a short high excursion at the boundary and the overlay rejects it. |
| RTX 4070 Ti | Jul–Aug 2024 | — | `out_of_history`, no candidates | `missing_keep_na`. |
| RTX 4070 Ti | Nov 2025 and Jan 2026 | 905, 1026 | `missing_line_segment`, no accepted position | `missing_keep_na`; the source chart contains unsupported/disconnected late regions. |
| RTX 4080 SUPER | Jul–Aug 2024 | — | `out_of_history`, no candidates | `missing_keep_na`. |
| RTX 4080 SUPER | Oct 2025 | 843 | Rejected candidate, `isolated_spike`, vertical-spike flag | `ambiguous_keep_na`; the visible short peak is not treated as the monthly price. |
| RTX 5070 | Jul–Aug 2024 | — | `out_of_history`, no candidates | `missing_keep_na`. |
| RTX 5070 | Sep 2024–Jan 2025 | 55, 113, 175, 235, 296 | `missing_line_segment`, no accepted position | `missing_keep_na`; the requested early history is unsupported in the actual-price trace. |
| RTX 5070 | Feb 2025 | 359 | Rejected candidate, `isolated_spike`, vertical-spike flag | `ambiguous_keep_na`; the orange overlay marker coincides with a brief launch-region spike. |
| RTX 5080 | Jul–Aug 2024 | — | `out_of_history`, no candidates | `missing_keep_na`. |
| RTX 5080 | Sep 2024–Jan 2025 | 55, 113, 175, 235, 296 | `missing_line_segment`, no accepted position | `missing_keep_na`; source chart history is not supported at those target positions. |
| Radeon RX 7700 XT | Jul–Aug 2024 | — | `out_of_history`, no candidates | `missing_keep_na`. |
| Radeon RX 7800 XT | Jul–Aug 2024 | — | `out_of_history`, no candidates | `missing_keep_na`. |
| Radeon RX 7900 XT | Jul–Aug 2024 | — | `out_of_history`, no candidates | `missing_keep_na`. |

The grouped rows expand to 34 monthly cells; no flagged month is omitted. `N/A` values are retained rather than interpolated from neighboring line segments.

## Observed-value review

The 11 values labelled `observed` were checked separately from the estimates. Each accepted marker sits on the black actual-price line in the corresponding source chart and is close to a readable horizontal calibrated level. This supports the quality classification, but does not establish a universal accuracy threshold.

| GPU | Month | Value | x | y | Finding |
|---|---|---:|---:|---:|---|
| Arc A770 | May 2025 | $300.00 | 537 | 228 | `visually_supported`; on the black plateau at the $300 gridline. |
| Arc A770 | Jul 2025 | $400.00 | 659 | 159 | `visually_supported`; on the black line near the $400 gridline. |
| RTX 4070 Ti | Oct 2024 | $800.00 | 113 | 162 | `visually_supported`; on the black line near $800. |
| RTX 4070 Ti | Jan 2025 | $800.00 | 296 | 161 | `visually_supported`. |
| RTX 4070 Ti | May 2025 | $800.00 | 537 | 161 | `visually_supported`. |
| RTX 4070 Ti | Jun 2025 | $800.00 | 599 | 160 | `visually_supported`. |
| RTX 4070 Ti | Jul 2025 | $800.00 | 659 | 162 | `visually_supported`; later unsupported dips remain separate `N/A` decisions. |
| Radeon RX 7800 XT | Oct 2025 | $600.00 | 843 | 226 | `visually_supported`; marker follows the line around the $600 level. |
| Radeon RX 7800 XT | Dec 2025 | $600.00 | 965 | 228 | `visually_supported`. |
| Radeon RX 7900 XT | May 2025 | $800.00 | 537 | 160 | `visually_supported`. |
| Radeon RX 7900 XT | Jun 2025 | $800.00 | 599 | 163 | `visually_supported`. |

## Estimated-value review

All 126 estimated numeric values remain `estimated` and `review_required`. The source charts and overlays show that the accepted markers generally track the black actual-price line, including changing and relatively flat sections. That is useful extraction evidence, but the line thickness, grid scale, and absence of independent numeric ground truth prevent reclassifying any estimate as `observed`. No estimate was silently converted, rounded differently, or replaced.

## Defects and limitations

No confirmed extraction defect was found. In particular, the reviewed overlays show orange rejection markers at the four isolated-spike positions and no accepted marker there; missing-history and missing-line positions have no numeric value. The audit therefore found no evidence supporting a price correction.

The remaining limitation is material: 126 of 137 numeric values are estimates, and all nine records remain `needs_review`. Visual attachment to the line is not sufficient to approve a complete dataset, especially where the monthly meaning of a boundary transition is unresolved. The audit also does not supply independent ground truth for exact-dollar error.

## Expansion recommendation

Do not expand to Queue B or the 23-GPU batch yet. The current method is suitable for continued supervised review of this pilot, but the evidence is not sufficient to claim reliable unattended expansion. The next gate is human adjudication of the 126 estimates and the four ambiguous spike rejections, with the 30 missing/out-of-history values kept `N/A`; any policy change requires separate approval.

## Commands and preservation check

Read-only inspection used PowerShell directory inspection, the project virtual-environment Python interpreter to read JSON diagnostics/output, and the image viewer for all nine source charts and all nine Step 19 overlays. No scraper, OCR, API, extraction runner, or test-changing code was run. Existing Step 9 and Step 19 outputs and diagnostics were preserved.

