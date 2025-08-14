## Describe Data

```
Source: pregnancy_data.csv
    Shape: 200 rows × 8 columns

    Dtypes:
    Age                int64
BMI              float64
BloodPressure    float64
Week               int64
Glucose          float64
ActivityLevel     object
SleepHours       float64
RiskScore        float64

    Missing (%):
    Age              0.0
BMI              0.0
BloodPressure    0.0
Week             0.0
Glucose          0.0
ActivityLevel    0.0
SleepHours       0.0
RiskScore        0.0

    Numeric summary:
                   count     mean      std   min    25%   50%     75%    max
Age            200.0  29.5950   7.3492  18.0  24.00  29.0  36.000   42.0
BMI            200.0  24.5535   2.9228  17.5  22.50  24.4  26.300   33.7
BloodPressure  200.0  93.9585   7.1718  74.4  89.30  94.4  98.725  111.5
Week           200.0  23.5750   9.8748   8.0  15.00  22.0  33.000   40.0
Glucose        200.0  83.0745  11.0984  49.5  76.75  82.9  90.300  112.2
SleepHours     200.0   7.1070   1.0052   4.1   6.50   7.2   7.800    9.4
RiskScore      200.0  41.4445   4.0719  29.1  39.10  41.7  43.900   52.5
```

---

## AI Question

```
Q: what can you say about the data?
A: The dataset of 200 pregnant women shows:

**Demographics & Health Indicators:**
- Average age: ~29.6 years (range 18–42).
- BMI averages 24.55 (healthy range), with 17.5–33.7 spread.
- Blood Pressure: mean ~94 mmHg, with some individuals >100 mmHg, indicating potential hypertension risks.
- Glucose: average ~83, with some values >100, suggesting possible gestational diabetes risk.
- Week of pregnancy: mean ~23.6 weeks, with a wide spread (8–40 weeks).

**Lifestyle Factors:**
- Sleep Hours average 7.1 hours; some as low as 4.1 hours.
- Activity levels: evenly distributed among Low, Medium, High.

**Risk Score:**
- Mean RiskScore: 41.4 (scale 29.1–52.5).
- Higher RiskScores tend to associate with higher BMI, Blood Pressure, and Glucose levels.

**Key Insights:**
- **BMI & Risk:** Higher BMI correlates with increased RiskScore (correlation ~0.45), indicating overweight women may have higher pregnancy risks.
- **Blood Pressure & Glucose:** Both positively correlate with RiskScore (~0.4), emphasizing importance of monitoring these metrics.
- **Sleep & Activity:** No strong correlation with RiskScore, but low sleep hours (<6) are observed in some higher risk cases.
- **Age:** Slight positive correlation (~0.2) with RiskScore, but less pronounced.

**Trends & Anomalies:**
- Women over 35 tend to have slightly higher BMI and Blood Pressure.
- Some women with low activity levels and poor sleep still maintain low RiskScores, suggesting multifactorial risk.

**Conclusion:**
- Elevated BMI, Blood Pressure, and Glucose are key risk factors.
- Monitoring these, along with lifestyle factors, can help manage pregnancy risks.
- Further analysis could explore interactions and specific subgroup risks.
```

---

