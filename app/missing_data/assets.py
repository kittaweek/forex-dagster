from typing import List

from dagster import asset
from dagster import AssetExecutionContext
from dagster import define_asset_job
from dagster import load_assets_from_current_module
from pyspark.sql import functions as F
from pyspark.sql import Window
from pyspark.sql.functions import col
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType
from pyspark.sql.types import TimestampType

from resources import spark_gcs_session

# from dagster import ScheduleDefinition

symbol = "eur_usd"
gs_path = "gs://forex-ai/dagster/missing_data"
parquet_raws_data_path = f"{gs_path}/raws_data/{symbol}"
parquet_missing_data_path = f"{gs_path}/missing_data/{symbol}"


custom_schema = StructType(
    [
        StructField("symbol", StringType(), False),
        StructField("datetime", TimestampType(), False),
    ]
)
resource_defs = {
    "spark_gcs": spark_gcs_session,
    # "spark": spark_session
}


def get_resources(context: AssetExecutionContext):
    return [
        "aud_cad",
        "aud_jpy",
        "btc_usd",
        "eth_usd",
        "eur_usd",
        "gbp_aud",
        "gbp_cad",
        "gbp_usd",
        "usd_jpy",
        "xag_usd",
        "xau_usd",
    ]


def missing_data_aud_cad(context: AssetExecutionContext) -> str:
    return "aud_cad"


@asset(key="get_raws_data", group_name="raws_data", resource_defs=resource_defs)
def get_raws_data(context: AssetExecutionContext, symbol: List[str]):
    df = context.resources.spark_gcs.read.json(
        f"gs://forex-ai/raws/time_series_{symbol}", schema=custom_schema
    )
    df.select("symbol", "datetime").distinct()
    df.write.parquet(parquet_raws_data_path, mode="overwrite")


@asset(
    key="check_missing_data_asset",
    deps=[get_raws_data],
    group_name="raws_data",
    resource_defs=resource_defs,
)
def check_missing_data_asset(context: AssetExecutionContext):
    df = context.resources.spark_gcs.read.parquet(parquet_raws_data_path)

    w = Window.partitionBy("symbol").orderBy("datetime")
    next_date = F.lead(col("datetime"), 1).over(w)

    df = (
        df.sort("datetime")
        .withColumn("next_date", next_date)
        .withColumn("next_date_timestamp", F.unix_timestamp(next_date))
        .withColumn("datetime_timestamp", F.unix_timestamp(col("datetime")))
        .withColumn(
            "date_diff",
            F.abs(col("next_date_timestamp") - col("datetime_timestamp")),
        )
        .drop("next_date_timestamp", "datetime_timestamp")
    )

    df.write.parquet(parquet_missing_data_path, mode="overwrite")


assets = load_assets_from_current_module()

job = define_asset_job(
    name="missing_data_job",
    selection=[missing_data_aud_cad, get_raws_data, check_missing_data_asset],
    # partitions_def=daily_partitions_def,
)
