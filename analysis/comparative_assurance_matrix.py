"""First comparative assurance experiment for the Canton paymaster case study.

Synthetic scenario model only. It does not execute Canton code or use observed network data.

Run:
    python analysis/comparative_assurance_matrix.py
    python -m unittest discover -s tests -v
"""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Scenario:
    name: str
    actual_units: Optional[int]
    reported_units: Optional[int]
    burn_cc: Optional[float]
    report_present: bool
    source_evidence_available: bool


@dataclass(frozen=True)
class Assessment:
    architecture: str
    scenario: str
    outcome: str
    evidence_used: str
    limitation: str


def assess_public_burn(s: Scenario) -> Assessment:
    return Assessment(
        "A: public burn only", s.name,
        "burn observed; accounting relationship unverified" if s.burn_cc is not None
        else "no burn observed; liability unknown",
        "public burn event only",
        "Cannot inspect private activity, report completeness or agreement liability.",
    )


def assess_signed_reconciliation(s: Scenario, price_per_unit: float = 0.1) -> Assessment:
    if not s.report_present or s.reported_units is None:
        outcome = "incomplete: missing report"
    else:
        calculated = s.reported_units * price_per_unit
        burned = s.burn_cc or 0.0
        outcome = "reconciled to submitted report" if abs(calculated - burned) < 1e-9 \
            else "payment mismatch against submitted report"
    return Assessment(
        "B: signed report + agreement reconciliation", s.name, outcome,
        "signed report, known agreement price and public burn reference",
        "A signature authenticates the report source; it does not establish measurement completeness.",
    )


def assess_confidential_audit(s: Scenario, price_per_unit: float = 0.1) -> Assessment:
    if not s.report_present or s.reported_units is None:
        outcome = "incomplete: missing report/source evidence"
    elif not s.source_evidence_available or s.actual_units is None:
        outcome = "inconclusive: independent source evidence unavailable"
    elif s.reported_units != s.actual_units:
        outcome = "measurement discrepancy detected"
    else:
        expected = s.actual_units * price_per_unit
        burned = s.burn_cc or 0.0
        outcome = "source measurement and payment reconcile" if abs(expected - burned) < 1e-9 \
            else "payment mismatch against independently checked activity"
    return Assessment(
        "C: independent confidential audit", s.name, outcome,
        "report, agreement, burn and independent source evidence where available",
        "Assurance depends on auditor independence, source reliability and complete access.",
    )


def assess_cryptographic_proof(s: Scenario, price_per_unit: float = 0.1,
                               completeness_manifest: bool = True) -> Assessment:
    if not s.report_present or s.reported_units is None:
        outcome = ("proof failure: required interval absent from completeness manifest"
                   if completeness_manifest else
                   "absence not identifiable without completeness manifest")
    else:
        calculated = s.reported_units * price_per_unit
        burned = s.burn_cc or 0.0
        outcome = "proof verifies submitted-input calculation" if abs(calculated - burned) < 1e-9 \
            else "proof rejects submitted-input payment mismatch"
    return Assessment(
        "D: cryptographic proof over submitted inputs", s.name, outcome,
        "commitment/proof for report, agreement calculation and burn allocation",
        "A valid proof over an under-reported input remains valid; source completeness needs a separately trusted measurement binding.",
    )


def run_experiment() -> list[Assessment]:
    scenarios = [
        Scenario("accurate accounting", 100, 100, 10.0, True, True),
        Scenario("under-reporting", 100, 80, 8.0, True, True),
        Scenario("missing report", 100, None, None, False, True),
    ]
    assessors = [
        assess_public_burn,
        assess_signed_reconciliation,
        assess_confidential_audit,
        assess_cryptographic_proof,
    ]
    return [assessor(s) for s in scenarios for assessor in assessors]


def main() -> None:
    rows = run_experiment()
    print("SCENARIO | ARCHITECTURE | RESULT")
    print("-" * 110)
    for row in rows:
        print(f"{row.scenario} | {row.architecture} | {row.outcome}")


if __name__ == "__main__":
    main()
