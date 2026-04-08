import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, month, dayofweek, year, dayofmonth, lag, avg, when
from pyspark.sql.window import Window
import warnings

warnings.filterwarnings('ignore')

def process_data():
    # Initialize Spark Session
    # Using local[*] to use all cores
    spark = SparkSession.builder \
        .appName("RetailDemandForecasting") \
        .config("spark.driver.memory", "4g") \
        .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
        .getOrCreate()
        
    print("Spark Session created.")

    import os
    if not os.path.exists("data/raw/sales_data.csv"):
        print("Raw data not found! Please run data_generator.py first.")
        return

    # 1. Load Data
    print("Loading data...")
    df = spark.read.csv("data/raw/sales_data.csv", header=True, inferSchema=True)
    
    # 2. Time-Based Features
    print("Creating time-based features...")
    df = df.withColumn("date_type", col("date").cast("date"))
    df = df.withColumn("year", year("date_type"))
    df = df.withColumn("month", month("date_type"))
    df = df.withColumn("day", dayofmonth("date_type"))
    df = df.withColumn("day_of_week", dayofweek("date_type"))
    
    # 3. Lag Features and Rolling Averages
    print("Creating lag features and rolling averages...")
    # Window specification: partition by store and product, order by date
    windowSpec = Window.partitionBy("store_id", "product_id").orderBy("date_type")
    
    # Lags
    df = df.withColumn("sales_lag_7", lag("sales", 7).over(windowSpec))
    df = df.withColumn("sales_lag_30", lag("sales", 30).over(windowSpec))
    
    # Rolling averages
    # For rolling mean 7, we take the average of standard lags 1 to 7
    windowSpec7 = Window.partitionBy("store_id", "product_id").orderBy("date_type").rowsBetween(-7, -1)
    df = df.withColumn("rolling_mean_7", avg("sales").over(windowSpec7))
    
    windowSpec30 = Window.partitionBy("store_id", "product_id").orderBy("date_type").rowsBetween(-30, -1)
    df = df.withColumn("rolling_mean_30", avg("sales").over(windowSpec30))

    # Drop intermediate date_type and rows with nulls (due to lags)
    df = df.drop("date_type")
    df = df.na.drop()
    
    # Ensure processed directory exists
    os.makedirs("data/processed", exist_ok=True)
    
    # 4. Save Processed Data
    print("Saving processed data to parquet...")
    # Convert to Pandas for ease of use in Scikit/XGBoost locally, or save as parquet
    # For compatibility locally with XGBoost in this MVP, let's save as CSV to avoid PyArrow issues on Windows 
    # Or parquet if PyArrow is installed. I will use parquet for better performance if possible, else CSV.
    # We will just write as CSV for maximum compatibility without needing extra dependencies installed by the user.
    pandas_df = df.toPandas()
    pandas_df.to_csv("data/processed/features.csv", index=False)
    
    print("Data processing complete. Saved to data/processed/features.csv")
    spark.stop()

if __name__ == "__main__":
    process_data()
