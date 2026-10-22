# PCPartPicker GPU Price-Trend Retrieval

This project retrieves PCPartPicker GPU trend-chart images and produces a reviewable monthly USD price dataset. It combines a Scrapy/Selenium collector with a conservative chart-extraction pipeline and preserves the evidence needed to audit each result.

## Current status

The published dataset is [`Monthly_Scraped_Data/pcpartpicker_gpu_trends_final.json`](Monthly_Scraped_Data/pcpartpicker_gpu_trends_final.json).

- 23 unique GPU records and 27 monthly fields per record.
- Requested date range: July 2024 through September 2026.
- 621 monthly positions: 307 numeric and 314 `N/A`.
- Numeric values: 25 `observed` and 282 `estimated`.
- All 23 records require review because the extension months are unvalidated; one record is failed.
- The extension validation run passed 40 automated tests.

The counts reconcile: `307 + 314 = 621` and `25 + 282 = 307`. The dataset is structurally complete, but not fully numerically complete or production-approved. The saved `2026.03.03` charts visibly reach approximately February 2026; February–September 2026 were retained as `N/A` because the extension was not validated, and March–September are outside the saved chart history. Radeon RX 7600 XT remains blocked by `ValueError: Expected 7 horizontal gridlines, detected 6`; its calibration was not bypassed.

## Quick start

The verified local runtime is Python 3.11.3.

```powershell
cd <repository-root>
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

The vision extractor reads `OPENAI_API_KEY` from the environment or a local `.env` file. Never commit credentials. A controlled API sample is:

```powershell
python gpu_trends_image_extraction.py --limit 1 --output Monthly_Scraped_Data/pcpartpicker_gpu_trends_test.json
```

The calibrated local runner, which does not require the external API, is:

```powershell
python coordinate_calibration_runner.py --input sample_input.json --calibration sample_calibration.json --output Monthly_Scraped_Data/pcpartpicker_gpu_trends_coordinate_sample.json --artifact-dir diagnostics/coordinate_sample
```

The scraper can be inspected with `python -m scrapy --settings=batch.settings list` and run with `python -m scrapy --settings=batch.settings crawl pcpartpicker_gpu_trends -a headless=true`. A broad extraction must not be run without fresh calibration and review approval.

## Data quality and schema

Every record retains `gpu_model_name`, `image_url`, the backward-compatible `price_trend` field, `price_quality`, review metadata, and `extraction_status`. `price_trend` has exactly the 27 keys from `2024-07-01` through `2026-09-01`.

- `observed` means the line position is directly supported by visible chart evidence.
- `estimated` means a readable chart position was mapped conservatively; it is rounded to dollars, formatted with two decimals, and remains review-required.
- `N/A` means history is unsupported, missing, disconnected, or ambiguous. Prices are never interpolated, extrapolated, smoothed, or invented.

The eight extension months carry `N/A` and `extension_not_validated`; no future prices were inferred from the last visible point.

### Source investigation status

Live PCPartPicker retrieval remains blocked by a Cloudflare challenge. A saved local page contains 23 newer CDN URL references dated `2026.07.03`; these are cached source metadata, not proof of current live coverage. One Arc A380 image was downloaded and visually checked, reaching approximately July 2026. The other 22 charts, August 2026, and September 2026 remain unverified. See [`docs/AUTHORIZED_SOURCE_ALTERNATIVE_20261022.md`](docs/AUTHORIZED_SOURCE_ALTERNATIVE_20261022.md) and the [cached URL manifest](Monthly_Scraped_Data/pcpartpicker_gpu_sources_cached_2026.07.03.json). Do not resume extraction until chart identity and date coverage are reviewed.

Calibration checks and failure metadata must be preserved. Numeric output is not a claim of transaction-level ground truth.

## Repository structure

```text
README.md
docs/                         authoritative project documentation
batch/                        Scrapy/Selenium collector
Monthly_Scraped_Data/         final published dataset
diagnostics/turnover_blocker_attempt/  compact published evidence
tests/                        deterministic tests
coordinate_calibration.py     chart calibration and line selection
coordinate_calibration_runner.py  isolated calibrated runner
gpu_trends_image_extraction.py    vision extraction utility
extend_dataset.py             safe monthly-schema extension utility
final_dataset_calibration.json    calibration configuration
pcpartpicker_gpu_trends.json     input GPU records
requirements.txt              Python dependencies
```

## Testing

Run the deterministic suite with:

```powershell
python -m unittest discover -s tests -v
```

The reported final integration validation passed 22 tests. The pre-extension full suite passed 38 tests, and the current extension suite passes 40 tests, including calibration, runner, pipeline, output-safety, schema, and date-range checks. Passing tests do not independently prove the accuracy of every raster-chart reading.

## Documentation index

- [Project overview](docs/PROJECT_OVERVIEW.md)
- [Workflow and operations](docs/WORKFLOW.md)
- [Data quality and calibration policy](docs/DATA_QUALITY_AND_CALIBRATION.md)
- [Technical reference and decisions](docs/TECHNICAL_REFERENCE.md)
- [Supervised pilot evidence](docs/SUPERVISED_EXTRACTION_PILOT.md)
- [Turnover and validation report](docs/TURNOVER_AND_VALIDATION_REPORT.md)
- [Extended dataset validation](docs/EXTENDED_DATASET_VALIDATION.json)
- [Authorized source investigation](docs/AUTHORIZED_SOURCE_ALTERNATIVE_20261022.md)

GitHub: [ranvijaykumarg2c/pcPartPicker](https://github.com/ranvijaykumarg2c/pcPartPicker)
