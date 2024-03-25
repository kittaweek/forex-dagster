from dagster import EnvVar
from dagster import resource
from pyspark.sql import SparkSession

from utils.pyspark_gcs import get_spark_gcs_session

###############################################################################
# GCS
###############################################################################
credentials_key = EnvVar("GCP_CREDENTIALS").get_value()
project_id = EnvVar("GCP_PROJECT_ID").get_value()
email = EnvVar("GCP_EMAIL").get_value()


@resource()
def spark_gcs_session() -> SparkSession:
    return get_spark_gcs_session(
        project=project_id, email=email, service_account_keyfile_path=credentials_key
    )


@resource()
def spark_session() -> SparkSession:
    return SparkSession.builder.getOrCreate()
