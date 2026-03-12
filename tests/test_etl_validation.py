from src.event_tracker.etl.validate import validate_rows

def test_validate_rows_flags_expected_issues():
    rows = [
        {"ts": "2026-01-21T10:00:00", "label": "click", "value": "100", "source": "manual"},
        {"ts": "2026-01-21T10:00:00", "label": "click", "value": "100", "source": "manual"}, # duplicate
        {"ts": "2026-01-21T11:00:00", "label": "signup", "value": "200", "source": ""}, # missing source
        {"ts": "2026-01-21T12:00:00", "label": "page_view", "value": "2000000", "source": "sensor"}, # out of range
        {"ts": "2026-01-21T13:00:00", "label": "page_view", "value": "abc", "extra": "x"}  # schema mismatch and not a number
    ]

    result = validate_rows(rows)
    summary = result["summary"]

    assert summary["missing_values"] == 2
    assert summary["duplicates"] == 1
    assert summary["out_of_range"] == 1
    assert summary["schema_mismatches"] == 2