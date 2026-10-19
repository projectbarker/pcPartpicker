# Product Knowledge Quiz

Attempt the questions before reading the answer key.

## Questions

1. Multiple choice: What does a PCPartPicker trend image contain?  
   A. A transaction-level database export  B. A visual history of average video-card pricing  C. A list of retailer inventory IDs  D. A GPU benchmark result

2. Short answer: Which two fields does the scraper place in `pcpartpicker_gpu_trends.json`?

3. Multiple choice: Which line is used for extraction?  
   A. Blue range lines  B. Shaded area  C. Thick black actual-price line  D. Watermark

4. Short answer: Why can a chart image support only an approximate monthly observation?

5. Multiple choice: What does `--limit 1` do?  
   A. Deletes all but one input record  B. Runs one controlled extraction without changing the input  C. Forces one retry  D. Changes the date range

6. Short answer: Why is an HTTP 200 response not enough to mark extraction successful?

7. Multiple choice: Which status means some months have numeric values and others are `N/A`?  
   A. success  B. partial  C. failed  D. skipped

8. Short answer: What is the purpose of `EXPECTED_MONTHS`?

9. Scenario: The model returns valid JSON containing only `N/A`. What status should be written and why?

10. Scenario: The image URL returns HTML with status 200. What should happen?

11. Multiple choice: Where should the OpenAI key live?  
   A. Python source  B. README  C. `.env` or process environment  D. JSON output

12. Short answer: What does the temporary-file replacement protect against?

13. Scenario: `scrapy` fails because the browser driver cannot start. Name two useful checks.

14. Short answer: Why are mocked API tests useful here?

15. Multiple choice: Which file explains the actual implemented commands and recovery flow?  
   A. `DECISIONS.md`  B. `WORKFLOW.md`  C. `requirements.txt`  D. `items.py`

16. Short answer: What is the difference between `observed` and `estimated` in `price_quality`?

17. Scenario: A month has a clear line but it lies between USD gridlines. What should the extractor do?

18. Multiple choice: Which status is appropriate when numeric values exist but at least one is estimated?  
   A. success  B. partial  C. needs_review  D. failed

19. Scenario: A model returns 19 numeric values in a neat repeated pattern, but the black chart line visibly disagrees. What should you do?

20. Scenario: A monthly x-window contains a thin vertical black spike and a horizontally supported line candidate. Which evidence should control selection?

21. Scenario: Two disconnected candidates have comparable horizontal support and no reliable neighboring line. What should the extractor return?

## Answer key

1. B. It is a visual history, not a row-level transaction export.
2. `gpu_model` and `image_url`.
3. C. The prompt explicitly ignores range lines, projections, annotations, and watermarks.
4. Pixels, line thickness, grid spacing, and chart resolution limit precision; some points fall between gridlines or are obscured.
5. B. It selects the first record for a controlled API test and leaves the source unchanged.
6. The request can succeed while the model returns malformed, empty, or entirely unusable values.
7. B, `partial`.
8. It defines the 19 required chronological month keys from 2024-07-01 through 2026-01-01.
9. `failed`, because there are no usable numeric observations.
10. Mark the image validation failed, write a failed record with `N/A`, and continue safely.
11. C. Never place secrets in source, documentation, or outputs.
12. It prevents a failed write from leaving a partially written final JSON file.
13. Check Chrome installation/version, driver compatibility, and run with `headless=false` to observe startup; also inspect the error log.
14. They test parsing, statuses, retries, and backups without API cost or nondeterministic model responses.
15. B, `WORKFLOW.md`.
16. `observed` is directly readable from a clear line/gridline level; `estimated` uses clear-axis interpolation and must be reviewed.
17. Return a nearest-dollar estimate in `price_trend`, mark its quality `estimated`, and require review.
18. C, `needs_review`.
19. Do not accept the output as production data. Preserve the diagnostic, mark it for review, compare against manual anchors, and use coordinate calibration if direct vision remains unreliable.
20. The horizontally supported connected component and neighboring line continuity should control selection; the isolated spike should be rejected and recorded in diagnostics.
21. Return `N/A` with an ambiguity review reason. Do not guess, smooth, or interpolate across the conflict.

## Scoring

16–18: ready to run and troubleshoot the pipeline independently. 13–15: operationally comfortable; review chart semantics and recovery. 9–12: revisit the workflow and run the one-GPU test with supervision. Below 9: review the answer key, then trace one record from input to output.

After completing the quiz, you should be able to run a one-GPU test, explain every output field, distinguish API success from extraction success, recover a previous output, identify when human chart review is required, and recognize when direct vision needs coordinate-based validation.
