"""Integration of interval coverage with settlement reconciliation.

The module is implementation-neutral and consumes synthetic inputs. Corrections
create explicit adjustment records; they never mutate prior settlement records.
"""
from dataclasses import dataclass
from interval_coverage import evaluate_coverage
from reconciliation_state_machine import reconcile

@dataclass(frozen=True)
class PriorSettlement:
    settlement_id: str
    interval_id: str
    settled_report_id: str
    settled_liability_cc: int

def reconcile_with_interval_coverage(
    case, expected_intervals, interval_reports, prior_settlements=(),
    allow_late_reports=False,
):
    coverage = evaluate_coverage(expected_intervals, interval_reports, _parse_time(case.evaluation_time))
    if coverage["state"] == "INVALID":
        return {
            "coverage": coverage,
            "payment_state": "BLOCKED_INVALID_INTERVAL_EVIDENCE",
            "overall_state": "BLOCKED_INVALID_INTERVAL_EVIDENCE",
            "adjustments": [],
        }

    acceptable = coverage["state"] == "COMPLETE" or (
        allow_late_reports and coverage["state"] == "COMPLETE_WITH_LATE_REPORTS"
    )
    if not acceptable:
        return {
            "coverage": coverage,
            "payment_state": "BLOCKED_INTERVAL_COVERAGE",
            "overall_state": "BLOCKED_INTERVAL_COVERAGE",
            "adjustments": [],
        }

    result = reconcile(case)
    latest_by_interval = {
        row["interval_id"]: row.get("latest_report_id")
        for row in coverage["intervals"]
    }
    adjustments = []
    report_by_id = {r.report_id: r for r in interval_reports}
    for prior in prior_settlements:
        latest_id = latest_by_interval.get(prior.interval_id)
        if latest_id is None or latest_id == prior.settled_report_id:
            continue
        if latest_id not in report_by_id or prior.settled_report_id not in report_by_id:
            return {
                "coverage": coverage,
                "payment_state": "BLOCKED_CORRECTION_LINEAGE",
                "overall_state": "BLOCKED_CORRECTION_LINEAGE",
                "adjustments": [],
            }
        # Liability values are supplied by the agreement-aware calculation layer.
        # This integration refuses to infer a new amount from traffic metadata.
        if latest_id not in case.liability_by_report_id:
            return {
                "coverage": coverage,
                "payment_state": "BLOCKED_CORRECTION_LIABILITY",
                "overall_state": "BLOCKED_CORRECTION_LIABILITY",
                "adjustments": [],
            }
        revised = case.liability_by_report_id[latest_id]
        delta = revised - prior.settled_liability_cc
        if delta:
            adjustments.append({
                "adjustment_id": f"adjust:{prior.settlement_id}:{latest_id}",
                "prior_settlement_id": prior.settlement_id,
                "interval_id": prior.interval_id,
                "superseded_report_id": prior.settled_report_id,
                "corrected_report_id": latest_id,
                "previous_liability_cc": prior.settled_liability_cc,
                "revised_liability_cc": revised,
                "adjustment_cc": delta,
                "status": "REQUIRES_SEPARATE_SETTLEMENT",
            })
    result["coverage"] = coverage
    result["adjustments"] = adjustments
    result["correction_policy"] = "APPEND_ONLY_ADJUSTMENT"
    return result

def _parse_time(value):
    from datetime import datetime
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed
