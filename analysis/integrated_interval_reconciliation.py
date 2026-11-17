"""Integration of interval coverage, pricing and settlement reconciliation."""
from dataclasses import dataclass, replace
from interval_coverage import evaluate_coverage
from pricing_liability import calculate_liability
from reconciliation_state_machine import reconcile

@dataclass(frozen=True)
class PriorSettlement:
    settlement_id: str
    interval_id: str
    settled_report_id: str
    settled_liability_cc: int

def reconcile_with_interval_coverage(
    case, expected_intervals, interval_reports, prior_settlements=(),
    allow_late_reports=False, pricing_agreements=None,
):
    interval_reports=tuple(interval_reports)
    coverage=evaluate_coverage(expected_intervals,interval_reports,_parse_time(case.evaluation_time))
    if coverage["state"]=="INVALID":
        return _blocked(coverage,"BLOCKED_INVALID_INTERVAL_EVIDENCE")
    acceptable=coverage["state"]=="COMPLETE" or (
        allow_late_reports and coverage["state"]=="COMPLETE_WITH_LATE_REPORTS"
    )
    if not acceptable:
        return _blocked(coverage,"BLOCKED_INTERVAL_COVERAGE")

    report_by_id={r.report_id:r for r in interval_reports}
    latest_by_interval={row["interval_id"]:row.get("latest_report_id") for row in coverage["intervals"]}
    liabilities={}
    pricing_results={}
    obligation_for_interval={}
    if pricing_agreements is not None:
        for interval_id,report_id in latest_by_interval.items():
            report=report_by_id[report_id]
            if report.agreement_version not in pricing_agreements:
                return _blocked(coverage,"BLOCKED_PRICING_AGREEMENT")
            try:
                priced=calculate_liability(report,pricing_agreements[report.agreement_version])
            except (ValueError,TypeError) as exc:
                out=_blocked(coverage,"BLOCKED_PRICING_INPUT")
                out["pricing_error"]=str(exc)
                return out
            liabilities[report_id]=priced["liability_cc"]
            pricing_results[report_id]=priced
            obligation_id=report.obligation_id
            if obligation_id is None:
                linked=next((x for x in case.reports if x.report_id==report_id),None)
                if linked is None:
                    prior=next((p for p in prior_settlements if p.interval_id==interval_id),None)
                    if prior:
                        linked=next((x for x in case.reports if x.report_id==prior.settled_report_id),None)
                obligation_id=linked.obligation_id if linked else None
            if obligation_id is None:
                return _blocked(coverage,"BLOCKED_REPORT_BINDING")
            obligation_for_interval[interval_id]=obligation_id
            if report.synchronizer_id is None:
                return _blocked(coverage,"BLOCKED_REPORT_BINDING")
            obligation=next((o for o in case.obligations if o.obligation_id==obligation_id),None)
            if obligation is None or obligation.synchronizer_id!=report.synchronizer_id:
                return _blocked(coverage,"BLOCKED_REPORT_BINDING")

        # Multiple expected intervals may contribute to one obligation.
        # Sum their separately priced liabilities instead of overwriting them.
        priced_by_obligation={}
        for interval_id,obligation_id in obligation_for_interval.items():
            priced_by_obligation[obligation_id]=(
                priced_by_obligation.get(obligation_id,0)
                + liabilities[latest_by_interval[interval_id]]
            )
        case=replace(case,obligations=tuple(
            replace(o,due_cc=priced_by_obligation.get(o.obligation_id,o.due_cc))
            for o in case.obligations
        ))

    result=reconcile(case)
    adjustments=[]
    for prior in prior_settlements:
        latest_id=latest_by_interval.get(prior.interval_id)
        if latest_id is None or latest_id==prior.settled_report_id:
            continue
        if latest_id not in report_by_id or prior.settled_report_id not in report_by_id:
            return _blocked(coverage,"BLOCKED_CORRECTION_LINEAGE")
        if pricing_agreements is not None:
            revised=liabilities[latest_id]
        else:
            supplied=getattr(case,"liability_by_report_id",{}) or {}
            if latest_id not in supplied:
                return _blocked(coverage,"BLOCKED_CORRECTION_LIABILITY")
            revised=supplied[latest_id]
        delta=revised-prior.settled_liability_cc
        if delta:
            adjustments.append({
                "adjustment_id":f"adjust:{prior.settlement_id}:{latest_id}",
                "prior_settlement_id":prior.settlement_id,
                "interval_id":prior.interval_id,
                "superseded_report_id":prior.settled_report_id,
                "corrected_report_id":latest_id,
                "previous_liability_cc":prior.settled_liability_cc,
                "revised_liability_cc":revised,
                "adjustment_cc":delta,
                "status":"REQUIRES_SEPARATE_SETTLEMENT",
            })
    result["coverage"]=coverage
    result["pricing_results"]=pricing_results
    result["adjustments"]=adjustments
    result["correction_policy"]="APPEND_ONLY_ADJUSTMENT"
    return result

def _blocked(coverage,state):
    return {"coverage":coverage,"payment_state":state,"overall_state":state,"adjustments":[]}

def _parse_time(value):
    from datetime import datetime
    return datetime.fromisoformat(value.replace("Z","+00:00"))
