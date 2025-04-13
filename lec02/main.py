from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/")
def health_check():
    return jsonify({"status": "OK"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081)
