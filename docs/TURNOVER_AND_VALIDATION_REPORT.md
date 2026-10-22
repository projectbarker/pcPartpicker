# Turnover and Validation Report

## Final artifact

The published dataset is [`../Monthly_Scraped_Data/pcpartpicker_gpu_trends_final.json`](../Monthly_Scraped_Data/pcpartpicker_gpu_trends_final.json). The extended file contains 23 unique GPU records, 27 monthly keys per record, and 621 total positions.

| Measure | Result |
|---|---:|
| Numeric values | 404 |
| `N/A` values | 217 |
| `observed` values | 31 |
| `estimated` values | 373 |
| Records requiring review | 23 |
| Failed records | 1 |
| Reported passing tests | 43 |

The counts reconcile: `404 + 217 = 621` and `31 + 373 = 404`.

The prior integrated baseline contained 19 months, 437 positions, 307 numeric values, and 130 `N/A` values. The cached July 2026 run preserved every baseline month and added 97 numeric values across February–July where supported. August and September remain `N/A` with `extension_not_validated`.

## Integration evidence

Six Queue B records had previously been recovered through a focused calibration attempt. The cached July run then processed the 23 refreshed images in isolation: 17 records produced new February–July numeric values, while six failed calibration and remained conservative. Radeon RX 7600 XT remains failed with all 27 monthly values `N/A`.

The original turnover dataset, recovery output, and frozen Step 9 and Step 19 pilot artifacts were preserved. The final file was checked for unique models, exact month keys, metadata presence, count reconciliation, and failure isolation. The coordinate and runner test command was:

```powershell
python -m unittest tests.test_coordinate_calibration tests.test_coordinate_calibration_runner -v
```

The current full suite passes 43 tests.

## Extension evidence and source coverage

The cached source URLs are dated `2026.07.03`. All 23 cached images were retrieved and inspected; their rolling x-axes support approximately July 2026, not August or September. A local calibrated extraction added 97 numeric values for February–July where supported. No live scraper/API extraction was run, and August–September remain `N/A` rather than being inferred.

The October 2026 authorized-source investigation found a saved local page with 23 newer CDN references dated `2026.07.03`. All 23 URL references differ from the March sources and were retrieved for the controlled run. Live page retrieval remains blocked by Cloudflare, no official public chart-data API was found, and no prices were extracted for unsupported months. See [`CACHED_JULY_2026_EXTRACTION_REPORT.md`](CACHED_JULY_2026_EXTRACTION_REPORT.md).

Machine-readable validation is in [`EXTENDED_DATASET_VALIDATION.json`](EXTENDED_DATASET_VALIDATION.json). The baseline SHA-256 was `71DB952DD497189C15AD2E73376C39941BAF298620832518087086FF8F1C92C9`; the extended output SHA-256 is recorded there.

## Limitations

This is a structurally complete turnover dataset, not a fully numeric or production-approved dataset. Estimated values remain review-required, and all records are review-required for the unvalidated extension months. Historical chart readings are raster observations and manual references are approximate. RX 7600 XT remains blocked by:

```text
ValueError: Expected 7 horizontal gridlines, detected 6
```

The correct next action is a separately reviewed, evidence-based calibration investigation for that one record. Do not relax validation or rewrite historical outputs to remove the blocker.

## Handover readiness

The engineering handover is complete with caveats, not a production-readiness approval. The documented workflow, schema, failure isolation, atomic writes, pilot evidence, and 43-test suite are in place. The monthly-boundary business meaning still requires stakeholder clarification, and the cached-source run still has six calibration failures, including RX 7600 XT. The conservative quality policy was not relaxed.

The next owner should preserve the frozen pilots, obtain the monthly-boundary decision, and resolve or explicitly accept the RX 7600 XT calibration block before any new broad extraction. The final dataset must not be rewritten merely to increase numeric coverage.

## Publication scope

The repository publishes the final dataset, source code, tests, selected manifests/reports, and compact blocker-attempt diagnostics. Raw source image collections, intermediate experiment outputs, local environments, caches, and debug files remain local and are not required for the published runtime.
