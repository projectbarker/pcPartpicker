# Three-GPU Policy Sample Validation

Date: 2026-10-16

The complete 23-GPU batch was not run.

## Sample inputs

The sample used the exact records from `sample_input.json`:

- Arc A380
- GeForce RTX 4090
- Radeon RX 7900 XTX

Each image returned HTTP 200 and was accepted as a PNG before its OpenAI request. Raw model JSON responses are preserved under `diagnostics/policy_sample/`. The normalized sample is `Monthly_Scraped_Data/pcpartpicker_gpu_trends_policy_sample_revalidated.json`.

## Automated sample results

| GPU | Numeric values | Missing values | Status | Review reason |
|---|---:|---:|---|---|
| Arc A380 | 0 | 19 | failed | outside_visible_history returned by model |
| GeForce RTX 4090 | 0 | 19 | failed | outside_visible_history returned by model |
| Radeon RX 7900 XTX | 19 | 0 | needs_review | suspicious_sequence |

The two `failed` records are not evidence that the charts lack history. Manual inspection shows visible black-line history. They demonstrate that the model can misinterpret a readable chart as having no history.

The Radeon response returned a complete numeric sequence, but it followed an artificial pattern of repeated 50-dollar changes. The post-parser heuristic correctly changed this from `success` to `needs_review`.

## Manual chart anchors

These are approximate visual readings from the chart raster, recorded as validation anchors rather than exact ground truth. The chart does not expose transaction-level values, and no business accuracy threshold has been assumed.

### Arc A380

| Position | Approximate manual reading | Machine result |
|---|---:|---|
| First visible month, Sep 2024 | ~$145 | N/A |
| Flat segment, Oct 2024 | ~$135 | N/A |
| Upward movement, Apr 2025 | ~$185 | N/A |
| High point, May 2025 | ~$205 | N/A |
| Downward movement, Nov 2025 | ~$160 | N/A |
| Ambiguous/missing segment | No distinct missing segment selected | N/A |

### GeForce RTX 4090

| Position | Approximate manual reading | Machine result |
|---|---:|---|
| First visible month, Sep 2024 | ~$2,100 | N/A |
| Flat segment, Oct 2024 | ~$1,950 | N/A |
| Spring 2025 baseline | ~$1,800 | N/A |
| Mid-2025 baseline | ~$1,800 | N/A |
| Late-2025 decline region | Visibly unstable; no single reliable anchor selected | N/A |
| Ambiguous/missing segment | Large spikes and drops require review | N/A |

### Radeon RX 7900 XTX

| Position | Approximate manual reading | Machine value | Absolute difference |
|---|---:|---:|---:|
| First visible month, Sep 2024 | ~$1,000 | $1,000 | ~$0 |
| Flat segment, Oct 2024 | ~$975 | $850 | ~$125 |
| Upward movement, Feb 2025 | ~$1,150 | $750 | ~$400 |
| Downward movement, Nov 2025 | ~$910 | $1,200 | ~$290 |
| Estimated/inter-gridline, Apr 2025 | ~$1,060 | $850 | ~$210 |
| Ambiguous/missing segment | No distinct missing segment selected | Not applicable | Not applicable |

The Radeon comparison is sufficient to show that a valid JSON response and visually plausible first value do not establish chart accuracy. Four of the five comparable anchors differ materially from the manual reading.

## Assessment

Direct image interpretation is not sufficient for production use in its current form. The sample showed:

- inconsistent date-history interpretation;
- a fabricated-looking uniform price sequence;
- no estimated values despite the approved estimation policy;
- no reliable per-month comparison for two charts;
- a need to verify the black line and coordinate mapping outside the language model.

The minimal coordinate-calibration prototype is now implemented and evaluated below. The vision model remains a fallback/reviewer and is no longer treated as the sole source of numeric values.

No accuracy threshold has been declared. Before implementation of coordinate calibration, the user should approve a validation criterion based on a larger manually read sample and the chart's visible y-axis spacing.

## Coordinate-calibration prototype results

The prototype used Pillow, not OpenCV or OCR. For each image it detected the horizontal and vertical gridlines independently. All three images produced plot bounds `(55, 27, 1149, 427)` and seven horizontal gridlines plus the monthly vertical gridline sequence. The y-axis tick values were supplied from the readable labels in the sample-specific calibration file:

- Arc A380: `$300` down to `$0` in `$50` increments.
- GeForce RTX 4090: `$6000` down to `$0` in `$1000` increments.
- Radeon RX 7900 XTX: `$1500` down to `$0` in `$250` increments.

The visible date anchor was `Oct 2024` at the detected gridline near x=113. July and August 2024 were correctly classified as outside visible history; the chart begins around September 2024.

| GPU | Numeric values | Missing values | Status | Review reasons |
|---|---:|---:|---|---|
| Arc A380 | 17 | 2 | needs_review | estimated values, outside history |
| GeForce RTX 4090 | 14 | 5 | needs_review | estimated values, missing line segment, outside history |
| Radeon RX 7900 XTX | 17 | 2 | needs_review | estimated values, outside history |

Coordinate-calibrated manual anchor comparisons:

| GPU | Manual anchor | Calibrated value | Approx. absolute difference |
|---|---:|---:|---:|
| Arc A380, Sep 2024 | ~$145 | $147 | ~$2 |
| Arc A380, Oct 2024 | ~$135 | $134 | ~$1 |
| Arc A380, Apr 2025 | ~$185 | $184 | ~$1 |
| Arc A380, May 2025 | ~$205 | $195 | ~$10 |
| Arc A380, Nov 2025 | ~$160 | $169 | ~$9 |
| GeForce RTX 4090, Sep 2024 | ~$2,100 | $2,239 | ~$139 |
| GeForce RTX 4090, Oct 2024 | ~$1,950 | $1,940 | ~$10 |
| GeForce RTX 4090, Mar 2025 | ~$1,800 | $1,821 | ~$21 |
| GeForce RTX 4090, Jun 2025 | ~$1,800 | $2,075 | ~$275 |
| GeForce RTX 4090, Oct 2025 | ~$1,000 | $742 | ~$258 |
| Radeon RX 7900 XTX, Sep 2024 | ~$1,000 | $1,000 | ~$0 |
| Radeon RX 7900 XTX, Oct 2024 | ~$975 | $1,019 | ~$44 |
| Radeon RX 7900 XTX, Mar 2025 | ~$1,150 | $1,160 | ~$10 |
| Radeon RX 7900 XTX, Apr 2025 | ~$1,060 | $1,075 | ~$15 |
| Radeon RX 7900 XTX, Dec 2025 | ~$900 | $890 | ~$10 |

These manual values remain approximate visual anchors; no business accuracy threshold has been assumed.

Diagnostic evidence is in `diagnostics/coordinate_sample/`. Each GPU has a calibration JSON file and an overlay PNG showing the detected magenta plot boundary, blue horizontal USD gridlines, green monthly gridlines, and red sampled black-line positions.

The coordinate prototype is materially better than direct vision, but it is not yet production-ready. RTX 4090 black spikes create ambiguous/missing samples, and y-axis tick values plus one date-label anchor are currently supplied in `sample_calibration.json` because OCR is not installed. The next improvement should be black-line continuity handling and automated y-axis/date-label recognition; OpenCV/OCR should only be added if Pillow plus explicit calibration metadata cannot scale safely.

Proposed acceptance criterion for review: on a larger manually labelled sample, every out-of-history and ambiguous month must be classified correctly, every accepted numeric point must fall within one visible y-axis grid interval of the manual reading, and no record may be `success` when any point requires review. This is a proposal, not an applied business threshold.

## Continuity-aware calibration results

Date: 2026-10-17. The full 23-GPU batch was not run.

The sampler was changed to inspect connected black-pixel components in a wider local x-window. It records horizontal support, vertical span, and candidate y positions. Thin isolated vertical components are marked as `isolated_spike`; multiple similarly supported candidates remain `N/A` with `ambiguous_line_candidate`. A candidate is accepted only with local component evidence and, where available, continuity with a neighboring accepted sample. No interpolation across a missing segment is performed.

The rerun used the same three images and manually supplied calibration values. It wrote a new output, `Monthly_Scraped_Data/pcpartpicker_gpu_trends_coordinate_continuity_sample.json`, and new overlays/calibration diagnostics under `diagnostics/coordinate_continuity_sample/`. The prior coordinate sample and all historical outputs were preserved.

| GPU | Before numeric/missing | After numeric/missing | After status | After review reasons |
|---|---:|---:|---|---|
| Arc A380 | 17 / 2 | 17 / 2 | needs_review | estimated values, outside history |
| GeForce RTX 4090 | 14 / 5 | 14 / 5 | needs_review | estimated values, missing line segment, outside history |
| Radeon RX 7900 XTX | 17 / 2 | 17 / 2 | needs_review | estimated values, outside history |

The unchanged coverage is expected: continuity handling changes point selection and rejection behavior, not chart history. It also preserves the two out-of-history months as `N/A`. The RTX overlay now exposes the long spike regions and missing-line decisions for review rather than silently averaging all dark rows.

### Before/after visual-reference comparisons

The following are approximate manual chart readings, not ground truth. Absolute differences are descriptive only; no new business accuracy threshold has been invented.

| GPU / month | Visual reference | Before coordinate value | After continuity value | After absolute difference |
|---|---:|---:|---:|---:|
| Arc A380 / Sep 2024 | ~$145 | $147 | $146 | ~$1 |
| Arc A380 / Oct 2024 | ~$135 | $134 | $135 | ~$0 |
| Arc A380 / Apr 2025 | ~$185 | $184 | $185 | ~$0 |
| Arc A380 / May 2025 | ~$205 | $195 | $192 | ~$13 |
| Arc A380 / Nov 2025 | ~$160 | $169 | $168 | ~$8 |
| RTX 4090 / Sep 2024 | ~$2,100 | $2,239 | $2,194 | ~$94 |
| RTX 4090 / Oct 2024 | ~$1,950 | $1,940 | $1,940 | ~$10 |
| RTX 4090 / Mar 2025 | ~$1,800 | $1,821 | $1,821 | ~$21 |
| RTX 4090 / Jun 2025 | ~$1,800 | $2,075 | $2,075 | ~$275 |
| RTX 4090 / Oct 2025 | ~$1,000 | $742 | $1,000 | ~$0 |
| Radeon / Sep 2024 | ~$1,000 | $1,000 | $1,026 | ~$26 |
| Radeon / Oct 2024 | ~$975 | $1,019 | $1,015 | ~$40 |
| Radeon / Mar 2025 | ~$1,150 | $1,160 | $1,146 | ~$4 |
| Radeon / Apr 2025 | ~$1,060 | $1,075 | $1,067 | ~$7 |
| Radeon / Dec 2025 | ~$900 | $890 | $890 | ~$10 |

Continuity corrected or materially improved several points, especially RTX October 2025, and reduced the Radeon March/April differences. It did not resolve all visually unstable regions: RTX June 2025 remains a large-spike review case, and Arc May/November remain approximate. These results support further review, not production readiness.

## Validation handover

- Test suite: 24 tests passed, including the existing pipeline tests and new deterministic continuity tests.
- Diagnostic evidence: each sample has a calibration JSON and overlay. Overlays show the magenta plot bounds, blue y-gridlines, green monthly x-gridlines, green accepted samples, and orange rejected vertical-spike candidates; ambiguous candidates are outlined yellow.
- Remaining limitations: date labels and USD tick values are still manually supplied; there is no OCR/date recognition; raster artifacts and thick/steep lines can still require human review.
- Next action: review the three continuity overlays and the visual-reference table, then approve or revise the proposed validation criterion before any consideration of the full batch.
