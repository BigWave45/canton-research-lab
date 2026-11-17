"""Participant lifecycle accounting experiment.

Models the exact aggregation rule in the inspected TrafficReport PR:
only participants present in the end-of-interval state contribute a delta.
This is a synthetic policy analysis, not a Canton deployment test.
"""
from dataclasses import dataclass
from decimal import Decimal

D = Decimal


@dataclass(frozen=True)
class Participant:
    participant_id: str
    consumed_before_exit: Decimal
    present_at_interval_end: bool


def current_end_state_aggregate(participants: list[Participant]) -> Decimal:
    """Approximate TrafficReport.participantsConsumed population semantics."""
    return sum(
        (p.consumed_before_exit for p in participants if p.present_at_interval_end),
        D("0"),
    )


def chargeable_total(
    participants: list[Participant], departure_usage_is_chargeable: bool
) -> Decimal:
    if departure_usage_is_chargeable:
        return sum((p.consumed_before_exit for p in participants), D("0"))
    return current_end_state_aggregate(participants)


def compare_policy(
    participants: list[Participant], departure_usage_is_chargeable: bool
) -> dict:
    observed = current_end_state_aggregate(participants)
    economic_total = chargeable_total(participants, departure_usage_is_chargeable)
    return {
        "reported_aggregate": observed,
        "economic_total_under_policy": economic_total,
        "uncounted_units": economic_total - observed,
        "status": (
            "complete_under_policy"
            if economic_total == observed
            else "undercount_if_departure_usage_is_chargeable"
        ),
    }


def run() -> None:
    cases = {
        "low departure use": [
            Participant("continuing", D("100"), True),
            Participant("departed", D("10"), False),
            Participant("joined", D("25"), True),
        ],
        "medium departure use": [
            Participant("continuing", D("100"), True),
            Participant("departed", D("40"), False),
            Participant("joined", D("25"), True),
        ],
        "high departure use": [
            Participant("continuing", D("100"), True),
            Participant("departed", D("80"), False),
            Participant("joined", D("25"), True),
        ],
    }
    for name, participants in cases.items():
        result = compare_policy(participants, True)
        assert result["reported_aggregate"] == D("125")
        print(f"{name}: {result}")

    excluded = compare_policy(cases["medium departure use"], False)
    assert excluded["uncounted_units"] == D("0")
    print("explicit exclusion policy:", excluded)


if __name__ == "__main__":
    run()
