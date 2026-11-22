"""Integration of interval coverage, pricing and settlement reconciliation."""
from dataclasses import dataclass, replace
from interval_coverage import evaluate_coverage
from pricing_liability import calculate_liability
from reconciliation_state_machine import Allocation, reconcile

@dataclass(frozen=True)
class PriorSettlement:
    """Immutable settlement snapshot and optional exact prior-credit evidence."""

    settlement_id: str
    interval_id: str
    settled_report_id: str
    settled_liability_cc: int
    settled_amount_cc: int | None = None
    burn_event_ids: tuple[str, ...] = ()
    committed_allocations: tuple[Allocation, ...] = ()
    committed_allocation_ids: tuple[str, ...] = ()
    committed_reward_record_ids: tuple[str, ...] = ()
    synchronizer_id: str | None = None
    paymaster_id: str | None = None
    obligation_id: str | None = None
    agreement_version: str | None = None
    authority_reference: str | None = None
    prior_allocation_details_complete: bool = False

def reconcile_with_interval_coverage(
    case, expected_intervals, interval_reports, prior_settlements=(),
    allow_late_reports=False, pricing_agreements=None, schedule_anchor=None,
    require_schedule_anchor=False, processed_adjustment_ids=(),
):
    """Reconcile the current report revision and emit append-only correction deltas.

    When prior allocation snapshots are supplied, ``case.allocations`` contains
    additional claims; prior and current allocations are validated together.
    ``processed_adjustment_ids`` must come from durable caller-managed history.
    """
    interval_reports=tuple(interval_reports)
    prior_settlements=tuple(prior_settlements)
    processed_adjustment_ids=set(processed_adjustment_ids)
    coverage=evaluate_coverage(
        expected_intervals,
        interval_reports,
        _parse_time(case.evaluation_time),
        schedule_anchor=schedule_anchor,
        require_schedule_anchor=require_schedule_anchor,
    )
    if coverage["state"]=="INVALID":
        return _blocked(coverage,"BLOCKED_INVALID_INTERVAL_EVIDENCE")
    acceptable=coverage["state"]=="COMPLETE" or (
        allow_late_reports and coverage["state"]=="COMPLETE_WITH_LATE_REPORTS"
    )
    if not acceptable:
        return _blocked(coverage,"BLOCKED_INTERVAL_COVERAGE")

    report_by_id={r.report_id:r for r in interval_reports}
    latest_by_interval={row["interval_id"]:row.get("latest_report_id") for row in coverage["intervals"]}
    prior_settlement_ids=[prior.settlement_id for prior in prior_settlements]
    if (
        any(not isinstance(value,str) or not value.strip() for value in prior_settlement_ids)
        or len(prior_settlement_ids)!=len(set(prior_settlement_ids))
    ):
        return _blocked(coverage,"BLOCKED_INVALID_PRIOR_SETTLEMENT")
    committed_allocations=tuple(
        allocation for prior in prior_settlements
        for allocation in prior.committed_allocations
    )
    object_allocation_ids=[allocation.allocation_id for allocation in committed_allocations]
    declared_allocation_ids=[
        allocation_id for prior in prior_settlements
        for allocation_id in prior.committed_allocation_ids
    ]
    if (
        len(set(object_allocation_ids)) != len(object_allocation_ids)
        or len(set(declared_allocation_ids)) != len(declared_allocation_ids)
    ):
        return _blocked(coverage,"BLOCKED_DUPLICATE_PRIOR_ALLOCATION")
    committed_allocation_ids=set(object_allocation_ids)|set(declared_allocation_ids)
    current_allocation_ids={a.allocation_id for a in case.allocations}
    new_correction_allocations=tuple(case.allocations)
    if current_allocation_ids.intersection(committed_allocation_ids):
        return _blocked(coverage,"BLOCKED_CORRECTION_REPLAY")
    for prior in prior_settlements:
        latest_id=latest_by_interval.get(prior.interval_id)
        if latest_id is None or latest_id==prior.settled_report_id:
            continue
        latest=report_by_id.get(latest_id)
        if latest is None:
            return _blocked(coverage,"BLOCKED_CORRECTION_LINEAGE")
        if (
            (prior.synchronizer_id is not None and latest.synchronizer_id!=prior.synchronizer_id)
            or (prior.paymaster_id is not None and latest.paymaster_id!=prior.paymaster_id)
            or (prior.obligation_id is not None and latest.obligation_id!=prior.obligation_id)
            or (prior.agreement_version is not None and latest.agreement_version!=prior.agreement_version)
            or (prior.authority_reference is not None
                and latest.authority_reference!=prior.authority_reference)
        ):
            return _blocked(coverage,"BLOCKED_CORRECTION_BINDING_CHANGED")
        if (
            type(prior.settled_liability_cc) is not int
            or prior.settled_liability_cc<0
            or not isinstance(prior.settlement_id,str)
            or not prior.settlement_id.strip()
            or not isinstance(prior.settled_report_id,str)
            or not prior.settled_report_id.strip()
        ):
            return _blocked(coverage,"BLOCKED_INVALID_PRIOR_SETTLEMENT")
        if prior.settled_amount_cc is not None and (
            type(prior.settled_amount_cc) is not int or prior.settled_amount_cc<0
        ):
            return _blocked(coverage,"BLOCKED_INVALID_PRIOR_SETTLEMENT")
        if not isinstance(prior.prior_allocation_details_complete,bool):
            return _blocked(coverage,"BLOCKED_INVALID_PRIOR_SETTLEMENT")
        prior_credit_exists=(
            (prior.settled_amount_cc is not None and prior.settled_amount_cc>0)
            or bool(prior.burn_event_ids)
            or bool(prior.committed_allocations)
            or bool(prior.committed_allocation_ids)
        )
        if (
            new_correction_allocations
            and prior_credit_exists
            and not prior.prior_allocation_details_complete
        ):
            return _blocked(coverage,"BLOCKED_PRIOR_ALLOCATION_DETAILS_INCOMPLETE")
        current_reward_ids=set(case.reward_record_ids)
        if (
            current_reward_ids.intersection(prior.committed_reward_record_ids)
        ):
            return _blocked(coverage,"BLOCKED_CORRECTION_REPLAY")
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

    if committed_allocations:
        case=replace(case,allocations=committed_allocations+tuple(case.allocations))
    result=reconcile(case)
    adjustments=[]
    already_processed_adjustment_ids=[]
    for prior in prior_settlements:
        latest_id=latest_by_interval.get(prior.interval_id)
        if latest_id is None or latest_id==prior.settled_report_id:
            continue
        if latest_id not in report_by_id or prior.settled_report_id not in report_by_id:
            return _blocked(coverage,"BLOCKED_CORRECTION_LINEAGE")
        if (
            report_by_id[prior.settled_report_id].interval_id!=prior.interval_id
            or report_by_id[latest_id].interval_id!=prior.interval_id
        ):
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
            adjustment_id=f"adjust:{prior.settlement_id}:{latest_id}"
            if adjustment_id in processed_adjustment_ids:
                already_processed_adjustment_ids.append(adjustment_id)
                continue
            adjustment={
                "adjustment_id":adjustment_id,
                "prior_settlement_id":prior.settlement_id,
                "interval_id":prior.interval_id,
                "superseded_report_id":prior.settled_report_id,
                "corrected_report_id":latest_id,
                "paymaster_id":report_by_id[latest_id].paymaster_id,
                "synchronizer_id":report_by_id[latest_id].synchronizer_id,
                "obligation_id":report_by_id[latest_id].obligation_id,
                "agreement_version":report_by_id[latest_id].agreement_version,
                "authority_reference":report_by_id[latest_id].authority_reference,
                "prior_burn_event_ids":tuple(sorted(
                    set(prior.burn_event_ids)
                    | {allocation.burn_event_id for allocation in prior.committed_allocations}
                )),
                "prior_allocation_ids":tuple(sorted(
                    set(prior.committed_allocation_ids)
                    | {allocation.allocation_id for allocation in prior.committed_allocations}
                )),
                "prior_allocation_details_complete":prior.prior_allocation_details_complete,
                "prior_reward_record_ids":tuple(prior.committed_reward_record_ids),
                "current_allocation_ids":tuple(sorted(
                    allocation.allocation_id for allocation in new_correction_allocations
                    if allocation.obligation_id==report_by_id[latest_id].obligation_id
                )),
                "current_burn_event_ids":tuple(sorted({
                    allocation.burn_event_id for allocation in new_correction_allocations
                    if allocation.obligation_id==report_by_id[latest_id].obligation_id
                })),
                "previous_liability_cc":prior.settled_liability_cc,
                "revised_liability_cc":revised,
                "adjustment_cc":delta,
                "prior_settled_amount_cc":prior.settled_amount_cc,
                "outstanding_after_correction_cc":(
                    max(0,revised-prior.settled_amount_cc)
                    if prior.settled_amount_cc is not None else None
                ),
                "credit_candidate_cc":(
                    max(0,prior.settled_amount_cc-revised)
                    if prior.settled_amount_cc is not None else None
                ),
                "status":"REQUIRES_SEPARATE_SETTLEMENT",
                "reward_adjustment_state":(
                    "REQUIRES_EXPLICIT_REWARD_RECONCILIATION"
                    if prior.committed_reward_record_ids
                    else "NO_PRIOR_REWARD_IDS_RECORDED"
                ),
            }
            if prior.settled_amount_cc is not None:
                new_allocation_amount=sum(
                    allocation.amount_cc for allocation in new_correction_allocations
                    if allocation.obligation_id==report_by_id[latest_id].obligation_id
                )
                adjustment["new_allocation_amount_cc"]=new_allocation_amount
                adjustment["outstanding_after_new_allocations_cc"]=max(
                    0,revised-prior.settled_amount_cc-new_allocation_amount
                )
            else:
                adjustment["new_allocation_amount_cc"]=None
                adjustment["outstanding_after_new_allocations_cc"]=None
            if prior.settled_amount_cc is None:
                adjustment["settlement_state"]="SETTLED_AMOUNT_UNKNOWN"
            elif prior.settled_amount_cc < prior.settled_liability_cc:
                adjustment["settlement_state"]="PARTIALLY_SETTLED"
            elif prior.settled_amount_cc == prior.settled_liability_cc:
                adjustment["settlement_state"]="FULLY_SETTLED"
            else:
                adjustment["settlement_state"]="PRIOR_OVERPAID"
            if prior.settled_liability_cc + delta != revised:
                return _blocked(coverage,"BLOCKED_ADJUSTMENT_BALANCE")
            adjustments.append(adjustment)
    result["coverage"]=coverage
    result["pricing_results"]=pricing_results
    result["adjustments"]=adjustments
    result["already_processed_adjustment_ids"]=tuple(sorted(already_processed_adjustment_ids))
    result["correction_policy"]="APPEND_ONLY_ADJUSTMENT"
    result["correction_credit_policy"]="NO_AUTOMATIC_REFUND_OR_CARRY_FORWARD"
    return result

def _blocked(coverage,state):
    return {"coverage":coverage,"payment_state":state,"overall_state":state,"adjustments":[]}

def _parse_time(value):
    from datetime import datetime
    return datetime.fromisoformat(value.replace("Z","+00:00"))
