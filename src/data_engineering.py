import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, month, dayofweek, year, dayofmonth, lag, avg, when
from pyspark.sql.window import Window

def process_data():
    if not os.path.exists("data/raw/sales_data.csv"):
        print("Error: Raw data not found. Please run data_generator.py first.")
        return

    spark = SparkSession.builder \
        .appName("RetailDemandForecasting") \
        .config("spark.driver.memory", "4g") \
        .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
        .getOrCreate()
        
    df = spark.read.csv("data/raw/sales_data.csv", header=True, inferSchema=True)
    
    df = df.withColumn("date_type", col("date").cast("date"))
    df = df.withColumn("year", year("date_type"))
    df = df.withColumn("month", month("date_type"))
    df = df.withColumn("day", dayofmonth("date_type"))
    df = df.withColumn("day_of_week", dayofweek("date_type"))
    
    windowSpec = Window.partitionBy("store_id", "product_id").orderBy("date_type")
    
    df = df.withColumn("sales_lag_7", lag("sales", 7).over(windowSpec))
    df = df.withColumn("sales_lag_30", lag("sales", 30).over(windowSpec))
    
    windowSpec7 = Window.partitionBy("store_id", "product_id").orderBy("date_type").rowsBetween(-7, -1)
    df = df.withColumn("rolling_mean_7", avg("sales").over(windowSpec7))
    
    windowSpec30 = Window.partitionBy("store_id", "product_id").orderBy("date_type").rowsBetween(-30, -1)
    df = df.withColumn("rolling_mean_30", avg("sales").over(windowSpec30))

    df = df.drop("date_type")
    df = df.na.drop()
    
    os.makedirs("data/processed", exist_ok=True)
    df.toPandas().to_csv("data/processed/features.csv", index=False)
    
    spark.stop()

if __name__ == "__main__":
    process_data()
