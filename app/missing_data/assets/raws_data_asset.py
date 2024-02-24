from dagster import asset


@asset
def get_raw_data(symbol: str) -> str:
    return str


# def get_raw_data(symbol:str) -> DataFrame:
# df = spark.read.json(f"gs://forex-ai/raws/{symbol}", schema=custom_schema)
# return df.select("symbol", "datetime").distinct().sort("datetime")
