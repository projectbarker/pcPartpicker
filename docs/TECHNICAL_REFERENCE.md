# Technical Reference and Decisions

## Dependencies

The project uses Scrapy, BeautifulSoup, Selenium, undetected-chromedriver, python-dotenv, OpenAI, requests, itemadapter, and Pillow. Pillow was retained for the coordinate prototype; OCR and OpenCV were not added because the evidence did not justify the extra complexity.

## Calibration implementation

`coordinate_calibration.py` detects chart geometry, maps calibrated pixels to USD, identifies connected dark components near monthly positions, scores horizontal support and neighboring continuity, rejects isolated vertical spikes, and emits diagnostic overlays. `coordinate_calibration_runner.py` loads explicit per-image calibration, isolates record failures, normalizes the 19 monthly keys, and writes atomically.

The date anchor and tick mappings remain explicit calibration evidence rather than automated OCR. Axis mappings must be monotonic and in bounds. Invalid or contradictory calibration fails safely before numeric extraction.

## Important decisions

- Keep Selenium because the trends page is dynamically rendered.
- Keep the 19-month schema and backward-compatible `price_trend` field.
- Treat chart readings as observations, not exact ground truth.
- Use bounded API retries and classify all-`N/A` results as failed.
- Preserve `observed`, `estimated`, `N/A`, review, and failure metadata.
- Back up existing outputs and replace them atomically.
- Keep direct vision and post-boundary stability as controlled/diagnostic paths, not unreviewed production behavior.
- Never bypass calibration checks or fabricate missing history.

## Configuration and secrets

`OPENAI_API_KEY` is read from the environment. Local `.env` files, environments, caches, browser profiles, and temporary files are excluded by `.gitignore`. No secret values belong in source, reports, manifests, or datasets.

## Tests

The documented final integration validation run passed 22 tests. The post-cleanup full suite passed 38 tests covering calibration, runner behavior, pipeline validation, failure isolation, output schema, and safe writes. Tests verify behavior; they do not establish that every chart-derived value is ground truth.
