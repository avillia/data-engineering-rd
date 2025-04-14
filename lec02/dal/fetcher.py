from datetime import date as Date

from requests import get as run_get_request


def get_sales(date: Date, api_url: str, api_token: str) -> list[dict]:
    auth_headers = {
        "Authorization": api_token
    }

    response = run_get_request(
        api_url,
        headers=auth_headers,
        params={"date": str(date)},
    )
    response.raise_for_status()

    return response.json()
