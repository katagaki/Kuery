import json

from flask import Flask, render_template, request, jsonify
from pandas import DataFrame

from kx import do_qsql_query

app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/query", methods=["POST"])
def query():
    request_data = request.get_json()
    request_query = request_data["query"]

    query_results: DataFrame = do_qsql_query(request_query)

    return json.dumps(query_results.to_json(), indent=4)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
