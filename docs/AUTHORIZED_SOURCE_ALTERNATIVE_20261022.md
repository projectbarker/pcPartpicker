# Authorized PCPartPicker Source Alternative Investigation

## Conclusion

No live authorized replacement endpoint was available during this investigation. The PCPartPicker trends page remained behind a Cloudflare challenge, and no official public PCPartPicker chart-data API or downloadable trend dataset was found.

An older local cache did contain a useful, source-identifiable alternative: `pcpartpicker_debug_page.html` contains 23 GPU chart entries whose CDN image URLs are dated `2026.07.03`. These URLs are newer than the final dataset's `2026.03.03` URLs, but the HTML is a saved local artifact, not a live response. It therefore establishes cached source metadata, not current October coverage.

## Alternatives investigated

1. **Existing Selenium/Scrapy collector:** inspected in `batch/spiders/pc_part_picker.py`. It reads dynamically rendered `div.block img` elements from the PCPartPicker trends page. Browser compatibility is repaired, but the live page still returns `Just a moment...` and zero GPU blocks.
2. **Saved local cache:** `pcpartpicker_debug_page.html` was inspected. It contains 23 GPU identities and 23 CDN image references dated `2026.07.03`. All 23 cached URLs differ from the final dataset's March URLs.
3. **Public CDN asset:** the cached Arc A380 URL was downloaded to `diagnostics/authorized_source_cache/arc_a380_2026.07.03.png`. It loaded successfully as a `1176×484` chart, visibly identifies the Arc A380 series, and shows history approximately through July 2026. The last clearly labeled x-axis month is June 2026; the right edge represents the newest portion and is conservatively recorded as approximately July 2026.
4. **Structured/API alternatives:** searches found only unofficial wrappers and libraries. They are not PCPartPicker-authorized sources, do not establish access to the trend-chart series needed here, and were not used. No approved team browser session or manual-access artifact was available in the repository.

## Coverage determination

| Evidence | Result |
|---|---|
| Arc A380 cached chart | Approximately through July 2026; directly inspected |
| Other 22 cached chart URLs | Identity and July 3 URL metadata found; images not individually inspected |
| August 2026 | Not verified |
| September 2026 | Not verified |
| Live current page | Blocked by Cloudflare; zero chart blocks |

The cached July source is sufficient to justify a future supervised source-review pilot, but not a full extraction run. It does not support August or September prices, and it must not be treated as live current coverage for every GPU without image-by-image verification.

## Files created

- `Monthly_Scraped_Data/pcpartpicker_gpu_sources_cached_2026.07.03.json` — 23-entry old-to-cached URL mapping with provenance and verification flags.
- `diagnostics/authorized_source_cache/arc_a380_2026.07.03.png` — one downloaded cached chart used for identity/dimension/visual coverage verification.
- This report.

The final dataset was not modified. No price extraction, calibration, API call, commit, or push was performed.

## Recommended next action

Request manager approval to use the cached `2026.07.03` CDN URLs as a controlled source-review input, then inspect all 23 images individually before any extraction. Separately request an authorized current browser session or source export if August 2026 coverage is required. Keep September 2026 as `N/A` unless a chart visibly supports it.
