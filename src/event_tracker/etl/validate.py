from collections import Counter
from .models import EXPECTED_COLUMNS, VALUE_RANGE

def validate_rows(rows: list[dict]) -> dict:
    issues = {"missing_values": [], "duplicates": [], "schema_mismatches": [], "out_of_range": []}
    seen = Counter()

    for i, r in enumerate(rows):
        cols = set(r.keys())
        if cols != EXPECTED_COLUMNS:
            issues["schema_mismatches"].append({"row": i, "expected": sorted(EXPECTED_COLUMNS), "actual": sorted(cols)})
    
        for k in EXPECTED_COLUMNS:
            if r.get(k) in (None, ""):
                issues["missing_values"].append({"row": i, "column": k})

        key = (r.get("ts"), r.get("label"), r.get("value"), r.get("source"))
        seen[key] += 1
        if seen[key] > 1:
            issues["duplicates"].append({"row": i, "key": key})

        try:
            v = float(r.get("value"))
            if not (VALUE_RANGE[0] <= v <= VALUE_RANGE[1]):
                issues["out_of_range"].append({"row": i, "value": v, "range": VALUE_RANGE})
        except Exception:
            issues["schema_mismatches"].append({"row": i, "column": "value", "issue": "not a number"})

    issues["summary"] = {k: len(v) for k, v in issues.items() if isinstance(v, list)}
    return issues