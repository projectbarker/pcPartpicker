# PCPartPicker GPU Price-Trend Retrieval

This project retrieves PCPartPicker GPU trend-chart images and produces a reviewable monthly USD price dataset. It combines a Scrapy/Selenium collector with a conservative chart-extraction pipeline and preserves the evidence needed to audit each result.

## Current status

The published dataset is [`Monthly_Scraped_Data/pcpartpicker_gpu_trends_final.json`](Monthly_Scraped_Data/pcpartpicker_gpu_trends_final.json).

- 23 unique GPU records and 27 monthly fields per record.
- Verified date range: July 2024 through September 2026.
- 621 monthly positions: 459 numeric and 162 `N/A`.
- Numeric values: 38 `observed` and 421 `estimated`.
- All 23 records require review; August and September values were added through the approved official-CDN review package.
- The current deterministic test suite passes 44 tests.

The counts reconcile: `459 + 162 = 621` and `38 + 421 = 459`. The dataset is structurally complete for the verified source range, but not fully numerically complete; all records remain review-required. August and September were applied from the approved review package in `experimental/aug_sep_2026_full_review_20261022/`. Twelve target positions remain `N/A` because of missing or ambiguous line evidence.

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

August and September 2026 are present where the official chart evidence supported a numeric candidate; unresolved positions remain `N/A`. All new values remain review-required, and estimates remain explicitly marked `estimated`.

### Source investigation status

The current official CDN capture contains 23 native chart PNGs dated 2026-10-22, each mapped to a GPU model with a recorded SHA-256 and visible history through September 2026. The source manifest and capture report are [`docs/CDN_CHART_ASSET_MANIFEST_20261022.json`](docs/CDN_CHART_ASSET_MANIFEST_20261022.json) and [`docs/CDN_CHART_ASSET_CAPTURE_20261022.md`](docs/CDN_CHART_ASSET_CAPTURE_20261022.md). The final August–September review package and QA reports remain under `experimental/aug_sep_2026_full_review_20261022/` and `reports/qa_20261022/`.

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

The current full suite passes 44 tests, including calibration, runner, pipeline, output-safety, schema, source-collection setup, manual-axis validation, and date-range checks. Passing tests do not independently prove the accuracy of every raster-chart reading.

## Documentation index

- [Project overview](docs/PROJECT_OVERVIEW.md)
- [Workflow and operations](docs/WORKFLOW.md)
- [Data quality and calibration policy](docs/DATA_QUALITY_AND_CALIBRATION.md)
- [Technical reference and decisions](docs/TECHNICAL_REFERENCE.md)
- [Official CDN chart capture](docs/CDN_CHART_ASSET_CAPTURE_20261022.md)
- [Official CDN asset manifest](docs/CDN_CHART_ASSET_MANIFEST_20261022.json)
- [Dataset QA report](reports/qa_20261022/PCPARTPICKER_DATASET_QA_REPORT.md)
- [QA executive summary](reports/qa_20261022/QA_EXECUTIVE_SUMMARY.md)

GitHub: [ranvijaykumarg2c/pcPartPicker](https://github.com/ranvijaykumarg2c/pcPartPicker)
