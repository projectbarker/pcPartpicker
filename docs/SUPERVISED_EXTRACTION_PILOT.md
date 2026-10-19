# Supervised Extraction Pilot

## Purpose

The pilot artifacts demonstrate how chart calibration and line selection were evaluated before final integration. They are evidence for the final dataset, not a claim that every raster reading is exact.

## Step 9 and Step 19 results

The original seven-GPU pilot used the approved controlled records and preserved the RTX 4090 late-2025 review region. The nine-GPU Queue A pilot then used manually verified geometry and produced 19 monthly keys per record while retaining estimated, ambiguous, and missing classifications. Value-level review confirmed that estimated readings still require human confirmation and that unsupported positions remain `N/A`.

The Queue B calibration work reviewed six charts and accepted an evidence-backed bottom boundary for a focused recovery attempt. The unchanged runner still rejected those charts when its automatic gridline detector reported six lines, so the recovery used explicit manually verified calibration artifacts without changing global thresholds. Six records were processed into a separate candidate output and later integrated into the final dataset. Radeon RX 7600 XT was excluded because its boundary remained unapproved.

## Review conclusions

- Direct vision alone was unreliable on the first three-GPU sample.
- Coordinate calibration improved consistency and made selections inspectable through overlays.
- Vertical spikes, steep transitions, disconnected segments, and ambiguous candidates remain review cases.
- The current sampler is retained; post-boundary stability remains diagnostic-only.
- Manual visual readings are approximate references, not ground truth or a universal accuracy threshold.

## Reproducibility artifacts

Machine-readable pilot manifests and compact diagnostics are retained at the repository root and under `diagnostics/turnover_blocker_attempt/`. Frozen pilot outputs remain local historical artifacts and were not overwritten during final integration.
