import unittest

from agreement_schedule import Schedule, Tranche
from reconciliation_state_machine import (
    Case, Obligation, Report, reconcile_with_schedules,
)


class ScheduledReconciliationTests(unittest.TestCase):
    def make_case(self, evaluation_time):
        return Case(
            expected_report_ids=("r1",),
            reports=(Report("r1", "OK", "v1"),),
            obligations=(Obligation("sync-a", 0, "v1"),),
            burns=(),
            allocations=(),
            evaluation_time=evaluation_time,
            reward_required=False,
        )

    def make_schedule(self):
        return Schedule(
            agreement_version="v1",
            effective_from="2026-11-01T00:00:00Z",
            effective_until="2027-01-01T00:00:00Z",
            tranches=(Tranche("t1", "2026-11-10T00:00:00Z", 4),),
            grace_period_seconds=3 * 24 * 60 * 60,
        )

    def test_due_but_within_grace_is_not_short_paid(self):
        case = self.make_case("2026-11-11T00:00:00Z")
        result = reconcile_with_schedules(
            case, {"sync-a": self.make_schedule()}
        )
        self.assertEqual(result["payment_state"], "WITHIN_GRACE")
        self.assertEqual(result["schedule_results"]["sync-a"]["due_cc"], 4)

    def test_unpaid_amount_after_grace_is_past_grace(self):
        case = self.make_case("2026-11-15T00:00:00Z")
        result = reconcile_with_schedules(
            case, {"sync-a": self.make_schedule()}
        )
        self.assertEqual(result["payment_state"], "PAST_GRACE_UNPAID")
        self.assertEqual(result["overdue_obligations"], ["sync-a"])

    def test_missing_schedule_is_rejected(self):
        case = self.make_case("2026-11-15T00:00:00Z")
        with self.assertRaises(ValueError):
            reconcile_with_schedules(case, {})

    def test_prior_credit_reduces_due_only_when_schedule_allows_it(self):
        case = self.make_case("2026-11-15T00:00:00Z")
        result = reconcile_with_schedules(
            case,
            {"sync-a": self.make_schedule()},
            prior_credits={"sync-a": 4},
        )
        self.assertEqual(result["payment_state"], "RECONCILED")
        self.assertEqual(
            result["schedule_results"]["sync-a"]["prior_credit_applied_cc"], 0
        )

        carry_schedule = Schedule(
            agreement_version="v1",
            effective_from="2026-11-01T00:00:00Z",
            effective_until="2027-01-01T00:00:00Z",
            tranches=(Tranche("t1", "2026-11-10T00:00:00Z", 4),),
            grace_period_seconds=3 * 24 * 60 * 60,
            carry_forward_enabled=True,
        )
        carried = reconcile_with_schedules(
            case,
            {"sync-a": carry_schedule},
            prior_credits={"sync-a": 4},
        )
        self.assertEqual(carried["payment_state"], "RECONCILED")
        self.assertEqual(
            carried["schedule_results"]["sync-a"]["prior_credit_applied_cc"], 4
        )


if __name__ == "__main__":
    unittest.main()
