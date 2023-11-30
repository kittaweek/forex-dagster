import os
import re
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Dict

from dotenv import load_dotenv

load_dotenv()


def get_api_key() -> str:
    return os.getenv("SCRAPY_TWELVE_DATA_API_KEY")


def get_headers() -> Dict[str, str]:
    return {
        "Authorization": f"apikey {get_api_key()}",
    }


# interval : 1min | 5min | 15min | 30min | 45min | 1h | 2h | 4h | 1day | 1week | 1month
def get_dates(symbol: str, interval: str, outputsize: int) -> tuple[str, str]:
    input_path = f"./inputs/{symbol}"
    if not os.path.exists(input_path):
        os.makedirs(input_path)
    file_logs = f"{input_path}/{interval}.log"
    datetime_format = "%Y-%m-%d %H:%M:00"

    if os.path.exists(file_logs):
        with open(file_logs) as f:
            end_date = f.read()
    else:
        end_date = datetime.now(timezone.utc).strftime(datetime_format)

    start_date = datetime.strptime(end_date, datetime_format) + _time_delta(
        interval=interval, outputsize=outputsize
    )

    f = open(file_logs, "w")
    f.write(str(start_date))
    f.close()
    return (start_date, end_date)


def _time_delta(interval: str, outputsize: int) -> str:
    interval_val, interval_type = re.match(r"([0-9]+)([a-z]+)", interval, re.I).groups()
    delta_time = int(interval_val) * outputsize * -1

    if interval_type == "min":
        result = timedelta(minutes=delta_time)
    elif interval_type == "h":
        result = timedelta(hours=delta_time)
    elif interval_type == "day":
        result = timedelta(days=delta_time)
    elif interval_type == "week":
        result = timedelta(weeks=delta_time)
    else:
        result = timedelta(weeks=delta_time * 4)
    return result
