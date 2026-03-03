import csv, json
from pathlib import Path

def extract_csv(path: str) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))
                    
def extract_json(path: str) -> list[dict]:
    with Path(path).open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else ["rows"]