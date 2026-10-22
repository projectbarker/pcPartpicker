# Live PCPartPicker Chart Capture Report — 2026-10-22

## Outcome

The official PCPartPicker trends page was loaded in the existing authorized in-app browser. It displayed all 23 GPU chart entries and rendered axes visibly including August and September 2026.

The required reproducible native asset capture could not be completed. The available browser surface does not expose chart `src`/`srcset` attributes, page-source inspection, Chrome DevTools Protocol, DevTools Network logs, HAR export, or a supported native image-download operation. The separate Selenium path also remains unavailable because undetected-chromedriver needs an outbound driver-release request that the environment refused.

Because native live assets and exact URLs were not captured, the August–September extraction phase was not started. No production values were changed.

## Verified observations

- Official URL: `https://pcpartpicker.com/trends/price/video-card/`
- Page title: `Video Card Price Trends - PCPartPicker`
- GPU chart entries present: 23
- Rendered charts: visible and interactive in the authorized browser
- Visible axis range: approximately May 2025 through September 2026
- August 2026: visibly within the current chart range
- September 2026: visibly within the current chart range
- Native live files saved: 0
- Exact live chart URLs recovered: 0
- Prices extracted: 0

The prior July source images remain the only reproducible local chart set. They are preserved in [`diagnostics/cached_july_2026_sources`](../diagnostics/cached_july_2026_sources/) and must not be relabeled as live October evidence.

## Per-GPU capture status

All 23 entries were present on the live page. The machine-readable status for each is in [`LIVE_CHART_CAPTURE_MANIFEST_20261022.json`](LIVE_CHART_CAPTURE_MANIFEST_20261022.json). Each entry has:

- `chart_present: true`
- `live_asset_url: null`
- `native_image_path: null`
- `native_verification: pending_asset_export`
- page-level latest visible month `2026-09-01`

This records page evidence, not a claim that the live bytes were preserved.

## Why extraction did not proceed

The project policy requires a reproducible native image or exact source URL before reading monthly line positions. A responsive browser screenshot is insufficient for audit-grade calibration and cannot establish per-GPU checksums or native dimensions. Extracting from it would make the new values non-reproducible and would violate the requested evidence standard.

No calibration threshold, extraction code, production JSON, cached July image, or historical pilot artifact was changed.

## Validation

- Live page visual check: 23 chart entries present.
- Existing cached asset check: 23 individual PNGs, each `1176×484`.
- Production dataset check: 23 records, 25 months per record, last month `2026-07-01`.
- Production dataset SHA-256 unchanged: `920BFC9BD9F93DB05EC25D64598E4037D132D411B6B32CEA01C4DB38C105D2A1`.
- Full test suite was not rerun because no code or test files changed.

## Recommended next action

Use an authorized browser environment that exposes Chrome DevTools Protocol or Network inspection, or have the team export the 23 current CDN image URLs/files. Save them under a new timestamped directory, compute per-file checksums and dimensions, and only then run a small August–September extraction pilot.
