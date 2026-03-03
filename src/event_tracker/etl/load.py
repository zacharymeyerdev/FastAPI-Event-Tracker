import json, sqlite3
from pathlib import Path

def load_clean_events(db_path: str, events: list) -> int:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS etl_events(id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, label TEXT, category TEXT, value REAL, source TEXT)""")
    cur.executemany("""INSERT INTO etl_events(ts, label, category, value, source) VALUES (?, ?, ?, ?, ?)""", [(e.ts.isoformat(), e.label, e.category, e.value, e.source) for e in events])
    conn.commit()
    count = cur.rowcount
    conn.close()
    return count

def write_validation_report(out_path: str, report: dict) -> None:
    Path(out_path).write_text(json.dumps(report, indent=2), encoding="utf-8")