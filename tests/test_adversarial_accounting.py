import sys
import unittest
from decimal import Decimal as D, localcontext
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
from adversarial_accounting_tests import (
    AppActivityRecord, AppRewardRecord, BurnEvidence, PaidTrafficEvidence, Report, RewardRule,
    detect_split_view, reward_bound_holds, omitted_participant_counterexample,
    validate_app_reward_attribution,
)


class AdversarialAccountingTests(unittest.TestCase):
    def test_omitted_participant_is_invisible_to_report_based_reconciliation(self):
        result = omitted_participant_counterexample()
        self.assertTrue(result["reported_payment_reconciles"])
        self.assertTrue(result["actual_usage_understated"])
        self.assertEqual(result["hidden_liability"], D("5.40"))

    def test_conflicting_views_detectable_when_observers_compare(self):
        a = Report("sync-A", 7, D("100"), 1)
        b = Report("sync-A", 7, D("92"), 1)
        self.assertTrue(detect_split_view([a, b]))

    def test_identical_views_do_not_trigger_conflict(self):
        a = Report("sync-A", 7, D("100"), 1)
        self.assertFalse(detect_split_view([a, a]))

    def test_single_view_does_not_reveal_omission(self):
        b = Report("sync-A", 7, D("92"), 1)
        self.assertFalse(detect_split_view([b]))

    def test_reward_budget_prevents_overissuance(self):
        self.assertTrue(reward_bound_holds(D("9"), D("10")))
        self.assertFalse(reward_bound_holds(D("11"), D("10")))

    def test_reward_budget_does_not_prove_source_completeness(self):
        self.assertTrue(reward_bound_holds(D("9"), D("9")))


class RewardAttributionTests(unittest.TestCase):
    def setUp(self):
        self.burns = (BurnEvidence("burn-1", "paymaster-1"),)
        self.settlements = (
            PaidTrafficEvidence(
                "settlement-1", "burn-1", "paymaster-1", "sync-1", "epoch-1", D("100")
            ),
        )
        self.rules = (RewardRule("epoch-1", "weights-v1", D("0.5"), D("0.25"), D("20")),)
        self.activity = AppActivityRecord(
            "activity-record-1", "source-activity-1", "settlement-1", "burn-1",
            "paymaster-1", "sync-1", "epoch-1", "weights-v1", D("50"),
        )
        self.reward = AppRewardRecord(
            "reward-1", "activity-record-1", "settlement-1", "burn-1",
            "paymaster-1", "paymaster-1", "sync-1", "epoch-1", "weights-v1", D("12.5"),
        )

    def validate(self, *, burns=None, settlements=None, rules=None, activities=None, rewards=None):
        return validate_app_reward_attribution(
            self.burns if burns is None else burns,
            self.settlements if settlements is None else settlements,
            self.rules if rules is None else rules,
            (self.activity,) if activities is None else activities,
            (self.reward,) if rewards is None else rewards,
        )

    def test_paid_traffic_capacity_is_enforced_after_authorized_weight(self):
        excess = AppActivityRecord(
            **{
                **self.activity.__dict__,
                "activity_units": D("50.000000000000000000000000000000000001"),
            }
        )
        result = self.validate(activities=(excess,))
        self.assertIn(
            "ACTIVITY_EXCEEDS_PAID_WEIGHTED_CAPACITY:settlement-1", result["errors"]
        )

    def test_activity_must_use_settlement_epoch(self):
        wrong_epoch = AppActivityRecord(
            **{**self.activity.__dict__, "reward_epoch": "epoch-2"}
        )
        result = self.validate(activities=(wrong_epoch,))
        self.assertIn("ACTIVITY_EPOCH_MISMATCH:activity-record-1", result["errors"])

    def test_paymaster_and_synchronizer_identity_cannot_be_substituted(self):
        wrong_paymaster = AppActivityRecord(
            **{**self.activity.__dict__, "paymaster_id": "paymaster-2"}
        )
        wrong_synchronizer = AppRewardRecord(
            **{**self.reward.__dict__, "synchronizer_id": "sync-2"}
        )
        paymaster_result = self.validate(activities=(wrong_paymaster,))
        synchronizer_result = self.validate(rewards=(wrong_synchronizer,))
        self.assertIn(
            "ACTIVITY_PAYMASTER_MISMATCH:activity-record-1", paymaster_result["errors"]
        )
        self.assertIn(
            "REWARD_SYNCHRONIZER_MISMATCH:reward-1", synchronizer_result["errors"]
        )

    def test_activity_must_use_active_authorized_weight_version(self):
        obsolete = AppActivityRecord(
            **{**self.activity.__dict__, "weight_version": "weights-old"}
        )
        result = self.validate(activities=(obsolete,))
        self.assertIn(
            "UNAUTHORIZED_OR_OBSOLETE_WEIGHT_VERSION:activity-record-1", result["errors"]
        )

    def test_duplicate_activity_evidence_with_new_record_id_is_rejected(self):
        duplicate = AppActivityRecord(
            **{**self.activity.__dict__, "record_id": "activity-record-2"}
        )
        result = self.validate(activities=(self.activity, duplicate))
        self.assertIn(
            "DUPLICATE_OR_BROKEN_ACTIVITY_EVIDENCE:source-activity-1", result["errors"]
        )

    def test_unknown_burn_and_settlement_references_are_rejected(self):
        unknown = AppActivityRecord(
            **{
                **self.activity.__dict__,
                "settlement_id": "settlement-unknown",
                "burn_id": "burn-unknown",
            }
        )
        reward = AppRewardRecord(
            **{
                **self.reward.__dict__,
                "settlement_id": "settlement-unknown",
                "burn_id": "burn-unknown",
            }
        )
        result = self.validate(activities=(unknown,), rewards=(reward,))
        self.assertIn("UNKNOWN_SETTLEMENT_REFERENCE:settlement-unknown", result["errors"])
        self.assertIn("UNKNOWN_BURN_REFERENCE:burn-unknown", result["errors"])

    def test_validator_reward_coupon_cannot_be_counted_as_app_reward(self):
        validator_coupon = AppRewardRecord(
            **{**self.reward.__dict__, "reward_type": "validator"}
        )
        result = self.validate(rewards=(validator_coupon,))
        self.assertIn("NON_APP_REWARD_IN_APP_REWARDS:reward-1", result["errors"])

    def test_correct_aggregate_with_wrong_recipient_fails_individual_attribution(self):
        misattributed = AppRewardRecord(
            **{**self.reward.__dict__, "recipient_id": "participant-1"}
        )
        result = self.validate(rewards=(misattributed,))
        self.assertFalse(result["attribution_valid"])
        self.assertTrue(result["aggregate_cap_valid"])
        self.assertEqual(result["reward_totals_by_epoch"]["epoch-1"], D("12.5"))
        self.assertIn("REWARD_RECIPIENT_NOT_PAYMASTER:reward-1", result["errors"])

    def test_correct_paymaster_attribution_is_not_checked_against_participant_shares(self):
        result = self.validate(rewards=(self.reward,))
        self.assertTrue(result["valid"])
        self.assertEqual(self.reward.recipient_id, "paymaster-1")

    def test_correct_attribution_can_still_exceed_aggregate_reward_cap(self):
        low_cap = (RewardRule(
            "epoch-1", "weights-v1", D("0.5"), D("0.25"), D("12.49")
        ),)
        result = self.validate(rules=low_cap)
        self.assertTrue(result["attribution_valid"])
        self.assertFalse(result["aggregate_cap_valid"])
        self.assertIn("AGGREGATE_REWARD_CAP_EXCEEDED:epoch-1", result["errors"])

    def test_superseded_activity_cannot_receive_duplicate_reward_credit(self):
        corrected = AppActivityRecord(
            "activity-record-2", "source-activity-1", "settlement-1", "burn-1",
            "paymaster-1", "sync-1", "epoch-1", "weights-v1", D("40"),
            supersedes_record_id="activity-record-1",
        )
        corrected_reward = AppRewardRecord(
            "reward-2", "activity-record-2", "settlement-1", "burn-1",
            "paymaster-1", "paymaster-1", "sync-1", "epoch-1", "weights-v1", D("10"),
        )
        only_corrected = self.validate(
            activities=(self.activity, corrected), rewards=(corrected_reward,)
        )
        self.assertTrue(only_corrected["valid"])

        both_credited = self.validate(
            activities=(self.activity, corrected), rewards=(self.reward, corrected_reward)
        )
        self.assertFalse(both_credited["attribution_valid"])
        self.assertIn("SUPERSEDED_ACTIVITY_REWARDED:activity-record-1", both_credited["errors"])

    def test_exact_decimal_weight_and_reward_products_do_not_round(self):
        paid_bytes = D("0.123456789012345678901234567890123456789")
        weight = D("0.987654321098765432109876543210987654321")
        rate = D("0.111111111111111111111111111111111111111")
        with localcontext() as context:
            context.prec = 200
            weighted_units = paid_bytes * weight
            exact_reward = weighted_units * rate
        settlement = PaidTrafficEvidence(
            "settlement-1", "burn-1", "paymaster-1", "sync-1", "epoch-1", paid_bytes
        )
        rule = RewardRule("epoch-1", "weights-v1", weight, rate, exact_reward)
        activity = AppActivityRecord(
            "activity-record-1", "source-activity-1", "settlement-1", "burn-1",
            "paymaster-1", "sync-1", "epoch-1", "weights-v1", weighted_units,
        )
        reward = AppRewardRecord(
            "reward-1", "activity-record-1", "settlement-1", "burn-1",
            "paymaster-1", "paymaster-1", "sync-1", "epoch-1", "weights-v1", exact_reward,
        )
        result = self.validate(
            settlements=(settlement,), rules=(rule,), activities=(activity,), rewards=(reward,)
        )
        self.assertTrue(result["valid"])
        self.assertEqual(result["reward_totals_by_epoch"]["epoch-1"], exact_reward)

    def test_float_activity_quantity_is_rejected_without_conversion(self):
        float_activity = AppActivityRecord(
            **{**self.activity.__dict__, "activity_units": 50.0}
        )
        result = self.validate(activities=(float_activity,))
        self.assertIn("INVALID_ACTIVITY_QUANTITY:activity-record-1", result["errors"])

    def test_duplicate_reward_for_activity_is_rejected_even_with_distinct_reward_ids(self):
        duplicate = AppRewardRecord(
            **{**self.reward.__dict__, "reward_id": "reward-2"}
        )
        result = self.validate(rewards=(self.reward, duplicate))
        self.assertIn("DUPLICATE_REWARD_FOR_ACTIVITY:activity-record-1", result["errors"])


if __name__ == "__main__":
    unittest.main()
