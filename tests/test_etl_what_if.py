from datetime import datetime

import pytest

from src.event_tracker.etl.models import CanonicalEvent
from src.event_tracker.etl.what_if import run_what_if

def test_run_what_if_delta_math():
    events = [
        CanonicalEvent(ts=datetime(2026, 1, 21, 10, 0, 0), label="click", category="engagement", value=100.0, source="manual"),
        CanonicalEvent(ts=datetime(2026, 1, 21, 11, 0, 0), label="signup", category="conversion", value=200.0, source="manual"),
        CanonicalEvent(ts=datetime(2026, 1, 21, 12, 0, 0), label="page_view", category="navigation", value=50.0, source="sensor")
    ]

    result = run_what_if(events, {"engagement": 1.2, "conversion": 1.0, "navigation": 1.0})

    assert result["baseline"]["total_value"] == 350.0
    assert result["scenario"]["total_value"] == 370.0
    assert result["delta_total"] == 20.0
    assert result["delta_pct"] == pytest.approx((20.0 / 350.0) * 100)