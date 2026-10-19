# PCPartPicker GPU Price-Trend Retrieval

This project collects PCPartPicker GPU trend-chart URLs and extracts monthly USD prices from the black actual-price line. The published dataset covers 23 GPU models and July 2024 through January 2026, with 19 monthly fields per record.

## Current status

The final integrated dataset is [`Monthly_Scraped_Data/pcpartpicker_gpu_trends_final.json`](Monthly_Scraped_Data/pcpartpicker_gpu_trends_final.json).

It contains 23 unique records and 437 monthly positions:

- 307 numeric values: 25 `observed` and 282 `estimated`.
- 130 `N/A` values for unsupported or ambiguous chart positions.
- 22 records requiring review.
- 1 failed record: Radeon RX 7600 XT.

RX 7600 XT remains blocked by `ValueError: Expected 7 horizontal gridlines, detected 6`. The dataset is structurally complete, but not fully numerically complete or production-approved.

See [`FINAL_TURNOVER_DATASET_REPORT.md`](FINAL_TURNOVER_DATASET_REPORT.md) for the execution history, validation results, calibration evidence, and limitations.

## Workflow

1. `batch/spiders/pc_part_picker.py` collects GPU model names and PCPartPicker trend-image URLs using Scrapy/Selenium.
2. `gpu_trends_image_extraction.py` provides the vision-based extraction path using the OpenAI API. It reads `OPENAI_API_KEY` from the environment and preserves `observed`, `estimated`, `N/A`, review, and failure metadata.
3. `coordinate_calibration.py` provides Pillow-based chart calibration, pixel-to-price mapping, continuity-aware black-line selection, spike rejection, and diagnostic overlays.
4. `coordinate_calibration_runner.py` runs explicit local calibrated samples with per-record failure isolation and atomic output writes.

Missing, disconnected, or ambiguous line segments remain `N/A`; the project does not interpolate, extrapolate, smooth, or invent prices. Estimated readings remain marked `estimated` and review-required.

## Setup

From PowerShell:

```powershell
cd C:\path\to\GPU_PCPARTPICKER
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Set `OPENAI_API_KEY` in the process environment or in a local `.env` file. `.env`, virtual environments, browser profiles, caches, and temporary files are excluded from Git; never commit credentials.

## Running the scraper and extraction

```powershell
python -m scrapy --settings=batch.settings list
python -m scrapy --settings=batch.settings crawl pcpartpicker_gpu_trends -a headless=true
```

For a controlled API extraction sample:

```powershell
python gpu_trends_image_extraction.py --limit 1 --output Monthly_Scraped_Data/pcpartpicker_gpu_trends_test.json
```

For a calibrated local sample:

```powershell
python coordinate_calibration_runner.py --input sample_input.json --calibration sample_calibration.json --output Monthly_Scraped_Data/pcpartpicker_gpu_trends_coordinate_sample.json --artifact-dir diagnostics/coordinate_sample
```

Outputs are written through a temporary file and atomically replaced; an existing output is backed up first. Do not run a broad batch until calibration, source-image access, and review requirements are approved.

## Output schema

Each record retains:

- `gpu_model_name` and `image_url`.
- `price_trend`: exactly 19 `YYYY-MM-01` keys from `2024-07-01` through `2026-01-01`.
- `price_quality`: `observed`, `estimated`, or `N/A` for each month.
- `review_required` and `review_reasons`.
- `extraction_status`, plus failure stage/reason where applicable.

The historical `price_trend` field remains backward-compatible. Quality metadata must be interpreted together with the chart diagnostics; numeric does not mean independently verified ground truth.

## Testing

```powershell
python -m unittest tests.test_coordinate_calibration tests.test_coordinate_calibration_runner -v
```

The final integration was validated with 22 passing tests, 23 unique GPU records, 19 monthly keys per record, reconciled numeric/`N/A` counts, and explicit RX 7600 XT failure isolation.

## Important files

- `Monthly_Scraped_Data/pcpartpicker_gpu_trends_final.json` — final integrated dataset.
- `FINAL_TURNOVER_DATASET_REPORT.md` — final execution and handover report.
- `WORKFLOW.md` — operational workflow and safety rules.
- `DECISIONS.md` — calibration and data-quality decisions.
- `coordinate_calibration.py` — calibration and line extraction logic.
- `coordinate_calibration_runner.py` — isolated calibrated runner.
- `gpu_trends_image_extraction.py` — OpenAI vision extraction utility.
- `tests/` — deterministic pipeline and calibration tests.

Historical pilot outputs and diagnostic artifacts are preserved locally; only reviewed, relevant supporting artifacts should be published.
