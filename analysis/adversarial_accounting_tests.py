"""Adversarial accounting demonstrations; synthetic, not production tests."""
from dataclasses import dataclass
from decimal import Decimal
from hashlib import sha256

D = Decimal


@dataclass(frozen=True)
class Report:
    synchronizer: str
    interval: int
    reported_units: Decimal
    version: int


def report_digest(report: Report) -> str:
    payload = "|".join((report.synchronizer, str(report.interval),
                        str(report.reported_units), str(report.version)))
    return sha256(payload.encode()).hexdigest()


def detect_split_view(reports: list[Report]) -> bool:
    by_key: dict[tuple[str, int, int], set[str]] = {}
    for report in reports:
        key = (report.synchronizer, report.interval, report.version)
        by_key.setdefault(key, set()).add(report_digest(report))
    return any(len(digests) > 1 for digests in by_key.values())


def reward_bound_holds(issued: Decimal, authorised_budget: Decimal) -> bool:
    if issued < 0 or authorised_budget < 0:
        raise ValueError("reward amounts must be non-negative")
    return issued <= authorised_budget


def omitted_participant_counterexample() -> dict:
    actual_units = D("16")
    reported_units = D("10")  # six units omitted
    rate = D("1")
    discount = D("0.10")
    reported_payable = reported_units * rate * (D("1") - discount)
    actual_payable = actual_units * rate * (D("1") - discount)
    burn = reported_payable
    return {
        "reported_payment_reconciles": burn == reported_payable,
        "actual_usage_understated": reported_units < actual_units,
        "hidden_liability": actual_payable - burn,
    }


def run() -> None:
    omitted = omitted_participant_counterexample()
    assert omitted == {
        "reported_payment_reconciles": True,
        "actual_usage_understated": True,
        "hidden_liability": D("5.40"),
    }
    print("omitted participant:", omitted)

    a = Report("sync-A", 7, D("100"), 1)
    b = Report("sync-A", 7, D("92"), 1)
    assert detect_split_view([a, b])
    assert not detect_split_view([a, a])
    assert not detect_split_view([b])  # one view cannot reveal its own omission
    print("split-view conflict detected only when observers compare")

    assert reward_bound_holds(D("9"), D("10"))
    assert not reward_bound_holds(D("11"), D("10"))
    assert reward_bound_holds(D("9"), D("9"))  # budget itself may be understated
    print("reward cap blocks over-issuance but not understated input")


if __name__ == "__main__":
    run()
