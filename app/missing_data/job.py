from dagster import job
from dagster import op

# from pyspark.sql import Window,DataFrame
# from pyspark.sql import functions as F
# from pyspark.sql.functions import col
# from resources import spark_gcs_session
# from assets.raws_data_asset import get_raw_data

# from pyspark.sql.types import (
#     StructType,
#     StructField,
#     StringType,
#     FloatType,
#     TimestampType,
#     DoubleType,
#     LongType,
# )

# resource_defs = {
#     "spark_gcs_session": spark_gcs_session,
# }


# custom_schema = StructType(
#     [
#         StructField("symbol", StringType(), False),
#         StructField("datetime", TimestampType(), False),
#     ]
# )


@op
def add_one(arg):
    return f"Completerd : {arg}"


@job
def do_stuff2():
    add_one()
