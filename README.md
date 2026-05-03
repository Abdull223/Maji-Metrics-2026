# 🚰 Maji Metrics: Predictive Maintenance for Water Infrastructure
### **Live Web App:** [https://predictive-maintenance-equitable-water-infrastructure-group-2.streamlit.app/](https://predictive-maintenance-equitable-water-infrastructure-group-2.streamlit.app/)

*Strategic Focus on **SDG 6: Clean Water and Sanitation***

---

## Project Overview
In rural Kenya, water infrastructure failure is a silent crisis that disrupts thousands of lives daily. Research indicates that approximately **30% of rural water points in sub-Saharan Africa** are non-functional at any given time, leading to "sunk costs" for donors and a loss of basic services for communities.

**The Solution:** This project transforms water point maintenance from **reactive** (repairing after failure) to **proactive** (predicting failure). Using the **Kenya Water Points Dataset (WPdx)**, we developed a data-driven predictive roadmap to help government agencies and NGOs ensure consistent and reliable water access.

---

## The Project Team
*   **Abdullahi Abdi Hassan (Lead Statistics):** Responsible for statistical validation, baseline modeling, and defining the **0.2 mathematical threshold**.
*   **Claire (Data Architect):** Managed high-volume data ingestion and intensive initial cleaning of the **21,300+ record** dataset.
*   **Yvonne (Feature Engineer):** Created domain-specific features, such as **infrastructure age** and standardized management categories.
*   **Dahir (ML Engineer):** Implemented the **CatBoost Champion model** and performed hyperparameter optimization.
*   **Lauren (Visualization Specialist):** Designed technical charts and **geospatial risk hotspot visualizations** across Kenya's 47 counties.
*   **Samantha (Pipeline Engineer):** Developed the end-to-end **automated Python pipeline** for deployment.

---

## Data & Methodology

### 1. Data Profile
*   **Source:** [WPdx Kenya Dataset](https://data.waterpointdata.org/dataset/Kenya-Data/e2gs-xfxf)
*   **Scope:** 21,300+ entries covering diverse technologies and regional patterns across all **47 counties in Kenya**.

### 2. Key Insights (EDA)
*   **Technology Risk:** **Motorized Pumps** exhibit the highest failure rates, nearing 100% in certain sub-groups.
*   **Resilient Tech:** **Public Tapstands** remain the most resilient technology across the dataset.
*   **Geospatial Trends:** Significant failure clusters were identified in **Western Kenya** and the **Nairobi** outskirts.

### 3. Modeling Strategy
We used a tiered approach to ensure stability and interpretability:
*   **Baseline:** Logistic Regression to quantify linear relationships.
*   **Advanced Ensembles:** Random Forest, XGBoost, and **CatBoost**.

---

## Model Evaluation

| Model Architecture | Mean ROC-AUC | Mean Accuracy | Mean Recall (Broken) | Mean Precision (Broken) | Stability ($\sigma$) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **CatBoost (Champion)** | **0.9687** | **0.9312** | **0.8922** | **0.9038** | **$\pm$ 0.0026** |
| **Random Forest** | 0.9664 | 0.9185 | 0.9215 | 0.8532 | $\pm$ 0.0031 |
| **Extra Trees** | 0.9621 | 0.9104 | 0.9104 | 0.8666 | $\pm$ 0.0038 |
| **XGBoost** | 0.9642 | 0.8955 | 0.9431 | 0.7476 | $\pm$ 0.0042 |
| **Logistic Regression** | 0.9510 | 0.8922 | 0.8842 | 0.8840 | $\pm$ 0.0051 |

### **The Strategic Choice: Recall Over Precision**
We prioritize **Recall (89.22%)** to maximize humanitarian impact. 
*   **Asymmetric Risk:** Missing a broken pump (False Negative) leaves a community without water; a False Positive only results in a minor operational check.
*   **0.2 Threshold:** We use a **0.2 tuned probability threshold** to intentionally lower the bar for flagging failures, ensuring high-risk points are inspected early.

---

## Final Recommendations
1.  **Targeted Regional Response:** Deploy maintenance teams to identified hotspots in **Western Kenya** and **Nairobi**.
2.  **Predictive Alerts:** Trigger inspections for any water point with a failure probability **$> 20\%$**.
3.  **Technological Phase-out:** Immediately flag **Motorized Pump** and **Rope and Bucket** systems for replacement with resilient **Tapstand technology**.
4.  **Continuous Monitoring:** Implement real-time digital reporting in **"High-Risk Failure Zones"**.

---
*Developed as part of the Data Science program at Moringa School.*