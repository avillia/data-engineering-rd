from sys import argv

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.functions import col, to_date

args = getResolvedOptions(argv, ["JOB_NAME", "BUCKET_NAME"])
spark_context = SparkContext()
glueContext = GlueContext(spark_context)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)


bronze_df = glueContext.create_dynamic_frame.from_catalog(
    database="default",
    table_name="sales_bronze",
).toDF()


silver_df = bronze_df.select(
    col("CustomerId").alias("client_id"),
    to_date(col("PurchaseDate"), "yyyy-MM-dd").alias("purchase_date"),
    col("Product").alias("product_name"),
    col("Price").cast("float").alias("price"),
).filter("client_id is not null and purchase_date is not null")


output_path = f"s3://{args['BUCKET_NAME']}/silver/sales/"
silver_df.write.mode("overwrite").partitionBy("purchase_date").parquet(output_path)

job.commit()
