# Project Overview

## Purpose

PCPartPicker publishes GPU trend charts rather than a structured monthly-price API. This project retrieves the chart references and converts the black actual-price line into a fixed, reviewable monthly dataset for July 2024 through September 2026.

The output is a chart-derived observation. It is not a transaction database and does not claim more precision than the source raster supports.

## Current result

The current dataset contains 23 unique GPU records and 621 monthly positions. There are 425 numeric values and 196 `N/A` values; numeric values split into 35 `observed` and 390 `estimated`. All 23 records require review. The six former automatic gridline failures now have individually verified manual-axis geometry; unsupported line segments and August–September 2026 remain `N/A`.

## Main components

- `batch/spiders/pc_part_picker.py` collects dynamically rendered PCPartPicker trend-image URLs with Scrapy and Selenium.
- `gpu_trends_image_extraction.py` is the OpenAI vision extraction path for controlled API experiments.
- `coordinate_calibration.py` performs Pillow-based axis calibration, pixel-to-price conversion, continuity-aware black-line selection, spike rejection, and overlays.
- `coordinate_calibration_runner.py` runs local calibrated records with per-record failure isolation and safe output writes.
- `tests/` contains deterministic calibration, runner, and pipeline tests.

## Reproducibility

The final JSON, compact blocker-attempt diagnostics, calibration manifests, and validation reports are published. Earlier raw images, intermediate outputs, and local environments remain outside the publication set unless explicitly needed for a future investigation.
