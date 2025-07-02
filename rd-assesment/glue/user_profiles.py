from sys import argv

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext

args = getResolvedOptions(argv, ["JOB_NAME", "BUCKET_NAME"])
spark_context = SparkContext()
glue_context = GlueContext(spark_context)
spark = glue_context.spark_session
job = Job(glue_context)
job.init(args["JOB_NAME"], args)


verified_dataframe = glue_context.create_dynamic_frame.from_catalog(
    database="default",
    table_name="user_profiles_bronze",
).toDF()


output_path = f"s3://{args['BUCKET_NAME']}/silver/user_profiles/"
verified_dataframe.write.mode("overwrite").parquet(output_path)

job.commit()
