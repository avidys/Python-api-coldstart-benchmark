"""Flask application exposed as an AWS Lambda handler."""
from __future__ import annotations

from flask import Flask, jsonify
from werkzeug.test import EnvironBuilder
from werkzeug.wrappers import Response as WerkzeugResponse

app = Flask(__name__)


@app.route("/")
def read_root():
    """Return a simple JSON payload."""
    return jsonify(message="Hello from Flask")


def _invoke_via_test_client(event: dict) -> WerkzeugResponse:
    method = event.get("requestContext", {}).get("http", {}).get("method", "GET")
    path = event.get("rawPath", "/")
    query_string = event.get("rawQueryString", "")
    headers = event.get("headers") or {}
    body = event.get("body")

    builder = EnvironBuilder(
        method=method,
        path=path,
        query_string=query_string,
        headers=headers,
        data=body,
    )
    env = builder.get_environ()

    with app.test_client() as client:
        response = client.open(environ_overrides=env)
    return response


def lambda_handler(event, context):
    """Entrypoint that mimics the AWS Lambda handler signature."""
    response = _invoke_via_test_client(event)
    return {
        "statusCode": response.status_code,
        "headers": dict(response.headers),
        "body": response.get_data(as_text=True),
        "isBase64Encoded": False,
    }
