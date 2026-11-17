"""Synthetic shared-paymaster burn allocation model.

A single public burn may be partitioned across multiple obligations. This model
checks allocation uniqueness, aggregate allocation bounds and due liabilities.
All values are illustrative, not Canton observations.
"""

ARCHITECTURES = (
    "public_burn_only",
    "signed_reconciliation",
    "independent_confidential_audit",
    "cryptographic_proof",
)

SCENARIOS = {
    "valid_partition": {
        "burn_id": "burn-001",
        "burn_total_cc": 10,
        "due_by_obligation": {"sync-A": 6, "sync-B": 4},
        "allocations": [
            {"allocation_id": "alloc-A", "obligation": "sync-A", "burn_id": "burn-001", "amount_cc": 6},
            {"allocation_id": "alloc-B", "obligation": "sync-B", "burn_id": "burn-001", "amount_cc": 4},
        ],
    },
    "duplicate_claim": {
        "burn_id": "burn-001",
        "burn_total_cc": 10,
        "due_by_obligation": {"sync-A": 6, "sync-B": 4},
        "allocations": [
            {"allocation_id": "alloc-A", "obligation": "sync-A", "burn_id": "burn-001", "amount_cc": 6},
            {"allocation_id": "alloc-A", "obligation": "sync-B", "burn_id": "burn-001", "amount_cc": 4},
        ],
    },
    "over_allocation": {
        "burn_id": "burn-001",
        "burn_total_cc": 10,
        "due_by_obligation": {"sync-A": 7, "sync-B": 5},
        "allocations": [
            {"allocation_id": "alloc-A", "obligation": "sync-A", "burn_id": "burn-001", "amount_cc": 7},
            {"allocation_id": "alloc-B", "obligation": "sync-B", "burn_id": "burn-001", "amount_cc": 5},
        ],
    },
    "partial_allocation_shortfall": {
        "burn_id": "burn-001",
        "burn_total_cc": 10,
        "due_by_obligation": {"sync-A": 6, "sync-B": 4},
        "allocations": [
            {"allocation_id": "alloc-A", "obligation": "sync-A", "burn_id": "burn-001", "amount_cc": 6},
            {"allocation_id": "alloc-B", "obligation": "sync-B", "burn_id": "burn-001", "amount_cc": 2},
        ],
    },
}


def validate_allocations(scenario: dict) -> dict:
    """Return deterministic portfolio-level allocation checks."""
    allocations = scenario["allocations"]
    ids = [item["allocation_id"] for item in allocations]
    duplicate_ids = sorted({item for item in ids if ids.count(item) > 1})
    wrong_burn_refs = [
        item["allocation_id"]
        for item in allocations
        if item["burn_id"] != scenario["burn_id"]
    ]
    allocated_total = sum(item["amount_cc"] for item in allocations)
    burn_total = scenario["burn_total_cc"]
    unknown_obligations = sorted({
        item["obligation"]
        for item in allocations
        if item["obligation"] not in scenario["due_by_obligation"]
    })
    by_obligation = {
        obligation: sum(
            item["amount_cc"]
            for item in allocations
            if item["obligation"] == obligation
        )
        for obligation in scenario["due_by_obligation"]
    }
    shortfalls = {
        obligation: due - by_obligation[obligation]
        for obligation, due in scenario["due_by_obligation"].items()
        if by_obligation[obligation] < due
    }
    overpayments = {
        obligation: by_obligation[obligation] - due
        for obligation, due in scenario["due_by_obligation"].items()
        if by_obligation[obligation] > due
    }

    return {
        "duplicate_allocation_ids": duplicate_ids,
        "wrong_burn_references": wrong_burn_refs,
        "unknown_obligations": unknown_obligations,
        "allocated_total_cc": allocated_total,
        "burn_total_cc": burn_total,
        "over_allocated_cc": max(0, allocated_total - burn_total),
        "shortfalls_cc": shortfalls,
        "overpayments_cc": overpayments,
        "valid": (
            not duplicate_ids
            and not wrong_burn_refs
            and not unknown_obligations
            and allocated_total <= burn_total
            and not shortfalls
            and not overpayments
        ),
    }


def assess(scenario_name: str, architecture: str) -> dict:
    """Assess whether the architecture can verify the portfolio allocation."""
    if scenario_name not in SCENARIOS:
        raise KeyError(f"Unknown scenario: {scenario_name}")
    if architecture not in ARCHITECTURES:
        raise KeyError(f"Unknown architecture: {architecture}")

    s = SCENARIOS[scenario_name]
    checks = validate_allocations(s)

    if architecture == "public_burn_only":
        return {
            "exception_detected": False,
            "portfolio_reconciled": None,
            "result": "aggregate_burn_observed_only",
            "reason": "The public burn is visible, but private obligations and allocation claims are not available.",
        }

    # Signed reconciliation and confidential audit see the allocation manifest.
    # Audit additionally has controlled access to the source agreement records.
    # The proof verifies the same allocation constraints over committed values.
    if checks["valid"]:
        return {
            "exception_detected": False,
            "portfolio_reconciled": True,
            "result": "valid_partition",
            "reason": "Unique allocation records partition the observed burn and fully cover both due obligations.",
        }

    issues = []
    if checks["duplicate_allocation_ids"]:
        issues.append("duplicate allocation identifier")
    if checks["wrong_burn_references"]:
        issues.append("allocation references a different burn")
    if checks["unknown_obligations"]:
        issues.append("unknown obligation")
    if checks["over_allocated_cc"]:
        issues.append(f'allocations exceed burn by {checks["over_allocated_cc"]} CC')
    if checks["shortfalls_cc"]:
        issues.append("one or more obligations remain underpaid")
    if checks["overpayments_cc"]:
        issues.append("one or more obligations are over-allocated")

    return {
        "exception_detected": True,
        "portfolio_reconciled": False,
        "result": "allocation_exception_detected",
        "reason": "; ".join(issues) + ".",
    }


def comparison_matrix() -> list[dict]:
    return [
        {
            "scenario": scenario_name,
            "architecture": architecture,
            **assess(scenario_name, architecture),
        }
        for scenario_name in SCENARIOS
        for architecture in ARCHITECTURES
    ]


if __name__ == "__main__":
    for scenario_name, scenario in SCENARIOS.items():
        print(scenario_name, validate_allocations(scenario))
