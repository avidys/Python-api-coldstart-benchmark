"""FastAPI application exposed as an AWS Lambda handler."""
from fastapi import FastAPI
from mangum import Mangum

app = FastAPI(title="FastAPI Cold Start Benchmark")


@app.get("/")
def read_root():
    """Return a simple JSON payload."""
    return {"message": "Hello from FastAPI"}


_handler = Mangum(app)


def lambda_handler(event, context):
    """Entrypoint that mimics the AWS Lambda handler signature."""
    return _handler(event, context)
