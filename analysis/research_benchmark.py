"""Reproducible microbenchmarks for existing Canton accounting research prototypes.

Run from the repository root:
  python analysis/research_benchmark.py --repeats 30 --sizes 10,50,100,250

Outputs JSON to stdout. Measurements describe this local research code and
synthetic fixtures only; they are not Canton production benchmarks.
"""
import argparse
import json
import statistics
import sys
import time
import tracemalloc
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from aggregate_linear_leakage import matrix_rank, uniquely_identifiable_participants
from portfolio_allocation_model import validate_allocations
from settlement_manifest_validator import (
    BurnEvidence, IntervalEvidence, SettlementManifest, validate_manifest,
)


def percentile(values, q):
    ordered = sorted(values)
    if not ordered:
        return None
    index = min(len(ordered) - 1, max(0, int((len(ordered) - 1) * q)))
    return ordered[index]


def measure(fn, repeats):
    for _ in range(min(3, repeats)):
        fn()
    samples = []
    tracemalloc.start()
    for _ in range(repeats):
        start = time.perf_counter_ns()
        fn()
        samples.append((time.perf_counter_ns() - start) / 1_000_000)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {
        "median_ms": round(statistics.median(samples), 6),
        "p95_ms": round(percentile(samples, 0.95), 6),
        "min_ms": round(min(samples), 6),
        "max_ms": round(max(samples), 6),
        "peak_traced_bytes": peak,
        "repeats": repeats,
    }


def manifest_fixture(count):
    intervals = tuple(
        IntervalEvidence(
            start=i * 600,
            end=(i + 1) * 600,
            status="Ok",
            traffic_bytes=1024 + i,
            agreement_version="agreement-v1",
            report_digest=f"sha256:report-{i:06d}",
        )
        for i in range(count)
    )
    manifest = SettlementManifest(
        settlement_id=f"settlement-{count}",
        synchronizer_id="sync-A",
        window_start=0,
        window_end=count * 600,
        intervals=intervals,
        expected_cc=Decimal("1.00"),
        burns=(BurnEvidence("burn-001", Decimal("1.00"), f"settlement-{count}"),),
    )
    payload = {
        "settlement_id": manifest.settlement_id,
        "synchronizer_id": manifest.synchronizer_id,
        "window_start": manifest.window_start,
        "window_end": manifest.window_end,
        "intervals": [
            {
                "start": x.start, "end": x.end, "status": x.status,
                "traffic_bytes": x.traffic_bytes,
                "agreement_version": x.agreement_version,
                "report_digest": x.report_digest,
            }
            for x in manifest.intervals
        ],
        "expected_cc": str(manifest.expected_cc),
        "burns": [
            {"event_id": x.event_id, "amount_cc": str(x.amount_cc),
             "settlement_id": x.settlement_id}
            for x in manifest.burns
        ],
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return manifest, len(encoded)


def allocation_fixture(count):
    obligations = {f"sync-{i}": 1 for i in range(count)}
    allocations = [
        {
            "allocation_id": f"alloc-{i}",
            "obligation": f"sync-{i}",
            "burn_id": "burn-benchmark",
            "amount_cc": 1,
        }
        for i in range(count)
    ]
    scenario = {
        "burn_id": "burn-benchmark",
        "burn_total_cc": count,
        "due_by_obligation": obligations,
        "allocations": allocations,
    }
    encoded = json.dumps(scenario, sort_keys=True, separators=(",", ":")).encode()
    return scenario, len(encoded)


def privacy_fixture(count):
    # Two overlapping aggregates: the difference isolates participant 0.
    rows = [[1] * count, [0] + [1] * (count - 1)]
    encoded = json.dumps(rows, separators=(",", ":")).encode()
    return rows, len(encoded)


def run_size(count, repeats):
    manifest, manifest_bytes = manifest_fixture(count)
    allocation, allocation_bytes = allocation_fixture(count)
    rows, privacy_bytes = privacy_fixture(count)

    manifest_result = validate_manifest(manifest)
    allocation_result = validate_allocations(allocation)
    identified = uniquely_identifiable_participants(rows)
    if manifest_result.status != "reconciled":
        raise AssertionError(f"manifest fixture invalid at size {count}: {manifest_result}")
    if not allocation_result["valid"]:
        raise AssertionError(f"allocation fixture invalid at size {count}: {allocation_result}")
    if identified != [0]:
        raise AssertionError(f"privacy fixture did not isolate participant 0: {identified}")

    return {
        "scale": count,
        "manifest": {
            "serialized_bytes": manifest_bytes,
            "validation": measure(lambda: validate_manifest(manifest), repeats),
        },
        "allocation": {
            "serialized_bytes": allocation_bytes,
            "validation": measure(lambda: validate_allocations(allocation), repeats),
        },
        "privacy": {
            "matrix_serialized_bytes": privacy_bytes,
            "matrix_rank": matrix_rank(rows),
            "uniquely_identifiable_participant_indices": identified,
            "analysis": measure(lambda: uniquely_identifiable_participants(rows), repeats),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeats", type=int, default=30)
    parser.add_argument("--sizes", default="10,50,100,250")
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error("--repeats must be positive")
    try:
        sizes = [int(value) for value in args.sizes.split(",")]
    except ValueError:
        parser.error("--sizes must be comma-separated positive integers")
    if not sizes or any(value < 1 for value in sizes) or sizes != sorted(set(sizes)):
        parser.error("--sizes must be unique, ascending positive integers")

    output = {
        "evidence_class": "LOCAL_SYNTHETIC_MICROBENCHMARK",
        "warning": (
            "Not Canton production performance. Results depend on local hardware, "
            "Python version, runtime load and synthetic workload shape."
        ),
        "environment": {
            "python": sys.version,
            "platform": sys.platform,
        },
        "method": {
            "timing": "perf_counter_ns; median, nearest-rank lower p95, min and max",
            "memory": "tracemalloc peak across repeated calls; excludes interpreter baseline",
            "serialization": "UTF-8 compact sorted JSON; schema-specific research fixture",
            "warmup_calls": min(3, args.repeats),
        },
        "results": [run_size(size, args.repeats) for size in sizes],
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
