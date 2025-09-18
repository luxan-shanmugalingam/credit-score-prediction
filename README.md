# Credit Score Prediction & Analysis

![Credit Score App Demo](assets/demo.gif)

## Project Overview
This project is an end-to-end analysis and prediction of credit scores, classified as Poor, Standard, or Good. Starting with a large dataset of over 100,000 records, we performed in-depth Exploratory Data Analysis (EDA) to uncover key financial patterns. The best-performing model, CatBoost, achieved 85% accuracy. The project culminates in a functional web application designed for financial institutions to assess credit risk in real-time.

## Key Features
* **Comprehensive Data Analysis:** Performed in-depth Exploratory Data Analysis (EDA) to understand the complex relationships between 28 different financial, demographic, and behavioral variables.
* **Machine Learning Model Comparison:** Trained and evaluated 7 different classification models, including Logistic Regression, SVM, Random Forest, and CatBoost, to find the most accurate predictor of credit scores.
* **High-Performance Prediction:** The final CatBoost model achieved an 85% accuracy on the test set, providing a reliable tool for risk assessment.
* **Interactive Web Application:** Developed a secure, login-protected Flask web application for credit officers to get real-time credit score predictions.
* **Personalized Customer Insights:** The app includes visualizations of individual customer financial trajectories, offering a deeper, more personalized level of analysis.

## Tech Stack
* **Languages:** Python
* **Libraries:** Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn
* **Web Framework:** Flask
* **Deployment:** Local deployment

## Project Structure
```

credit-score-prediction/
│
├── 📂 assets/
│   └── 🖼️ demo.gif
│
├── 📂 notebooks/
│   ├── 📜 01_Data_Preprocessing_and_EDA.ipynb
│   └── 📜 02_Customer_Clustering_Analysis.ipynb
│
├── 📂 reports/
│   ├── 📄 01_EDA_Report.pdf
│   └── 📄 02_Modelling_Report.pdf
│
├── 📂 web\_app/
│   └── ... (contents of your Flask app)
│
├── 📜 README.md
└── 📜 requirements.txt

````

## Usage
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/luxan-shanmugalingam/credit-score-prediction.git](https://github.com/luxan-shanmugalingam/credit-score-prediction.git)
    cd credit-score-prediction
    ```
2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    # On Windows, use: venv\Scripts\activate
    ```
3.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the application:**
    ```bash
    python web_app/Finpulse.py
    ```
    
## Key Findings
* **Debt and Payment Behavior are Crucial:** The analysis showed a strong link between poor credit scores and higher debt loads, a greater number of loans, and increased payment delays.
* **Credit Card Usage Patterns:** The median number of credit cards increased with worsening credit scores, rising from 4 for "Good" scores to 7 for "Poor" scores.
* **The "Minimum Payment" Trap:** Paying only the minimum amount due was a significant indicator of poor credit. Of the customers who only paid the minimum, 39.6% were in the "Poor" credit category, while only 3.7% were in the "Good" category.
* **Seasonal Trends:** The distribution of credit scores showed statistically significant variations across the months, suggesting that time-dependent financial behaviors may influence creditworthiness. 

## Future Work
* **Temporal Modeling:** Implement time-series or longitudinal models to better understand how customer credit scores evolve over time.
* **Model Explainability:** Use tools like SHAP or LIME to provide deeper insights into individual predictions.
* **Advanced Clustering:** Apply density-based clustering algorithms like DBSCAN to capture more complex, non-linear customer segments.

## Authors
* Tishani Wijekoon (S16379)
* Chami Sewwandi (S16028)
* W.K.Hiruni Hasara (S16210)
* S.Luxan (s16329)
