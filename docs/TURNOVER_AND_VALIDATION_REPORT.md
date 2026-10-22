# Turnover and Validation Report

## Final artifact

The published dataset is [`../Monthly_Scraped_Data/pcpartpicker_gpu_trends_final.json`](../Monthly_Scraped_Data/pcpartpicker_gpu_trends_final.json). The extended file contains 23 unique GPU records, 27 monthly keys per record, and 621 total positions.

| Measure | Result |
|---|---:|
| Numeric values | 307 |
| `N/A` values | 314 |
| `observed` values | 25 |
| `estimated` values | 282 |
| Records requiring review | 23 |
| Failed records | 1 |
| Reported passing tests | 22 |

The counts reconcile: `307 + 314 = 621` and `25 + 282 = 307`.

The prior integrated baseline contained 19 months, 437 positions, 307 numeric values, and 130 `N/A` values. The extension preserved every baseline month in the backup and added February through September 2026 as `N/A` with `extension_not_validated`.

## Integration evidence

Six Queue B records were recovered through a focused, evidence-backed calibration attempt and written to a new candidate output before integration. Only those six records replaced their earlier zero-numeric failure records. The unrelated records were retained from the supervised pilot evidence, and Radeon RX 7600 XT remained failed with 19 baseline `N/A` values (27 after the extension).

The original turnover dataset, recovery output, and frozen Step 9 and Step 19 pilot artifacts were preserved. The final file was checked for unique models, exact month keys, metadata presence, count reconciliation, and failure isolation. The coordinate and runner test command was:

```powershell
python -m unittest tests.test_coordinate_calibration tests.test_coordinate_calibration_runner -v
```

The reported integration run passed 22 tests; the pre-extension full suite passed 38 tests; the extension suite passed 40 tests.

## Extension evidence and source coverage

The existing source URLs are dated `2026.03.03`. Direct inspection of the saved representative chart image showed visible x-axis history through approximately February 2026, not September 2026. No API extraction or scraper refresh was run. Consequently, the eight new months were added conservatively as `N/A` rather than inferred from the last visible point. March through September are outside the saved chart history; February is visible in the chart family but remains unvalidated because no approved extraction was run for the extension.

The October 2026 authorized-source investigation found a saved local page with 23 newer CDN references dated `2026.07.03`. All 23 URL references differ from the March sources. Only Arc A380 was downloaded and visually inspected; it supports approximately July 2026 coverage. The other 22 charts and August–September coverage remain unverified. Live retrieval is still blocked by Cloudflare, no official public chart-data API was found, and no final-dataset values were changed. See [`AUTHORIZED_SOURCE_ALTERNATIVE_20261022.md`](AUTHORIZED_SOURCE_ALTERNATIVE_20261022.md).

Machine-readable validation is in [`EXTENDED_DATASET_VALIDATION.json`](EXTENDED_DATASET_VALIDATION.json). The baseline SHA-256 was `71DB952DD497189C15AD2E73376C39941BAF298620832518087086FF8F1C92C9`; the extended output SHA-256 is recorded there.

## Limitations

This is a structurally complete turnover dataset, not a fully numeric or production-approved dataset. Estimated values remain review-required, and all records are review-required for the unvalidated extension months. Historical chart readings are raster observations and manual references are approximate. RX 7600 XT remains blocked by:

```text
ValueError: Expected 7 horizontal gridlines, detected 6
```

The correct next action is a separately reviewed, evidence-based calibration investigation for that one record. Do not relax validation or rewrite historical outputs to remove the blocker.

## Handover readiness

The engineering handover is complete with caveats, not a production-readiness approval. The documented workflow, schema, failure isolation, atomic writes, pilot evidence, and 40-test extension suite are in place. The monthly-boundary business meaning still requires stakeholder clarification, and the full 23-GPU batch remains unapproved. Earlier readiness work identified seven pilot-ready records, fifteen requiring manual calibration, and one separately blocked record; later supervised pilots and the six-record recovery reduced the final dataset's unresolved processing result to RX 7600 XT only, without changing the conservative quality policy.

The next owner should preserve the frozen pilots, obtain the monthly-boundary decision, and resolve or explicitly accept the RX 7600 XT calibration block before any new broad extraction. The final dataset must not be rewritten merely to increase numeric coverage.

## Publication scope

The repository publishes the final dataset, source code, tests, selected manifests/reports, and compact blocker-attempt diagnostics. Raw source image collections, intermediate experiment outputs, local environments, caches, and debug files remain local and are not required for the published runtime.
