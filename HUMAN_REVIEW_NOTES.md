# Human Review Notes — GeForce RTX 4070 Ti

## Provisional reviewer observation

- GPU: GeForce RTX 4070 Ti
- Review period: August–September 2026
- Reviewer observation: “The price line appears to reach approximately $700 between August and September 2026.”
- Status: Provisional observation only. It does not change the production dataset, review flags, or the existing review register.

## Exact evidence files

The matching rows in both `final_review_register.csv` and `manual_review_queue.json` identify the same artifacts:

- Source chart: `C:\Users\ranvi\Documents\Ranvijay_Work\GPU_PCPARTPICKER\diagnostics\live_chart_sources_20261022\geforce_rtx_4070_ti.png`
  - Native dimensions: 1176 × 484
  - SHA-256: `7E27B78525F14033B4B3954B5C32ADADD560CB308F72BF0F1780B74F2F943FB5`
  - Created: 2026-10-22 12:25:27 UTC
- Overlay: `C:\Users\ranvi\Documents\Ranvijay_Work\GPU_PCPARTPICKER\experimental\aug_sep_2026_full_review_20261022\geforce_rtx_4070_ti.overlay.png`
  - SHA-256: `DD5120B051CDC95E36600799FE6F1ECD15E29B597FC559B6EB91A92723DD822F`
  - Created: 2026-10-22 12:31:16 UTC
- Diagnostic JSON: `C:\Users\ranvi\Documents\Ranvijay_Work\GPU_PCPARTPICKER\experimental\aug_sep_2026_full_review_20261022\geforce_rtx_4070_ti.diagnostic.json`
  - SHA-256: `94E4CFEEE1E1299D59CFCC52469E490F5D7EC16246748ED146D8838054ED04BB`
  - Created: 2026-10-22 12:31:16 UTC

These are the relevant files; similarly named Queue A, Queue B, and earlier pilot files were not substituted.

## Evidence review

The diagnostic records the calibrated plot and monthly positions as follows:

- Plot bounds: x=55..1149, y=27..427.
- Y-axis ticks: y=427=$0, y=361=$200, y=294=$400, y=227=$600, y=161=$800, y=94=$1,000, y=27=$1,200.
- August 2026 monthly x-position: x=985.
- September 2026 monthly x-position: x=1047.
- Diagnostic result at both monthly positions: no accepted black-line component; `missing_line_segment`; price remains `N/A`.

Native-pixel inspection shows the dark trace is at the bottom axis from approximately x=960 through x=1032, then rises in a narrow feature around x=1033..1039. The top of that feature is near y=193, which maps to approximately $700 using the verified y-axis scale. The feature returns to the bottom axis by approximately x=1040 and is therefore between the August anchor x=985 and September anchor x=1047, not at either monthly sampling position.

In simple terms: the chart supports “a short feature around $700 between the two month anchors.” It does not establish that the feature belongs to August or September. Assigning $700 to both months, or assigning it to one month without an explicit chart date marker, would be inference rather than direct evidence.

## Current disposition

Retain both August 2026 and September 2026 as `N/A` with the existing `missing_line_segment` reason. The reviewer observation is useful context but is not sufficient to replace either value.

Additional evidence needed to finalize a numeric month would be an explicit date marker or source data showing whether the short feature occurred on the August or September observation date. The current chart image and overlay do not provide that evidence. No production file was modified.

## Provisional note — GeForce RTX 4070 Ti SUPER, August 2026

- Reviewer observation: the black line appears to reach approximately `$1,600–$1,700`; the reviewer identifies the blue horizontal gridline as `$1,500`.
- Exact source chart: `C:\Users\ranvi\Documents\Ranvijay_Work\GPU_PCPARTPICKER\diagnostics\live_chart_sources_20261022\geforce_rtx_4070_ti_super.png`.
- Exact overlay: `C:\Users\ranvi\Documents\Ranvijay_Work\GPU_PCPARTPICKER\experimental\aug_sep_2026_full_review_20261022\geforce_rtx_4070_ti_super.overlay.png`.
- Exact diagnostic: `C:\Users\ranvi\Documents\Ranvijay_Work\GPU_PCPARTPICKER\experimental\aug_sep_2026_full_review_20261022\geforce_rtx_4070_ti_super.diagnostic.json`.
- Calibration: y=427 is `$0`; y=361 is `$500`; y=294 is `$1,000`; y=227 is `$1,500`; y=161 is `$2,000`; y=94 is `$2,500`; y=27 is `$3,000`. August is x=985 and September is x=1047.
- Pixel inspection: the tall feature is approximately x=995..1005 with its top near y=219, mapping to roughly `$1,560`. It is between the August and September x-positions. Additional short features occur around x=1023..1027 and x=1033..1039, also between the monthly positions.
- Diagnostic status: both August and September have no accepted y-position and remain `missing_line_segment` / `N/A`.
- Provisional disposition: the chart confirms a nearby $1,600–$1,700 feature, but does not establish it as the August monthly value. Retain August and September as `N/A`; do not classify this observation as observed or estimated without a defensible month assignment.
