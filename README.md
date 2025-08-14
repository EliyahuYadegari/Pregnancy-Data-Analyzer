
# Pregnancy Data Analyzer with AI

A Python program to explore, visualize, and analyze pregnancy-related data using AI. Users can describe datasets, generate visualizations, ask AI questions, and save a report as a PDF.

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
* Packages: `pandas`, `matplotlib`, `seaborn`, `openai`, `python-dotenv`, `reportlab`

Install dependencies with:

```bash
pip install pandas matplotlib seaborn openai python-dotenv reportlab
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
```


* **1 – Load data:** Load default or upload your dataset.
* **2 – Describe data:** Print dataset summary.
* **3 – Visualize data:** Generate bar plots, pie charts, and heatmaps.
* **4 – Ask AI:** Ask questions about your dataset.
* **5 – Save report:** Save collected outputs and plots to a PDF file.
* **6 – Exit:** Close the program.

---

## Notes

* Only numeric columns are considered for correlation and heatmap plots.
* PDF report includes all descriptions, AI Q\&A, and generated plots.
* Ensure the OpenAI API key is valid to use the AI features.
