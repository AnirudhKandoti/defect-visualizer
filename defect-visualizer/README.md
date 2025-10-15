# Defect Pattern Analysis & Visualization Tool

**Short:** Django app that ingests defect logs (CSV), clusters similar defect descriptions using TF-IDF + DBSCAN, computes per-module risk scores (frequency × severity × cluster diversity), and visualizes results using Plotly.

**Purpose:** Prototype for risk-based testing and QA analytics — aligns with thesis/project: *Risk-based testing through data analysis in Quality Assurance*.

## Features
- CSV upload of defect logs
- TF-IDF vectorization + DBSCAN clustering of descriptions
- Per-module risk scoring and ranking
- Interactive Plotly charts embedded in templates
- Sample dataset generator included

## Data format (CSV)
Required columns:

id,module,severity,error_type,description,occurrence_date


## Quickstart (local dev)
```bash
python -m venv .venv
source .venv/bin/activate         # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python sample_data/generate_sample_data.py   # generates sample_defects.csv
python manage.py runserver
# open http://127.0.0.1:8000/
