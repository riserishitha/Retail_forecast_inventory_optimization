<div align="center">
  <h1>🚀 AI-Powered Retail Inventory Optimizer (Product Management Portfolio)</h1>
  <p>A B2B SaaS Product solving retail out-of-stock and overstocking issues using AI demand forecasting.</p>
  
  [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
  [![Product Management](https://img.shields.io/badge/Role-Product_Manager-success.svg)]()
  [![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B.svg)](https://streamlit.io/)
</div>

<br />

## 🎯 Product Vision & Strategy

Large retailers face a massive supply chain optimization problem. Our product acts as an AI "Co-Pilot" for Supply Chain Managers to dynamically optimize inventory based on predictive demand, rather than static historical rules.

**Product Vision:** Empower retailers to achieve >98% product availability while reducing holding costs by dynamically adjusting safety stock using machine learning.

### User Personas
1. **Supply Chain Manager (Primary):** Wants a high-level view of inventory health and risk across regions. Needs to see ROI and reduce working capital.
2. **Store Manager (Secondary):** Wants actionable, daily, store-level reorder point (ROP) recommendations to keep shelves stocked without manually crunching numbers.

---

## 📈 Key Performance Indicators (KPIs) & Business Impact

This product is designed to move the needle on several key business metrics:
- **Primary Metric:** Out-of-Stock (OOS) Rate (Target: < 2%)
- **Secondary Metric:** Inventory Turnover Ratio (Target: +15% improvement)
- **Financial Metric:** Working Capital Cost Savings (e.g., millions saved by preventing over-ordering).
- **Adoption Metric:** Weekly Active Users (WAU) among store managers using the dashboard for ordering.

---

## 🏗️ Core Features & Epics

As a PM, I've structured the product development into the following core epics:

### Epic 1: Intelligent Demand Forecasting
- **User Story:** As a store manager, I want the system to predict how much of Product X I will sell in the next 30 days so that I don't under-order for the holidays.
- **Implementation:** PySpark for feature engineering, XGBoost for time-series forecasting. 

### Epic 2: Dynamic Inventory Optimization Engine
- **User Story:** As a supply chain manager, I want the system to automatically calculate my Safety Stock and Reorder Point (ROP) based on lead times and demand volatility.
- **Implementation:** Statistical Operations Research formulas dynamically applied to the AI forecasts.

### Epic 3: Interactive "What-If" Scenario Planning
- **User Story:** As a planner, I want to simulate supply chain delays (e.g., lead time increases to 15 days) so I can proactively adjust my purchase orders.
- **Implementation:** Interactive Streamlit dashboard allowing real-time param modification.

---

## 🚀 How to Run the Product Prototype

Experience the end-to-end MVP locally.

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Generate Data & Train Models (Backend)
Simulates data, runs PySpark ETL, and trains the ML models.
```bash
python src/data_generator.py
python src/data_engineering.py
python src/forecasting_models.py
python src/inventory_optimizer.py
```

### 3. Launch the Product Dashboard MVP
Explore the PM & Business View, and the Store Operations View.
```bash
streamlit run dashboard/app.py
```

---

## 🗺️ Product Roadmap (Next 6-12 Months)

**Q1 (MVP & Pilot):**
- Launch XGBoost prediction for top 50 high-velocity SKUs.
- Pilot dashboard with 3 store locations.
- **A/B Testing:** Compare OOS rates of AI-recommended reorders vs. baseline manual ordering.

**Q2 (Scale & Integration):**
- Direct API integration with the retailer's core ERP system (e.g., SAP, Oracle).
- Automated PO (Purchase Order) creation based on Reorder Points.

**Q3 (Advanced Analytics):**
- Incorporate external data (weather, local events, macroeconomic indicators) into the forecasting model.
- Multi-echelon inventory optimization (optimizing warehouse vs. store levels simultaneously).

---

## 🏆 Why this Product Matters

- **Business Value over Tech:** While the backend is powered by complex distributed computing (PySpark) and ML (XGBoost), the frontend delivers simple, actionable insights. 
- **Scalability:** Built on enterprise-ready architecture to handle millions of daily SKU-store combinations.