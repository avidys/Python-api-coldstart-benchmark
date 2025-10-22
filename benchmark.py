"""Benchmark cold start times for FastAPI and Flask Lambda functions."""
from __future__ import annotations

import argparse
import json
import statistics
import subprocess
import sys
import time
from dataclasses import dataclass
from typing import Dict, List

FRAMEWORK_MODULES: Dict[str, str] = {
    "fastapi": "fastapi_function.invoke",
    "flask": "flask_function.invoke",
}


@dataclass
class BenchmarkResult:
    framework: str
    runs: List[float]

    @property
    def cold_start(self) -> float:
        return self.runs[0]

    @property
    def warm_runs(self) -> List[float]:
        return self.runs[1:]

    @property
    def warm_average(self) -> float | None:
        if not self.warm_runs:
            return None
        return statistics.mean(self.warm_runs)

    @property
    def warm_stdev(self) -> float | None:
        if len(self.warm_runs) <= 1:
            return None
        return statistics.stdev(self.warm_runs)


def invoke_module(module: str) -> float:
    start = time.perf_counter()
    completed = subprocess.run(
        [sys.executable, "-m", module],
        check=True,
        capture_output=True,
        text=True,
    )
    duration = time.perf_counter() - start

    # Ensure the handler returned a JSON response to catch import errors early.
    json.loads(completed.stdout.strip() or "{}")
    return duration


def run_benchmark(framework: str, runs: int) -> BenchmarkResult:
    module = FRAMEWORK_MODULES[framework]
    timings = [invoke_module(module) for _ in range(runs)]
    return BenchmarkResult(framework=framework, runs=timings)


def format_seconds(value: float | None) -> str:
    if value is None:
        return "-"
    return f"{value:.4f}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--runs",
        type=int,
        default=3,
        help="Number of times to invoke each function (default: 3)",
    )
    args = parser.parse_args()

    if args.runs < 1:
        parser.error("--runs must be at least 1")

    results = [run_benchmark(framework, args.runs) for framework in FRAMEWORK_MODULES]

    print("Framework | Cold start (s) | Warm avg (s) | Warm stdev (s)")
    print("--------- | -------------- | ------------ | --------------")
    for result in results:
        print(
            f"{result.framework:<9}|"
            f" {format_seconds(result.cold_start):>14} |"
            f" {format_seconds(result.warm_average):>12} |"
            f" {format_seconds(result.warm_stdev):>14}"
        )


if __name__ == "__main__":
    main()
