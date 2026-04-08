import pandas as pd
import numpy as np

def calculate_inventory():
    import os
    if not os.path.exists("data/processed/forecasts.csv") or not os.path.exists("data/processed/features.csv"):
        print("Missing required processed data. Please run data engineering and forecasting models first.")
        return

    print("Loading data for inventory optimization...")
    forecasts = pd.read_csv("data/processed/forecasts.csv")
    history = pd.read_csv("data/processed/features.csv")
    
    # Calculate historical standard deviation of demand
    std_demand = history.groupby(['store_id', 'product_id'])['sales'].std().reset_index()
    std_demand.rename(columns={'sales': 'std_dev_demand'}, inplace=True)
    
    # Calculate average forecasted demand (future 30 days expected daily demand)
    avg_predicted_demand = forecasts.groupby(['store_id', 'product_id'])['forecast_sales'].mean().reset_index()
    avg_predicted_demand.rename(columns={'forecast_sales': 'daily_demand'}, inplace=True)
    
    # Merge
    inventory_df = pd.merge(avg_predicted_demand, std_demand, on=['store_id', 'product_id'])
    
    # Assume static factors (These could be inputs in a real system)
    # Service level Z-score (1.65 for 95% availability)
    Z = 1.65
    # Lead time in days
    lead_time = 7 
    
    print("Calculating Safety Stock and Reorder Points (ROP)...")
    
    # Safety Stock formula: SS = Z * std_demand * sqrt(Lead_Time)
    inventory_df['safety_stock'] = Z * inventory_df['std_dev_demand'] * np.sqrt(lead_time)
    inventory_df['safety_stock'] = np.ceil(inventory_df['safety_stock']).fillna(0)
    
    # ROP formula: expected_demand_during_lead_time + Safety Stock
    inventory_df['reorder_point'] = (inventory_df['daily_demand'] * lead_time) + inventory_df['safety_stock']
    inventory_df['reorder_point'] = np.ceil(inventory_df['reorder_point']).fillna(0)
    
    # Calculate stockout risk proxy (if std dev is high compared to demand, risk is high)
    inventory_df['stockout_risk_proxy'] = inventory_df['std_dev_demand'] / (inventory_df['daily_demand'] + 1e-5)
    
    inventory_df.to_csv("data/processed/inventory_metrics.csv", index=False)
    print("Inventory metrics saved to data/processed/inventory_metrics.csv")
    
    print("\nSAMPLE INVENTORY METRICS:")
    print(inventory_df.head())

if __name__ == "__main__":
    calculate_inventory()
