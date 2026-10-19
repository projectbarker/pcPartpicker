# Step 9 — Supervised Seven-GPU Coordinate-Extraction Pilot

Assessment date: 2026-10-17

## Scope and controls

This was an experimental pilot limited to the seven records marked `ready_for_controlled_pilot` in `CALIBRATION_READINESS_INVENTORY.json`:

- Arc A380
- Arc A750
- GeForce RTX 4070
- GeForce RTX 4080
- GeForce RTX 4090
- GeForce RTX 5090
- Radeon RX 7900 XTX

The 15 `manual_calibration_required` records and blocked Radeon RX 7600 XT were excluded. No scraper, OpenAI API, OCR, or full 23-GPU batch was run. Existing outputs and diagnostics were not overwritten.

The pilot used the existing `process_record()` coordinate-calibration path. Because the approved source images were local evidence artifacts, a test-only local-image adapter supplied those PNG bytes to the existing request boundary; the extraction and calibration functions were not changed. This avoided live image retrieval and preserved the original source URLs in the output.

## Frozen configuration

The configuration was recorded before extraction in:

- `STEP9_PILOT_MANIFEST.json`
- `step9_pilot_input.json`
- `step9_pilot_calibration.json`

All seven source images were verified as 1176×484 PNGs. The manifest records their local paths, URL, SHA-256 prefix, date anchor (`2024-10-01`), anchor x (`113`), and manually supplied top-to-bottom USD tick mappings. The working tree had no available Git revision, so the manifest records that limitation.

## Pilot artifacts

- Output: `Monthly_Scraped_Data/pcpartpicker_gpu_trends_step9_seven_gpu_pilot.json`
- Overlays and per-record diagnostic JSON: `diagnostics/step9_seven_gpu_pilot/`
- Frozen manifest: `STEP9_PILOT_MANIFEST.json`
- Frozen input: `step9_pilot_input.json`
- Frozen calibration: `step9_pilot_calibration.json`
- Reproducible local-only harness: `step9_run_pilot.py`

## Coverage and status

| GPU | Numeric | `N/A` | Status | Review reasons |
|---|---:|---:|---|---|
| Arc A380 | 17 | 2 | `needs_review` | `estimated_values_present`, `outside_visible_history` |
| Arc A750 | 16 | 3 | `needs_review` | `estimated_values_present`, `missing_line_segment`, `outside_visible_history` |
| GeForce RTX 4070 | 17 | 2 | `needs_review` | `estimated_values_present`, `outside_visible_history` |
| GeForce RTX 4080 | 16 | 3 | `needs_review` | `estimated_values_present`, `isolated_spike`, `outside_visible_history` |
| GeForce RTX 4090 | 13 | 6 | `needs_review` | `estimated_values_present`, `isolated_spike`, `missing_line_segment`, `outside_visible_history` |
| GeForce RTX 5090 | 12 | 7 | `needs_review` | `estimated_values_present`, `missing_line_segment`, `outside_visible_history` |
| Radeon RX 7900 XTX | 17 | 2 | `needs_review` | `estimated_values_present`, `outside_visible_history` |
| **Total** | **108** | **25** | **7 `needs_review`** | **0 failed; 0 success** |

All seven output records contain the expected 19 monthly keys. No record was marked `success`; every record retains review metadata.

## Overlay and diagnostic review

All seven Step 9 overlays were opened and reviewed across the full 19-month sampling sequence. Green accepted markers generally sit on the black actual-price line at the detected monthly positions. Blue horizontal gridlines, green monthly x-gridlines, and the magenta plot boundary are consistently aligned with the 1176×484 chart layout. Orange markers identify rejected spike candidates where applicable; months with no accepted marker remain `N/A`.

### Arc A380

The 17 accepted points follow the black line through the visible September 2024–January 2026 history. July and August 2024 remain out of visible history. The March–May 2025 rise and December 2025 drop are visually steep but the selected points remain attached to the line. No spike or ambiguity rejection was reported.

### Arc A750

The accepted markers follow the mostly low, gradually rising black line. September 2024 has no supported candidate and remains `N/A` with `missing_line_segment`; July and August are outside history. The May–June 2025 rise is visible and accepted. No ambiguity candidate was reported.

### GeForce RTX 4070

The line is relatively flat around the $580–$650 range after the visible start. Seventeen points were accepted, with July and August 2024 correctly outside visible history. The late flat section is mapped to the upper-$600 region without spike or missing-line flags. This is the cleanest pilot chart, but estimated-value review remains required.

### GeForce RTX 4080

The accepted points track the black line after the early history. September 2024 is rejected as `isolated_spike` rather than converted into a numeric value; July and August are outside history. The early line contains abrupt changes and the overlay shows the rejection at the left edge. No ambiguity candidate was reported.

### GeForce RTX 4090

This remains the highest-risk pilot chart. Thirteen points are accepted through September 2025. October 2025 is rejected as `isolated_spike`, and November 2025 through January 2026 remain `N/A` with `missing_line_segment`. The overlay visibly shows tall vertical structures and disconnected late-2025 regions. Those months were not converted into numeric prices.

### GeForce RTX 5090

The chart begins later than the requested period. July 2024 through January 2025 remain `N/A` with `outside_visible_history` or `missing_line_segment`; numeric extraction begins in February 2025. The accepted points follow the rising and then easing black line through January 2026. No ambiguity candidate was reported, but the large y-axis grid interval makes visual precision coarse.

### Radeon RX 7900 XTX

Seventeen accepted points follow the black line through the visible history, including the spring 2025 rise and the late-2025 dip/recovery. July and August 2024 remain outside history. No spike, ambiguity, or missing-line rejection was reported.

## Approximate visual reference comparisons

These are independent visual readings from the reviewed chart/overlay images, not ground truth. Differences are descriptive only, and no universal accuracy threshold is being introduced. The relevant visible grid interval is included to show scale.

| GPU / month | Approx. visual reference | Pilot value | Absolute difference | Grid interval |
|---|---:|---:|---:|---:|
| Arc A380 / Sep 2024 | ~$145 | $146 | ~$1 | $50 |
| Arc A380 / May 2025 | ~$205 | $192 | ~$13 | $50 |
| Arc A380 / Nov 2025 | ~$160 | $168 | ~$8 | $50 |
| Arc A750 / Oct 2024 | ~$245 | $242 | ~$3 | $100 |
| Arc A750 / Jun 2025 | ~$315 | $317 | ~$2 | $100 |
| Arc A750 / Nov 2025 | ~$300 | $300 | ~$0 | $100 |
| RTX 4070 / Oct 2024 | ~$615 | $615 | ~$0 | $200 |
| RTX 4070 / Jun 2025 | ~$600 | $600 | ~$0 | $200 |
| RTX 4070 / Aug 2025 | ~$650 | $648 | ~$2 | $200 |
| RTX 4080 / Oct 2024 | ~$1,300 | $1,336 | ~$36 | $500 |
| RTX 4080 / Feb 2025 | ~$1,600 | $1,598 | ~$2 | $500 |
| RTX 4080 / Oct 2025 | ~$1,550 | $1,545 | ~$5 | $500 |
| RTX 4090 / Sep 2024 | ~$2,100 | $2,194 | ~$94 | $1,000 |
| RTX 4090 / Jun 2025 | ~$1,800 | $2,075 | ~$275 | $1,000 |
| RTX 4090 / Oct 2025 | ~$1,000 | `N/A` | Not applicable | $1,000 |
| RTX 5090 / Mar 2025 | ~$2,700 | $2,687 | ~$13 | $1,000 |
| RTX 5090 / Jun 2025 | ~$3,250 | $3,258 | ~$8 | $1,000 |
| RTX 5090 / Dec 2025 | ~$2,850 | $2,851 | ~$1 | $1,000 |
| RX 7900 XTX / Sep 2024 | ~$1,000 | $1,026 | ~$26 | $250 |
| RX 7900 XTX / Mar 2025 | ~$1,150 | $1,146 | ~$4 | $250 |
| RX 7900 XTX / Dec 2025 | ~$900 | $890 | ~$10 | $250 |

The RTX 4090 comparison demonstrates why agreement within a coarse grid interval is not sufficient evidence of accuracy: the June difference is approximately $275 despite being below the $1,000 grid interval. This remains a review concern, not a newly adopted threshold.

## Tests and commands

Pilot command (local-image adapter invoking the existing runner function):

```powershell
& .\\.venv\\Scripts\\python.exe step9_run_pilot.py
```

Actual pilot result: 7 records, 7 `needs_review`, 0 `success`, 0 `partial`, 0 `failed`; 108 numeric monthly values and 25 `N/A` values. The harness reads only the seven frozen local PNG paths and does not make network or API calls.

Targeted and full regression tests:

```powershell
& .\\.venv\\Scripts\\python.exe -m unittest tests.test_coordinate_calibration_runner tests.test_pipeline -v
& .\\.venv\\Scripts\\python.exe -m unittest discover -s tests -v
```

Result: **22 targeted tests passed** and **38 full-suite tests passed**, with 0 failures.

## Eligibility and limitations

All seven records remain eligible for another supervised pilot, subject to human review of their overlays and `N/A` classifications. None is approved for unattended or production extraction.

Remaining limitations:

- Tick values and date anchor remain manually supplied; OCR/date recognition is not implemented.
- The visual comparisons are approximate and not ground truth.
- The RTX 4090 late-2025 region remains unresolved and should stay `N/A` where the sampler reports no supported line.
- The pilot used verified local copies rather than live URL retrieval, so current remote-image accessibility was not tested.
- No business accuracy threshold was invented or applied.

## Recommendation

Continue controlled validation only. The pilot demonstrates safe calibration and conservative handling of spikes, missing history, and review flags across seven charts, but it does not establish production readiness. The next decision should be human review of the Step 9 overlays and visual-reference table before any expansion beyond these seven records.
