# ✈️ Flight Data Quality Pipeline (CLI)

A production-style **Data Engineering mini-project**.

This project ingests flight data (CSV), cleans and validates it using **Pandera**, exports it to **Parquet**, and generates a **data quality report** with an optional **quality gate** that can fail the pipeline.

---

## 🧠 Why This Project?

This project demonstrates key Data Engineering concepts:

- Schema validation & data contracts (Pandera)
- Batch processing pipeline (CSV → Clean → Validate → Parquet)
- Data quality monitoring
- Quality gate with non-zero exit codes (CI/CD ready)
- Automated testing (Pytest)
- Dockerized execution
- CI with GitHub Actions

---

## 🏗 Architecture

CSV Input
↓
Cleaning & Standardization
↓
Schema Validation (Pandera)
↓
Parquet Export
↓
Quality Report + Optional Quality Gate

---

## 🏗 Project Structure

```text
Flight-Data-Quality-Pipeline-CLI/
├── src/flight_pipeline/
│ ├── cli.py # CLI interface (Typer)
│ ├── schema.py # Pandera validation schema
│ ├── transform.py # Cleaning & normalization
│ ├── quality.py # Data quality metrics
│ └── io.py # CSV / Parquet I/O
├── tests/
├── data/raw/flights_sample.csv
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── .github/workflows/ci.yml
```

---

## 🚀 Run Locally

### 1️⃣ Create virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
# source .venv/bin/activate

pip install -U pip
pip install -e .
```

### 2️⃣ Run pipeline

```bash
python -m flight_pipeline.cli run \
  -i data/raw/flights_sample.csv \
  -o data/processed/flights.parquet
```

### 3️⃣ Generate quality report

```bash
python -m flight_pipeline.cli report \
  -i data/processed/flights.parquet \
  -o reports/quality_report.md
```

## 🚦 Quality Gate (CI/CD Ready)
Fail the pipeline if data quality thresholds are exceeded:

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
Test coverage includes:
- Schema validation
- Cleaning logic
- Quality metrics
- Quality gate behavior

## 🐳 Run with Docker

Build:
```bash
docker compose build
```
Run pipeline:
```bash
docker compose run --rm flight-pipeline run \
  -i data/raw/flights_sample.csv \
  -o data/processed/flights.parquet
```
Generate report:
```bash
docker compose run --rm flight-pipeline report \
  -i data/processed/flights.parquet \
  -o reports/quality_report.md
```
## 🔄 Continuous Integration

GitHub Actions automatically runs the test suite on every push and pull request.

Add CI badge:
```code
![CI](https://github.com/USERNAME/REPO/actions/workflows/ci.yml/badge.svg)
```

## 📈 Potential Improvements

- Partitioned Parquet output (data lake style)
- JSON metrics export for monitoring systems
- Airflow orchestration example
- Integration with object storage (S3-compatible)
