import sys
import unittest
from decimal import Decimal as D
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
from adversarial_accounting_tests import (
    Report, detect_split_view, reward_bound_holds, omitted_participant_counterexample
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


if __name__ == "__main__":
    unittest.main()
