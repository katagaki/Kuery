import json
import re
from subprocess import Popen, PIPE, STDOUT

from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/query", methods=["POST"])
def query():
    request_data = request.get_json()
    request_query = request_data["query"]

    subprocess = Popen(
        args=["python", "kx.py", request_query],
        stdout=PIPE,
        stderr=STDOUT
    )
    stdout, stderr = subprocess.communicate()

    subprocess_output = stdout.decode("utf-8")
    response_json = re.search(r"```KXResultJSON```([\s\S]*)```KXResultJSON```", subprocess_output).group(1)
    return jsonify(json.loads(response_json))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
