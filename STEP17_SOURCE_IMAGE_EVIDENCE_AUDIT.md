# Step 17 — Source Image Evidence Audit

**Date:** 2026-10-19  
**Scope:** Recovery and calibration-evidence review for the 15 records marked `manual_calibration_required`. No monthly prices were extracted.

## Result summary

- Inventory source of truth: `CALIBRATION_READINESS_INVENTORY.json`.
- Exact manual-calibration records: 15.
- Images recovered from their already-recorded URLs: **15 of 15**.
- Images visually inspected: **15 of 15**.
- Dimensions: all recovered images are `1176×484`.
- Seven horizontal gridlines detected by the existing detector: **9**.
- Six horizontal gridlines detected: **6**; these require direct verification of the bottom `y≈427` gridline before calibration is accepted.
- Images suitable to enter the manual-calibration queue: **15**, subject to the evidence-specific conditions below.
- Monthly extraction run: **No**.

The recovered images are evidence for calibration review, not permission to generate prices. Several charts have incomplete black-line history for the requested July 2024–January 2026 interval, and those months must remain `N/A` unless a visible supported line is later verified.

## Recovery method and preservation

The 15 URLs were copied exactly from the existing inventory and retrieved directly into the new directory `diagnostics/step17_source_images/`. The scraper, OpenAI API, OCR, and extraction runner were not used. Existing calibration files, pilot outputs, historical outputs, and diagnostics were not overwritten.

The machine-readable details, local paths, URL identities, dimensions, SHA-256 prefixes, detector rows, visible tick readings, and next actions are in [STEP17_SOURCE_IMAGE_EVIDENCE_MANIFEST.json](STEP17_SOURCE_IMAGE_EVIDENCE_MANIFEST.json).

## Exact records and evidence findings

| GPU | Image found | Dimensions | Gridline detector | Visible axis/tick evidence | Manual calibration assessment | History/review note |
|---|---|---:|---|---|---|---|
| Arc A770 | Yes | 1176×484 | 7 rows | `$600` to `$0`, 100-dollar steps; October anchor visually available | Feasible | Line spans chart but has irregular sections and late spikes; review required |
| GeForce RTX 4070 SUPER | Yes | 1176×484 | 7 rows | `$1200` to `$0`, 200-dollar steps; October anchor visually available | Feasible | Broad line coverage; late flat section still needs review |
| GeForce RTX 4070 Ti | Yes | 1176×484 | 7 rows | `$1200` to `$0`, 200-dollar steps; October anchor visually available | Feasible | Repeated sharp drops and disconnected-looking structures need review |
| GeForce RTX 4070 Ti SUPER | Yes | 1176×484 | 6 rows | `$1200` to `$0`, 200-dollar steps visually readable | Feasible after bottom-row verification | Late drop/unsupported-looking region; do not treat calibration as price support |
| GeForce RTX 4080 SUPER | Yes | 1176×484 | 7 rows | `$1500` to `$0`, 250-dollar steps; October anchor visually available | Feasible | Broad line coverage with a short late peak; review required |
| GeForce RTX 5060 Ti | Yes | 1176×484 | 6 rows | `$1200` to `$0`, 200-dollar steps visually readable | Feasible after bottom-row verification | Black history begins materially later; early requested months are unsupported |
| GeForce RTX 5070 | Yes | 1176×484 | 7 rows | `$1200` to `$0`, 200-dollar steps; October anchor visually available | Feasible | Black history begins late 2024/early 2025; preserve earlier `N/A` |
| GeForce RTX 5070 Ti | Yes | 1176×484 | 6 rows | `$1500` to `$0`, 250-dollar steps visually readable | Feasible after bottom-row verification | Black history begins around early 2025; preserve earlier `N/A` |
| GeForce RTX 5080 | Yes | 1176×484 | 7 rows | `$3000` to `$0`, 500-dollar steps; October anchor visually available | Feasible | Black history begins around early 2025; coarse scale limits precision |
| Radeon RX 7700 XT | Yes | 1176×484 | 7 rows | `$1200` to `$0`, 200-dollar steps; October anchor visually available | Feasible | Broad line coverage with local irregularities; review required |
| Radeon RX 7800 XT | Yes | 1176×484 | 7 rows | `$1200` to `$0`, 200-dollar steps; October anchor visually available | Feasible | Broad line coverage with drops/late irregularities; review required |
| Radeon RX 7900 XT | Yes | 1176×484 | 7 rows | `$1200` to `$0`, 200-dollar steps; October anchor visually available | Feasible | Noisy line and late drop; reject ambiguous candidates |
| Radeon RX 9060 XT | Yes | 1176×484 | 6 rows | `$1200` to `$0`, 200-dollar steps visually readable | Feasible after bottom-row verification | Black history begins around mid-2025; earlier months unsupported |
| Radeon RX 9070 | Yes | 1176×484 | 6 rows | `$1200` to `$0`, 200-dollar steps visually readable | Feasible after bottom-row verification | Later history and early vertical structures; early months unsupported |
| Radeon RX 9070 XT | Yes | 1176×484 | 6 rows | `$1200` to `$0`, 200-dollar steps visually readable | Feasible after bottom-row verification | Later history and early vertical structures; early months unsupported |

## What “19 monthly positions visible” means here

All recovered charts show the common monthly date-axis gridline layout, including the requested span’s x positions. That does not mean the black actual-price line supports all 19 months. The newer products visibly begin later than July 2024, including RTX 5060 Ti, RTX 5070, RTX 5070 Ti, RTX 5080, RX 9060 XT, RX 9070, and RX 9070 XT. Their unsupported early months must remain `N/A`; no carry-forward or extrapolation is permitted.

The older charts generally show a black line across more of the requested span, but sharp drops, disconnected-looking segments, or local noise still require the existing line-selection and human-review policy.

## Proposed manual-calibration queue

### Queue A — ready for direct manual calibration review

These nine images have valid PNGs, readable axes/ticks, the common date-axis anchor near October 2024, and seven detected horizontal gridlines:

1. Arc A770
2. GeForce RTX 4070 SUPER
3. GeForce RTX 4070 Ti
4. GeForce RTX 4080 SUPER
5. GeForce RTX 5070
6. GeForce RTX 5080
7. Radeon RX 7700 XT
8. Radeon RX 7800 XT
9. Radeon RX 7900 XT

Manual work should record the chart-specific anchor/tick mapping and produce a separate calibration artifact. It must not create monthly values yet.

### Queue B — bottom-gridline verification required

These six images are readable and have visible tick labels, but the existing detector returns six rows rather than seven:

- GeForce RTX 4070 Ti SUPER
- GeForce RTX 5060 Ti
- GeForce RTX 5070 Ti
- Radeon RX 9060 XT
- Radeon RX 9070
- Radeon RX 9070 XT

The failure pattern is the same as the previously investigated RX 7600 XT case: the bottom axis/gridline near `y=427` is visually present but is partly dark, so it fails the detector’s neutral-gray coverage rule. This is a calibration-evidence issue, not permission to reduce the threshold globally. Each record needs direct manual verification or a narrowly scoped, separately tested detector improvement.

### Separate blocked record — Radeon RX 7600 XT

RX 7600 XT remains outside the 15-record queue. Its image is locally readable and its `$600`–`$0` scale is visible, but it remains blocked under the existing safety check until the seventh gridline is separately verified or a minimal detector correction is justified and tested.

## Policy and safety confirmation

The recovered images do not change the approved policy:

- No source URL was changed.
- No price was estimated or filled.
- No missing history was interpolated or extrapolated.
- Ambiguous line candidates remain review-required or `N/A`.
- The 19-month schema and `observed`/`estimated`/`N/A` semantics remain unchanged.
- Frozen Step 9 values and historical artifacts were not rewritten.
- Post-boundary stability sampling remains diagnostic-only.

## Validation performed

Read-only/recovery commands and checks:

- Parsed `CALIBRATION_READINESS_INVENTORY.json` to select the exact 15 records.
- Retrieved only the 15 recorded image URLs into the new Step 17 evidence directory.
- Verified each response has a PNG signature and recorded file size/hash prefix.
- Opened and visually inspected all 15 recovered images.
- Ran the existing `detect_gridlines()` function only; no monthly extraction function was called.
- Confirmed all images are `1176×484` and all have the expected vertical date-grid pattern with anchor near `x=113`.

No code or test files changed, so the automated test suite was not rerun for this evidence-only step.

## Status and next action

**15 of 15 images were recovered locally. All 15 are suitable to enter a manual-calibration queue, but only 9 currently have complete detector geometry and 6 require bottom-gridline verification.** Several charts still have incomplete visible black-line history and will require `N/A` months after calibration.

Safe progress toward the full 23-GPU dataset is possible today only at the calibration-evidence stage. A complete 23-GPU monthly dataset is not safe today because calibration artifacts are not yet approved for these 15 records, RX 7600 XT remains blocked, and monthly extraction must still pass visual review.

**Single next action:** manually verify and record the chart-specific anchor/tick calibration for Queue A, beginning with Arc A770, then resolve the bottom-gridline evidence for Queue B; do not start price extraction until those calibration artifacts are reviewed.

