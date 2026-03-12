# SOP: ETL Pipeline Operations, Data Quality Checks, and What-If Analysis

## 1. Purpose
This SOP defines how to run the Python ETL workflow that ingests structured event data, standardizes it into a canonical schema, applies validation checks, and generates baseline plus what-if summary outputs.

## 2. Scope
In scope:
- CSV-based ETL ingestion.
- Standardization into a canonical event schema.
- Validation checks for missing values, duplicates, schema mismatches, and out-of-range numeric values.
- Baseline and what-if summary comparisons.

Out of scope (current implementation):
- Automated dashboard deployment/hosting.
- Multi-source orchestration beyond CSV in the pipeline entrypoint.

Intended users:
- Project owner.
- New collaborator taking over ETL reruns.

## 3. Inputs and Prerequisites
Data sources:
- Structured CSV file with columns: `ts`, `label`, `value`, `source`.

Required environment:
- Python 3.10+
- Installed dependencies from project environment.

Working directory:
- Run commands from repository root.

Required CLI parameters:
- `--input-csv`: path to input CSV file.
- `--db-path`: path to SQLite database for cleaned rows.
- `--report-path`: path to JSON validation report output.
- `--multipliers-json`: JSON object mapping category names to numeric factors for what-if runs.

Example command:

```bash
python -m src.event_tracker.etl.cli \
	--input-csv data/input/events.csv \
	--db-path data/output/etl_events.db \
	--report-path data/output/validation_report.json \
	--multipliers-json "{\"damage\": 1.10, \"corrosion\": 0.95}"
```

## 4. Canonical Schema
Canonical event model fields:
- `ts`: datetime
- `label`: string
- `category`: string
- `value`: float
- `source`: optional string

Expected raw input columns:
- `ts`, `label`, `value`, `source`

Allowed labels (reference set):
- `crack`, `rust`, `note`

Numeric range constraints:
- `value` must be within `[0.0, 1_000_000.0]`.

## 5. Metric Definitions
Baseline metrics:
- `total_value`: sum of `value` across all standardized rows.
- `category_totals`: sum of `value` grouped by `category`.
- `row_count`: number of standardized rows.

What-if metrics:
- `scenario.total_value`, `scenario.category_totals`, `scenario.row_count` after multipliers are applied.
- `delta_total`: scenario total minus baseline total.
- `delta_pct`: percentage change from baseline total.

## 6. Transformation Rules
Source columns are transformed as follows:
- `ts`: parsed from ISO-like string into datetime.
- `label`: normalized with trim + lowercase.
- `category`: mapped by label:
	- `crack` -> `damage`
	- `rust` -> `corrosion`
	- `note` -> `observation`
	- Unknown label -> `other`
- `value`: cast to float.
- `source`: carried forward as optional string.

## 7. Data Quality Validation Rules
Validation categories and behavior:
- Missing values:
	- For each expected column, flag row if value is `None` or empty string.
- Duplicates:
	- Flag repeated tuples of (`ts`, `label`, `value`, `source`).
- Schema mismatches:
	- Flag rows whose key set differs from expected columns.
	- Flag non-numeric `value` conversion failures.
- Out-of-range values:
	- Flag numeric `value` outside `[0.0, 1_000_000.0]`.

Validation output:
- Row-level issue lists for each validation type.
- `summary` object containing counts by issue type.

## 8. Baseline Run Procedure
1. Prepare input CSV with required columns.
2. Run ETL CLI with `--multipliers-json "{}"` for baseline.
3. Confirm command exits successfully and prints JSON result.
4. Verify outputs:
	 - SQLite table `etl_events` created/updated at `--db-path`.
	 - Validation report JSON written at `--report-path`.
	 - Console JSON contains `loaded_rows`, `validation`, and `what_if.baseline`.

## 9. What-If Run Procedure
1. Select scenario assumptions as category multipliers.
2. Re-run ETL CLI with non-empty `--multipliers-json`.
3. Compare in command output:
	 - `what_if.baseline`
	 - `what_if.scenario`
	 - `what_if.delta_total`
	 - `what_if.delta_pct`
4. Record assumptions and resulting deltas for decision support notes.

## 10. Outputs and Artifacts
Generated artifacts per run:
- Clean standardized rows in SQLite table `etl_events`.
- Validation JSON report at specified report path.
- Console JSON summary including:
	- loaded row count
	- validation summary counts
	- baseline and scenario metrics
	- delta values

Recommended output storage layout:
- `data/input/` for source files.
- `data/output/` for DB and validation reports.
- `data/output/scenarios/` for scenario snapshots.

## 11. Troubleshooting
Common failure cases:
- Missing required CSV columns:
	- Symptom: high `schema_mismatches` counts.
	- Action: confirm exact column names (`ts`, `label`, `value`, `source`).
- Invalid timestamp format:
	- Symptom: transform stage failure during datetime parsing.
	- Action: convert `ts` values to ISO format (e.g., `2026-01-21T12:00:00`).
- Non-numeric value field:
	- Symptom: `schema_mismatches` entries with `value` conversion issue.
	- Action: clean source data and rerun.
- Invalid JSON for multipliers:
	- Symptom: CLI parse error.
	- Action: pass valid JSON object string.

Rerun policy:
- Reruns are allowed after fixing source data issues.
- Keep report files from each run to preserve audit trail.

## 12. Handoff Checklist
- Input source path and version/date documented.
- CLI command used for baseline recorded.
- CLI command used for scenario recorded.
- Validation report reviewed and accepted.
- Baseline vs scenario deltas documented.
- Output artifact paths shared with next owner.
