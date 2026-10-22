# Historical Chart Recovery Report

Date: 2026-10-22
Scope: recovery of original PCPartPicker chart evidence for four unresolved historical QA warnings.
Production data, prices, classifications, review flags, source artifacts, and QA findings were not modified.

## Outcome summary

| QA finding | GPU / month | Existing value | Outcome | Evidence conclusion | Next action |
|---|---|---:|---|---|---|
| `QA-20261022-L15` | GeForce RTX 4080 — 2024-11-01 | `$1,104.00` | `not_found` | No retained chart image or cached response visibly covers November 2024. The available chart is a July 2026 snapshot whose visible history begins around January/February 2025. | Request the original historical chart image or an approved archive export covering November 2024, then verify date and y-axis calibration. |
| `QA-20261022-L16` | GeForce RTX 4080 — 2024-12-01 | `$1,403.00` | `not_found` | No retained chart image or cached response visibly covers December 2024. | Request the original historical chart image or an approved archive export covering December 2024, then verify date and y-axis calibration. |
| `QA-20261022-L17` | GeForce RTX 4080 — 2025-01-01 | `$1,291.00` | `candidate_requires_validation` | The retained July 2026 chart reaches the left boundary near January/February 2025, but the diagnostic maps January to `x=55` and rejects it as `missing_line_segment`. This is a candidate artifact, not verified historical evidence. | Obtain an original/earlier chart or separately verify the left-edge date anchor and connected line point without weakening missing-segment rejection. |
| `QA-20261022-L19` | GeForce RTX 4090 — 2024-10-01 | `$1,940.00` | `not_found` | No retained chart image or cached response visibly covers October 2024. The available chart is a July 2026 snapshot whose visible history begins around January/February 2025. | Request the original historical chart image or an approved archive export covering October 2024, then verify date and y-axis calibration. |

`not_found` means no suitable retained artifact was found; it does not prove that the source never existed. `candidate_requires_validation` means a related retained artifact exists, but it cannot establish the requested month and value under the current evidence policy.

## Artifacts and provenance inspected

### Retained chart images

| GPU | Local artifact | Dimensions | Provenance | Suitability for the warning |
|---|---|---:|---|---|
| RTX 4080 | `diagnostics/cached_july_2026_sources/geforce_rtx_4080.png` | 1176×484 | Cached July 3, 2026 CDN source set; not an original 2024 capture | Suitable for checking the retained calibration only; does not show Nov/Dec 2024 and does not securely establish Jan 2025. |
| RTX 4090 | `diagnostics/cached_july_2026_sources/geforce_rtx_4090.png` | 1176×484 | Cached July 3, 2026 CDN source set; not an original 2024 capture | Suitable for checking the retained calibration only; does not show Oct 2024. |

### Overlays and diagnostics

- RTX 4080 overlay: `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_4080.overlay.png`
- RTX 4080 diagnostic: `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_4080.diagnostics.json`
- RTX 4090 overlay: `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_4090.overlay.png`
- RTX 4090 diagnostic: `diagnostics/cached_july_2026_extraction/recovery_artifacts/geforce_rtx_4090.diagnostics.json`

The diagnostics use an anchor of `2025-02-01` and x-grid positions beginning at `x=55`. RTX 4080 November and December 2024 and RTX 4090 October 2024 are recorded as `out_of_history`. RTX 4080 January 2025 maps to the left boundary and is rejected as `missing_line_segment`; no accepted y-coordinate is recorded.

### Source URLs and metadata

The following metadata was inspected:

- `Monthly_Scraped_Data/pcpartpicker_gpu_sources_cached_2026.07.03.json`
- `pcpartpicker_gpu_trends.json`
- `docs/CACHED_JULY_2026_EXTRACTION_REPORT.md` and `docs/CACHED_JULY_2026_COMPLETION_AUDIT.md` as retained in Git history
- `docs/CDN_CHART_ASSET_CAPTURE_20261022.md`
- `docs/DATA_QUALITY_AND_CALIBRATION.md`
- `docs/WORKFLOW.md`

The documented RTX 4080 URLs are:

- March 3, 2026 URL: `https://cdna.pcpartpicker.com/static/forever/images/trends/2026.03.03.usd.gpu.chipset.geforce-rtx-4080.1a458cb629180b007380226fb7d85212.png`
- July 3, 2026 URL: `https://cdna.pcpartpicker.com/static/forever/images/trends/2026.07.03.usd.gpu.chipset.geforce-rtx-4080.4bb4ec8ae38fc313e72ec0bf68c1aabd.png`

The documented RTX 4090 URLs are:

- March 3, 2026 URL: `https://cdna.pcpartpicker.com/static/forever/images/trends/2026.03.03.usd.gpu.chipset.geforce-rtx-4090.6cffaa467e9701ce93547594581181d0.png`
- July 3, 2026 URL: `https://cdna.pcpartpicker.com/static/forever/images/trends/2026.07.03.usd.gpu.chipset.geforce-rtx-4090.9dd4d989ef10793beed5719b3397797c.png`

These URLs identify later source snapshots, not 2024 historical captures. The cached metadata explicitly marks live verification as false and the source type as local cached HTML.

## Repository and Git-history search

The repository, diagnostics, backups, cached assets, manifests, and Git object history were searched for:

- 2024-dated chart PNGs or cached responses;
- earlier RTX 4080 or RTX 4090 chart captures;
- extraction inputs containing original image bytes or URLs;
- archive/export metadata that could prove the requested month coverage.

Only the March 2026 URL references and July 2026 cached chart assets were found for these GPUs. Git history contains reports and data revisions, but no separate original chart image covering the requested October–December 2024 dates.

## Normal retrieval check

One ordinary `HEAD` request was attempted against the documented March 3, 2026 RTX 4080 CDN URL. The request failed locally with:

`No connection could be made because the target machine actively refused it. (127.0.0.1:9)`

This is an environment/proxy connectivity failure, not evidence that the CDN URL is unavailable. No access-control bypass, proxy rotation, scraper run, or source-artifact overwrite was attempted. No new artifact was saved.

## Required evidence to resolve the warnings

For RTX 4080 November and December 2024 and RTX 4090 October 2024, obtain an approved native chart image or archived source response that visibly includes the target month. The evidence package must preserve provenance, GPU identity, image dimensions, date anchors, and readable y-axis ticks.

For RTX 4080 January 2025, obtain either an earlier chart with unambiguous January history or a separately reviewed calibration showing that the left-edge point is genuinely January and connected to the actual-price line. Existing safeguards must remain in force.

Until that evidence exists, retain the current production values and their `estimated`, `review_required`, and unresolved/pending-approval state. Do not convert them to new prices or mark them verified.

## Integrity and validation

- Production dataset: `Monthly_Scraped_Data/pcpartpicker_gpu_trends_final.json`
  - SHA-256: `773F35F2BCA7081DFCF80D2F09CDE56914A0E8FEE1F1AFFA17B0A4CD044A9D16`
- Original backup: `Monthly_Scraped_Data/pcpartpicker_gpu_trends_final.backup_20261022_181917.json`
  - SHA-256: `920BFC9BD9F93DB05EC25D64598E4037D132D411B6B32CEA01C4DB38C105D2A1`

The full deterministic test suite was rerun after this report was created: 44 tests passed. `git diff --check` also passed. These results validate project behavior and formatting only; they do not verify the four prices or authorize valuation use.
