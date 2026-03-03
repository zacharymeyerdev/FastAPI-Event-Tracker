from dataclasses import replace
from .metrics import summarize

def run_what_if(events:list, category_multipliers: dict[str, float]) -> dict:
    baseline = summarize(events)
    adjusted = []
    for e in events:
        factor = category_multipliers.get(e.category, 1.0)
        adjusted.append(replace(e, value=e.value * factor))
    scenario = summarize(adjusted)

    delta_total = scenario["total_value"] - baseline["total_value"]
    pct = (delta_total / baseline["total_value"] * 100.0) if baseline["total_value"] else 0.0
    return {"baseline": baseline, "scenario": scenario, "delta_total": delta_total, "delta_pct": pct}