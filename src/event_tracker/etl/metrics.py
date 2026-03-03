def summarize(events:list) -> dict:
    total = sum(e.value for e in events)
    by_category = {}
    for e in events:
        by_category.setdefault(e.category, 0.0)
        by_category[e.category] += e.value
    return {"total_value": total, "category_totals": by_category, "row_count": len(events)}