# Official PCPartPicker CDN Chart Asset Capture — 2026-10-22

## Result

The requested `2026.10.22` CDN capture could not start because the 23 exact URLs referenced by the task are not present in the accessible conversation content or repository artifacts. The repository contains only the earlier March and July URL inventories. The task forbids guessing the per-image hashes or constructing replacement URLs, so no CDN request was made with an unverified URL.

Production data was preserved unchanged.

## Verified baseline

- Production file: `Monthly_Scraped_Data/pcpartpicker_gpu_trends_final.json`
- Production SHA-256: `920BFC9BD9F93DB05EC25D64598E4037D132D411B6B32CEA01C4DB38C105D2A1`
- Records: 23
- Coverage: July 2024 through July 2026
- Existing native assets: `diagnostics/cached_july_2026_sources/`, 23 PNGs at `1176×484`
- Existing source inventory: `Monthly_Scraped_Data/pcpartpicker_gpu_sources_cached_2026.07.03.json`

## Evidence check

The requested pattern `2026.10.22.usd.gpu.chipset.<slug>.<hash>.png` was searched across the repository. No matching URL, HTML export, browser network log, HAR, or saved native image was found. The only matching CDN references are dated `2026.03.03` or `2026.07.03`.

The prior authorized browser session confirmed that the official page can render 23 chart entries, but the available browser interface does not expose the image `src`/`srcset`, page source, network requests, DevTools Protocol, or native asset download. A rendered page is not enough to reconstruct exact CDN URLs.

## Capture status

| Item | Count | Status |
|---|---:|---|
| Exact `2026.10.22` URLs supplied to this environment | 0 | Blocked: inventory absent |
| CDN requests attempted with authoritative URLs | 0 | Not attempted to avoid guessing |
| Native `2026.10.22` images saved | 0 | Not recovered |
| August 2026 values verified | 0 | No current native source |
| September 2026 values verified | 0 | No current native source |
| Extraction pilot runs | 0 | Correctly skipped |

## Why extraction did not proceed

The current calibration pipeline requires a reproducible native image and a verified GPU-to-asset mapping. The July images cannot be relabeled as October sources, and a URL date alone would not prove that the line is readable for August or September. No production keys or prices were added.

## Required next action

Provide the 23 exact CDN URLs in a local manifest or paste them into the task context. The minimum required fields are GPU model, exact URL, and capture timestamp. Once received, download only those URLs into a new `diagnostics/live_chart_sources_20261022/` directory, verify PNG signatures, dimensions, checksums, GPU mapping, and month coverage, then run the requested three-GPU pilot.

## Preservation

- No production JSON, calibration, policy, or cached July image was changed.
- No credentials, cookies, browser profiles, HAR files, or authorization headers were accessed.

## Resumed capture addendum — exact URLs supplied

The earlier blocked status is superseded by the exact 23 URLs supplied in the resumed task. All 23 ordinary HTTPS requests succeeded and were saved under `diagnostics/live_chart_sources_20261022/`.

| Result | Count |
|---|---:|
| HTTP 200 PNG responses | 23 |
| Native images saved and dimension-validated | 23 |
| Images at `1176×484` | 23 |
| Failed downloads | 0 |
| Verified August values in the controlled pilot | 3 |
| Verified September values in the controlled pilot | 3 |

The exact URL, file size, dimension, SHA-256, and GPU mapping are recorded in the updated machine-readable manifest. The contact sheet and native images were reviewed for identity; the rolling x-axis visibly reaches September 2026. This establishes source coverage, not automatic numeric correctness for every GPU-month.

## Controlled pilot

Pilot directory: `experimental/live_october_pilot_20261022/`
Pilot months: `2026-08-01`, `2026-09-01`
Calibration: detected seven horizontal gridlines at `[27, 94, 161, 227, 294, 361, 427]`; detected monthly gridlines; May 2025 anchor verified at `x=71` for these charts.

| GPU | August | September | Quality / review |
|---|---:|---:|---|
| Arc A380 | `$200.00` | `$206.00` | August observed; September estimated; review required |
| GeForce RTX 5070 | `$856.00` | `$1,000.00` | August estimated; September observed; review required |
| Radeon RX 7900 XT | `$871.00` | `$943.00` | Both estimated; review required |

These are chart-derived pilot estimates, not exact published values. The overlays show the sampling positions on the black line. No interpolation, extrapolation, threshold relaxation, or production update was performed. The remaining 20 charts have current native assets, but their August/September numeric points remain pending individual extraction review.

## Final status for this task

- Official native assets captured: 23/23.
- August values recovered in the pilot: 3/3 tested GPUs.
- September values recovered in the pilot: 3/3 tested GPUs.
- Production dataset changed: no.
- Production SHA-256 remains `920BFC9BD9F93DB05EC25D64598E4037D132D411B6B32CEA01C4DB38C105D2A1`.
- Full 23-GPU extraction: not run; review is required before scaling beyond the pilot.
