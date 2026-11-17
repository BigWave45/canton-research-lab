"""Deterministic agreement schedule calculator for synthetic CC obligations.

All timestamps must be ISO-8601 strings with an explicit UTC offset. Amounts
are integer CC smallest units to avoid floating-point rounding.
"""
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Iterable


@dataclass(frozen=True)
class Tranche:
    tranche_id: str
    due_at: str
    amount_cc: int


@dataclass(frozen=True)
class Schedule:
    agreement_version: str
    effective_from: str
    effective_until: str | None
    tranches: tuple[Tranche, ...]
    grace_period_seconds: int = 0
    tolerance_cc: int = 0
    carry_forward_enabled: bool = False


def _parse_timestamp(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid ISO-8601 timestamp: {value!r}") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"Timestamp must include a UTC offset: {value!r}")
    return parsed


def calculate_due(
    schedule: Schedule,
    evaluation_time: str,
    allocated_payment_cc: int,
    prior_credit_cc: int = 0,
) -> dict:
    """Calculate due, overdue and payment status for one agreement obligation.

    Payments are applied FIFO to the oldest due tranches. Prior credit is
    applied only when carry-forward is explicitly enabled. Grace delays the
    late/short-paid classification; it does not change the contractual due
    date or erase the amount due.
    """
    evaluation = _parse_timestamp(evaluation_time)
    start = _parse_timestamp(schedule.effective_from)
    end = _parse_timestamp(schedule.effective_until) if schedule.effective_until else None

    if evaluation < start or (end is not None and evaluation >= end):
        raise ValueError("Agreement version is not effective at evaluation_time")
    if schedule.grace_period_seconds < 0 or schedule.tolerance_cc < 0:
        raise ValueError("Grace period and tolerance must be non-negative")
    if allocated_payment_cc < 0 or prior_credit_cc < 0:
        raise ValueError("Payment and prior credit must be non-negative")

    ids = [t.tranche_id for t in schedule.tranches]
    if len(ids) != len(set(ids)):
        raise ValueError("Tranche IDs must be unique")

    parsed = []
    for tranche in schedule.tranches:
        due_at = _parse_timestamp(tranche.due_at)
        if tranche.amount_cc < 0:
            raise ValueError("Tranche amounts must be non-negative")
        if due_at < start or (end is not None and due_at >= end):
            raise ValueError(f"Tranche {tranche.tranche_id} falls outside agreement version")
        parsed.append((due_at, tranche))

    parsed.sort(key=lambda item: (item[0], item[1].tranche_id))
    due = [(dt, t) for dt, t in parsed if dt <= evaluation]
    future = [(dt, t) for dt, t in parsed if dt > evaluation]

    gross_due = sum(t.amount_cc for _, t in due)
    gross_future = sum(t.amount_cc for _, t in future)
    gross_overdue = sum(
        t.amount_cc for dt, t in due
        if dt + timedelta(seconds=schedule.grace_period_seconds) <= evaluation
    )

    credit_applied = min(prior_credit_cc, gross_due) if schedule.carry_forward_enabled else 0
    remaining_credit = prior_credit_cc - credit_applied if schedule.carry_forward_enabled else 0
    due_after_credit = gross_due - credit_applied

    # Allocate available payment FIFO to due tranches. This identifies the
    # unpaid portion of tranches whose grace deadline has passed.
    payment_left = allocated_payment_cc
    credit_left = credit_applied
    overdue_unpaid = 0
    due_unpaid = 0
    tranche_results = []

    for due_at, tranche in due:
        credit_for_tranche = min(credit_left, tranche.amount_cc)
        credit_left -= credit_for_tranche
        after_credit = tranche.amount_cc - credit_for_tranche
        payment_for_tranche = min(payment_left, after_credit)
        payment_left -= payment_for_tranche
        unpaid = after_credit - payment_for_tranche
        is_overdue = (
            due_at + timedelta(seconds=schedule.grace_period_seconds) <= evaluation
        )
        due_unpaid += unpaid
        if is_overdue:
            overdue_unpaid += unpaid
        tranche_results.append({
            "tranche_id": tranche.tranche_id,
            "due_at": due_at.isoformat(),
            "amount_cc": tranche.amount_cc,
            "credit_applied_cc": credit_for_tranche,
            "payment_applied_cc": payment_for_tranche,
            "unpaid_cc": unpaid,
            "grace_expired": is_overdue,
        })

    tolerance = schedule.tolerance_cc
    if due_unpaid <= tolerance:
        status = "NOT_YET_DUE" if gross_due == 0 else "RECONCILED"
    elif overdue_unpaid > tolerance:
        status = "PAST_GRACE_UNPAID"
    else:
        status = "WITHIN_GRACE"

    return {
        "agreement_version": schedule.agreement_version,
        "evaluation_time": evaluation.isoformat(),
        "gross_due_cc": gross_due,
        "prior_credit_applied_cc": credit_applied,
        "due_cc": due_after_credit,
        "past_grace_due_cc": max(0, gross_overdue - credit_applied),
        "gross_future_cc": gross_future,
        "allocated_payment_cc": allocated_payment_cc,
        "unapplied_payment_cc": payment_left,
        "due_unpaid_cc": due_unpaid,
        "past_grace_unpaid_cc": overdue_unpaid,
        "tolerance_cc": tolerance,
        "remaining_carry_forward_credit_cc": remaining_credit,
        "status": status,
        "tranches": tranche_results,
        "limitations": [
            "The calculator assumes the supplied agreement version is authoritative.",
            "It calculates contractual schedule arithmetic, not the truth of traffic measurement.",
            "It assumes payments are allocated FIFO to the oldest due tranches.",
            "It does not resolve disputes over payment finality or legal interpretation.",
        ],
    }
