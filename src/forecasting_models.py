import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
import xgboost as xgb
import os
import joblib

def train_and_forecast():
    if not os.path.exists("data/processed/features.csv"):
        print("Error: Features file not found. Please run data_engineering.py first.")
        return

    df = pd.read_csv("data/processed/features.csv")
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by=['store_id', 'product_id', 'date'])
    
    max_date = df['date'].max()
    test_start_date = max_date - pd.Timedelta(days=30)
    
    train = df[df['date'] < test_start_date]
    test = df[df['date'] >= test_start_date]
    
    features = [
        'store_id', 'product_id', 'is_holiday', 'year', 'month', 'day', 'day_of_week',
        'sales_lag_7', 'sales_lag_30', 'rolling_mean_7', 'rolling_mean_30'
    ]
    target = 'sales'
    
    X_train = train[features]
    y_train = train[target]
    
    X_test = test[features]
    y_test = test[target]
    
    model = xgb.XGBRegressor(
        n_estimators=100, 
        learning_rate=0.1, 
        max_depth=6, 
        random_state=42,
        objective='reg:squarederror'
    )
    model.fit(X_train, y_train)
    
    y_pred_xgb = model.predict(X_test)
    
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/xgboost_demand_model.pkl")
    
    test_results = test[['date', 'store_id', 'product_id', 'sales']].copy()
    test_results['forecast_sales'] = np.maximum(0, y_pred_xgb)
    
    test_results.to_csv("data/processed/forecasts.csv", index=False)

if __name__ == "__main__":
    train_and_forecast()
