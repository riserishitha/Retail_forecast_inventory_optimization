import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Product OS: Retail Inventory", layout="wide", page_icon="📦")

st.title("📦 AI-Powered Retail Inventory Optimizer")
st.markdown("**Product Management View:** Drive ROI through predictive demand and dynamic inventory management.")

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
    st.warning("Processed Data not found. Please run the backend pipeline first (`src/data_generator.py`, etc.).")
    st.stop()

tab1, tab2, tab3 = st.tabs(["📈 Product KPIs & MVP Impact", "🏪 Store Operations View", "🧪 A/B Testing & Roadmap"])

with tab1:
    st.header("Executive Summary & Product Impact")
    st.markdown("This view aggregates the projected impact of our AI inventory optimizer MVP across the pilot stores.")
    
    # Calculate mock aggregate metrics
    total_safety_stock = metrics['safety_stock'].sum()
    avg_stockout_risk = metrics['stockout_risk_proxy'].mean()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Pilot Stores deployed", f"{metrics['store_id'].nunique()}")
    col2.metric("Active SKUs optimized", f"{metrics['product_id'].nunique()}")
    col3.metric("Proj. Working Capital Savings", "$1.2M", "14% reduction")
    col4.metric("Avg Store Stockout Risk", f"{avg_stockout_risk:.2f}", "-3.5% vs baseline", delta_color="inverse")
    
    st.divider()
    
    st.subheader("Regional Allocations (MVP Rollout)")
    # Group by store for a simple bar chart
    store_agg = metrics.groupby('store_id')['safety_stock'].sum().reset_index()
    store_agg['store_id'] = store_agg['store_id'].astype(str)
    fig_agg = px.bar(store_agg, x='store_id', y='safety_stock', 
                     title="Total Safety Stock Unit Allocation per Pilot Store",
                     labels={'store_id': 'Store ID', 'safety_stock': 'Total Safety Stock Units'},
                     color='safety_stock', color_continuous_scale='Mint')
    st.plotly_chart(fig_agg, use_container_width=True)

with tab2:
    st.header("Store Operations Dashboard")
    st.markdown("Actionable daily insights for **Store Managers**.")
    
    # --- Sidebar / Selectors ---
    col_a, col_b = st.columns(2)
    with col_a:
        selected_store = st.selectbox("Select Store ID", sorted(forecasts['store_id'].unique()))
    with col_b:
        selected_product = st.selectbox("Select Product ID", sorted(forecasts['product_id'].unique()))

    # Filter data
    store_prod_forecast = forecasts[(forecasts['store_id'] == selected_store) & (forecasts['product_id'] == selected_product)]
    store_prod_metric = metrics[(metrics['store_id'] == selected_store) & (metrics['product_id'] == selected_product)].iloc[0]

    # --- Top KPIs ---
    st.subheader(f"Inventory Recommendations | Store {selected_store} - Product {selected_product}")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avg Daily Demand", f"{store_prod_metric['daily_demand']:.1f} units")
    col2.metric("Safety Stock (SS)", f"{store_prod_metric['safety_stock']:.0f} units")
    col3.metric("Reorder Point (ROP)", f"{store_prod_metric['reorder_point']:.0f} units")

    risk_color = "red" if store_prod_metric['stockout_risk_proxy'] > 1.0 else "green"
    col4.markdown(f"**Stockout Risk Proxy:** <br><span style='color:{risk_color}; font-size: 24px'>{store_prod_metric['stockout_risk_proxy']:.2f}</span>", unsafe_allow_html=True)

    # --- Demand Forecast Visualization ---
    st.subheader("📈 30-Day Predictive Demand")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=store_prod_forecast['date'], y=store_prod_forecast['sales'], 
                             mode='lines', name='Actual Sales', line=dict(color='#8B5CF6')))
    fig.add_trace(go.Scatter(x=store_prod_forecast['date'], y=store_prod_forecast['forecast_sales'], 
                             mode='lines', name='Predicted Demand (AI)', line=dict(color='#10B981', dash='dash')))

    fig.update_layout(xaxis_title="Date", yaxis_title="Sales / Demand", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    # --- Scenario Simulation ---
    st.divider()
    st.subheader("🧪 Scenario Planning (Simulation Engine)")
    st.markdown("Supply Chain Managers: Simulate lead time disruptions or demand surges to test ROP resilience.")

    sim_col1, sim_col2 = st.columns(2)
    with sim_col1:
        sim_lead_time = st.slider("Simulate Expected Lead Time (Days)", min_value=1, max_value=30, value=7, step=1)
    with sim_col2:
        sim_demand_surge = st.slider("Simulate Demand Surge (%)", min_value=-50, max_value=100, value=0, step=5)

    # Calculate simulated metrics
    sim_daily_demand = store_prod_metric['daily_demand'] * (1 + (sim_demand_surge / 100))
    sim_safety_stock = 1.65 * store_prod_metric['std_dev_demand'] * (sim_lead_time ** 0.5)
    sim_reorder_point = (sim_daily_demand * sim_lead_time) + sim_safety_stock

    st.markdown("### Simulated Adjusted Actions:")
    res_col1, res_col2 = st.columns(2)
    res_col1.metric("Adjusted Reorder Point (ROP)", f"{sim_reorder_point:.0f} units", delta=f"{sim_reorder_point - store_prod_metric['reorder_point']:.0f} units from baseline", delta_color="inverse")
    res_col2.metric("Adjusted Safety Stock", f"{sim_safety_stock:.0f} units", delta=f"{sim_safety_stock - store_prod_metric['safety_stock']:.0f} units from baseline", delta_color="inverse")

with tab3:
    st.header("Product Iteration & Roadmap")
    
    st.subheader("A/B Testing Hypothesis")
    st.markdown("""
    **Core Hypothesis:** By shifting from static 14-day reorder rules to dynamic XGBoost-driven Reorder Points (ROP), we will reduce the Out-of-Stock (OOS) event rate by at least 15% without increasing our average holding costs.
    
    **Current Status:** Pilot Phase MVP
    - **Control Group:** Stores 1 & 2 (Using legacy ordering logic and historical moving averages).
    - **Variant Group:** Stores 3, 4 & 5 (Using the AI Dashboard's dynamic Reorder Points).
    """)
    
    st.subheader("Upcoming Features (Product Roadmap)")
    st.markdown("""
    - [ ] **Feature:** Automated Purchase Order (PO) creation via SAP ERP API integration.
    - [ ] **Feature:** Macro / External Data Integration (inclement weather patterns, local events) into the forecasting engine.
    - [ ] **UX Upgrade:** Native iOS / Android application for Store Managers to check inventory and approve ROPs directly on the warehouse floor.
    """)
