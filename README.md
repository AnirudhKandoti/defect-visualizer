# 🧠 Defect Pattern Analysis & Visualization Tool

[![Made with Django](https://img.shields.io/badge/Made%20with-Django-green)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Prototype-success)]()

---

### 🎯 Overview
**Defect Pattern Analysis & Visualization Tool** is a data-driven Quality Assurance (QA) prototype that enables **risk-based testing** through **defect clustering and visualization**.  
It analyzes historical defect logs, detects recurring error patterns, and calculates module-level risk scores — helping QA teams prioritize testing on high-risk components.

---

### 🧩 Features
- 📂 CSV upload interface for defect logs  
- 🔍 TF-IDF + DBSCAN clustering of textual defect descriptions  
- 📊 Per-module **risk scoring** combining frequency, severity, and cluster diversity  
- 🌐 Interactive **Plotly** dashboards (bar chart, pie chart, and timeline heatmap)  
- 📈 Automatic trend analysis across modules and months  
- 💾 Sample dataset generator included  

---

### 🧠 Tech Stack
| Layer | Technology |
|-------|-------------|
| **Backend** | Django 4.2, Python 3.10 + |
| **Data Processing** | pandas, scikit-learn (TF-IDF, DBSCAN), numpy |
| **Visualization** | Plotly (interactive charts) |
| **Database** | SQLite 3 |
| **Frontend** | Django Templates + Bootstrap CSS |
| **Deployment Ready** | GitHub / Render / PythonAnywhere |

---

### 📁 Folder Structure
```
defect-visualizer/
│
├── defect_visualizer/ # Django project settings
│── qa_tool/ # Main app with analysis logic
│ ├── analysis.py # TF-IDF, DBSCAN, risk scoring, Plotly
│ ├── views.py # Upload & dashboard endpoints
│ ├── templates/qa_tool/ # HTML templates
│ └── static/sample_defects.csv
│
├── sample_data/ # Data generator script
├── requirements.txt
└── README.md

```
---

### 🧾 Data Format
The tool expects a `.csv` file with the following columns:

| Column | Description |
|---------|-------------|
| `id` | Unique defect ID |
| `module` | Module/component name |
| `severity` | Low / Medium / High / Critical |
| `error_type` | Type/category of defect |
| `description` | Textual description of the defect |
| `occurrence_date` | Date of defect occurrence (`YYYY-MM-DD`) |

A **sample dataset** is included at `qa_tool/static/sample_defects.csv`.

---

### ⚙️ Setup & Run Locally
```bash
# 1️⃣ Clone repository
git clone https://github.com/<your-username>/defect-visualizer.git
cd defect-visualizer

# 2️⃣ Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate          # on Windows: .venv\Scripts\activate

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Apply migrations and run sample generator
python manage.py migrate
python sample_data/generate_sample_data.py

# 5️⃣ Start the Django server
python manage.py runserver

```
Then open http://127.0.0.1:8000/
 in your browser.

📊 Output Preview

Bar Chart: module-wise risk scores

Pie Chart: cluster distribution (DBSCAN results)

Heatmap: monthly defect trends per module

Table: top modules ranked by computed risk score

Cluster Summary: representative text of top defect clusters

🧮 Risk Score Formula

The risk score for each module is computed as:


R=normalized((D×S)×(1+C))

Where:

D = Number of defects

S = Average severity weight (Low=1, Medium=2, High=4, Critical=8)

C = Unique clusters associated with that module

💡 Future Improvements

Integrate SentenceTransformer embeddings for semantic clustering

Implement anomaly detection for rare high-impact defects

Add PDF/CSV export and advanced filters

Automate data ingestion from JIRA / GitHub Issues APIs

📜 License

MIT License © 2025 Kandoti Venkata Anirudh Sankarshan


