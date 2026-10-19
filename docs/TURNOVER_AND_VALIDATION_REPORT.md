# Turnover and Validation Report

## Final artifact

The published dataset is [`../Monthly_Scraped_Data/pcpartpicker_gpu_trends_final.json`](../Monthly_Scraped_Data/pcpartpicker_gpu_trends_final.json). It contains 23 unique GPU records, 19 monthly keys per record, and 437 total positions.

| Measure | Result |
|---|---:|
| Numeric values | 307 |
| `N/A` values | 130 |
| `observed` values | 25 |
| `estimated` values | 282 |
| Records requiring review | 22 |
| Failed records | 1 |
| Reported passing tests | 22 |

The counts reconcile: `307 + 130 = 437` and `25 + 282 = 307`.

## Integration evidence

Six Queue B records were recovered through a focused, evidence-backed calibration attempt and written to a new candidate output before integration. Only those six records replaced their earlier zero-numeric failure records. The unrelated records were retained from the supervised Step 9/19 evidence, and Radeon RX 7600 XT remained failed with 19 `N/A` values.

The original turnover dataset, recovery output, and frozen Step 9 and Step 19 pilot artifacts were preserved. The final file was checked for unique models, exact month keys, metadata presence, count reconciliation, and failure isolation. The coordinate and runner test command was:

```powershell
python -m unittest tests.test_coordinate_calibration tests.test_coordinate_calibration_runner -v
```

The reported integration run passed 22 tests; the subsequent full post-cleanup suite passed 38 tests.

## Limitations

This is a structurally complete turnover dataset, not a fully numeric or production-approved dataset. Estimated values remain review-required. Historical chart readings are raster observations and manual references are approximate. RX 7600 XT remains blocked by:

```text
ValueError: Expected 7 horizontal gridlines, detected 6
```

The correct next action is a separately reviewed, evidence-based calibration investigation for that one record. Do not relax validation or rewrite historical outputs to remove the blocker.

## Handover readiness

The engineering handover is complete with caveats, not a production-readiness approval. The documented workflow, schema, failure isolation, atomic writes, pilot evidence, and 38-test suite are in place. The monthly-boundary business meaning still requires stakeholder clarification, and the full 23-GPU batch remains unapproved. Earlier readiness work identified seven pilot-ready records, fifteen requiring manual calibration, and one separately blocked record; later supervised pilots and the six-record recovery reduced the final dataset's unresolved processing result to RX 7600 XT only, without changing the conservative quality policy.

The next owner should preserve the frozen pilots, obtain the monthly-boundary decision, and resolve or explicitly accept the RX 7600 XT calibration block before any new broad extraction. The final dataset must not be rewritten merely to increase numeric coverage.

## Publication scope

The repository publishes the final dataset, source code, tests, selected manifests/reports, and compact blocker-attempt diagnostics. Raw source image collections, intermediate experiment outputs, local environments, caches, and debug files remain local and are not required for the published runtime.
