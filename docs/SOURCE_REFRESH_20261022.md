# PCPartPicker GPU Source Refresh — 2026-10-22

## Result

The source refresh was not verified. No refreshed GPU URL metadata was retained, and the final dataset was not modified.

The existing scraper uses Selenium/undetected-Chromedriver, opens `https://pcpartpicker.com/trends/price/video-card/`, waits for `div.block img`, and extracts each block's first `h3` text and image `src`. The normal Scrapy launcher failed before starting with `running 'scrapy crawl' with more than one spider is not supported`, although `scrapy list` showed one spider. Direct invocation of the same spider then failed because the installed browser is Chrome 155 while the cached driver supports Chrome 156.

A bounded compatibility attempt using ChromeDriver version 155 reached the live site, but the page returned Cloudflare's `Just a moment...` page: zero GPU blocks and zero image URLs. A read-only HTTP request and the web fetch both returned HTTP 403. Therefore no current source URLs or chart coverage could be established.

## Existing source coverage

The final dataset still contains 23 records whose saved chart URLs are dated `2026.03.03`. The existing saved evidence supports the previously documented conclusion that a representative chart reaches approximately February 2026; this refresh did not independently verify coverage for any GPU or month.

Accordingly, the requested months remain unverified:

| Month | Refresh result |
|---|---|
| February 2026 | Not independently verified in this refresh |
| March 2026 | Not verified |
| April 2026 | Not verified |
| May 2026 | Not verified |
| June 2026 | Not verified |
| July 2026 | Not verified |
| August 2026 | Not verified |
| September 2026 | Not verified |

No month should be populated from this attempt. Existing `N/A` values with `extension_not_validated` remain correct pending accessible, visibly inspectable source charts.

## Dataset preservation

`Monthly_Scraped_Data/pcpartpicker_gpu_trends_final.json` was not changed. Its SHA-256 after the refresh attempt is:

`FBD1F9126A899F57D01A41BC46E54897DA515B37C42E4FBE9CDB33CF32CE5459`

The temporary empty refresh file created during the failed write attempt was removed; no misleading zero-record source metadata was retained.

## Next safe action

Repair the browser/driver compatibility or obtain an approved, accessible PCPartPicker source session, then rerun only the source-URL collection into a new metadata file. Do not begin price extraction until each refreshed chart's visible date range has been reviewed.

## Browser compatibility follow-up — 2026-10-22

The installed browser is Chrome `155.0.8059.85`. The collector previously allowed undetected-chromedriver to auto-select a driver and received a ChromeDriver 156 session, producing `SessionNotCreatedException` before navigation. The collector now detects the installed Windows executable's file-version metadata and passes its major version as `version_main` to undetected-chromedriver. No dependency was added and no global threshold or extraction behavior changed.

The repaired setup was tested successfully with detected major version `155`. The browser launched and navigated to both the trends page and the existing Arc A380 chart URL. The saved chart URL loaded normally and reported `1176×484`. The trends page still returned the Cloudflare `Just a moment...` page, with zero `div.block` GPU chart blocks, so source collection remains blocked. Browser startup success must not be interpreted as source access success.

Tests run:

- `python -m unittest tests.test_scraper_browser_setup -v` — 3 passed.
- Browser navigation smoke test — driver compatibility passed; trends page access failed at Cloudflare challenge; actual GPU chart block count `0`.

The final dataset remains unchanged with SHA-256 `FBD1F9126A899F57D01A41BC46E54897DA515B37C42E4FBE9CDB33CF32CE5459`. No source refresh or price extraction was run.

## Cached-source follow-up

Inspection of the existing local `pcpartpicker_debug_page.html` found 23 CDN chart references dated `2026.07.03`, newer than the March URLs. This is a saved artifact rather than a live response. One Arc A380 image was downloaded and visually verified at `1176×484`, with visible history approximately through July 2026. The other 22 charts, August 2026, and September 2026 remain unverified. The URL inventory and provenance are recorded in `Monthly_Scraped_Data/pcpartpicker_gpu_sources_cached_2026.07.03.json`; the detailed decision is in `docs/AUTHORIZED_SOURCE_ALTERNATIVE_20261022.md`.
