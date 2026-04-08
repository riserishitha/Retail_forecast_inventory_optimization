import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_retail_data(num_stores=5, num_products=10, days=1095): # 3 years
    np.random.seed(42)
    start_date = datetime(2021, 1, 1)
    date_list = [start_date + timedelta(days=x) for x in range(days)]
    
    data = []
    
    # Define baseline base demand for products
    product_base_demand = {p: np.random.randint(10, 100) for p in range(1, num_products + 1)}
    
    # Store multipliers (some stores sell more)
    store_multiplier = {s: np.random.uniform(0.5, 1.5) for s in range(1, num_stores + 1)}
    
    for date in date_list:
        # Seasonality effects
        month = date.month
        day_of_week = date.weekday()
        
        # Monthly seasonality (e.g., peak in summer and December)
        monthly_seasonality = 1.0
        if month in [6, 7, 8]:
            monthly_seasonality = 1.2
        elif month == 12:
            monthly_seasonality = 1.5
            
        # Weekly seasonality (weekend bump)
        weekly_seasonality = 1.3 if day_of_week in [5, 6] else 1.0
        
        # Holiday effect: let's pick some dates (e.g., Nov 25, Dec 24, July 4)
        is_holiday = 1 if (month == 11 and date.day == 25) or (month == 12 and date.day == 24) or (month == 7 and date.day == 4) else 0
        holiday_multiplier = 2.0 if is_holiday else 1.0
        
        for store in range(1, num_stores + 1):
            for product in range(1, num_products + 1):
                base = product_base_demand[product]
                store_mult = store_multiplier[store]
                
                # Noise
                noise = np.random.normal(1, 0.1)
                
                # Calculate final demand
                demand = base * store_mult * monthly_seasonality * weekly_seasonality * holiday_multiplier * noise
                demand = max(0, int(np.round(demand))) # Ensure non-negative integers
                
                # Random stockout (1% chance)
                if np.random.rand() < 0.01:
                    demand = 0 
                
                data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'store_id': store,
                    'product_id': product,
                    'sales': demand,
                    'is_holiday': is_holiday
                })
                
    df = pd.DataFrame(data)
    
    # Save the data
    os.makedirs('data/raw', exist_ok=True)
    df.to_csv('data/raw/sales_data.csv', index=False)
    print(f"Generated {len(df)} rows of synthetic retail sales data.")
    print("Saved to data/raw/sales_data.csv")

if __name__ == "__main__":
    generate_retail_data()
