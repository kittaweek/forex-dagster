from dagster import repository
from experiment.repository import repos as experiment_repo
from missing_data.repository import repos as missing_data_repo


@repository
def forex_ai():
    return [
        *missing_data_repo,
        *experiment_repo,
    ]
