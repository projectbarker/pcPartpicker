# Decision Register

## D-001 — Keep Selenium browser collection

- Problem: the trends page is dynamically rendered.
- Options: requests-only HTML, Playwright, or the existing Selenium/undetected-chromedriver approach.
- Chosen: keep the existing browser approach and add explicit waits, validation, deduplication, and clean shutdown.
- Rationale: smallest change consistent with the observed project and current HTML.
- Trade-off: browser startup is slower and depends on Chrome/driver compatibility.
- Classification: evidence-based conclusion.
- Affected: `batch/spiders/pc_part_picker.py`.
- Validation: source inspection and import/compile checks; live browser collection remains an external-run step.

## D-002 — Use July 2024 through January 2026

- Problem: the extractor needs a fixed monthly schema.
- Chosen: preserve the existing 19-month range found in the prompt and output.
- Classification: evidence-based conclusion, not a new business approval.
- Risk: newer chart images may include later months, but those are outside the requested schema.
- Affected: `EXPECTED_MONTHS`, prompt, output validation.

## D-003 — Treat chart reading as observation, not exact ground truth

- Problem: the source is a raster chart whose line can fall between gridlines or be obscured.
- Chosen: use only the black actual-price line, interpolate only when reasonably supported, and use `N/A` otherwise.
- Classification: evidence-based interpretation from the existing prompt; ambiguous points require human review.

## D-004 — Make all-`N/A` output failed

- Problem: the previous run returned HTTP 200 and valid JSON but no useful prices and was marked successful.
- Chosen: `success` requires all 19 numeric values; some numeric values are `partial`; no numeric values are `failed`.
- Affected: parser, extractor, summary, documentation.
- Validation: automated tests cover complete, partial, missing, malformed, and invalid values.

## D-005 — Use bounded API retries

- Problem: transient API errors should not abort the whole run, but malformed model output should not cause endless retries.
- Chosen: retry API-call exceptions twice after the initial attempt; parse failures return `failed` immediately.
- Classification: engineering decision.

## D-006 — Preserve schema and add status quality

- Chosen: retain `gpu_model_name`, `image_url`, and `price_trend`; add reliable `extraction_status` semantics rather than redesigning the data model.
- Classification: engineering decision.

## D-007 — Back up and atomically write outputs

- Problem: the prior one-GPU experiment overwrote the historical target file.
- Chosen: timestamped backup followed by temporary-file replacement.
- Classification: engineering decision.
- Validation: automated backup/write test.

## D-008 — Keep API cost controlled

- Chosen: support `--limit 1` and require human confirmation before a 23-GPU live batch. No full live batch has been run in this handover yet.
- Classification: pending user approval for the API-consuming batch.

## D-009 — Remove unused Scrapy network integrations

- Problem: old settings enabled Playwright/ScrapeOps components that were not used by the Selenium spider and were absent from the environment.
- Chosen: minimal settings with no downloader middleware or Playwright handler.
- Trade-off: future Scrapy request-based spiders would need their own settings.
- Affected: `batch/settings.py`, `requirements.txt`.

## D-010 — Do not expose secrets

- Chosen: retain environment-variable loading for OpenAI credentials, add `.gitignore`, and remove active hardcoded proxy settings from the runtime settings.
- Remaining action: rotate any credentials that may have been shared previously.

## D-011 — Pause the full batch after the controlled live test

- Evidence: Arc A380's image was reachable and the OpenAI API returned HTTP 200, but the model supplied no usable numeric monthly values under the conservative prompt.
- Chosen: classify the test as `failed` and pause the 23-GPU batch.
- Why: a larger run would multiply API cost without demonstrating that the extraction semantics produce useful data.
- Pending user decision: whether visually estimated chart readings should be accepted as numeric observations with an explicit estimate marker, or whether only highly confident readings should be retained.

## D-012 — Approved visual-estimation policy

- Chosen: accept visually estimated monthly values only when the axes, month boundary, and black line are clear; label them `estimated`, round to the nearest whole USD while retaining two-decimal strings, and require human review.
- Missing history, gaps, ambiguous points, and unclear axes remain `N/A`.
- Affected: prompt, parser, output fields, tests, and review workflow.
- Classification: user-approved decision from the project policy brief.
- Validation: automated parser tests added; three-GPU live sample is the remaining evidence gate.

## D-013 — Direct vision is not sufficient for production

- Evidence: three live chart calls returned two false missing-history interpretations and one suspicious uniform numeric sequence that disagreed with manual chart anchors.
- Chosen: do not run the 23-GPU batch; implement and evaluate a minimal coordinate-calibration prototype before production extraction.
- Classification: evidence-based conclusion from the three-GPU sample.
- Remaining decision: user review of the prototype evidence and approval of its manual validation criterion before production use.

## D-014 — Use a Pillow coordinate-calibration prototype

- Chosen: detect per-image gridlines with Pillow, map monthly x positions from a visible date anchor, map y pixels using visible sample-specific USD tick labels, and trace dark pixels for the black line.
- Why: it improves consistency without adding OpenCV/OCR before evidence justifies those dependencies.
- Trade-offs: sample tick/date anchors are currently manually supplied; black spikes can still confuse the sampler; every estimated value remains review-required.
- Validation: 18 automated tests pass; three calibrated sample outputs and overlay/calibration artifacts were produced.
- Classification: engineering prototype based on current evidence.
- Future reconsideration: add OCR or OpenCV only if explicit calibration metadata cannot scale safely.

## D-015 — Prefer continuity-aware component selection

- Evidence: the first coordinate prototype averaged dark rows in a local x-window, allowing vertical spikes and month-boundary artifacts to displace the black actual-price line.
- Chosen: inspect connected black components, score horizontal support and local continuity, reject isolated vertical spikes, and preserve `N/A` for ambiguity or missing segments.
- Rationale: this is the smallest change that improves consistency without adding OpenCV or OCR.
- Validation: 24 tests pass; the three-GPU continuity sample was rerun into a separate output and produced inspectable overlays.
- Status: still a validation prototype; no production readiness claim and no full batch run.
