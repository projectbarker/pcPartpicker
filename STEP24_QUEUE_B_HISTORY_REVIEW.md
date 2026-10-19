# Step 24 — Queue B Black-Line History Review

**Date:** 2026-10-19  
**Scope:** Six Queue B charts, July 2024–January 2026. No price extraction, OCR, API, or batch processing.

## Evidence and limitation

The six original source charts under `diagnostics/step17_source_images/` were opened and reviewed against the Step 23 calibration artifacts. The Step 23 and Step 22 directories contain calibration JSON artifacts but no Queue B-specific overlay PNGs; therefore this review does not claim to have inspected a nonexistent overlay. The source chart pixels, axis labels, accepted geometry, and monthly x positions were used directly.

The review distinguishes a clearly traceable black line from dark pixels lying on the accepted `$0` boundary. A baseline overlap is not treated as a valid zero price. No missing history was interpolated or extrapolated.

## Classification totals

Across 6 × 19 = 114 monthly positions:

- Clearly visible and traceable: **64**
- Present but ambiguous/disconnected: **38**
- Not in the visible calibrated history: **12**

The 12 outside-history positions are July and August 2024 for each chart. The remaining early black/bottom or transition regions are conservatively ambiguous rather than numeric history.

## Per-GPU review

| GPU | First supported month | Clearly visible | Ambiguous/disconnected | Outside visible history | Unresolved concerns |
|---|---|---:|---:|---:|---|
| RTX 4070 Ti SUPER | September 2024 | 13 | 4 | 2 | Sharp October 2025 drop and late black/$0 overlap. |
| RTX 5060 Ti | May 2025 | 9 | 8 | 2 | Early black trace lies on the bottom boundary; not accepted as zero prices. |
| RTX 5070 Ti | March 2025 | 11 | 6 | 2 | Early launch/zero structures are disconnected; no pre-March inference. |
| RX 9060 XT | March 2025 | 11 | 6 | 2 | Steep February/March transition; earlier baseline is unsupported. |
| RX 9070 | April 2025 | 10 | 7 | 2 | Early vertical/zero structures and March transition are ambiguous. |
| RX 9070 XT | April 2025 | 10 | 7 | 2 | Early vertical/zero structures and March transition are ambiguous. |

## Month-level findings

The machine-readable manifest records every requested month. The following ranges summarize the same per-month classifications:

| GPU | Not in visible history | Ambiguous/disconnected | Clearly visible |
|---|---|---|---|
| RTX 4070 Ti SUPER | Jul–Aug 2024 | Oct 2025–Jan 2026 | Sep 2024–Sep 2025 |
| RTX 5060 Ti | Jul–Aug 2024 | Sep 2024–Apr 2025 | May 2025–Jan 2026 |
| RTX 5070 Ti | Jul–Aug 2024 | Sep 2024–Feb 2025 | Mar 2025–Jan 2026 |
| RX 9060 XT | Jul–Aug 2024 | Sep 2024–Feb 2025 | Mar 2025–Jan 2026 |
| RX 9070 | Jul–Aug 2024 | Sep 2024–Mar 2025 | Apr 2025–Jan 2026 |
| RX 9070 XT | Jul–Aug 2024 | Sep 2024–Mar 2025 | Apr 2025–Jan 2026 |

These ranges are classifications of visual support, not extracted prices or ground truth. In particular, a black line at the bottom is treated as ambiguous when it could be the chart baseline, missing history, or a transition into supported history.

## Policy application

The result follows the existing policy: clearly supported segments may be considered in a supervised pilot; ambiguous or disconnected months must remain `N/A` with review reasons; outside-history months must remain `N/A` with an out-of-history reason. No smoothing, carry-forward, interpolation, or extrapolation is justified by these images.

## Artifacts and validation

The machine-readable month classifications are in `STEP24_QUEUE_B_HISTORY_REVIEW_MANIFEST.json`. No new annotated overlay was generated because no Queue B overlay existed to extend and no accepted monthly price points were produced in this review. Previous Step 21–23 artifacts and the Step 19 pilot output were preserved.

No code or tests were changed. No extraction run was performed. RX 7600 XT remains separate and blocked.

## Recommendation

Do not start a six-GPU price pilot yet. The single next action is to create a supervised month-level calibration review for the 38 ambiguous/disconnected positions, with an explicit human decision for each; the 12 outside-history positions should remain `N/A`.

