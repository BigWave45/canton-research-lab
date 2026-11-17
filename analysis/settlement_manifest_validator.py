"""Reference validator for a proposed report-to-burn settlement manifest."""
from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable

D = Decimal


@dataclass(frozen=True)
class IntervalEvidence:
    start: int
    end: int
    status: str
    traffic_bytes: int | None
    agreement_version: str
    report_digest: str


@dataclass(frozen=True)
class BurnEvidence:
    event_id: str
    amount_cc: Decimal
    settlement_id: str


@dataclass(frozen=True)
class SettlementManifest:
    settlement_id: str
    synchronizer_id: str
    window_start: int
    window_end: int
    intervals: tuple[IntervalEvidence, ...]
    expected_cc: Decimal
    burns: tuple[BurnEvidence, ...]
    tolerance_cc: Decimal = D("0.01")


@dataclass(frozen=True)
class Validation:
    status: str
    total_reported_bytes: int | None
    expected_cc: Decimal | None
    burned_cc: Decimal
    residual_cc: Decimal | None
    errors: tuple[str, ...]


def validate_manifest(manifest: SettlementManifest,
                      globally_claimed_burn_ids: set[str] | None = None) -> Validation:
    errors: list[str] = []
    if manifest.window_start >= manifest.window_end:
        errors.append("invalid settlement window")
    ordered = sorted(manifest.intervals, key=lambda item: item.start)
    if not ordered:
        errors.append("no interval evidence supplied")
    cursor = manifest.window_start
    total_bytes = 0
    for interval in ordered:
        if interval.start != cursor:
            errors.append(f"interval coverage gap or overlap at {cursor}")
        if interval.end <= interval.start or interval.end > manifest.window_end:
            errors.append(f"invalid interval bounds at {interval.start}")
        if interval.status != "Ok" or interval.traffic_bytes is None:
            errors.append(f"interval {interval.start} is not complete")
        elif interval.traffic_bytes < 0:
            errors.append(f"negative traffic at interval {interval.start}")
        else:
            total_bytes += interval.traffic_bytes
        if not interval.agreement_version:
            errors.append(f"missing agreement version at interval {interval.start}")
        if not interval.report_digest:
            errors.append(f"missing report digest at interval {interval.start}")
        cursor = interval.end
    if ordered and cursor != manifest.window_end:
        errors.append("interval coverage does not reach settlement-window end")
    if manifest.expected_cc < 0 or manifest.tolerance_cc < 0:
        errors.append("negative expected amount or tolerance")
    burn_ids: set[str] = set()
    burned = D("0")
    for burn in manifest.burns:
        if burn.event_id in burn_ids:
            errors.append(f"duplicate burn event within manifest: {burn.event_id}")
        burn_ids.add(burn.event_id)
        if globally_claimed_burn_ids is not None and burn.event_id in globally_claimed_burn_ids:
            errors.append(f"burn event already claimed by another settlement: {burn.event_id}")
        if burn.settlement_id != manifest.settlement_id:
            errors.append(f"burn event assigned to wrong settlement: {burn.event_id}")
        if burn.amount_cc < 0:
            errors.append(f"negative burn amount: {burn.event_id}")
        burned += burn.amount_cc
    if errors:
        return Validation("incomplete_or_invalid", None, None, burned, None, tuple(errors))
    residual = manifest.expected_cc - burned
    status = "reconciled" if abs(residual) <= manifest.tolerance_cc else "payment_mismatch"
    return Validation(status, total_bytes, manifest.expected_cc, burned, residual, ())


def example_manifest() -> SettlementManifest:
    return SettlementManifest(
        "settlement-2026-11-17-A", "dSync-A", 0, 1200,
        (
            IntervalEvidence(0, 600, "Ok", 1000, "agreement-v3", "sha256:report-a"),
            IntervalEvidence(600, 1200, "Ok", 1500, "agreement-v3", "sha256:report-b"),
        ),
        D("9.00"),
        (BurnEvidence("burn-001", D("9.00"), "settlement-2026-11-17-A"),),
    )


def run() -> None:
    valid = example_manifest()
    result = validate_manifest(valid)
    assert result.status == "reconciled" and result.total_reported_bytes == 2500
    print("valid manifest:", result)
    missing = SettlementManifest(
        valid.settlement_id, valid.synchronizer_id, 0, 1200,
        (valid.intervals[0], IntervalEvidence(600, 1200, "CannotProvide", None, "agreement-v3", "r2")),
        valid.expected_cc, valid.burns,
    )
    assert validate_manifest(missing).status == "incomplete_or_invalid"
    duplicate = SettlementManifest(
        valid.settlement_id, valid.synchronizer_id, 0, 1200,
        valid.intervals, valid.expected_cc, (valid.burns[0], valid.burns[0]),
    )
    assert validate_manifest(duplicate).status == "incomplete_or_invalid"
    wrong_window = SettlementManifest(
        valid.settlement_id, valid.synchronizer_id, 0, 1800,
        valid.intervals, valid.expected_cc, valid.burns,
    )
    assert validate_manifest(wrong_window).status == "incomplete_or_invalid"
    underpaid = SettlementManifest(
        valid.settlement_id, valid.synchronizer_id, 0, 1200,
        valid.intervals, valid.expected_cc,
        (BurnEvidence("burn-002", D("8.50"), valid.settlement_id),),
    )
    assert validate_manifest(underpaid).status == "payment_mismatch"
    print("missing interval, duplicate burn, uncovered window and payment mismatch rejected")


if __name__ == "__main__":
    run()
