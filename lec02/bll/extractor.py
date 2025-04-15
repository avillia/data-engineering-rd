from datetime import date as Date

from lec02.dal.fetcher import get_sales
from lec02.dal.storager import dump_to_raw_folder


def fetch_sales_api(date: Date, api_url: str, api_token: str, file_storage: str) -> str:
    endpoint = "sales"
    date_as_str = date.strftime("%Y-%m-%d")
    data = get_sales(
        date_as_str,
        api_url + endpoint,
        api_token,
    )
    file_name = dump_to_raw_folder(
        data,
        file_storage,
        endpoint,
        date_as_str,
    )
    return file_name
