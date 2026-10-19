# Workflow and Operations

## Data flow

1. The Scrapy/Selenium spider loads the PCPartPicker trends page and records GPU names and image URLs.
2. Input records are validated and deduplicated.
3. A chart image is checked before extraction. Unreadable or unavailable images become failed records with monthly `N/A` values.
4. The vision path or the manually calibrated Pillow path identifies chart axes and the black actual-price line.
5. Monthly positions are mapped to USD values, retaining quality and review metadata.
6. Diagnostics and the structured JSON are written through a temporary file, with an existing output backed up before atomic replacement.

## Commands

From the repository root:

The validated local runtime is Python 3.11.3.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m scrapy --settings=batch.settings list
python -m scrapy --settings=batch.settings crawl pcpartpicker_gpu_trends -a headless=true
python gpu_trends_image_extraction.py --limit 1 --output Monthly_Scraped_Data/pcpartpicker_gpu_trends_test.json
python coordinate_calibration_runner.py --input sample_input.json --calibration sample_calibration.json --output Monthly_Scraped_Data/pcpartpicker_gpu_trends_coordinate_sample.json --artifact-dir diagnostics/coordinate_sample
```

The vision command requires `OPENAI_API_KEY` in the environment. The local coordinate runner uses explicit calibration evidence and does not call the external API.

## Safety rules

Do not run a broad batch without approving source-image access, calibration evidence, and human-review requirements. Never bypass calibration errors to increase numeric coverage. Preserve the frozen pilot files and write experiments to new output paths. Missing, disconnected, or ambiguous line segments remain `N/A`; no interpolation or extrapolation is allowed.

## Output handling

The runner preserves the compatibility `price_trend` field and writes `price_quality`, `review_required`, `review_reasons`, and `extraction_status`. Per-record failures do not silently retain stale numeric values and do not prevent independent records from being represented in the output.
