import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
import xgboost as xgb
import os
import joblib

def train_and_forecast():
    import os
    if not os.path.exists("data/processed/features.csv"):
        print("Features file not found! Please run data_engineering.py first.")
        return

    print("Loading engineered features...")
    df = pd.read_csv("data/processed/features.csv")
    
    # Sort by date
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by=['store_id', 'product_id', 'date'])
    
    # Split train/test (last 30 days as test)
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
    
    # 1. Baseline Model: Moving Average (Uses rolling_mean_7 as prediction)
    print("Evaluating Baseline Model (Moving Average 7-day)...")
    y_pred_baseline = test['rolling_mean_7'].fillna(0)
    baseline_rmse = np.sqrt(mean_squared_error(y_test, y_pred_baseline))
    # Replace zeros in y_test for MAPE to avoid division by zero
    y_test_safe = np.where(y_test == 0, 1, y_test)
    baseline_mape = mean_absolute_percentage_error(y_test_safe, y_pred_baseline)
    print(f"Baseline RMSE: {baseline_rmse:.2f}")
    print(f"Baseline MAPE: {baseline_mape:.2%}")
    
    # 2. Advanced Model: XGBoost
    print("Training XGBoost...")
    model = xgb.XGBRegressor(
        n_estimators=100, 
        learning_rate=0.1, 
        max_depth=6, 
        random_state=42,
        objective='reg:squarederror'
    )
    model.fit(X_train, y_train)
    
    y_pred_xgb = model.predict(X_test)
    xgb_rmse = np.sqrt(mean_squared_error(y_test, y_pred_xgb))
    xgb_mape = mean_absolute_percentage_error(y_test_safe, y_pred_xgb)
    print(f"XGBoost RMSE: {xgb_rmse:.2f}")
    print(f"XGBoost MAPE: {xgb_mape:.2%}")
    
    # Save the model
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/xgboost_demand_model.pkl")
    print("Model saved to models/xgboost_demand_model.pkl")
    
    # Generate Future Forecast (Next 30 days based on last known data)
    print("Generating Future Forecasts...")
    test_results = test[['date', 'store_id', 'product_id', 'sales']].copy()
    test_results['forecast_sales'] = np.maximum(0, y_pred_xgb) # No negative sales
    
    test_results.to_csv("data/processed/forecasts.csv", index=False)
    print("Forecasts saved to data/processed/forecasts.csv")

if __name__ == "__main__":
    train_and_forecast()
