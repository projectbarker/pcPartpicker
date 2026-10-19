"""Run the frozen Step 9 pilot against verified local source PNGs only."""

import json
from pathlib import Path
from unittest.mock import patch

from coordinate_calibration_runner import process_record
from gpu_trends_image_extraction import backup_and_write, load_gpu_records


ROOT = Path(__file__).parent
INPUT_PATH = ROOT / "step9_pilot_input.json"
CALIBRATION_PATH = ROOT / "step9_pilot_calibration.json"
ARTIFACT_DIR = ROOT / "diagnostics" / "step9_seven_gpu_pilot"
OUTPUT_PATH = ROOT / "Monthly_Scraped_Data" / "pcpartpicker_gpu_trends_step9_seven_gpu_pilot.json"


class LocalResponse:
    def __init__(self, content: bytes):
        self.content = content

    def raise_for_status(self) -> None:
        return None


def main() -> int:
    input_records = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    configs = json.loads(CALIBRATION_PATH.read_text(encoding="utf-8"))
    records = load_gpu_records(INPUT_PATH)
    if len(records) != 7 or {record["gpu_model"] for record in records} != set(configs):
        raise ValueError("Step 9 pilot input/configuration does not contain exactly the frozen seven records")

    def local_get(url: str, **_kwargs: object) -> LocalResponse:
        item = next(record for record in input_records if record["image_url"] == url)
        return LocalResponse((ROOT / item["local_source_path"]).read_bytes())

    results = []
    with patch("coordinate_calibration_runner.requests.get", side_effect=local_get):
        for item in records:
            results.append(process_record(item, configs[item["gpu_model"]], ARTIFACT_DIR))
    backup_and_write(results, OUTPUT_PATH)
    summary = {
        "records": len(results),
        "statuses": {status: sum(record["extraction_status"] == status for record in results) for status in ("success", "partial", "needs_review", "failed")},
        "numeric_monthly_values": sum(value != "N/A" for record in results for value in record["price_trend"].values()),
        "missing_monthly_values": sum(value == "N/A" for record in results for value in record["price_trend"].values()),
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
