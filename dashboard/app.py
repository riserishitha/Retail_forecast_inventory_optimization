import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Retail Demand & Inventory Optimization", layout="wide", page_icon="📦")

st.title("🚀 Retail Demand Forecasting & Inventory Optimization System")
st.markdown("Predict store-level product demand and optimize inventory to minimize stockouts and holding costs.")

# Load Data
@st.cache_data
def load_data():
    if not os.path.exists("data/processed/forecasts.csv") or not os.path.exists("data/processed/inventory_metrics.csv"):
        return None, None
    forecasts = pd.read_csv("data/processed/forecasts.csv")
    metrics = pd.read_csv("data/processed/inventory_metrics.csv")
    return forecasts, metrics

forecasts, metrics = load_data()

if forecasts is None or metrics is None:
    st.warning("Processed Data not found. Please run the data pipelines `data_generator.py`, `data_engineering.py`, `forecasting_models.py`, and `inventory_optimizer.py` first.")
    st.stop()

# --- Sidebar Filters ---
st.sidebar.header("Filter Options")
selected_store = st.sidebar.selectbox("Select Store ID", sorted(forecasts['store_id'].unique()))
selected_product = st.sidebar.selectbox("Select Product ID", sorted(forecasts['product_id'].unique()))

# Filter data
store_prod_forecast = forecasts[(forecasts['store_id'] == selected_store) & (forecasts['product_id'] == selected_product)]
store_prod_metric = metrics[(metrics['store_id'] == selected_store) & (metrics['product_id'] == selected_product)].iloc[0]

# --- Top KPIs ---
st.subheader(f"Inventory Metrics for Store {selected_store} | Product {selected_product}")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Avg Daily Demand", f"{store_prod_metric['daily_demand']:.1f} units")
col2.metric("Safety Stock (SS)", f"{store_prod_metric['safety_stock']:.0f} units")
col3.metric("Reorder Point (ROP)", f"{store_prod_metric['reorder_point']:.0f} units")

risk_color = "red" if store_prod_metric['stockout_risk_proxy'] > 1.0 else "green"
col4.markdown(f"**Stockout Risk Proxy:** <br><span style='color:{risk_color}; font-size: 24px'>{store_prod_metric['stockout_risk_proxy']:.2f}</span>", unsafe_allow_html=True)

# --- Demand Forecast Visualization ---
st.subheader("📈 30-Day Demand Forecast vs Actuals")

# Let's mock up recent actuals vs forecast. We will just use the available data for demonstration.
# The `sales` column contains the actual history used in the test set. 
# The `forecast_sales` contains the XGBoost prediction.

fig = go.Figure()
fig.add_trace(go.Scatter(x=store_prod_forecast['date'], y=store_prod_forecast['sales'], 
                         mode='lines', name='Actual Sales', line=dict(color='blue')))
fig.add_trace(go.Scatter(x=store_prod_forecast['date'], y=store_prod_forecast['forecast_sales'], 
                         mode='lines', name='Predicted Demand (XGBoost)', line=dict(color='orange', dash='dash')))

fig.update_layout(xaxis_title="Date", yaxis_title="Sales / Demand", hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

# --- Scenario Simulation ---
st.divider()
st.subheader("🧪 Scenario Simulation")
st.markdown("Simulate 'What-If' scenarios by modifying expected lead times and demand surges. See how Reorder Point and Safety Stock dynamically adapt.")

sim_col1, sim_col2 = st.columns(2)
with sim_col1:
    sim_lead_time = st.slider("Simulate Expected Lead Time (Days)", min_value=1, max_value=30, value=7, step=1)
with sim_col2:
    sim_demand_surge = st.slider("Simulate Demand Surge (%)", min_value=-50, max_value=100, value=0, step=5)

# Calculate simulated metrics
sim_daily_demand = store_prod_metric['daily_demand'] * (1 + (sim_demand_surge / 100))
sim_safety_stock = 1.65 * store_prod_metric['std_dev_demand'] * (sim_lead_time ** 0.5)
sim_reorder_point = (sim_daily_demand * sim_lead_time) + sim_safety_stock

st.markdown("### Simulated Outcomes:")
res_col1, res_col2 = st.columns(2)
res_col1.metric("Adjusted Reorder Point (ROP)", f"{sim_reorder_point:.0f} units", delta=f"{sim_reorder_point - store_prod_metric['reorder_point']:.0f} units from baseline")
res_col2.metric("Adjusted Safety Stock", f"{sim_safety_stock:.0f} units", delta=f"{sim_safety_stock - store_prod_metric['safety_stock']:.0f} units from baseline")

st.info(f"**Business Action:** In this simulation, you should reorder when your on-hand inventory drops to **{sim_reorder_point:.0f} units**. This accounts for a **{sim_lead_time} day** supply delay and a **{sim_demand_surge}%** change in projected demand.")
