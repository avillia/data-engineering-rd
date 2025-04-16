import traceback
from datetime import datetime
from os import getenv

from flask import Flask, jsonify, request, Response
from requests.exceptions import HTTPError

from lec02.bll.extractor import fetch_sales_api

AUTH_TOKEN = getenv("API_AUTH_TOKEN")
API_URL = "https://fake-api-vycpfa6oca-uc.a.run.app/"


if not AUTH_TOKEN:
    raise KeyError("'API_AUTH_TOKEN' environment variable must be set!")

app = Flask(__name__)


def generate_error_json(message: str) -> Response:
    return jsonify(
        {
            "status": "ERROR",
            "error": message,
        }
    )


@app.get("/")
def health_check():
    return jsonify({"status": "OK"})


@app.post("/")
def fetch_data_from_sales_API():
    try:
        input_data: dict[str:str] = request.json
        date = datetime.strptime(input_data["date"], "%Y-%m-%d").date()
        raw_dir = input_data["raw_dir"]
    except ValueError:
        return generate_error_json(
            "Date is in a wrong format! Must be 'YYYY-MM-DD'!"
        ), 400
    except KeyError:
        return generate_error_json(
            "Both raw_dir and date parameters should be provided!"
        ), 400

    try:
        result_dir_path = fetch_sales_api(date, API_URL, AUTH_TOKEN, raw_dir)
        return jsonify(
            {
                "status": "OK",
                "result_dir_path": result_dir_path,
            }
        ), 201
    except ValueError as exception:
        return generate_error_json(str(exception)), 404
    except HTTPError as exception:
        return generate_error_json(
            f"Error on the sales API side: {traceback.format_exception(exception)}",
        ), 503
    except OSError as exception:
        return generate_error_json(
            f"Error while trying to save results: {traceback.format_exception(exception)}",
        ), 500


if __name__ == "__main__":
    app.run(host="localhost", port=8081, debug=True)
