import json
import os
import sys

import pykx as kx
from dotenv import load_dotenv

load_dotenv()


def query_q_server(query) -> str:
    try:
        with kx.SyncQConnection(
                host=os.environ.get("KDB_HOST", "localhost"),
                port=int(os.environ.get("KDB_PORT", 5000)),
                username=os.environ.get("KDB_USERNAME", None),
                password=os.environ.get("KDB_PASSWORD", None),
                timeout=120,
                tls=True
        ) as q_connection:
            q_response_in_dataframes = q_connection(query).pd()
            q_response_in_proper_json = q_response_in_dataframes.to_json()
            return json.dumps(json.loads(q_response_in_proper_json), ensure_ascii=False, indent=4)[:1000]
    except Exception as e:
        return f"Error: {str(e)}\nObject: {e}\nType: {type(e)}"


def get_ssl_info():
    try:
        ssl_info = kx.ssl_info().py()
        ssl_info_string = "PyKX SSL Details:\n"
        for key, value in ssl_info.items():
            ssl_info_string += f"{key}: {value}\n"
        return ssl_info_string
    except Exception as e:
        return f"Error: {str(e)}\nObject: {e}\nType: {type(e)}"


if __name__ == "__main__":
    request_query = sys.argv[1] if len(sys.argv) > 1 else None
    if request_query:
        response_json = {
            "result": query_q_server(request_query),
            "sslInfo": get_ssl_info()
        }
    else:
        response_json = {
            "result": "No query provided",
            "sslInfo": get_ssl_info()
        }
    print("```KXResultJSON```")
    print(json.dumps(response_json, ensure_ascii=False, indent=4))
    print("```KXResultJSON```")
