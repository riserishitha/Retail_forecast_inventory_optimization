<div align="center">
  <h1>🚀 Retail Demand Forecasting & Inventory Optimization System</h1>
  <p>An end-to-end Machine Learning pipeline to predict store-level product demand and optimize inventory decisions to minimize stockouts and holding costs.</p>
  
  [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
  [![PySpark](https://img.shields.io/badge/Apache_Spark-PySpark-orange.svg)](https://spark.apache.org/)
  [![XGBoost](https://img.shields.io/badge/Machine_Learning-XGBoost-1D2939.svg)](https://xgboost.readthedocs.io/)
  [![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B.svg)](https://streamlit.io/)
</div>

<br />

## 🧠 Business Problem

Large retailers (like Lowe's, Walmart, Home Depot) deal with thousands of stores, highly seasonal demand patterns, and regional differences. Two of the biggest challenges they face are:
1. **Stockouts:** Losing sales because a product is not on the shelf when a customer wants to buy it.
2. **Overstocking:** Tying up capital in unsold inventory and increasing holding/warehousing costs.

**Goal:** Predict product demand accurately at the store-level and implement a statistical inventory optimization framework to determine *when* and *how much* to reorder.

---

## 🔧 End-to-End Architecture

This project is not just a Jupyter Notebook—it is a fully modular, end-to-end pipeline structured exactly how a real-world enterprise analytics system operates.

1. **📊 Data Layer**: Generates 3 years of highly realistic synthetic daily sales data (including seasonality, weekend bumps, and holidays).
2. **🧹 Data Engineering (PySpark)**: Distributed data processing to build time-based features, 7-day and 30-day lags, and rolling averages.
3. **📈 Forecasting Model (Core ML)**: Uses **XGBoost Regressor** to predict future demand, compared against a baseline Moving Average model. Metrics: RMSE, MAPE.
4. **📦 Inventory Optimization Logic**: The "WOW" factor. Implements statistical safety stock and calculates the exact Reorder Point (ROP).
5. **📊 Business Dashboard**: An interactive Streamlit application to visualize risks, demand, and simulate supply-chain scenarios.

---

## 🧮 Inventory Optimization Mathematics

Most projects stop at prediction. This project converts predictions into actionable business logic using Operations Research formulas:

**Reorder Point (ROP)** tells the warehouse *when* to place a new order.
> $$ROP = (d \times L) + SS$$

Where:
- **$$d$$**: Expected Demand per day (Predicted by XGBoost).
- **$$L$$**: Lead Time in days (How long the supplier takes to deliver).
- **$$SS$$** (Safety Stock): Buffer stock to handle demand volatility.
  - $$SS = Z \times \sigma_{demand} \times \sqrt{L}$$
  - **$$Z$$**: Z-score for desired service level (e.g., 1.65 for 95% availability).
  - **$$\sigma_{demand}$$**: Standard deviation of historical daily demand.

---

## 🏗️ Tech Stack

- **Data Processing**: Pandas, NumPy, Apache Spark (PySpark)
- **Machine Learning**: Scikit-learn, XGBoost
- **Dashboard & Visualization**: Streamlit, Plotly
- **Environment**: Python natively running locally

---

## 🚀 How to Run the Project

Follow these steps to generate data, train the model, calculate inventory, and view the dashboard locally.

### 1. Install Requirements
Make sure you have Python 3.8+ installed. You also need Java installed on your machine for `PySpark` to work.
```bash
pip install -r requirements.txt
```

### 2. Generate the Data
This simulates 3 years of daily sales for multiple stores and products, saving to `data/raw/sales_data.csv`.
```bash
python src/data_generator.py
```

### 3. Data Engineering (PySpark)
Processes raw data, creates lags and rolling features, and saves to `data/processed/features.csv`.
```bash
python src/data_engineering.py
```

### 4. Train Models & Predict
Trains the XGBoost models and creates a 30-day forecast.
```bash
python src/forecasting_models.py
```

### 5. Calculate Inventory Optimization Metrics
Uses the forecasts to calculate Safety Stock and ROP.
```bash
python src/inventory_optimizer.py
```

### 6. Launch the Dashboard
Open the interactive UI to visualize forecasts and run scenario simulations (e.g. "What if Lead Time increases by 5 days?").
```bash
streamlit run dashboard/app.py
```

---

## 📁 Repository Structure

```text
├── data/
│   ├── raw/                 # Raw generated CSV data
│   └── processed/           # PySpark output, model forecasts, inventory metrics
├── src/
│   ├── data_generator.py    # Synthetic data simulation
│   ├── data_engineering.py  # PySpark feature engineering
│   ├── forecasting_models.py# XGBoost & Baseline models
│   └── inventory_optimizer.py # Safety Stock & ROP Logic
├── dashboard/
│   └── app.py               # Streamlit application
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

---

## 🏆 Final Results & Deliverables

- **Modular Codebase:** Clean scripts instead of messy notebooks.
- **Actionable AI:** The ML translates directly to Reorder Points (ROP) that a store manager can natively understand and execute.
- **Dynamic Scenario Planning:** The Streamlit dashboard allows non-technical business users to see the impact of supply chain delays immediately.