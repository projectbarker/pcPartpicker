# August–September 2026 Full GPU Review

This is an experimental candidate package. It does not modify production data and no candidate is fully verified until human review of the native chart and diagnostics is complete.

## Asset validation

All 23 manifest assets were present, SHA-256 matched, and loaded as native PNGs at 1176×484.

## Extraction

The existing coordinate calibration and black-line sampler were used. The existing verified horizontal-gridline override `[27, 94, 161, 227, 294, 361, 427]` was used where automatic detection returned six lines; no threshold or production code was changed.

Summary: {"estimated_count": 33, "gpu_count": 23, "human_verification_complete": false, "na_count": 10, "numeric_count": 36, "observed_count": 3, "pilot_comparison_positions": 6, "pilot_discrepancy_count": 0, "position_count": 46, "review_required_count": 46}

## Per-GPU review status

| GPU | Aug candidate | Sep candidate | Numeric/2 | N/A/2 | Overlay | Diagnostic |
|---|---:|---:|---:|---:|---|---|
| Arc A380 | 200.00 (observed) | 206.00 (estimated) | 2 | 0 | `experimental\aug_sep_2026_full_review_20261022\arc_a380.overlay.png` | `experimental\aug_sep_2026_full_review_20261022\arc_a380.diagnostic.json` |
| Arc A750 | 293.00 (estimated) | 294.00 (estimated) | 2 | 0 | `experimental\aug_sep_2026_full_review_20261022\arc_a750.overlay.png` | `experimental\aug_sep_2026_full_review_20261022\arc_a750.diagnostic.json` |
| Arc A770 | 240.00 (estimated) | 255.00 (estimated) | 2 | 0 | `experimental\aug_sep_2026_full_review_20261022\arc_a770.overlay.png` | `experimental\aug_sep_2026_full_review_20261022\arc_a770.diagnostic.json` |
| GeForce RTX 4070 | 648.00 (estimated) | 648.00 (estimated) | 2 | 0 | `experimental\aug_sep_2026_full_review_20261022\geforce_rtx_4070.overlay.png` | `experimental\aug_sep_2026_full_review_20261022\geforce_rtx_4070.diagnostic.json` |
| GeForce RTX 4070 SUPER | 633.00 (estimated) | 688.00 (estimated) | 2 | 0 | `experimental\aug_sep_2026_full_review_20261022\geforce_rtx_4070_super.overlay.png` | `experimental\aug_sep_2026_full_review_20261022\geforce_rtx_4070_super.diagnostic.json` |
| GeForce RTX 4070 Ti | N/A (N/A) | N/A (N/A) | 0 | 2 | `experimental\aug_sep_2026_full_review_20261022\geforce_rtx_4070_ti.overlay.png` | `experimental\aug_sep_2026_full_review_20261022\geforce_rtx_4070_ti.diagnostic.json` |
| GeForce RTX 4070 Ti SUPER | N/A (N/A) | N/A (N/A) | 0 | 2 | `experimental\aug_sep_2026_full_review_20261022\geforce_rtx_4070_ti_super.overlay.png` | `experimental\aug_sep_2026_full_review_20261022\geforce_rtx_4070_ti_super.diagnostic.json` |
| GeForce RTX 4080 | 1545.00 (estimated) | 1545.00 (estimated) | 2 | 0 | `experimental\aug_sep_2026_full_review_20261022\geforce_rtx_4080.overlay.png` | `experimental\aug_sep_2026_full_review_20261022\geforce_rtx_4080.diagnostic.json` |
| GeForce RTX 4080 SUPER | 1198.00 (estimated) | 1198.00 (estimated) | 2 | 0 | `experimental\aug_sep_2026_full_review_20261022\geforce_rtx_4080_super.overlay.png` | `experimental\aug_sep_2026_full_review_20261022\geforce_rtx_4080_super.diagnostic.json` |
| GeForce RTX 4090 | N/A (N/A) | N/A (N/A) | 0 | 2 | `experimental\aug_sep_2026_full_review_20261022\geforce_rtx_4090.overlay.png` | `experimental\aug_sep_2026_full_review_20261022\geforce_rtx_4090.diagnostic.json` |
| GeForce RTX 5060 Ti | 648.00 (estimated) | 748.00 (estimated) | 2 | 0 | `experimental\aug_sep_2026_full_review_20261022\geforce_rtx_5060_ti.overlay.png` | `experimental\aug_sep_2026_full_review_20261022\geforce_rtx_5060_ti.diagnostic.json` |
| GeForce RTX 5070 | 856.00 (estimated) | 1000.00 (observed) | 2 | 0 | `experimental\aug_sep_2026_full_review_20261022\geforce_rtx_5070.overlay.png` | `experimental\aug_sep_2026_full_review_20261022\geforce_rtx_5070.diagnostic.json` |
| GeForce RTX 5070 Ti | 608.00 (estimated) | 668.00 (estimated) | 2 | 0 | `experimental\aug_sep_2026_full_review_20261022\geforce_rtx_5070_ti.overlay.png` | `experimental\aug_sep_2026_full_review_20261022\geforce_rtx_5070_ti.diagnostic.json` |
| GeForce RTX 5080 | 1750.00 (estimated) | 1894.00 (estimated) | 2 | 0 | `experimental\aug_sep_2026_full_review_20261022\geforce_rtx_5080.overlay.png` | `experimental\aug_sep_2026_full_review_20261022\geforce_rtx_5080.diagnostic.json` |
| GeForce RTX 5090 | 4284.00 (estimated) | 4537.00 (estimated) | 2 | 0 | `experimental\aug_sep_2026_full_review_20261022\geforce_rtx_5090.overlay.png` | `experimental\aug_sep_2026_full_review_20261022\geforce_rtx_5090.diagnostic.json` |
| Radeon RX 7600 XT | 761.00 (estimated) | N/A (N/A) | 1 | 1 | `experimental\aug_sep_2026_full_review_20261022\radeon_rx_7600_xt.overlay.png` | `experimental\aug_sep_2026_full_review_20261022\radeon_rx_7600_xt.diagnostic.json` |
| Radeon RX 7700 XT | 499.00 (estimated) | 567.00 (estimated) | 2 | 0 | `experimental\aug_sep_2026_full_review_20261022\radeon_rx_7700_xt.overlay.png` | `experimental\aug_sep_2026_full_review_20261022\radeon_rx_7700_xt.diagnostic.json` |
| Radeon RX 7800 XT | N/A (N/A) | N/A (N/A) | 0 | 2 | `experimental\aug_sep_2026_full_review_20261022\radeon_rx_7800_xt.overlay.png` | `experimental\aug_sep_2026_full_review_20261022\radeon_rx_7800_xt.diagnostic.json` |
| Radeon RX 7900 XT | 871.00 (estimated) | 943.00 (estimated) | 2 | 0 | `experimental\aug_sep_2026_full_review_20261022\radeon_rx_7900_xt.overlay.png` | `experimental\aug_sep_2026_full_review_20261022\radeon_rx_7900_xt.diagnostic.json` |
| Radeon RX 7900 XTX | 928.00 (estimated) | N/A (N/A) | 1 | 1 | `experimental\aug_sep_2026_full_review_20261022\radeon_rx_7900_xtx.overlay.png` | `experimental\aug_sep_2026_full_review_20261022\radeon_rx_7900_xtx.diagnostic.json` |
| Radeon RX 9060 XT | 549.00 (estimated) | 600.00 (observed) | 2 | 0 | `experimental\aug_sep_2026_full_review_20261022\radeon_rx_9060_xt.overlay.png` | `experimental\aug_sep_2026_full_review_20261022\radeon_rx_9060_xt.diagnostic.json` |
| Radeon RX 9070 | 827.00 (estimated) | 845.00 (estimated) | 2 | 0 | `experimental\aug_sep_2026_full_review_20261022\radeon_rx_9070.overlay.png` | `experimental\aug_sep_2026_full_review_20261022\radeon_rx_9070.diagnostic.json` |
| Radeon RX 9070 XT | 712.00 (estimated) | 770.00 (estimated) | 2 | 0 | `experimental\aug_sep_2026_full_review_20261022\radeon_rx_9070_xt.overlay.png` | `experimental\aug_sep_2026_full_review_20261022\radeon_rx_9070_xt.diagnostic.json` |

## Pilot comparison

The three saved pilot GPUs were compared at six positions; discrepancies: 0.

## Review status

All 46 GPU-month candidates remain review-required. Values marked observed or estimated are algorithmic classifications, not independent human verification. N/A values remain N/A and are not interpolated. `manual_review_queue.json` contains the complete position-level queue, including source hashes and pixel coordinates.
