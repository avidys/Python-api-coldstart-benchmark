"""Utility to invoke the Flask Lambda handler once."""
from __future__ import annotations

import json
from typing import Any

from .handler import lambda_handler

EVENT: dict[str, Any] = {
    "version": "2.0",
    "routeKey": "GET /",
    "rawPath": "/",
    "rawQueryString": "",
    "headers": {
        "accept": "application/json",
        "host": "example.com",
    },
    "requestContext": {
        "http": {
            "method": "GET",
            "path": "/",
            "protocol": "HTTP/1.1",
        }
    },
    "isBase64Encoded": False,
}


def main() -> None:
    response = lambda_handler(EVENT, context=None)
    print(json.dumps(response))


if __name__ == "__main__":
    main()
