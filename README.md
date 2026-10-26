# PCPartPicker GPU Price-Trend Retrieval

## Project Overview

This project collects PCPartPicker GPU trend-chart assets and converts the black actual-price line into a reviewable monthly USD dataset. It is a chart-derived research dataset, not a transaction database or a source of valuation-approved prices.

The repository contains the scraper, local calibration and extraction tools, deterministic tests, production data, source manifests, and retained chart diagnostics needed for technical review.

## Final Conclusion and Current Status

The current production dataset is `Monthly_Scraped_Data/pcpartpicker_gpu_trends_final.json`.

- 23 unique GPU records.
- 27 monthly fields per record, July 2024 through September 2026.
- 621 GPU-month positions.
- 459 numeric values and 162 `N/A` values.
- Numeric quality: 38 `observed` and 421 `estimated`.
- All 23 records remain `review_required=true`.
- The deterministic test suite passes 47 tests.

The dataset is structurally complete for the 27-month field range, but it is not fully numerically complete or independently human-validated. Twelve August–September 2026 positions remain `N/A` because the line evidence is missing, disconnected, ambiguous, or spike-like. Four historical QA warnings remain unresolved:

- GeForce RTX 4080 — November 2024 — `$1,104.00` estimated.
- GeForce RTX 4080 — December 2024 — `$1,403.00` estimated.
- GeForce RTX 4080 — January 2025 — `$1,291.00` estimated; left-edge `missing_line_segment`.
- GeForce RTX 4090 — October 2024 — `$1,940.00` estimated.

These values must not be treated as approved valuation data. The August–September dispositions are retained in `experimental/aug_sep_2026_full_review_20261022/final_review_register.csv`, and the historical warnings are retained in `reports/qa_20261022/HISTORICAL_QA_WARNING_REGISTER.csv`. The review outcomes are `KEEP_NA` for 5 positions, `NEED_MORE_EVIDENCE` for 7 positions, and `KEEP_ESTIMATED_UNRESOLVED` for the 4 historical warnings. No value was approved as a new production observation.

## Data Collection Workflow

1. The Scrapy/Selenium spider loads the PCPartPicker trends page and records GPU names and chart-image URLs.
2. Input records are validated and duplicate GPU models are skipped.
3. Source images are retained with model mappings and, for the official CDN capture, URLs and SHA-256 hashes.
4. Charts are calibrated using visible plot bounds, date anchors, tick labels, and horizontal gridlines.
5. The extraction path samples the black actual-price line at monthly positions.
6. Missing, disconnected, ambiguous, and spike-like readings remain `N/A`; no interpolation, extrapolation, smoothing, or third-party substitution is used.
7. Outputs preserve review metadata and are written through backup and atomic-replacement safeguards.

The original extraction phase covered 19 months through January 2026. A cached July 2026 source phase extended the available field range through July 2026. The later official CDN asset package contains 23 native chart PNGs whose visible axes reach September 2026. These are historical source phases, not interchangeable source snapshots.

## Price Extraction Method

The local calibration implementation uses Pillow and explicit per-image calibration. It maps pixel coordinates to USD using the chart's own axis evidence and selects dark connected components near monthly x-positions. Continuity and horizontal support are used to reject isolated vertical spikes and unrelated dark pixels.

Quality classes:

- `observed`: the line position is directly supported by a clear chart point and valid calibration.
- `estimated`: a readable chart position was mapped conservatively and rounded to dollars; it remains review-required.
- `N/A`: the month is outside visible history, missing, disconnected, ambiguous, or rejected by a safety rule.

The post-boundary stability experiment remains diagnostic-only. It is not the production sampler. Invalid or contradictory calibration fails safely before trusted numeric extraction.

## Data Structure

Each production record contains the GPU model, source image URL, the backward-compatible `price_trend` object, `price_quality`, review metadata, and `extraction_status`.

`price_trend` contains exactly these 27 keys:

`2024-07-01` through `2026-09-01`.

Important metadata includes:

- `price_quality`: `observed`, `estimated`, or `N/A` per month.
- `review_required`: record-level or value-level review requirement.
- `review_reasons`: evidence and safety reasons for review.
- `extraction_status`: success, needs review, or failure details.
- `price_trend`: the compatibility field consumed by existing downstream code.

Calibration or image failures must not retain stale numeric values. Failed records retain all expected monthly keys as `N/A` and record that extraction was skipped.

## Data Quality and Validation Results

The independent coverage audit is available as:

- `reports/coverage_audit_20261023.csv` — one row per GPU-month.
- `reports/coverage_summary_20261023.json` — reconciled counts and classifications.

The audit confirms 23 models, 621 unique GPU-month positions, 459 numeric values, 162 `N/A`, 38 observed, and 421 estimated. It records 35 automated-only statistical transition explanations, 12 unresolved August–September positions, and 4 unresolved historical warnings. Automated evidence is not human approval.

The test suite is run with:

```powershell
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The latest verified result is 47 passing tests. `git diff --check` also passes after documentation changes. Test success verifies implementation behavior; it does not prove that every chart-derived price is accurate.

## Known Limitations and Review Requirements

- The source charts are raster images, so visual precision is limited by line thickness, gridlines, date alignment, and image resolution.
- Current source assets do not independently verify every historical month. Later rolling charts cannot recreate an original chart view that is no longer visible.
- Four historical warnings remain unresolved because the retained chart does not show the requested month or rejects the left-edge point.
- Twelve August–September positions remain `N/A` until a reviewer can establish a supported monthly line point.
- The six former automatic calibration failures have bounded manual-axis artifacts, but calibration success alone does not validate every price.
- All records remain review-required. No valuation approval has been granted.

Do not clear review flags, replace `N/A`, or change an estimated value without source evidence, preserved provenance, an explicit before/after review, and approval.

## Project Structure

```text
README.md                              This handover document
batch/                                 Scrapy/Selenium source collector
tests/                                 Deterministic test suite
Monthly_Scraped_Data/                  Production JSON, source inventory, and backup
diagnostics/                           Source images, overlays, calibration diagnostics
experimental/                          Controlled pilot inputs, outputs, and review registers
reports/                               Machine-readable audits and QA registers
docs/CDN_CHART_ASSET_MANIFEST_20261022.json  Official source URL, hash, dimension, and endpoint manifest
coordinate_calibration.py             Axis calibration and line selection
coordinate_calibration_runner.py      Local calibrated runner with failure isolation
gpu_trends_image_extraction.py        Controlled vision extraction utility
coverage_config.py                    Central month-range definitions
coverage_audit.py                     Month-level evidence audit generator
extend_dataset.py                     Safe schema-extension utility
final_dataset_calibration.json         Per-record calibration configuration
pcpartpicker_gpu_trends.json           Input GPU records
requirements.txt                       Python dependencies
scrapy.cfg                             Scrapy project configuration
```

The retained JSON, CSV, image, overlay, and diagnostic artifacts are evidence or reproducibility inputs. The local `.env`, `.venv`, Python caches, and browser/cache artifacts are machine-local and are excluded from publication by `.gitignore`.

## Setup and Execution

Use Python 3.11 or a compatible Python 3 environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run tests before any data operation:

```powershell
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Inspect the Scrapy project without collecting data:

```powershell
python -m scrapy --settings=batch.settings list
```

The scraper requires ordinary authorized browser access and may be blocked by the source site. Do not bypass access controls. A broad extraction requires fresh source verification, calibration review, and explicit approval.

The local calibrated sample runner does not require an external API:

```powershell
python coordinate_calibration_runner.py --input sample_input.json --calibration sample_calibration.json --output Monthly_Scraped_Data/pcpartpicker_gpu_trends_coordinate_sample.json --artifact-dir diagnostics/coordinate_sample
```

The vision utility requires `OPENAI_API_KEY` from a local environment and must only be used for an approved controlled experiment. Never commit credentials.

## Final Handover Notes

Complete:

- Scraper, calibration, runner, failure isolation, safe-write behavior, and deterministic tests are implemented.
- Production schema and month coverage are consistent.
- Source manifests, chart assets, calibration artifacts, diagnostics, QA registers, and coverage audits are retained.
- Human review outcomes are retained in the machine-readable review registers under `experimental/aug_sep_2026_full_review_20261022/` and `reports/qa_20261022/`.

Pending:

- Human approval of unresolved chart readings.
- Additional historical chart evidence for the four unresolved warnings, if the estimates are to be independently verified.
- Any production price correction must be proposed and approved separately; none is authorized by this cleanup.

The production dataset SHA-256 is `D1C4FA395366829F0965927BE4051840D94441BFBC4265A3245E3D801FA1E7E5`. The original backup SHA-256 is `920BFC9BD9F93DB05EC25D64598E4037D132D411B6B32CEA01C4DB38C105D2A1`.
