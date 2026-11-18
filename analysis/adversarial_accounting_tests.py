"""Adversarial accounting demonstrations; synthetic, not production tests."""
from dataclasses import dataclass
from decimal import Decimal, localcontext
from hashlib import sha256
from typing import Iterable

D = Decimal


@dataclass(frozen=True)
class BurnEvidence:
    burn_id: str
    paymaster_id: str


@dataclass(frozen=True)
class PaidTrafficEvidence:
    settlement_id: str
    burn_id: str
    paymaster_id: str
    synchronizer_id: str
    reward_epoch: str
    paid_bytes: Decimal


@dataclass(frozen=True)
class RewardRule:
    reward_epoch: str
    weight_version: str
    app_activity_weight: Decimal
    reward_per_activity_unit: Decimal
    aggregate_reward_cap: Decimal


@dataclass(frozen=True)
class AppActivityRecord:
    record_id: str
    source_activity_id: str
    settlement_id: str
    burn_id: str
    paymaster_id: str
    synchronizer_id: str
    reward_epoch: str
    weight_version: str
    activity_units: Decimal
    supersedes_record_id: str | None = None


@dataclass(frozen=True)
class AppRewardRecord:
    reward_id: str
    activity_record_id: str
    settlement_id: str
    burn_id: str
    paymaster_id: str
    recipient_id: str
    synchronizer_id: str
    reward_epoch: str
    weight_version: str
    amount: Decimal
    reward_type: str = "app"


def _is_finite_decimal(value: object) -> bool:
    return isinstance(value, Decimal) and value.is_finite()


def _exact_product(left: Decimal, right: Decimal) -> Decimal:
    precision = len(left.as_tuple().digits) + len(right.as_tuple().digits) + 1
    with localcontext() as context:
        context.prec = max(1, precision)
        return left * right


def _exact_sum(values: Iterable[Decimal]) -> Decimal:
    values = tuple(values)
    if not values:
        return D("0")
    lowest_exponent = min(value.as_tuple().exponent for value in values)
    max_digits = max(
        len(value.as_tuple().digits) + value.as_tuple().exponent - lowest_exponent
        for value in values
    )
    precision = max_digits + len(str(len(values))) + 2
    with localcontext() as context:
        context.prec = max(1, precision)
        return sum(values, D("0"))


def validate_app_reward_attribution(
    burns: Iterable[BurnEvidence],
    settlements: Iterable[PaidTrafficEvidence],
    rules: Iterable[RewardRule],
    activities: Iterable[AppActivityRecord],
    rewards: Iterable[AppRewardRecord],
) -> dict:
    """Validate app rewards against supplied paid-traffic evidence and active rules.

    The evidence and rule inputs are assumed to have been authenticated and
    authorised elsewhere. Phase 1 attribution is to the paymaster, not its
    synchronizer participants.
    """
    burns = tuple(burns)
    settlements = tuple(settlements)
    rules = tuple(rules)
    activities = tuple(activities)
    rewards = tuple(rewards)
    errors = set()
    cap_errors = set()

    def unique_index(records, key, missing_code, duplicate_code):
        groups = {}
        for record in records:
            value = getattr(record, key)
            if not isinstance(value, str) or not value.strip():
                errors.add(missing_code)
                continue
            groups.setdefault(value, []).append(record)
        indexed = {}
        for value, entries in groups.items():
            if len(entries) != 1:
                errors.add(f"{duplicate_code}:{value}")
            else:
                indexed[value] = entries[0]
        return indexed

    burn_by_id = unique_index(
        burns, "burn_id", "BURN_ID_MISSING", "DUPLICATE_BURN_ID"
    )
    settlement_by_id = unique_index(
        settlements, "settlement_id", "SETTLEMENT_ID_MISSING", "DUPLICATE_SETTLEMENT_ID"
    )
    activity_by_id = unique_index(
        activities, "record_id", "ACTIVITY_RECORD_ID_MISSING", "DUPLICATE_ACTIVITY_RECORD_ID"
    )
    unique_index(rewards, "reward_id", "REWARD_ID_MISSING", "DUPLICATE_REWARD_ID")

    rules_by_epoch = {}
    for rule in rules:
        if not isinstance(rule.reward_epoch, str) or not rule.reward_epoch.strip():
            errors.add("REWARD_RULE_EPOCH_MISSING")
            continue
        rules_by_epoch.setdefault(rule.reward_epoch, []).append(rule)
        if (
            not isinstance(rule.weight_version, str)
            or not rule.weight_version.strip()
            or not _is_finite_decimal(rule.app_activity_weight)
            or rule.app_activity_weight < 0
            or not _is_finite_decimal(rule.reward_per_activity_unit)
            or rule.reward_per_activity_unit < 0
            or not _is_finite_decimal(rule.aggregate_reward_cap)
            or rule.aggregate_reward_cap < 0
        ):
            errors.add(f"INVALID_REWARD_RULE:{rule.reward_epoch}")
            cap_errors.add(f"INVALID_REWARD_CAP:{rule.reward_epoch}")
    for epoch, entries in rules_by_epoch.items():
        if len(entries) != 1:
            errors.add(f"AMBIGUOUS_ACTIVE_REWARD_RULE:{epoch}")
            cap_errors.add(f"AMBIGUOUS_ACTIVE_REWARD_CAP:{epoch}")
    active_rule_by_epoch = {}
    for epoch, entries in rules_by_epoch.items():
        if len(entries) != 1:
            continue
        rule = entries[0]
        if (
            isinstance(rule.weight_version, str)
            and rule.weight_version.strip()
            and _is_finite_decimal(rule.app_activity_weight)
            and rule.app_activity_weight >= 0
            and _is_finite_decimal(rule.reward_per_activity_unit)
            and rule.reward_per_activity_unit >= 0
            and _is_finite_decimal(rule.aggregate_reward_cap)
            and rule.aggregate_reward_cap >= 0
        ):
            active_rule_by_epoch[epoch] = rule

    for settlement in settlements:
        burn = burn_by_id.get(settlement.burn_id)
        if burn is None:
            errors.add(f"UNKNOWN_BURN_REFERENCE:{settlement.burn_id}")
        elif burn.paymaster_id != settlement.paymaster_id:
            errors.add(f"SETTLEMENT_BURN_PAYMASTER_MISMATCH:{settlement.settlement_id}")
        if not _is_finite_decimal(settlement.paid_bytes) or settlement.paid_bytes < 0:
            errors.add(f"INVALID_PAID_TRAFFIC:{settlement.settlement_id}")

    children_by_parent = {}
    activity_by_source = {}
    for activity in activities:
        activity_by_source.setdefault(activity.source_activity_id, []).append(activity)
        if activity.supersedes_record_id is not None:
            if not isinstance(activity.supersedes_record_id, str) or not activity.supersedes_record_id.strip():
                errors.add(f"BROKEN_ACTIVITY_SUPERSESSION_CHAIN:{activity.record_id}")
                continue
            children_by_parent.setdefault(activity.supersedes_record_id, []).append(activity.record_id)
            predecessor = activity_by_id.get(activity.supersedes_record_id)
            if predecessor is None:
                errors.add(f"MISSING_ACTIVITY_PREDECESSOR:{activity.record_id}")
            elif (
                predecessor.source_activity_id != activity.source_activity_id
                or predecessor.settlement_id != activity.settlement_id
                or predecessor.burn_id != activity.burn_id
                or predecessor.paymaster_id != activity.paymaster_id
                or predecessor.synchronizer_id != activity.synchronizer_id
                or predecessor.reward_epoch != activity.reward_epoch
            ):
                errors.add(f"BROKEN_ACTIVITY_SUPERSESSION_CHAIN:{activity.record_id}")
        if not isinstance(activity.source_activity_id, str) or not activity.source_activity_id.strip():
            errors.add(f"SOURCE_ACTIVITY_ID_MISSING:{activity.record_id}")
        settlement = settlement_by_id.get(activity.settlement_id)
        if settlement is None:
            errors.add(f"UNKNOWN_SETTLEMENT_REFERENCE:{activity.settlement_id}")
        else:
            if activity.burn_id != settlement.burn_id:
                errors.add(f"ACTIVITY_BURN_MISMATCH:{activity.record_id}")
            if activity.paymaster_id != settlement.paymaster_id:
                errors.add(f"ACTIVITY_PAYMASTER_MISMATCH:{activity.record_id}")
            if activity.synchronizer_id != settlement.synchronizer_id:
                errors.add(f"ACTIVITY_SYNCHRONIZER_MISMATCH:{activity.record_id}")
            if activity.reward_epoch != settlement.reward_epoch:
                errors.add(f"ACTIVITY_EPOCH_MISMATCH:{activity.record_id}")
        if activity.burn_id not in burn_by_id:
            errors.add(f"UNKNOWN_BURN_REFERENCE:{activity.burn_id}")
        rule = active_rule_by_epoch.get(activity.reward_epoch)
        if rule is None:
            errors.add(f"UNKNOWN_REWARD_EPOCH:{activity.reward_epoch}")
        elif activity.weight_version != rule.weight_version:
            errors.add(f"UNAUTHORIZED_OR_OBSOLETE_WEIGHT_VERSION:{activity.record_id}")
        if not _is_finite_decimal(activity.activity_units) or activity.activity_units < 0:
            errors.add(f"INVALID_ACTIVITY_QUANTITY:{activity.record_id}")

    for parent_id, child_ids in children_by_parent.items():
        if len(child_ids) > 1:
            errors.add(f"BRANCHED_ACTIVITY_SUPERSESSION_CHAIN:{parent_id}")
    for source_id, entries in activity_by_source.items():
        roots = [entry for entry in entries if not entry.supersedes_record_id]
        if len(roots) != 1:
            errors.add(f"DUPLICATE_OR_BROKEN_ACTIVITY_EVIDENCE:{source_id}")

    superseded_ids = set(children_by_parent)
    active_activities = [
        activity for activity in activity_by_id.values()
        if activity.record_id not in superseded_ids
    ]
    activity_units_by_settlement = {}
    for activity in active_activities:
        settlement = settlement_by_id.get(activity.settlement_id)
        rule = active_rule_by_epoch.get(activity.reward_epoch)
        if (
            settlement is None
            or rule is None
            or not _is_finite_decimal(activity.activity_units)
            or activity.activity_units < 0
            or activity.weight_version != rule.weight_version
        ):
            continue
        activity_units_by_settlement.setdefault(activity.settlement_id, []).append(
            activity.activity_units
        )
    for settlement_id, activity_units in activity_units_by_settlement.items():
        settlement = settlement_by_id[settlement_id]
        rule = active_rule_by_epoch[settlement.reward_epoch]
        if not _is_finite_decimal(settlement.paid_bytes) or settlement.paid_bytes < 0:
            continue
        eligible_units = _exact_product(settlement.paid_bytes, rule.app_activity_weight)
        claimed_units = _exact_sum(activity_units)
        if claimed_units > eligible_units:
            errors.add(f"ACTIVITY_EXCEEDS_PAID_WEIGHTED_CAPACITY:{settlement_id}")

    rewards_by_activity = {}
    for reward in rewards:
        rewards_by_activity.setdefault(reward.activity_record_id, []).append(reward)
        activity = activity_by_id.get(reward.activity_record_id)
        if activity is None:
            errors.add(f"UNKNOWN_ACTIVITY_REFERENCE:{reward.activity_record_id}")
        elif activity.record_id in superseded_ids:
            errors.add(f"SUPERSEDED_ACTIVITY_REWARDED:{activity.record_id}")
        settlement = settlement_by_id.get(reward.settlement_id)
        if settlement is None:
            errors.add(f"UNKNOWN_SETTLEMENT_REFERENCE:{reward.settlement_id}")
        else:
            if reward.burn_id != settlement.burn_id:
                errors.add(f"REWARD_BURN_MISMATCH:{reward.reward_id}")
            if reward.paymaster_id != settlement.paymaster_id:
                errors.add(f"REWARD_PAYMASTER_MISMATCH:{reward.reward_id}")
            if reward.recipient_id != settlement.paymaster_id:
                errors.add(f"REWARD_RECIPIENT_NOT_PAYMASTER:{reward.reward_id}")
            if reward.synchronizer_id != settlement.synchronizer_id:
                errors.add(f"REWARD_SYNCHRONIZER_MISMATCH:{reward.reward_id}")
            if reward.reward_epoch != settlement.reward_epoch:
                errors.add(f"REWARD_EPOCH_MISMATCH:{reward.reward_id}")
        if reward.burn_id not in burn_by_id:
            errors.add(f"UNKNOWN_BURN_REFERENCE:{reward.burn_id}")
        if reward.reward_type != "app":
            errors.add(f"NON_APP_REWARD_IN_APP_REWARDS:{reward.reward_id}")
        rule = active_rule_by_epoch.get(reward.reward_epoch)
        if rule is None:
            errors.add(f"UNKNOWN_REWARD_EPOCH:{reward.reward_epoch}")
        elif reward.weight_version != rule.weight_version:
            errors.add(f"UNAUTHORIZED_OR_OBSOLETE_WEIGHT_VERSION:{reward.reward_id}")
        if activity is not None and rule is not None:
            if (
                activity.settlement_id != reward.settlement_id
                or activity.burn_id != reward.burn_id
                or activity.paymaster_id != reward.paymaster_id
                or activity.synchronizer_id != reward.synchronizer_id
                or activity.reward_epoch != reward.reward_epoch
                or activity.weight_version != reward.weight_version
            ):
                errors.add(f"REWARD_ACTIVITY_BINDING_MISMATCH:{reward.reward_id}")
            if (
                _is_finite_decimal(activity.activity_units)
                and _is_finite_decimal(reward.amount)
                and reward.amount >= 0
                and reward.weight_version == rule.weight_version
            ):
                expected_amount = _exact_product(
                    activity.activity_units, rule.reward_per_activity_unit
                )
                if reward.amount != expected_amount:
                    errors.add(f"REWARD_AMOUNT_MISMATCH:{reward.reward_id}")
        if not _is_finite_decimal(reward.amount) or reward.amount < 0:
            errors.add(f"INVALID_REWARD_AMOUNT:{reward.reward_id}")

    for activity_id, activity_rewards in rewards_by_activity.items():
        if len(activity_rewards) > 1:
            errors.add(f"DUPLICATE_REWARD_FOR_ACTIVITY:{activity_id}")

    reward_totals_by_epoch = {}
    for reward in rewards:
        if _is_finite_decimal(reward.amount) and reward.amount >= 0:
            reward_totals_by_epoch.setdefault(reward.reward_epoch, []).append(reward.amount)
    exact_totals_by_epoch = {
        epoch: _exact_sum(amounts)
        for epoch, amounts in reward_totals_by_epoch.items()
    }
    for epoch, total in exact_totals_by_epoch.items():
        rule = active_rule_by_epoch.get(epoch)
        if rule is None:
            cap_errors.add(f"NO_AUTHORIZED_REWARD_CAP:{epoch}")
        elif not _is_finite_decimal(rule.aggregate_reward_cap) or total > rule.aggregate_reward_cap:
            cap_errors.add(f"AGGREGATE_REWARD_CAP_EXCEEDED:{epoch}")

    return {
        "valid": not errors and not cap_errors,
        "attribution_valid": not errors,
        "aggregate_cap_valid": not cap_errors,
        "errors": tuple(sorted(errors | cap_errors)),
        "attribution_errors": tuple(sorted(errors)),
        "aggregate_cap_errors": tuple(sorted(cap_errors)),
        "reward_totals_by_epoch": exact_totals_by_epoch,
    }


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
