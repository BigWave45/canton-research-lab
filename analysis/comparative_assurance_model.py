"""Synthetic comparison of accounting-assurance architectures.

The model represents evidence capabilities under explicit assumptions. It does
not estimate real-world detection probabilities or describe live Canton data.
All values are illustrative.
"""

ARCHITECTURES = (
    "public_burn_only",
    "signed_reconciliation",
    "independent_confidential_audit",
    "cryptographic_proof",
)

SCENARIOS = {
    "accurate_accounting": {
        "actual_activity": 100, "reported_activity": 100,
        "liability_cc": 10, "burn_cc": 10, "report_present": True,
        "agreement_expected": "v2", "agreement_used": "v2",
        "due_now_cc": 10,
    },
    "under_reporting": {
        "actual_activity": 100, "reported_activity": 90,
        "liability_cc": 9, "burn_cc": 9, "report_present": True,
        "agreement_expected": "v2", "agreement_used": "v2",
        "due_now_cc": 9,
    },
    "missing_interval": {
        "actual_activity": 100, "reported_activity": None,
        "liability_cc": None, "burn_cc": 0, "report_present": False,
        "agreement_expected": "v2", "agreement_used": None,
        "due_now_cc": None,
    },
    "agreement_version_mismatch": {
        "actual_activity": 100, "reported_activity": 100,
        "liability_cc": 8, "burn_cc": 8, "report_present": True,
        "agreement_expected": "v2", "agreement_used": "v1",
        "due_now_cc": 10,
    },
    "smoothing_not_yet_due": {
        "actual_activity": 100, "reported_activity": 100,
        "liability_cc": 10, "burn_cc": 4, "report_present": True,
        "agreement_expected": "v2", "agreement_used": "v2",
        "due_now_cc": 4,
    },
    "smoothing_overdue_shortfall": {
        "actual_activity": 100, "reported_activity": 100,
        "liability_cc": 10, "burn_cc": 4, "report_present": True,
        "agreement_expected": "v2", "agreement_used": "v2",
        "due_now_cc": 10,
    },
}


def assess(scenario_name: str, architecture: str) -> dict:
    """Return what the architecture can establish from its defined evidence."""
    if scenario_name not in SCENARIOS:
        raise KeyError(f"Unknown scenario: {scenario_name}")
    if architecture not in ARCHITECTURES:
        raise KeyError(f"Unknown architecture: {architecture}")

    s = SCENARIOS[scenario_name]
    if architecture == "public_burn_only":
        return {
            "exception_detected": False,
            "measurement_assured": False,
            "agreement_assured": False,
            "payment_reconciled": None,
            "result": "burn_observed_only",
            "reason": "Public burn data alone does not identify the required interval, applicable agreement, liability or due schedule.",
        }

    if not s["report_present"]:
        return {
            "exception_detected": True,
            "measurement_assured": architecture == "independent_confidential_audit",
            "agreement_assured": False,
            "payment_reconciled": False,
            "result": "missing_interval_detected",
            "reason": "The expected interval schedule is known; the required report is absent.",
        }

    version_mismatch = s["agreement_used"] != s["agreement_expected"]
    if version_mismatch:
        return {
            "exception_detected": True,
            "measurement_assured": architecture == "independent_confidential_audit",
            "agreement_assured": True,
            "payment_reconciled": False,
            "result": "agreement_version_mismatch_detected",
            "reason": "The applied agreement version differs from the authoritative version for this interval.",
        }

    under_reported = s["reported_activity"] < s["actual_activity"]
    if under_reported:
        is_audit = architecture == "independent_confidential_audit"
        return {
            "exception_detected": is_audit,
            "measurement_assured": is_audit,
            "agreement_assured": True,
            "payment_reconciled": s["burn_cc"] == s["liability_cc"],
            "result": "under_reporting_detected" if is_audit else "submitted_inputs_reconcile",
            "reason": (
                "Auditor compares the report with independent source records."
                if is_audit else
                "Submitted report, agreement calculation and burn reconcile, but source completeness is not established."
            ),
        }

    # Compare actual burn with the contractual amount due at the evaluation
    # time, not with the entire lifetime liability.
    shortfall = max(0, s["due_now_cc"] - s["burn_cc"])
    if shortfall:
        return {
            "exception_detected": True,
            "measurement_assured": architecture == "independent_confidential_audit",
            "agreement_assured": True,
            "payment_reconciled": False,
            "result": "overdue_shortfall_detected",
            "reason": f"{shortfall} CC remains unpaid against the amount due at this evaluation time.",
        }

    return {
        "exception_detected": False,
        "measurement_assured": architecture == "independent_confidential_audit",
        "agreement_assured": True,
        "payment_reconciled": True,
        "result": (
            "smoothed_payment_current"
            if s["burn_cc"] < s["liability_cc"]
            else "fully_reconciled"
        ),
        "reason": (
            "Burn covers the amount due now; the remaining liability is not yet due."
            if s["burn_cc"] < s["liability_cc"]
            else "Burn covers the full liability due."
        ),
    }


def comparison_matrix() -> list[dict]:
    """Return one result for every scenario/architecture pair."""
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
    for row in comparison_matrix():
        print(
            f'{row["scenario"]:30} | {row["architecture"]:34} | '
            f'{row["result"]:36} | detected={row["exception_detected"]}'
        )
