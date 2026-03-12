import csv
import json

from src.event_tracker.etl.pipeline import run_pipeline

def test_run_pipeline_creates_outputs(tmp_path):
    input_csv = tmp_path / "events.csv"
    db_path = tmp_path / "etl.db"
    report_path = tmp_path / "validation.json"

    with input_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["ts", "label", "value", "source"])
        writer.writeheader()
        writer.writerow({"ts": "2026-01-21T10:00:00", "label": "click", "value": 100, "source": "manual"})
        writer.writerow({"ts": "2026-01-21T11:00:00", "label": "page_view", "value": 50, "source": "sensor"})

    result = run_pipeline(input_csv=str(input_csv), db_path=str(db_path), report_path=str(report_path), multipliers={"engagement": 1.2})

    assert result["loaded_rows"] == 2
    assert report_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["summary"]["missing_values"] == 0
    assert report["summary"]["duplicates"] == 0
    assert report["summary"]["schema_mismatches"] == 0
    assert report["summary"]["out_of_range"] == 0

    assert "baseline" in result["what_if"]
    assert "scenario" in result["what_if"]
    assert "delta_total" in result["what_if"]
    assert result["what_if"]["delta_total"] > 0