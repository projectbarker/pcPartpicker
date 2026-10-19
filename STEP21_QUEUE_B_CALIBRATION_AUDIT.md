# Step 21 — Queue B Calibration Evidence Audit

**Audit date:** 2026-10-19  
**Scope:** GeForce RTX 4070 Ti SUPER, GeForce RTX 5060 Ti, GeForce RTX 5070 Ti, Radeon RX 9060 XT, Radeon RX 9070, and Radeon RX 9070 XT. No monthly extraction was run.

## Evidence inspected

The exact local source images and URLs recorded in `STEP17_SOURCE_IMAGE_EVIDENCE_MANIFEST.json` were used. All six images are PNGs with dimensions 1176×484 and were visually opened. The existing `coordinate_calibration.py` detector and calibration tests were inspected. No production code, threshold, policy, existing calibration, or pilot output was changed.

The detector found the same six interior horizontal lines for every chart:

`y = [27, 94, 161, 227, 294, 361]`

The visible lower chart boundary is at approximately `y=427`, but it is not accepted as the seventh neutral-gray line by the existing detector. Direct pixel inspection explains the failure: the detector requires at least 70% of the image row to be neutral gray with mean 90–190; at y=427, the six charts have neutral-gray coverage of approximately 68.1%, 55.4%, 68.2%, 46.7%, 67.3%, and 67.3%, respectively. Dark chart content and/or the border therefore displaces enough pixels to fail the existing rule. This is evidence about detector behavior, not permission to lower its threshold.

The visible y-axis labels were read from the chart images and recorded only where consistent with the six existing interior lines and the Step 17 manifest:

| GPU | Verified top-to-bottom tick labels |
|---|---|
| RTX 4070 Ti SUPER | 1200, 1000, 800, 600, 400, 200, 0 |
| RTX 5060 Ti | 1200, 1000, 800, 600, 400, 200, 0 |
| RTX 5070 Ti | 1500, 1250, 1000, 750, 500, 250, 0 |
| RX 9060 XT | 1200, 1000, 800, 600, 400, 200, 0 |
| RX 9070 | 1200, 1000, 800, 600, 400, 200, 0 |
| RX 9070 XT | 1200, 1000, 800, 600, 400, 200, 0 |

The date-axis anchor is visually consistent with October 2024 at `x=113` for all six. The detected vertical gridline sequence is `[55, 113, 175, 235, 296, 359, 415, 477, 537, 599, 659, 721, 783, 843, 905, 965, 1026, 1089, 1145, 1149]`; this is recorded as evidence, not a license to extract prices.

## Per-GPU assessment

| GPU | Image/chart evidence | Status | Reason |
|---|---|---|---|
| RTX 4070 Ti SUPER | Six interior lines and all tick labels are readable; bottom boundary is visually present but partly affected by the lower dark trace; late history has a sharp drop. | `manual_review_required` | Bottom calibration is not detector-complete and late line support needs review. |
| RTX 5060 Ti | Six interior lines and labels are readable; black history begins materially after the requested start; the lower row is dark/occluded. | `manual_review_required` | Confirm bottom y=427/$0 manually and preserve early months as unsupported. |
| RTX 5070 Ti | Six interior lines and labels are readable; black history begins around early 2025; bottom row is not a complete neutral-gray line. | `manual_review_required` | Confirm bottom calibration manually; no early-history prices may be inferred. |
| RX 9060 XT | Six interior lines and labels are readable; actual line begins later and bottom row has low neutral-gray coverage. | `manual_review_required` | Confirm bottom calibration manually and review history start. |
| RX 9070 | Six interior lines and labels are readable; early region includes disconnected-looking structures and lower row overlap. | `manual_review_required` | Bottom calibration and early-line support require human review. |
| RX 9070 XT | Six interior lines and labels are readable; visible actual history starts later; bottom row is not detector-complete. | `manual_review_required` | Confirm bottom calibration manually and preserve unsupported early months. |

None is classified `calibration_verified`, because the existing calibration contract requires the number of detected horizontal lines to match the supplied tick values and each chart returned six rather than seven. None is `blocked`: each source image is available and readable enough for a focused manual calibration review. The separate RX 7600 XT blocker remains unchanged and is not included in this audit.

## New artifacts

Per-GPU evidence artifacts are in `diagnostics/step21_queue_b/`. They retain verified dimensions, visible plot bounds, detected interior lines, visible tick labels, anchor, vertical gridlines, detector outcome, and unresolved concerns. The machine-readable summary is `STEP21_QUEUE_B_CALIBRATION_MANIFEST.json`.

## Tests and commands

Read-only checks executed:

- Read the Step 17/18/20 evidence and readiness files.
- Opened all six source images with the local image viewer.
- Ran `detect_gridlines` against the six images: each returned six horizontal lines and the expected vertical sequence.
- Inspected the detector implementation and calculated the y=427 neutral-gray coverage that causes the existing 70% rule to fail.

No code or tests were changed, so no test suite was rerun. No scraper, OCR, AI API, extraction runner, or 23-GPU batch was run.

## Recommendation

The six records are suitable for a short, human-supervised bottom-axis calibration review, but not for price extraction yet. The single next action is to have a reviewer explicitly approve or reject the visible `y=427 / $0` bottom boundary for each chart and record that decision in the Step 21 artifacts; do not lower the detector threshold or infer any prices before that approval.

