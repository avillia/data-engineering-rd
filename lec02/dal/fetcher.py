from requests import get as run_get_request


def get_sales(date: str, api_url: str, api_token: str) -> list[dict]:
    auth_headers = {
        "Authorization": api_token,
    }

    sales_data: list[dict] = []

    page = 1
    still_something_to_fetch = True
    while still_something_to_fetch:
        response = run_get_request(
            api_url,
            headers=auth_headers,
            params={
                "date": date,
                "page": page,
            },
        )
        if response.status_code == 200:
            sales_data.extend(response.json())
            page += 1
            still_something_to_fetch = True
        if response.status_code == 404:
            still_something_to_fetch = False

    if not sales_data:
        raise ValueError(f"Nothing found in the source API for the requested {date=}!")

    return sales_data
