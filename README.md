
# Pregnancy Data Analyzer with AI

A Python program to explore, visualize, and analyze pregnancy-related data using AI. Users can describe datasets, generate visualizations, ask AI questions, and save a report.

---

## Features

* Load preloaded dataset or upload your own CSV.
* Summarize data with column types, missing values, and numeric statistics.
* Generate visualizations: bar plots (feature correlation with RiskScore), pie charts (risk distribution), heatmaps (correlations).
* Ask AI questions about the dataset for insights.
* Save all outputs (descriptions, AI answers, visualizations) to a report.

---

## Requirements

* Python 3.8+
* Packages: `pandas`, `matplotlib`, `seaborn`, `openai`, `python-dotenv`, `reportlab`, `ext..`

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---

## Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/pregnancy-data-analyzer.git
cd pregnancy-data-analyzer
```

2. Add your OpenAI API key in a `.env` file in the project root:

```
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-5-nano
```

3. Place the default `pregnancy_data.csv` in the project folder, or upload your own CSV with these columns:

```
Age, BMI, BloodPressure, Week, Glucose, ActivityLevel, SleepHours, RiskScore
```

---

## How to Run

Run the program using Python:

```bash
python main.py
````

Menu options:

* **1 – Load data:** Load default or upload your dataset.
* **2 – Describe data:** Print dataset summary and save it to session log.
* **3 – Visualize data:** Generate bar plots, pie charts, and heatmaps. Images are saved automatically in the working directory.
* **4 – Ask AI:** Ask questions about your dataset. Answers are saved to session log.
* **5 – Save session:** Save all collected outputs (descriptions, AI Q\&A, visualizations) into a folder. A `session_log.md` file will be created with text outputs and images.
* **6 – Exit:** Close the program. Any unsaved temporary images will be deleted automatically.

```

## Notes

* Only numeric columns are considered for correlation and heatmap plots.
* Ensure the OpenAI API key is valid to use the AI features.
