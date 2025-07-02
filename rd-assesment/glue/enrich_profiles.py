from sys import argv

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.functions import coalesce

args = getResolvedOptions(argv, ["JOB_NAME", "BUCKET_NAME"])
spark_context = SparkContext()
glue_context = GlueContext(spark_context)
spark = glue_context.spark_session
job = Job(glue_context)
job.init(args["JOB_NAME"], args)

customers_df = spark.read.parquet(f"s3://{args['BUCKET_NAME']}/silver/customers/")

profiles_df = spark.read.parquet(f"s3://{args['BUCKET_NAME']}/silver/user_profiles/")

enriched_df = (
    customers_df.alias("c")
    .join(profiles_df.alias("p"), on="client_id", how="left")
    .select(
        "c.client_id",
        coalesce("c.first_name", "p.first_name").alias("first_name"),
        coalesce("c.last_name", "p.last_name").alias("last_name"),
        "c.email",
        "c.registration_date",
        coalesce("c.state", "p.state").alias("state"),
        "p.phone_number",
        "p.age",
    )
)

output_path = f"s3://{args['BUCKET_NAME']}/gold/user_profiles_enriched/"
enriched_df.write.mode("overwrite").parquet(output_path)

job.commit()
