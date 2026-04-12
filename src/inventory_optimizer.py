import pandas as pd
import numpy as np
import os

def calculate_inventory():
    if not os.path.exists("data/processed/forecasts.csv") or not os.path.exists("data/processed/features.csv"):
        print("Error: Missing required processed data. Please run data engineering and forecasting models first.")
        return

    forecasts = pd.read_csv("data/processed/forecasts.csv")
    history = pd.read_csv("data/processed/features.csv")
    
    std_demand = history.groupby(['store_id', 'product_id'])['sales'].std().reset_index()
    std_demand.rename(columns={'sales': 'std_dev_demand'}, inplace=True)
    
    avg_predicted_demand = forecasts.groupby(['store_id', 'product_id'])['forecast_sales'].mean().reset_index()
    avg_predicted_demand.rename(columns={'forecast_sales': 'daily_demand'}, inplace=True)
    
    inventory_df = pd.merge(avg_predicted_demand, std_demand, on=['store_id', 'product_id'])
    
    Z = 1.65
    lead_time = 7 
    
    inventory_df['safety_stock'] = Z * inventory_df['std_dev_demand'] * np.sqrt(lead_time)
    inventory_df['safety_stock'] = np.ceil(inventory_df['safety_stock']).fillna(0)
    
    inventory_df['reorder_point'] = (inventory_df['daily_demand'] * lead_time) + inventory_df['safety_stock']
    inventory_df['reorder_point'] = np.ceil(inventory_df['reorder_point']).fillna(0)
    
    inventory_df['stockout_risk_proxy'] = inventory_df['std_dev_demand'] / (inventory_df['daily_demand'] + 1e-5)
    
    inventory_df.to_csv("data/processed/inventory_metrics.csv", index=False)

if __name__ == "__main__":
    calculate_inventory()
