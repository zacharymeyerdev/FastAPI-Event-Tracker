import csv
import io
from typing import Any

def events_to_csv(events: list[dict]) -> str:
    """Convert a list of event dictionaries to a CSV string"""
    if not events:
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["id", "ts", "label", "description", "x", "y", "source"])
        writer.writeheader()
        return output.getvalue()
    
    output = io.StringIO()
    fieldnames = ["id", "ts", "label", "description", "x", "y", "source"]
    writer = csv.DictWriter(output, fieldnames=fieldnames)

    writer.writeheader()
    for event in events:
        writer.writerow(event)
    
    return output.getvalue()