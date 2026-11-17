import sys
import unittest
from decimal import Decimal as D
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
from paymaster_reconciliation_experiment import (
    Agreement, Burn, Interval, deduplicate_burns, reconcile_window
)


class ReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.agreements = {
            "v1": Agreement("v1", D("1"), D("0.10")),
            "v2": Agreement("v2", D("1"), D("0.20")),
        }
        self.rows = [Interval(i, D("10"), "v1") for i in range(4)]

    def test_smoothed_payment_reconciles_at_window_level(self):
        result = reconcile_window(self.rows, [Burn("b1", D("36"), "W")],
                                   self.agreements, "W")
        self.assertEqual(result.status, "reconciled")

    def test_shortfall_is_detected(self):
        result = reconcile_window(self.rows, [Burn("b1", D("32"), "W")],
                                   self.agreements, "W")
        self.assertEqual(result.status, "shortfall_or_overpayment")
        self.assertEqual(result.residual_cc, D("4.00"))

    def test_missing_report_is_incomplete_not_zero(self):
        rows = self.rows[:3] + [Interval(3, None, "v1", "cannot_provide")]
        result = reconcile_window(rows, [Burn("b1", D("36"), "W")],
                                   self.agreements, "W")
        self.assertEqual(result.status, "incomplete")
        self.assertIsNone(result.expected_cc)

    def test_undetermined_report_is_incomplete(self):
        rows = self.rows[:3] + [Interval(3, None, "v1", "undetermined")]
        result = reconcile_window(rows, [], self.agreements, "W")
        self.assertEqual(result.status, "incomplete")

    def test_counter_reset_or_upgrade_gap_is_not_zero_usage(self):
        rows = self.rows[:3] + [Interval(3, None, "v1", "cannot_provide")]
        result = reconcile_window(rows, [], self.agreements, "W")
        self.assertEqual(result.status, "incomplete")
        self.assertIsNone(result.expected_cc)

    def test_duplicate_delivery_is_idempotent(self):
        burns = [Burn("b1", D("36"), "W"), Burn("b1", D("36"), "W")]
        result = reconcile_window(self.rows, burns, self.agreements, "W")
        self.assertEqual(result.burned_cc, D("36"))
        self.assertEqual(result.duplicate_events_ignored, 1)

    def test_conflicting_duplicate_is_rejected(self):
        with self.assertRaises(ValueError):
            deduplicate_burns([Burn("b1", D("36"), "W"),
                               Burn("b1", D("35"), "W")])

    def test_agreement_version_change_is_applied_per_interval(self):
        rows = [Interval(0, D("10"), "v1"), Interval(1, D("10"), "v2")]
        result = reconcile_window(rows, [Burn("b1", D("17"), "W")],
                                   self.agreements, "W")
        self.assertEqual(result.status, "reconciled")
        self.assertEqual(result.expected_cc, D("17.00"))

    def test_missing_agreement_version_is_incomplete(self):
        rows = [Interval(0, D("10"), "unknown")]
        result = reconcile_window(rows, [], self.agreements, "W")
        self.assertEqual(result.status, "incomplete")

    def test_burn_outside_window_does_not_count(self):
        result = reconcile_window(self.rows, [Burn("b1", D("36"), "OTHER")],
                                   self.agreements, "W")
        self.assertEqual(result.burned_cc, D("0"))
        self.assertEqual(result.status, "shortfall_or_overpayment")


if __name__ == "__main__":
    unittest.main()
