"""Parameterized incremental cost model for accounting-assurance architectures.

All monetary inputs use one caller-selected currency and evaluation period.
The model does not provide default prices, probabilities or benchmarks.
It excludes residual expected-loss estimates unless separately evidenced.
"""
from decimal import Decimal, InvalidOperation

ARCHITECTURES = (
    "public_burn_only",
    "signed_reconciliation",
    "independent_confidential_audit",
    "cryptographic_proof",
)

REQUIRED_FIELDS = (
    "implementation_cost", "interval_count", "report_cost_per_interval",
    "exception_count", "investigation_cost_per_exception", "review_hours",
    "loaded_hourly_rate", "evidence_storage_gb", "storage_cost_per_gb",
    "delay_cost",
)


def _decimal(value, field):
    if isinstance(value, bool):
        raise ValueError(f"{field} must be a non-negative number")
    try:
        result = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError(f"{field} must be a non-negative number") from None
    if not result.is_finite() or result < 0:
        raise ValueError(f"{field} must be finite and non-negative")
    return result


def _count(value, field):
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{field} must be a non-negative integer")
    return value


def cost_breakdown(parameters):
    """Calculate one-time, recurring and total costs for one architecture."""
    missing = sorted(set(REQUIRED_FIELDS) - set(parameters))
    if missing:
        raise ValueError("Missing required cost inputs: " + ", ".join(missing))

    implementation = _decimal(parameters["implementation_cost"], "implementation_cost")
    intervals = _count(parameters["interval_count"], "interval_count")
    exceptions = _count(parameters["exception_count"], "exception_count")
    report_unit = _decimal(parameters["report_cost_per_interval"], "report_cost_per_interval")
    investigation_unit = _decimal(parameters["investigation_cost_per_exception"], "investigation_cost_per_exception")
    review_hours = _decimal(parameters["review_hours"], "review_hours")
    hourly_rate = _decimal(parameters["loaded_hourly_rate"], "loaded_hourly_rate")
    storage_gb = _decimal(parameters["evidence_storage_gb"], "evidence_storage_gb")
    storage_rate = _decimal(parameters["storage_cost_per_gb"], "storage_cost_per_gb")
    delay = _decimal(parameters["delay_cost"], "delay_cost")

    report_processing = intervals * report_unit
    exception_investigation = exceptions * investigation_unit
    human_review = review_hours * hourly_rate
    storage = storage_gb * storage_rate
    recurring = report_processing + exception_investigation + human_review + storage + delay
    total = implementation + recurring

    return {
        "one_time_implementation_cost": implementation,
        "report_processing_cost": report_processing,
        "exception_investigation_cost": exception_investigation,
        "human_review_cost": human_review,
        "evidence_storage_cost": storage,
        "delay_cost": delay,
        "recurring_cost": recurring,
        "total_cost": total,
        "interval_count": intervals,
        "exception_count": exceptions,
        "currency": parameters.get("currency", "UNSPECIFIED"),
        "evaluation_period": parameters.get("evaluation_period", "UNSPECIFIED"),
        "residual_expected_loss_included": False,
    }


def compare_architectures(cost_inputs, baseline="public_burn_only"):
    """Compare supplied architecture inputs against a supplied baseline."""
    if baseline not in ARCHITECTURES:
        raise KeyError(f"Unknown baseline architecture: {baseline}")
    missing_architectures = sorted(set(ARCHITECTURES) - set(cost_inputs))
    if missing_architectures:
        raise ValueError("Missing architecture cost inputs: " + ", ".join(missing_architectures))

    results = {name: cost_breakdown(cost_inputs[name]) for name in ARCHITECTURES}
    base = results[baseline]["total_cost"]
    for result in results.values():
        delta = result["total_cost"] - base
        intervals = result["interval_count"]
        result["delta_vs_baseline"] = delta
        result["break_even_avoided_loss_per_interval"] = delta / intervals if intervals else None

    return {
        "baseline": baseline,
        "currency": results[baseline]["currency"],
        "evaluation_period": results[baseline]["evaluation_period"],
        "results": results,
        "interpretation": (
            "Break-even avoided loss is the average avoided loss per interval "
            "required to offset incremental cost, assuming comparable interval counts. "
            "It is a threshold, not an estimate of realised savings."
        ),
        "evidence_status": "PARAMETERISED_INPUTS_ONLY",
    }


if __name__ == "__main__":
    print(
        "No benchmark values are bundled. Supply measured or explicitly "
        "illustrative inputs to cost_breakdown() or compare_architectures()."
    )
