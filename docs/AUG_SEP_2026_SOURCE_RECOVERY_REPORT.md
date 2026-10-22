# August–September 2026 PCPartPicker Source-Recovery Report

**Investigation date:** 2026-10-22  
**Scope:** Read-only recovery investigation; no production extraction or dataset modification.

## Executive summary

No official August or September 2026 prices were recovered. The only reproducible native chart assets available locally are the 23 cached PCPartPicker PNGs dated `2026.07.03`. Their native-resolution axes support approximately July 2026 and do not establish either target month. The authorized browser observation showed a live page with rendered timelines reaching September 2026, but it did not expose native image bytes, exact per-GPU URLs, or exportable network evidence. That observation is therefore not sufficient to publish prices.

The production dataset remained unchanged. Its SHA-256 before and after the investigation is:

`920BFC9BD9F93DB05EC25D64598E4037D132D411B6B32CEA01C4DB38C105D2A1`

## Baseline verified

- Branch: `main`; prior commit: `642fa4b docs: Finalize Documentation`.
- Production file: `Monthly_Scraped_Data/pcpartpicker_gpu_trends_final.json`.
- Records: 23 unique GPU models.
- Existing coverage: July 2024 through July 2026, 25 monthly fields per record.
- Existing totals: 575 GPU-month positions, 425 numeric values, 150 `N/A` values.
- Existing source inventory: `Monthly_Scraped_Data/pcpartpicker_gpu_sources_cached_2026.07.03.json`.

## Evidence inspected

1. `docs/LIVE_CHART_CAPTURE_REPORT_20261022.md` and its manifest: the official page was visible in an authorized in-app browser; all 23 entries rendered and page-level axes appeared to include August and September 2026, but zero native assets and zero exact live URLs were captured.
2. `pcpartpicker_debug_page.html`: 23 cached CDN references dated `2026.07.03`.
3. `Monthly_Scraped_Data/pcpartpicker_gpu_sources_cached_2026.07.03.json`: source identity and URL inventory for all 23 cached charts.
4. `diagnostics/cached_july_2026_sources/`: 23 native PNGs, each `1176×484`, plus a contact sheet. Native inspection of the RTX 4070 chart shows the saved rolling axis ending around July 2026; the contact sheet is consistent with the same cached set.
5. Git history and tracked artifact paths: no later native chart set, August/September values, HAR, or chart-data export was found.
6. Official public access attempts: the configured web access path returned HTTP 403 for the official trends page; the local PowerShell network path was refused by the environment proxy. The Internet Archive CDX endpoint was not accessible through the configured web path. No access-control bypass was attempted.

## Per-GPU recovery status

All 23 GPUs have a local July 3 cached image, but none has a verified native August or September source asset. The machine-readable manifest contains the exact URL, local path, dimensions, checksum, and status for each record.

| GPU count | Native August value recovered | Native September value recovered | Status |
|---:|---:|---:|---|
| 23 | 0 | 0 | `not_verified` |

The live-page observation applies only to rendered page-level evidence. It is not a per-GPU value source and is not used to populate the dataset.

## Rejected or insufficient artifacts

- The July 3 cached PNGs were rejected for August/September recovery because their visible rolling history ends around July 2026.
- The live browser screenshot/rendering was rejected as a production source because native resolution, per-GPU identity-to-file mapping, exact URLs, and checksums were unavailable.
- URL dates and file modification times were not treated as proof of chart coverage.
- No third-party prices were collected or used.

## Checks performed

- Calculated the production SHA-256 before investigation.
- Enumerated the production schema and confirmed no `2026-08-01` or `2026-09-01` keys are present.
- Enumerated all 23 cached PNGs and verified `1176×484` dimensions and SHA-256 values.
- Opened the cached contact sheet and a native-resolution RTX 4070 chart.
- Inspected Git history for later source assets and data files.
- Attempted ordinary official-page and archive access without bypassing restrictions.
- Recalculated the production SHA-256 after inspection; it is unchanged.

## Recommended next action

Obtain an approved native export of the current 23 PCPartPicker chart images or exact CDN URLs from the team, using a browser session with authorized DevTools Network/CDP export. Preserve each file with its GPU mapping, timestamp, dimensions, and checksum; then run a small two-month pilot before any production update.

Until that evidence exists, keep August and September unpopulated and do not alter the production dataset.
