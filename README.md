# ✈️ Flight Data Quality Pipeline (CLI)

A production-style data engineering mini-project: ingest flight data (CSV), validate it with **Pandera**, export to **Parquet**, and generate a **data quality report** with an optional **quality gate** (fail the pipeline if thresholds are exceeded).

---

## ✅ Key Features

- **Ingest** CSV flight data
- **Clean & standardize** (string normalization, null handling)
- **Validate** schema + business rules with **Pandera**
- **Export** clean dataset to **Parquet**
- **Report** quality metrics (missing rates, top airlines/routes)
- **Quality Gate**: fail with non-zero exit code if thresholds are exceeded
- **Tests** with Pytest
- **CI** with GitHub Actions

---

## 🏗 Project Structure

```text
Flight-Data-Quality-Pipeline-CLI/
├── src/flight_pipeline/
│   ├── cli.py
│   ├── schema.py
│   ├── transform.py
│   ├── quality.py
│   └── io.py
├── tests/
├── data/raw/flights_sample.csv
├── pyproject.toml
└── .github/workflows/ci.yml
```

## 📦 Installation

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
# source .venv/bin/activate

pip install -U pip
pip install -e .
```

## 🚀 Usage

1) Run pipeline (CSV → Parquet)

```bash
python -m flight_pipeline.cli run -i data/raw/flights_sample.csv -o data/processed/flights.parquet
```

2) Generate quality report (console + Markdown)

```bash
python -m flight_pipeline.cli report -i data/processed/flights.parquet -o reports/quality_report.md
```

3) Quality gate (fail if quality is below threshold)

```bash
python -m flight_pipeline.cli report \
  -i data/processed/flights.parquet \
  --fail-if-cancelled-rate 0.30 \
  --fail-if-missing-actual-dep 0.20
```

## 🧪 Testing

```bash
python -m pytest -vv
```

## 🔄 Continuous Integration

GitHub Actions runs the test suite automatically on each push and pull request.
