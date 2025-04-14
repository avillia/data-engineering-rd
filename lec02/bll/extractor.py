from datetime import date as Date

from dal.fetcher import get_sales
from dal.storager import dump_to_folder


def fetch_sales_api(date: Date, api_url: str, api_token: str, raw_dir: str) -> str:
    data = get_sales(date, api_url, api_token)
    return dump_to_folder(data, raw_dir)
