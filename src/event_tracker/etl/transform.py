from datetime import datetime
from .models import CanonicalEvent

LABEL_TO_CATEGORY = {"crack": "damage", "rust": "corrosion", "note": "observation"}

def transform_rows(rows: list[dict]) -> list[CanonicalEvent]:
    out = []
    for r in rows:
        ts = datetime.fromisoformat(r["ts"])
        label = str(r["label"]).strip().lower()
        category = LABEL_TO_CATEGORY.get(label, "other")
        value = float(r["value"])
        out.append(CanonicalEvent(ts=ts, label=label, category=category, value=value, source=r.get("source")))
    return out