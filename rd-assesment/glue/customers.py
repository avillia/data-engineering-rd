from sys import argv

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.functions import col, to_date

args = getResolvedOptions(argv, ["JOB_NAME", "BUCKET_NAME"])
spark_context = SparkContext()
glue_context = GlueContext(spark_context)
spark = glue_context.spark_session
job = Job(glue_context)
job.init(args["JOB_NAME"], args)


bronze_df = glue_context.create_dynamic_frame.from_catalog(
    database="default",
    table_name="customers_bronze",
).toDF()


silver_df = bronze_df.select(
    col("CustomerId").alias("client_id"),
    col("FirstName").alias("first_name"),
    col("LastName").alias("last_name"),
    col("Email").alias("email"),
    to_date(col("RegistrationDate"), "yyyy-MM-dd").alias("registration_date"),
    col("State").alias("state"),
).dropDuplicates(["client_id"])


output_path = f"s3://{args['BUCKET_NAME']}/silver/customers/"
silver_df.write.mode("overwrite").parquet(output_path)

job.commit()
