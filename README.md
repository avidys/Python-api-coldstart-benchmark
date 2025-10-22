# Python API Cold Start Benchmark

This project provides a reproducible benchmark that compares the cold start time of
FastAPI and Flask applications when they are packaged like AWS Lambda functions.

## Project layout

```
benchmark.py               # Benchmark driver
fastapi_function/           # FastAPI Lambda-style handler and helper
flask_function/             # Flask Lambda-style handler and helper
requirements.txt            # Python dependencies for the benchmark
```

Each framework exposes a simple handler that responds to an HTTP `GET /` request.
The benchmark script launches a fresh Python interpreter for every invocation to
capture realistic cold start timings (imports + handler execution).

## Getting started

1. Create and activate a virtual environment (optional but recommended).
2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the benchmark. The default executes three invocations per framework—the
   first represents the cold start and the remaining runs approximate warm
   starts:

   ```bash
   python benchmark.py --runs 3
   ```

4. Sample output:

   ```
   Framework | Cold start (s) | Warm avg (s) | Warm stdev (s)
   --------- | -------------- | ------------ | --------------
   fastapi   |        0.1800 |       0.0300 |         0.0020
   flask     |        0.1200 |       0.0200 |         0.0010
   ```

   Actual values depend on your machine. Increase `--runs` to gather more warm
   start samples.

The resulting numbers give a quick comparison of how much time the two frameworks
need to be imported and invoked as serverless functions from a cold state.
