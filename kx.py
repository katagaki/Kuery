import json
import os
import sys
from io import StringIO
from logging import getLogger
from subprocess import run
from uuid import uuid4

from dotenv import load_dotenv
from pandas import DataFrame, read_json

load_dotenv()

logger = getLogger(__name__)


def do_qsql_query(query: str) -> DataFrame:
    query_results_directory = "./query_results"
    if not os.path.exists(query_results_directory):
        os.makedirs(query_results_directory)

    query_results_path = os.path.abspath(f"{query_results_directory}/{str(uuid4())}.qsr")
    run(["python", "./kx.py", query_results_path, query])

    try:
        with open(query_results_path, "r") as query_results_file:
            subprocess_output_json_string = query_results_file.read()
        os.remove(query_results_path)
    except Exception as error:
        logger.error(f"{error}")
        subprocess_output_json_string = None

    return read_json(StringIO(subprocess_output_json_string), orient="records")


def query_q_server(query: str) -> str:
    try:
        os.environ["SSL_VERIFY_SERVER"] = "NO"

        import pykx as kx

        with kx.SyncQConnection(
                host=os.environ.get("KDB_HOST", "localhost"),
                port=int(os.environ.get("KDB_PORT", 5000)),
                username=os.environ.get("KDB_USERNAME", None),
                password=os.environ.get("KDB_PASSWORD", None),
                timeout=10,
                tls=True,
        ) as q_connection:
            q_response_in_dataframes: DataFrame = q_connection(query).pd()
            q_response_in_json: str = q_response_in_dataframes.to_json(orient="records", date_format="iso")
            return json.dumps(json.loads(q_response_in_json), ensure_ascii=False, indent=4)
    except Exception as error:
        return f"{error} ({type(error)})"


if __name__ == "__main__":
    executor_query_results_path = sys.argv[1] if len(sys.argv) > 2 else None
    executor_query = sys.argv[2] if len(sys.argv) > 2 else None

    query_results = query_q_server(executor_query)

    try:
        with open(executor_query_results_path, "w") as executor_query_results_file:
            executor_query_results_file.write(query_results)
    except Exception as main_thread_error:
        logger.error(f"{main_thread_error}")
