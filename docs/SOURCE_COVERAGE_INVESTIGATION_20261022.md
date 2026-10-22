# PCPartPicker Source Coverage Investigation — 2026-10-22

## Conclusion

The production dataset was not modified. The previously verified native chart set remains the `2026.07.03` cached set, whose saved images support approximately July 2026 and do not establish August or September 2026.

During this investigation, an ordinary authorized in-app browser session eventually loaded the live PCPartPicker trends page after initially showing a Cloudflare verification page. The live page visibly contained the official Video Card Price Trends page, 23 GPU entries, and chart images. A live GeForce RTX 4070 chart opened in the site's chart viewer and its trace visibly differed from the saved July snapshot, so newer live chart content is now observable.

The live browser rendering available to this task was responsive and scaled down. The final x-axis labels and the live image URLs were not readable or exposed with sufficient precision to prove the exact latest month for all 23 charts. Therefore:

| Month | Determination |
|---|---|
| July 2026 | Verified by the saved native-resolution `2026.07.03` chart set. |
| August 2026 | Not verified at native resolution in this investigation. Live-page evidence is suggestive of newer content, but not sufficient to publish prices. |
| September 2026 | Not verified at native resolution in this investigation. Live-page evidence is suggestive of newer content, but not sufficient to publish prices. |

This is a successful access observation, not a successful source refresh. No prices were extracted and no production calibration or schema change was made.

## Sources and access attempts

### Existing repository evidence

- `Monthly_Scraped_Data/pcpartpicker_gpu_trends_final.json` — unchanged; SHA-256 before and after investigation: `920BFC9BD9F93DB05EC25D64598E4037D132D411B6B32CEA01C4DB38C105D2A1`.
- `Monthly_Scraped_Data/pcpartpicker_gpu_sources_cached_2026.07.03.json` — 23-entry cached source inventory from `pcpartpicker_debug_page.html`; all cached references contain the `2026.07.03` URL date.
- `diagnostics/cached_july_2026_sources/` — 23 individual chart PNGs plus `contact_sheet.png`; every individual image is `1176×484`.
- `docs/CACHED_JULY_2026_VALIDATION.json` and `docs/CACHED_JULY_2026_EXTRACTION_REPORT.md` — document the saved chart set as approximately July 2026 coverage, with August and September not represented.
- `docs/SOURCE_REFRESH_20261022.md` and `docs/AUTHORIZED_SOURCE_ALTERNATIVE_20261022.md` — document the earlier live-access block and the provenance limits of the cached set.

The saved contact sheet was visually inspected at [`diagnostics/cached_july_2026_sources/contact_sheet.png`](../diagnostics/cached_july_2026_sources/contact_sheet.png), along with a native-resolution representative chart at [`diagnostics/cached_july_2026_sources/geforce_rtx_5090.png`](../diagnostics/cached_july_2026_sources/geforce_rtx_5090.png). The saved charts show labeled history through approximately June 2026 with the right edge representing approximately July 2026; no August or September segment is visible.

### Live official page

URL tested: `https://pcpartpicker.com/trends/price/video-card/`

Observed browser results:

1. Initial navigation showed `Just a moment...`, “Performing security verification,” and a Cloudflare Ray ID.
2. After the ordinary browser session completed its verification, the page title became `Video Card Price Trends - PCPartPicker`.
3. The page accessibility tree contained 23 GPU headings and 23 chart-image entries, from Arc A380 through Radeon RX 9070 XT.
4. The GeForce RTX 4070 chart opened in the official chart viewer. Its rendered trace differed from the locally saved July chart, establishing that newer live chart content can be observed in this session.
5. The browser surface did not expose the image `src` attributes or a native-resolution downloadable copy to this task. The scaled chart viewer did not make the final month labels readable enough for an auditable August/September determination.

The live page is therefore evidence of current accessibility and newer visual content, but not yet a verified 23-image source set.

### Existing Selenium setup

The repository spider remains `batch/spiders/pc_part_picker.py`. It detects Chrome major version 155 and passes that version to undetected-chromedriver.

A one-shot Selenium smoke attempt detected Chrome major `155`, but undetected-chromedriver could not bootstrap its patched driver because the environment refused the outbound driver-release connection (`WinError 10061`). It did not reach page navigation. This is separate from the in-app browser result above.

The local `bin/chromedriver.exe` is zero bytes and was not used as a valid driver. No driver or dependency was changed.

## All 23 saved source URL records

The URL date is metadata embedded in the CDN path; it is not treated as proof of the chart's latest visible month.

| GPU | URL date in production dataset | Cached July URL reference | Saved image |
|---|---:|---|---|
| Arc A380 | 2026.07.03 | 2026.07.03 | `arc_a380.png` |
| Arc A750 | 2026.07.03 | 2026.07.03 | `arc_a750.png` |
| Arc A770 | 2026.07.03 | 2026.07.03 | `arc_a770.png` |
| GeForce RTX 4070 | 2026.07.03 | 2026.07.03 | `geforce_rtx_4070.png` |
| GeForce RTX 4070 SUPER | 2026.07.03 | 2026.07.03 | `geforce_rtx_4070_super.png` |
| GeForce RTX 4070 Ti | 2026.03.03 | 2026.07.03 | `geforce_rtx_4070_ti.png` |
| GeForce RTX 4070 Ti SUPER | 2026.03.03 | 2026.07.03 | `geforce_rtx_4070_ti_super.png` |
| GeForce RTX 4080 | 2026.07.03 | 2026.07.03 | `geforce_rtx_4080.png` |
| GeForce RTX 4080 SUPER | 2026.07.03 | 2026.07.03 | `geforce_rtx_4080_super.png` |
| GeForce RTX 4090 | 2026.03.03 | 2026.07.03 | `geforce_rtx_4090.png` |
| GeForce RTX 5060 Ti | 2026.07.03 | 2026.07.03 | `geforce_rtx_5060_ti.png` |
| GeForce RTX 5070 | 2026.07.03 | 2026.07.03 | `geforce_rtx_5070.png` |
| GeForce RTX 5070 Ti | 2026.07.03 | 2026.07.03 | `geforce_rtx_5070_ti.png` |
| GeForce RTX 5080 | 2026.07.03 | 2026.07.03 | `geforce_rtx_5080.png` |
| GeForce RTX 5090 | 2026.07.03 | 2026.07.03 | `geforce_rtx_5090.png` |
| Radeon RX 7600 XT | 2026.07.03 | 2026.07.03 | `radeon_rx_7600_xt.png` |
| Radeon RX 7700 XT | 2026.07.03 | 2026.07.03 | `radeon_rx_7700_xt.png` |
| Radeon RX 7800 XT | 2026.07.03 | 2026.07.03 | `radeon_rx_7800_xt.png` |
| Radeon RX 7900 XT | 2026.07.03 | 2026.07.03 | `radeon_rx_7900_xt.png` |
| Radeon RX 7900 XTX | 2026.07.03 | 2026.07.03 | `radeon_rx_7900_xtx.png` |
| Radeon RX 9060 XT | 2026.07.03 | 2026.07.03 | `radeon_rx_9060_xt.png` |
| Radeon RX 9070 | 2026.07.03 | 2026.07.03 | `radeon_rx_9070.png` |
| Radeon RX 9070 XT | 2026.07.03 | 2026.07.03 | `radeon_rx_9070_xt.png` |

The full cached URL strings, including hashes, remain in `Monthly_Scraped_Data/pcpartpicker_gpu_sources_cached_2026.07.03.json`; they are not duplicated here to avoid creating a second source of truth.

## Files changed

Created:

- `docs/SOURCE_COVERAGE_INVESTIGATION_20261022.md` — this report.

No production dataset, calibration, extraction code, source manifest, cached image, or test file was modified. No new chart image was saved because the live browser surface did not provide an auditable native-resolution asset or URL export.

## Recommended next action

Use the now-accessible, authorized browser session to save the 23 live chart image assets or export their exact `src` URLs into a new, timestamped source-review directory. Then inspect the native-resolution x-axis of each image and record the latest supported month before any extraction. Until that evidence exists, keep the production cutoff at July 2026 and leave August/September unpopulated.
