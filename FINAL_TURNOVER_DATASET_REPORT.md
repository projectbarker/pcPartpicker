# PCPartPicker GPU Data Retrieval Turnover — Final Execution Report

**Date:** 2026-10-19  
**Scope:** All 23 input GPUs; July 2024 through January 2026; 19 monthly keys per record.

## Dataset produced

The consolidated dataset is:

[Monthly_Scraped_Data/pcpartpicker_gpu_trends_turnover_dataset.json](Monthly_Scraped_Data/pcpartpicker_gpu_trends_turnover_dataset.json)

It contains all 23 unique input GPU models and exactly 19 monthly keys per record. It was written through the existing atomic `backup_and_write` path to a new filename, so the frozen Step 9 and Step 19 outputs were not overwritten.

This is a structurally complete turnover dataset, not a fully numerically complete dataset: 16 records reuse verified supervised pilot results, while 7 records are explicit calibration failures with all monthly values set to `N/A`.

SHA-256: `7a8d47ee70746a029f6bd9892e9cba9e2a2845926109873dd9ea5bc9459a3b44`

## Execution matrix

| GPU | Source image | Calibration evidence | Existing pilot | Final handling |
|---|---|---|---|---|
| Arc A380 | Local/retrieved | Step 9 passed | Yes | Reused Step 9 |
| Arc A750 | Local/retrieved | Step 9 passed | Yes | Reused Step 9 |
| Arc A770 | Local/retrieved | Step 18 verified | Yes, Step 19 | Reused Step 19 |
| GeForce RTX 4070 | Local/retrieved | Step 9 passed | Yes | Reused Step 9 |
| GeForce RTX 4070 SUPER | Local/retrieved | Step 18 verified | Yes, Step 19 | Reused Step 19 |
| GeForce RTX 4070 Ti | Local/retrieved | Step 18 verified | Yes, Step 19 | Reused Step 19 |
| GeForce RTX 4070 Ti SUPER | Local/retrieved | Step 22 boundary accepted; runner geometry still detects 6 lines | No | Calibration failed; 19 `N/A` |
| GeForce RTX 4080 | Local/retrieved | Step 9 passed | Yes | Reused Step 9 |
| GeForce RTX 4080 SUPER | Local/retrieved | Step 18 verified | Yes, Step 19 | Reused Step 19 |
| GeForce RTX 4090 | Local/retrieved | Step 9 passed | Yes | Reused Step 9 |
| GeForce RTX 5060 Ti | Local/retrieved | Step 22 boundary accepted; runner geometry still detects 6 lines | No | Calibration failed; 19 `N/A` |
| GeForce RTX 5070 | Local/retrieved | Step 18 verified | Yes, Step 19 | Reused Step 19 |
| GeForce RTX 5070 Ti | Local/retrieved | Step 22 boundary accepted; runner geometry still detects 6 lines | No | Calibration failed; 19 `N/A` |
| GeForce RTX 5080 | Local/retrieved | Step 18 verified | Yes, Step 19 | Reused Step 19 |
| GeForce RTX 5090 | Local/retrieved | Step 9 passed | Yes | Reused Step 9 |
| Radeon RX 7600 XT | Local/retrieved | Blocked; six detected horizontal lines | No | Calibration failed; 19 `N/A` |
| Radeon RX 7700 XT | Local/retrieved | Step 18 verified | Yes, Step 19 | Reused Step 19 |
| Radeon RX 7800 XT | Local/retrieved | Step 18 verified | Yes, Step 19 | Reused Step 19 |
| Radeon RX 7900 XT | Local/retrieved | Step 18 verified | Yes, Step 19 | Reused Step 19 |
| Radeon RX 7900 XTX | Local/retrieved | Step 9 passed | Yes | Reused Step 9 |
| Radeon RX 9060 XT | Local/retrieved | Step 22 boundary accepted; runner geometry still detects 6 lines | No | Calibration failed; 19 `N/A` |
| Radeon RX 9070 | Local/retrieved | Step 22 boundary accepted; runner geometry still detects 6 lines | No | Calibration failed; 19 `N/A` |
| Radeon RX 9070 XT | Local/retrieved | Step 22 boundary accepted; runner geometry still detects 6 lines | No | Calibration failed; 19 `N/A` |

## Dataset-wide validation

| Measure | Result |
|---|---:|
| Expected GPU records | 23 |
| Actual records | 23 |
| Unique model names | 23 |
| Monthly keys per record | 19 for every record |
| Numeric monthly values | 245 |
| `N/A` monthly values | 192 |
| `observed` values | 21 |
| `estimated` values | 224 |
| Records with `needs_review` | 16 |
| Records with `failed` status | 7 |
| Records with missing model/month keys | 0 |

All records contain `gpu_model_name`, `image_url`, `price_trend`, `price_quality`, `review_required`, `review_reasons`, and `extraction_status`. Failed records also contain calibration failure stage/reason and `extraction_skipped: true`. No blocked record contains numeric monthly prices.

## Execution evidence and blocker

The unchanged coordinate runner was invoked against the full 23-record input with a new output and diagnostics path. The environment could not reach the recorded PCPartPicker CDN URLs, so the attempted fresh run recorded `image_validation_failed` for the 16 eligible records. It did not create numeric values from that attempt. The 7 records without pipeline-compatible calibration were isolated before image processing.

The final dataset therefore reuses the already verified Step 9 and Step 19 pilot outputs for the 16 eligible GPUs rather than repeating completed extraction work. This is auditable and preserves the earlier pilot artifacts.

For the six Queue B GPUs, the manually accepted y=427 boundary is not enough for the unchanged runner: its detector still returns six horizontal gridlines and `calibrate_chart` raises `ValueError: Expected 7 horizontal gridlines, detected 6`. RX 7600 XT has the same unresolved calibration failure and remains isolated.

## Tests

```text
python -m unittest tests.test_coordinate_calibration tests.test_coordinate_calibration_runner -v
Ran 22 tests
OK
```

The final JSON was independently checked for 23 records, unique models, 19 monthly keys, required metadata, and the stated numeric/`N/A` totals.

## Final status

The original produced file is structurally complete for all 23 GPUs, but the baseline price deliverable was not complete: 16 GPUs had supervised pilot values and 7 were blocked with explicit `N/A` values. No policy, threshold, estimate quality, or historical output was changed to improve coverage.

## Targeted seven-GPU blocker attempt

On 2026-10-19, one focused local-artifact attempt used the manually validated Step 23 geometries for the six Queue B charts. The attempt instantiated the existing `Calibration` object from the evidence-backed coordinates and then called the existing `extract_calibrated_prices` and overlay functions. No detector threshold or production code was changed. RX 7600 XT was intentionally not bypassed because its bottom boundary remains unapproved.

New candidate output:

`Monthly_Scraped_Data/pcpartpicker_gpu_trends_turnover_blocker_attempt.json`

New diagnostics and overlays:

`diagnostics/turnover_blocker_attempt/`

| Measure | Targeted-attempt result |
|---|---:|
| Records | 23 |
| Queue B GPUs processed | 6 |
| RX 7600 XT blocked | 1 |
| Numeric monthly values | 307 |
| `N/A` monthly values | 130 |
| `observed` values | 25 |
| `estimated` values | 282 |
| `needs_review` records | 22 |
| `failed` records | 1 |

All six Queue B records produced 19 monthly keys and retained review metadata. Unsupported and ambiguous months remain `N/A`. RX 7600 XT remains failed with `ValueError: Expected 7 horizontal gridlines, detected 6`.

The original turnover dataset at `Monthly_Scraped_Data/pcpartpicker_gpu_trends_turnover_dataset.json` remains unchanged. Step 9 and Step 19 pilot artifacts also remain unchanged. The new candidate output SHA-256 is `71db952dd497189c15ad2e73376c39941baf298620832518087086ff8f1c92c9`.

The relevant calibration and runner tests were rerun: 22 tests passed. This attempt reduces the remaining blocker count from seven to one, but the candidate output still requires review before replacing the baseline turnover dataset.

**Single remaining action:** resolve RX 7600 XT's calibration failure through a separately reviewed evidence-based calibration path, then process only that GPU into a new validated output.

## Final integration

The six successful recovery records were integrated into a new final file:

`Monthly_Scraped_Data/pcpartpicker_gpu_trends_final.json`

Only the six named recovery records replaced their prior zero-numeric calibration-failure records. RX 7600 XT was retained from the consolidated baseline as failed with 19 `N/A` values. The final integrated counts are:

| Metric | Final integrated result |
|---|---:|
| GPU records | 23 |
| Monthly fields per record | 19 |
| Total monthly positions | 437 |
| Numeric values | 307 |
| `N/A` values | 130 |
| `observed` values | 25 |
| `estimated` values | 282 |
| `needs_review` records | 22 |
| `failed` records | 1 |

The final file passed validation for unique models, exact month keys, metadata presence, count reconciliation, and RX 7600 XT failure isolation. Its SHA-256 is `71db952dd497189c15ad2e73376c39941baf298620832518087086ff8f1c92c9`.

The original consolidated dataset and recovery output hashes remain unchanged (`7a8d47ee70746a029f6bd9892e9cba9e2a2845926109873dd9ea5bc9459a3b44` and `71db952dd497189c15ad2e73376c39941baf298620832518087086ff8f1c92c9` respectively as recorded during integration); Step 9 and Step 19 historical artifacts were not modified.

The remaining limitation is Radeon RX 7600 XT: its calibration still fails with `ValueError: Expected 7 horizontal gridlines, detected 6`. The final integrated dataset is therefore structurally complete but not fully numerically complete.

