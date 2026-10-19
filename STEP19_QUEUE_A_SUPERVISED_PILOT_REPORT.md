# Step 19 — Queue A Supervised Nine-GPU Pilot Report

**Date:** 2026-10-19  
**Scope:** Separate supervised pilot for the nine Queue A GPUs with Step 18 `calibration_verified` geometry.

## Verdict

The pilot completed safely using the existing `coordinate_calibration_runner.py` and separate Step 19 paths:

- Records processed: **9**.
- `success`: **0**.
- `partial`: **0**.
- `needs_review`: **9**.
- `failed`: **0**.
- Numeric monthly values: **137**.
- `N/A` monthly values: **34**.
- Estimated values: **126**.
- Observed values: **11**.

The nine-GPU output is suitable for human review, not production use. Every record retained review metadata, and no record was marked successful. The full 23-GPU batch remains unapproved.

## Preflight and execution

The Step 18 manifest and all nine per-GPU artifacts were checked before execution:

- Exact model names, source URLs, and local source-image paths matched.
- Each Step 18 artifact reported `calibration_verified`.
- All coordinates were within 1176×484 bounds.
- Seven horizontal gridlines, monotonic y-ticks, and the October 2024 anchor were validated.
- The existing runner contract was verified: it consumes a model-keyed raw calibration map and fetches each exact `image_url` with `requests`.
- The Step 18 rich artifacts were translated into `step19_queue_a_pilot_calibration.json` without changing production code.
- The new output path did not exist before execution and is distinct from the frozen Step 9 output.
- The coordinate runner does not call OpenAI; no external extraction API or OCR was used.

Command executed:

```powershell
& .\.venv\Scripts\python.exe coordinate_calibration_runner.py `
  --input step19_queue_a_pilot_input.json `
  --calibration step19_queue_a_pilot_calibration.json `
  --output Monthly_Scraped_Data/pcpartpicker_gpu_trends_step19_queue_a_pilot.json `
  --artifact-dir diagnostics/step19_queue_a_pilot
```

Runner result:

```json
{"records":9,"statuses":{"success":0,"partial":0,"needs_review":9,"failed":0}}
```

The runner fetched the exact recorded URLs during execution. It does not consume local image paths directly; the local Step 17 paths remain the source-evidence references in the manifest. The generated calibration JSON matched the Step 18 geometry for all nine records. The runner does not retain response hashes, so byte identity between the earlier local files and the live response was not independently hashed in this run.

## Per-GPU results

| GPU | Numeric | `N/A` | Estimated | Observed | Status | Review reasons |
|---|---:|---:|---:|---:|---|---|
| Arc A770 | 16 | 3 | 14 | 2 | `needs_review` | `estimated_values_present`, `isolated_spike`, `outside_visible_history` |
| GeForce RTX 4070 SUPER | 16 | 3 | 16 | 0 | `needs_review` | `estimated_values_present`, `isolated_spike`, `outside_visible_history` |
| GeForce RTX 4070 Ti | 15 | 4 | 10 | 5 | `needs_review` | `estimated_values_present`, `missing_line_segment`, `outside_visible_history` |
| GeForce RTX 4080 SUPER | 16 | 3 | 16 | 0 | `needs_review` | `estimated_values_present`, `isolated_spike`, `outside_visible_history` |
| GeForce RTX 5070 | 11 | 8 | 11 | 0 | `needs_review` | `estimated_values_present`, `isolated_spike`, `missing_line_segment`, `outside_visible_history` |
| GeForce RTX 5080 | 12 | 7 | 12 | 0 | `needs_review` | `estimated_values_present`, `missing_line_segment`, `outside_visible_history` |
| Radeon RX 7700 XT | 17 | 2 | 17 | 0 | `needs_review` | `estimated_values_present`, `outside_visible_history` |
| Radeon RX 7800 XT | 17 | 2 | 15 | 2 | `needs_review` | `estimated_values_present`, `outside_visible_history` |
| Radeon RX 7900 XT | 17 | 2 | 15 | 2 | `needs_review` | `estimated_values_present`, `outside_visible_history` |
| **Total** | **137** | **34** | **126** | **11** | **9 `needs_review`** | **No failures** |

Every record contains all 19 expected month keys. No duplicate or malformed month keys were found. All numeric values use the existing two-decimal string format, and all quality values are within `observed`, `estimated`, or `N/A`.

## Missing-month and review observations

- Arc A770: July–September 2024 remain `N/A`; one later isolated spike is rejected.
- RTX 4070 SUPER: July–August 2024 and October 2025 remain `N/A`; the late candidate is conservatively rejected.
- RTX 4070 Ti: July–August 2024 and November 2025–January 2026 remain `N/A` due outside history or missing line support.
- RTX 4080 SUPER: July–August 2024 and October 2025 remain `N/A`; the late spike is rejected.
- RTX 5070: July 2024–February 2025 remain `N/A`; additional line-support rejection is retained.
- RTX 5080: July–December 2024 remain `N/A`; January 2025 is also unsupported by the visible line.
- RX 7700 XT: July–August 2024 remain `N/A`.
- RX 7800 XT: July–August 2024 remain `N/A`.
- RX 7900 XT: July–August 2024 remain `N/A`.

These missing values were not filled or interpolated. The output’s `review_reasons` preserve the distinction between outside visible history, missing line segments, and isolated spikes.

## Overlay and diagnostic audit

The runner generated one overlay and one calibration/diagnostic JSON file per GPU under `diagnostics/step19_queue_a_pilot/`. All nine overlays were opened and reviewed. Accepted green markers generally follow the black actual-price line at the mapped monthly gridlines. Orange rejection markers appear where the continuity sampler identifies an isolated spike. The overlays also make the early out-of-history regions and line-support gaps visible.

Generated files:

- Output: `Monthly_Scraped_Data/pcpartpicker_gpu_trends_step19_queue_a_pilot.json`.
- Diagnostics and overlays: `diagnostics/step19_queue_a_pilot/`.
- Input: `step19_queue_a_pilot_input.json`.
- Calibration input: `step19_queue_a_pilot_calibration.json`.
- Run manifest: `STEP19_QUEUE_A_PILOT_MANIFEST.json`.

## Tests and integrity checks

No production or test code changed. The existing targeted calibration tests were run after the pilot:

```powershell
& .\.venv\Scripts\python.exe -m unittest tests.test_coordinate_calibration -v
```

Result: **16 tests passed, 0 failures**.

Additional read-only checks found:

- 9 output records and 9 unique GPU models.
- 19 monthly keys on every record.
- 0 malformed price strings.
- 0 invalid quality values.
- 0 missing required output fields.
- 9 generated overlays and 9 generated diagnostic JSON files.
- Generated calibration geometry matched all Step 18 artifacts.
- Frozen Step 9 output SHA-256 remained `C5E7D53A1C0A29EDFD2C9405214F4C2592724BDD4E4C25E4DEF71524457AB20A`.

## Limitations and blockers

- The pilot uses the existing line sampler and therefore does not resolve the previously documented monthly-boundary business ambiguity.
- All nine records require human review; calibration verification does not make monthly values trusted.
- Several charts have missing or late-starting history, correctly retained as `N/A`.
- The runner fetched the exact URLs rather than reading local paths directly; response-byte hashes were not retained by the runner.
- Queue B and Radeon RX 7600 XT were not processed.
- The full 23-GPU batch remains unapproved and the overall dataset is not complete.

## Final status and next action

The nine-GPU output is suitable for a human audit of overlays, numeric estimates, and `N/A` classifications. It is not suitable for unattended or production use.

**Single next action:** perform human review of the nine Step 19 overlays and per-month diagnostics, beginning with the records containing isolated spikes or missing-line reasons, before approving any further pilot or broader processing. Do not run Queue B, RX 7600 XT, or the full 23-GPU batch yet.

