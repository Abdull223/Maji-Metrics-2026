# Predictive Maintenance & Equitable Water Infrastructure Using Data-Driven Technology

### Live Dashboard: [View the Interactive App](https://predictive-maintenance-equitable-water-infrastructure-group-2.streamlit.app/)

## Project Overview
In rural Kenya, water infrastructure failure is a silent crisis that disrupts thousands of lives daily. Using the **Kenya Water Points Dataset (WPdx)**, our team developed a model designed to identify at-risk water points before they fail. By moving from reactive repairs to a data-driven predictive roadmap, this model provides government agencies and NGOs with the insights needed for proactive maintenance, ensuring consistent and reliable water access for rural communities.

## Technical Deliverables & Repository Structure
* **[Final Group 2.ipynb](./Final%20Group%202.ipynb):** Complete research notebook including EDA, Hierarchical Imputation, and Cross-Validation.
* **[app.py](./app.py):** Python script powering the Streamlit deployment.
* **[water_point_model.pkl](./water_point_model.pkl):** The serialized CatBoost champion model.
* **[requirements.txt](./requirements.txt):** Dependency list for the cloud environment.
* **[wpdx_enhanced.csv](./wpdx_enhanced.csv):** The cleaned and feature-engineered dataset used for final modeling.

## Key Statistical Innovations
We implemented a **Hierarchical Imputation** strategy to handle the missing `install_year` values. This approach avoids the bias of global medians by using a tiered fallback system:
1. **County + Technology Median:** Leverages local infrastructure trends.
2. **County Median:** Used when technology-specific data is unavailable for a region.
3. **Global Median:** Final safety net to ensure data completeness.

This methodology significantly sharpened our **Infrastructure Age** feature, resulting in near-perfect model separation.

## Model Tournament & Performance
We evaluated five high-performance architectures using **5-Fold Stratified Cross-Validation**. To prioritize humanitarian impact, we optimized for **Recall** using a tuned decision threshold of **0.2**.

### Final Cross-Validated Metrics (Means)
| Model Architecture | ROC-AUC | Accuracy | Recall (Broken) | Precision (Broken) | Stability (σ) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **CatBoost (Champion)** | **0.9687** | **0.9312** | **0.8922** | **0.9038** | ± 0.0026 |
| **Random Forest** | 0.9664 | 0.9185 | 0.9215 | 0.8532 | ± 0.0031 |
| **Extra Trees** | 0.9621 | 0.9104 | 0.9104 | 0.8666 | ± 0.0038 |
| **XGBoost** | 0.9642 | 0.8955 | 0.9431 | 0.7476 | ± 0.0042 |
| **Logistic Regression** | 0.9510 | 0.8922 | 0.8842 | 0.8840 | ± 0.0051 |

## Evaluation & The "Best Model" Selection
The **CatBoost Pipeline** was selected as the superior engine for this deployment. While XGBoost offered slightly higher recall, CatBoost provided the most mathematically sound balance:
* **Maximum Precision (0.90):** Ensures that 9 out of 10 flagged pumps are truly at risk, preventing wasted technical resources.
* **Exceptional Stability (± 0.0026):** Proves the model is robust across different geographic regions of Kenya.
* **High Accuracy (93%):** Correctly classifies the vast majority of infrastructure points.

## Strategic Recommendations
1. **Proactive Maintenance:** Deploy the CatBoost engine to transition from reactive "break-fix" cycles to a predictive roadmap via a 0.2 threshold safety net.
2. **Standardized GPS Logging:** Maintain high predictive utility by ensuring future field audits use standardized GPS and technology classification.
3. **Fee-Based Sustainability:** Support community-managed payment systems, which the data shows are strongly correlated with pump longevity.

---
*This project is dedicated to achieving **Sustainable Development Goal 6 (SDG 6)**: Ensuring availability and sustainable management of water and sanitation for all in Kenya.*

## Project Team Members
* **Abdullahi Abdi Hassan (Lead Statistician):** Statistical validation, hierarchical imputation design, and threshold optimization.
* **Claire (Data Architect):** High-volume data ingestion and intensive pre-processing of the WPdx dataset.
* **Yvonne (Feature Engineer):** Creation of domain-specific features (Infrastructure Age, Management categories).
* **Dahir (ML Engineer):** Implementation of advanced ensemble algorithms and hyperparameter tuning.
* **Samantha (Data Scientist):** Exploratory data analysis (EDA), trend visualization, and cross-validation strategy.
* **Laura (Project Manager):** Documentation, stakeholder communication, and SDG 6 alignment.
