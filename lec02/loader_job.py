import traceback

from flask import Flask, jsonify, request, Response

from lec02.bll.loader import convert_data_to_stg_format

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
        raw_dir = input_data["raw_dir"]
        stg_dir = input_data["stg_dir"]
    except KeyError:
        return generate_error_json(
            "Both raw_dir and stg_dir parameters should be provided!"
        ), 400

    try:
        result_dir_path = convert_data_to_stg_format(raw_dir, stg_dir)
        return jsonify(
            {
                "status": "OK",
                "result_dir_path": result_dir_path,
            }
        ), 201
    except FileNotFoundError as exception:
        return generate_error_json(str(exception)), 404
    except OSError as exception:
        return generate_error_json(
            f"Error while trying to save results: {traceback.format_exception(exception)}",
        ), 500


if __name__ == '__main__':
    app.run(host="localhost", port=8082, debug=True)
