from dagster import asset
from dagster import define_asset_job
from dagster import load_assets_from_current_module


@asset
def return_five():
    return 5


@asset
def add_one():
    return 1


@asset
def do_stuff():
    add_one(return_five())


assets = load_assets_from_current_module()


job = define_asset_job(
    name="experiment_job",
    selection=[do_stuff],
    # partitions_def=daily_partitions_def,
)

# schedule = build_schedule_from_partitioned_job(job, minute_of_hour=15, hour_of_day=15)
