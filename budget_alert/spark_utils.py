from pyspark.sql import SparkSession
import os
from constants import *

os.environ["PYSPARK_PYTHON"] = "C:/Users/Snaha/anaconda3/envs/newproj/python.exe"
#Create and return a spark session for Oracle JDBC connection
def get_spark_session():
    spark = SparkSession.builder \
        .appName("OracleJDBC") \
        .config("spark.driver.extraClassPath", "D:/oracle/jdbc/lib/ojdbc8.jar") \
        .config("spark.executor.extraClassPath", "D:/oracle/jdbc/lib/ojdbc8.jar") \
        .getOrCreate()
    return spark

#Convert Oracle db table to dataframe and return df
def spark_db_to_df(spark,table_name):
    
    jdbc_url = f"jdbc:oracle:thin:@{dsn}"
    properties = {
        "user": oracle_username,
        "password": oracle_password,
        "driver": "oracle.jdbc.OracleDriver"
        }
    df = spark.read.jdbc(url=jdbc_url, table=table_name, properties=properties)
    return df


    