"""Disclosure-tier model for privacy-preserving accounting assurance.

This is a requirements matrix, not a cryptographic implementation or privacy
proof. It records which evidence each role needs for specified claims.
"""

EVIDENCE = {
    "public_burn_record": "Public ledger burn identifier, amount and timestamp",
    "aggregate_commitment": "Commitment to the private settlement manifest",
    "proof_of_allocation_constraints": "Proof of unique allocation and aggregate bounds",
    "agreement_version_reference": "Identifier of the governing agreement version",
    "exact_obligation_amounts": "Per-synchronizer liabilities and burn allocations",
    "interval_measurement_report": "Detailed interval resource measurements",
    "source_measurement_records": "Underlying records sufficient to independently check measurement",
    "private_transaction_payloads": "Confidential transaction contents and party-level payloads",
}

ROLES = ("public_verifier", "independent_auditor", "operator")

REQUIRED_EVIDENCE = {
    "public_verifier": {
        "public_burn_record",
        "aggregate_commitment",
        "proof_of_allocation_constraints",
        "agreement_version_reference",
    },
    "independent_auditor": {
        "public_burn_record",
        "aggregate_commitment",
        "agreement_version_reference",
        "exact_obligation_amounts",
        "interval_measurement_report",
        "source_measurement_records",
    },
    "operator": set(EVIDENCE),
}

CLAIMS = {
    "burn_exists": {"public_burn_record"},
    "allocation_constraints_hold": {
        "public_burn_record",
        "aggregate_commitment",
        "proof_of_allocation_constraints",
    },
    "correct_agreement_version_used": {"agreement_version_reference"},
    "per_synchronizer_payment_reconciles": {
        "agreement_version_reference",
        "exact_obligation_amounts",
        "public_burn_record",
    },
    "measurement_matches_source_records": {
        "interval_measurement_report",
        "source_measurement_records",
    },
    "private_payload_contents": {"private_transaction_payloads"},
}


def claim_support(role: str, claim: str) -> dict:
    if role not in ROLES:
        raise KeyError(f"Unknown role: {role}")
    if claim not in CLAIMS:
        raise KeyError(f"Unknown claim: {claim}")
    required = CLAIMS[claim]
    available = REQUIRED_EVIDENCE[role]
    missing = sorted(required - available)
    return {
        "role": role,
        "claim": claim,
        "supported": not missing,
        "missing_evidence": missing,
    }


def disclosure_matrix() -> list[dict]:
    return [
        claim_support(role, claim)
        for role in ROLES
        for claim in CLAIMS
    ]


def public_minimisation_check() -> dict:
    """Check that public tier excludes exact private values and payloads."""
    public = REQUIRED_EVIDENCE["public_verifier"]
    prohibited = {
        "exact_obligation_amounts",
        "interval_measurement_report",
        "source_measurement_records",
        "private_transaction_payloads",
    }
    return {
        "prohibited_fields_exposed": sorted(public & prohibited),
        "passes": not (public & prohibited),
    }


if __name__ == "__main__":
    for row in disclosure_matrix():
        print(row)
    print("public_minimisation:", public_minimisation_check())
