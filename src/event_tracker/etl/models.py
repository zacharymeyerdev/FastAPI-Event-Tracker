from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass(frozen=True)
class CanonicalEvent:
    ts: datetime
    label: str
    category: str
    value: float
    source: Optional[str] = None

EXPECTED_COLUMNS = {"ts", "label", "value", "source"}
ALLOWED_LABELS = {"crack", "rust", "note"}
VALUE_RANGE = (0.0, 1_000_000.0)