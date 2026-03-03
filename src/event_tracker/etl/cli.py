import argparse, json
from .pipeline import run_pipeline

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input-csv", required=True)
    p.add_argument("--db-path", required=True)
    p.add_argument("--report-path", required=True)
    p.add_argument("--multipliers-json", default="{}")
    args = p.parse_args()

    result = run_pipeline(input_csv=args.input_csv, db_path=args.db_path, report_path=args.report_path, multipliers=json.loads(args.multipliers_json))
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()