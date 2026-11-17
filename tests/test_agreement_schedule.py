import unittest

from agreement_schedule import Schedule, Tranche, calculate_due


def schedule(**changes):
    values = dict(
        agreement_version="v1",
        effective_from="2026-11-01T00:00:00Z",
        effective_until="2027-01-01T00:00:00Z",
        tranches=(
            Tranche("t1", "2026-11-10T00:00:00Z", 4),
            Tranche("t2", "2026-12-10T00:00:00Z", 6),
        ),
        grace_period_seconds=3 * 24 * 60 * 60,
        tolerance_cc=0,
        carry_forward_enabled=False,
    )
    values.update(changes)
    return Schedule(**values)


class AgreementScheduleTests(unittest.TestCase):
    def test_future_tranche_is_not_due(self):
        result = calculate_due(schedule(), "2026-11-05T00:00:00Z", 0)
        self.assertEqual(result["due_cc"], 0)
        self.assertEqual(result["gross_future_cc"], 10)
        self.assertEqual(result["status"], "NOT_YET_DUE")

    def test_due_tranche_inside_grace_is_not_late(self):
        result = calculate_due(schedule(), "2026-11-11T00:00:00Z", 0)
        self.assertEqual(result["due_cc"], 4)
        self.assertEqual(result["past_grace_due_cc"], 0)
        self.assertEqual(result["status"], "WITHIN_GRACE")

    def test_unpaid_tranche_after_grace_is_past_grace(self):
        result = calculate_due(schedule(), "2026-11-14T00:00:00Z", 0)
        self.assertEqual(result["past_grace_due_cc"], 4)
        self.assertEqual(result["status"], "PAST_GRACE_UNPAID")

    def test_payment_covers_oldest_tranche_fifo(self):
        result = calculate_due(schedule(), "2026-12-15T00:00:00Z", 4)
        self.assertEqual(result["due_unpaid_cc"], 6)
        self.assertEqual(result["past_grace_unpaid_cc"], 0)
        self.assertEqual(result["status"], "WITHIN_GRACE")

    def test_partial_payment_after_grace_leaves_overdue_shortfall(self):
        result = calculate_due(schedule(), "2026-11-15T00:00:00Z", 2)
        self.assertEqual(result["past_grace_unpaid_cc"], 2)
        self.assertEqual(result["status"], "PAST_GRACE_UNPAID")

    def test_prior_credit_applies_only_when_enabled(self):
        disabled = calculate_due(schedule(), "2026-11-15T00:00:00Z", 0, prior_credit_cc=2)
        enabled = calculate_due(
            schedule(carry_forward_enabled=True),
            "2026-11-15T00:00:00Z", 0, prior_credit_cc=2,
        )
        self.assertEqual(disabled["due_cc"], 4)
        self.assertEqual(enabled["due_cc"], 2)
        self.assertEqual(enabled["prior_credit_applied_cc"], 2)

    def test_excess_credit_remains_for_future_only_when_enabled(self):
        result = calculate_due(
            schedule(carry_forward_enabled=True),
            "2026-11-15T00:00:00Z", 0, prior_credit_cc=7,
        )
        self.assertEqual(result["due_cc"], 0)
        self.assertEqual(result["remaining_carry_forward_credit_cc"], 3)
        self.assertEqual(result["status"], "RECONCILED")

    def test_tolerance_is_explicit_and_bounded(self):
        result = calculate_due(
            schedule(tolerance_cc=1),
            "2026-11-15T00:00:00Z", 3,
        )
        self.assertEqual(result["due_unpaid_cc"], 1)
        self.assertEqual(result["status"], "RECONCILED")

    def test_timezone_offsets_are_respected(self):
        result = calculate_due(
            schedule(tranches=(Tranche("t1", "2026-11-10T01:00:00+01:00", 4),)),
            "2026-11-10T00:30:00Z", 0,
        )
        self.assertEqual(result["due_cc"], 0)

    def test_naive_timestamps_are_rejected(self):
        with self.assertRaises(ValueError):
            calculate_due(schedule(), "2026-11-15T00:00:00", 0)

    def test_wrong_agreement_effective_period_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_due(schedule(), "2027-01-01T00:00:00Z", 0)

    def test_duplicate_tranche_ids_are_rejected(self):
        duplicate = schedule(tranches=(
            Tranche("t1", "2026-11-10T00:00:00Z", 4),
            Tranche("t1", "2026-12-10T00:00:00Z", 6),
        ))
        with self.assertRaises(ValueError):
            calculate_due(duplicate, "2026-11-15T00:00:00Z", 0)


if __name__ == "__main__":
    unittest.main()
