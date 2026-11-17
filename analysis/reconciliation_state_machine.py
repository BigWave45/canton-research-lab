"""Synthetic, implementation-neutral paymaster reconciliation state machine.

This model checks submitted records and declared rules. It does not establish
that source measurement captured every chargeable event.
"""
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Report:
    report_id: str
    status: str  # OK, UNDETERMINED, CANNOT_PROVIDE
    agreement_version: str


@dataclass(frozen=True)
class Burn:
    burn_event_id: str
    amount_cc: int


@dataclass(frozen=True)
class Allocation:
    allocation_id: str
    burn_event_id: str
    obligation_id: str
    amount_cc: int


@dataclass(frozen=True)
class Obligation:
    obligation_id: str
    due_cc: int
    authoritative_agreement_version: str
    tolerance_cc: int = 0


@dataclass(frozen=True)
class Case:
    expected_report_ids: tuple[str, ...]
    reports: tuple[Report, ...]
    obligations: tuple[Obligation, ...]
    burns: tuple[Burn, ...]
    allocations: tuple[Allocation, ...]
    evaluation_time: str
    reward_required: bool = True
    reward_record_ids: tuple[str, ...] = ()


def reconcile(case: Case) -> dict:
    """Return independent report, agreement, payment and reward states."""
    expected = set(case.expected_report_ids)
    report_ids = [r.report_id for r in case.reports]
    duplicate_reports = len(report_ids) != len(set(report_ids))
    report_by_id = {r.report_id: r for r in case.reports}
    missing = sorted(expected - set(report_by_id))
    unexpected = sorted(set(report_by_id) - expected)
    invalid_status = sorted(
        r.report_id for r in case.reports
        if r.status not in {"OK", "UNDETERMINED", "CANNOT_PROVIDE"}
    )
    non_ok = sorted(
        r.report_id for r in case.reports if r.status != "OK"
    )

    if duplicate_reports or unexpected or invalid_status:
        report_state = "DISPUTED"
    elif missing or non_ok:
        report_state = "INCOMPLETE"
    else:
        report_state = "COMPLETE"

    obligation_versions = {
        o.authoritative_agreement_version for o in case.obligations
    }
    report_versions = {
        r.agreement_version for r in case.reports if r.status == "OK"
    }
    version_mismatch = bool(
        report_versions - obligation_versions
        or obligation_versions - report_versions
    )
    agreement_state = "MISMATCH" if version_mismatch else "MATCHED"

    burn_by_id = {b.burn_event_id: b for b in case.burns}
    duplicate_burn_ids = len(burn_by_id) != len(case.burns)
    allocation_ids = [a.allocation_id for a in case.allocations]
    duplicate_allocation_ids = len(allocation_ids) != len(set(allocation_ids))
    unknown_burns = sorted({
        a.burn_event_id for a in case.allocations
        if a.burn_event_id not in burn_by_id
    })
    unknown_obligations = sorted({
        a.obligation_id for a in case.allocations
        if a.obligation_id not in {o.obligation_id for o in case.obligations}
    })

    allocated_by_burn = defaultdict(int)
    allocated_by_obligation = defaultdict(int)
    for allocation in case.allocations:
        allocated_by_burn[allocation.burn_event_id] += allocation.amount_cc
        allocated_by_obligation[allocation.obligation_id] += allocation.amount_cc

    overallocated_burns = sorted(
        burn_id for burn_id, allocated in allocated_by_burn.items()
        if burn_id in burn_by_id and allocated > burn_by_id[burn_id].amount_cc
    )
    short_obligations = sorted(
        o.obligation_id for o in case.obligations
        if allocated_by_obligation[o.obligation_id] + o.tolerance_cc < o.due_cc
    )
    invalid_amounts = any(
        x.amount_cc < 0 for x in case.burns
    ) or any(
        a.amount_cc < 0 for a in case.allocations
    ) or any(
        o.due_cc < 0 or o.tolerance_cc < 0 for o in case.obligations
    )

    allocation_invalid = (
        duplicate_burn_ids or duplicate_allocation_ids or bool(unknown_burns)
        or bool(unknown_obligations) or bool(overallocated_burns) or invalid_amounts
    )

    if allocation_invalid:
        allocation_state = "INVALID"
    elif short_obligations:
        allocation_state = "SHORT"
    else:
        allocation_state = "COVERED"

    # A not-yet-due tranche is excluded from due_cc by construction.
    # This model does not calculate contractual schedules; it consumes the
    # authoritative amount due at evaluation_time.
    if report_state != "COMPLETE":
        payment_state = "BLOCKED_INCOMPLETE_REPORTS"
    elif agreement_state != "MATCHED":
        payment_state = "BLOCKED_AGREEMENT_MISMATCH"
    elif allocation_invalid:
        payment_state = "DISPUTED_ALLOCATION"
    elif short_obligations:
        payment_state = "SHORT_PAID"
    else:
        payment_state = "RECONCILED"

    if not case.reward_required:
        reward_state = "NOT_REQUIRED"
    elif not case.reward_record_ids:
        reward_state = "MISSING"
    else:
        reward_state = "RECORDED"

    if payment_state == "RECONCILED" and reward_state == "MISSING":
        overall_state = "REWARD_PENDING"
    elif payment_state == "RECONCILED":
        overall_state = "RECONCILED"
    else:
        overall_state = payment_state

    return {
        "evaluation_time": case.evaluation_time,
        "report_state": report_state,
        "missing_reports": missing,
        "non_ok_reports": non_ok,
        "unexpected_reports": unexpected,
        "agreement_state": agreement_state,
        "allocation_state": allocation_state,
        "overallocated_burns": overallocated_burns,
        "short_obligations": short_obligations,
        "payment_state": payment_state,
        "reward_state": reward_state,
        "overall_state": overall_state,
        "measurement_completeness": "NOT_ESTABLISHED_BY_THIS_MODEL",
        "limitations": [
            "The model checks submitted records, not the truth or completeness of source measurement.",
            "due_cc is supplied as an authoritative input; contractual smoothing is not calculated here.",
            "Agreement authority is assumed; version matching does not establish legal authority.",
            "Reward presence is checked, not reward amount or downstream distribution correctness.",
        ],
    }



def reconcile_with_schedules(
    case: Case,
    schedules: dict,
    prior_credits: dict | None = None,
) -> dict:
    """Calculate due amounts from schedules, then reconcile current allocations.

    schedules maps obligation_id to agreement_schedule.Schedule.
    prior_credits maps obligation_id to eligible prior carry-forward credit.
    """
    from collections import defaultdict
    from dataclasses import replace
    from agreement_schedule import calculate_due

    prior_credits = prior_credits or {}
    allocated = defaultdict(int)
    for allocation in case.allocations:
        allocated[allocation.obligation_id] += allocation.amount_cc

    schedule_results = {}
    scheduled_obligations = []
    schedule_version_mismatches = []
    for obligation in case.obligations:
        if obligation.obligation_id not in schedules:
            raise ValueError(
                f"Missing agreement schedule for {obligation.obligation_id}"
            )
        if schedules[obligation.obligation_id].agreement_version != obligation.authoritative_agreement_version:
            schedule_version_mismatches.append(obligation.obligation_id)
        result = calculate_due(
            schedules[obligation.obligation_id],
            case.evaluation_time,
            allocated[obligation.obligation_id],
            prior_credits.get(obligation.obligation_id, 0),
        )
        schedule_results[obligation.obligation_id] = result
        scheduled_obligations.append(
            replace(
                obligation,
                due_cc=result["due_cc"],
                tolerance_cc=result["tolerance_cc"],
            )
        )

    scheduled_case = replace(case, obligations=tuple(scheduled_obligations))
    result = reconcile(scheduled_case)
    result["schedule_results"] = schedule_results
    result["schedule_version_mismatches"] = schedule_version_mismatches
    if schedule_version_mismatches:
        result["agreement_state"] = "MISMATCH"
        result["payment_state"] = "BLOCKED_AGREEMENT_MISMATCH"
        result["overall_state"] = result["payment_state"]

    # Preserve higher-priority evidence failures. Only refine a valid-record
    # payment shortfall into within-grace versus past-grace.
    if result["payment_state"] == "SHORT_PAID":
        overdue = [
            obligation_id
            for obligation_id, schedule_result in schedule_results.items()
            if schedule_result["past_grace_unpaid_cc"] > schedule_result["tolerance_cc"]
        ]
        if overdue:
            result["payment_state"] = "PAST_GRACE_UNPAID"
            result["overdue_obligations"] = sorted(overdue)
        else:
            result["payment_state"] = "WITHIN_GRACE"
            result["within_grace_obligations"] = sorted(
                obligation_id
                for obligation_id, schedule_result in schedule_results.items()
                if schedule_result["due_unpaid_cc"] > schedule_result["tolerance_cc"]
            )

        result["overall_state"] = result["payment_state"]

    result["due_calculation"] = "CALCULATED_FROM_AGREEMENT_SCHEDULE"
    return result
