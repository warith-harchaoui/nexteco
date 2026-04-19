#!/usr/bin/env python3
from __future__ import annotations

import argparse
import statistics
import time

from nexteco.model import load_yaml, render_markdown


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark NextEco Markdown rendering")
    parser.add_argument("input", nargs="?", default="cost_of_running.full.yaml.example")
    parser.add_argument("--iterations", type=int, default=20)
    args = parser.parse_args()

    data = load_yaml(args.input)
    samples = []
    for _ in range(args.iterations):
        start = time.perf_counter()
        render_markdown(data)
        samples.append(time.perf_counter() - start)

    mean_s = statistics.mean(samples)
    median_s = statistics.median(samples)
    print("benchmark: render_markdown")
    print(f"input: {args.input}")
    print(f"iterations: {args.iterations}")
    print(f"mean_seconds: {mean_s:.6f}")
    print(f"median_seconds: {median_s:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
