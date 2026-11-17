"""Synthetic comparison of four accounting-assurance architectures.

This model encodes evidence limits, not real-world detection probabilities.
All amounts and activity values are illustrative.
"""

ARCHITECTURES = (
    "public_burn_only",
    "signed_reconciliation",
    "independent_confidential_audit",
    "cryptographic_proof",
)

SCENARIOS = {
    "accurate_accounting": {
        "actual_activity": 100,
        "reported_activity": 100,
        "liability_cc": 10,
        "burn_cc": 10,
        "report_present": True,
    },
    "under_reporting": {
        "actual_activity": 100,
        "reported_activity": 90,
        "liability_cc": 9,
        "burn_cc": 9,
        "report_present": True,
    },
    "missing_interval": {
        "actual_activity": 100,
        "reported_activity": None,
        "liability_cc": None,
        "burn_cc": 0,
        "report_present": False,
    },
}


def assess(scenario_name: str, architecture: str) -> dict:
    """Assess detectable exceptions under the documented evidence assumptions."""
    if scenario_name not in SCENARIOS:
        raise KeyError(f"Unknown scenario: {scenario_name}")
    if architecture not in ARCHITECTURES:
        raise KeyError(f"Unknown architecture: {architecture}")

    s = SCENARIOS[scenario_name]
    report_present = s["report_present"]
    under_reported = (
        report_present
        and s["reported_activity"] < s["actual_activity"]
    )

    if architecture == "public_burn_only":
        return {
            "exception_detected": False,
            "measurement_assured": False,
            "payment_reconciled": None,
            "result": "burn_observed_only",
            "reason": "Public burn evidence has no required-activity, report, or agreement reference.",
        }

    if architecture == "signed_reconciliation":
        if not report_present:
            return {
                "exception_detected": True,
                "measurement_assured": False,
                "payment_reconciled": False,
                "result": "missing_interval_detected",
                "reason": "An expected-interval schedule and signed coverage manifest expose the omission.",
            }
        return {
            "exception_detected": False,
            "measurement_assured": False,
            "payment_reconciled": s["liability_cc"] == s["burn_cc"],
            "result": "internally_reconciled_unverified_measurement",
            "reason": "The signed report and agreement calculation reconcile, but signatures do not prove source completeness.",
        }

    if architecture == "independent_confidential_audit":
        if not report_present:
            return {
                "exception_detected": True,
                "measurement_assured": True,
                "payment_reconciled": False,
                "result": "missing_interval_detected",
                "reason": "The auditor compares the expected schedule with complete, independently inspectable source records.",
            }
        if under_reported:
            return {
                "exception_detected": True,
                "measurement_assured": True,
                "payment_reconciled": s["liability_cc"] == s["burn_cc"],
                "result": "under_reporting_detected",
                "reason": "The auditor compares the report with independently inspectable source evidence.",
            }
        return {
            "exception_detected": False,
            "measurement_assured": True,
            "payment_reconciled": True,
            "result": "audited_and_reconciled",
            "reason": "The auditor verifies source completeness, agreement calculation, and burn allocation.",
        }

    # A proof can verify a coverage claim only if the expected interval set is
    # itself bound into the statement. It still cannot validate source truth.
    if not report_present:
        return {
            "exception_detected": True,
            "measurement_assured": False,
            "payment_reconciled": False,
            "result": "coverage_proof_missing",
            "reason": "The expected-interval set is public or otherwise verifier-known, so the missing interval prevents a complete proof.",
        }
    return {
        "exception_detected": False,
        "measurement_assured": False,
        "payment_reconciled": s["liability_cc"] == s["burn_cc"],
        "result": "proof_valid_for_submitted_inputs",
        "reason": "The proof verifies committed inputs and arithmetic; it cannot detect omitted source activity absent independent measurement.",
    }


def comparison_matrix() -> list[dict]:
    """Return one result for each of the 3 x 4 scenario/architecture pairs."""
    rows = []
    for scenario_name in SCENARIOS:
        for architecture in ARCHITECTURES:
            rows.append({
                "scenario": scenario_name,
                "architecture": architecture,
                **assess(scenario_name, architecture),
            })
    return rows


if __name__ == "__main__":
    for row in comparison_matrix():
        print(
            f'{row["scenario"]:22} | {row["architecture"]:34} | '
            f'{row["result"]:42} | detected={row["exception_detected"]}'
        )
