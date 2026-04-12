import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_retail_data(num_stores=5, num_products=10, days=1095):
    np.random.seed(42)
    start_date = datetime(2021, 1, 1)
    date_list = [start_date + timedelta(days=x) for x in range(days)]
    
    data = []
    product_base_demand = {p: np.random.randint(10, 100) for p in range(1, num_products + 1)}
    store_multiplier = {s: np.random.uniform(0.5, 1.5) for s in range(1, num_stores + 1)}
    
    for date in date_list:
        month = date.month
        day_of_week = date.weekday()
        
        monthly_seasonality = 1.0
        if month in [6, 7, 8]:
            monthly_seasonality = 1.2
        elif month == 12:
            monthly_seasonality = 1.5
            
        weekly_seasonality = 1.3 if day_of_week in [5, 6] else 1.0
        is_holiday = 1 if (month == 11 and date.day == 25) or (month == 12 and date.day == 24) or (month == 7 and date.day == 4) else 0
        holiday_multiplier = 2.0 if is_holiday else 1.0
        
        for store in range(1, num_stores + 1):
            for product in range(1, num_products + 1):
                base = product_base_demand[product]
                store_mult = store_multiplier[store]
                noise = np.random.normal(1, 0.1)
                
                demand = base * store_mult * monthly_seasonality * weekly_seasonality * holiday_multiplier * noise
                demand = max(0, int(np.round(demand)))
                
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
    os.makedirs('data/raw', exist_ok=True)
    df.to_csv('data/raw/sales_data.csv', index=False)

if __name__ == "__main__":
    generate_retail_data()
