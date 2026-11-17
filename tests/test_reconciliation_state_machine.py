import unittest

from reconciliation_state_machine import (
    Allocation, Burn, Case, Obligation, Report, reconcile,
)


def base_case(**changes):
    values = dict(
        expected_report_ids=("r1", "r2"),
        reports=(
            Report("r1", "OK", "v1", "sync-a", "synchronizer-a"),
            Report("r2", "OK", "v1", "sync-b", "synchronizer-b"),
        ),
        obligations=(Obligation("sync-a", 6, "v1", synchronizer_id="synchronizer-a"), Obligation("sync-b", 4, "v1", synchronizer_id="synchronizer-b")),
        burns=(Burn("burn-1", 10),),
        allocations=(
            Allocation("a1", "burn-1", "sync-a", 6),
            Allocation("a2", "burn-1", "sync-b", 4),
        ),
        evaluation_time="2026-11-17T12:00:00Z",
        reward_required=True,
        reward_record_ids=("reward-1",),
    )
    values.update(changes)
    return Case(**values)


class ReconciliationStateMachineTests(unittest.TestCase):
    def test_complete_and_fully_allocated_case_reconciles(self):
        result = reconcile(base_case())
        self.assertEqual(result["payment_state"], "RECONCILED")
        self.assertEqual(result["overall_state"], "RECONCILED")

    def test_missing_interval_blocks_final_reconciliation(self):
        result = reconcile(base_case(reports=(Report("r1", "OK", "v1", "sync-a", "synchronizer-a"),)))
        self.assertEqual(result["report_state"], "INCOMPLETE")
        self.assertEqual(result["payment_state"], "BLOCKED_INCOMPLETE_REPORTS")

    def test_undetermined_interval_is_not_zero_activity(self):
        result = reconcile(base_case(reports=(
            Report("r1", "OK", "v1", "sync-a", "synchronizer-a"),
            Report("r2", "UNDETERMINED", "v1", "sync-b", "synchronizer-b"),
        )))
        self.assertEqual(result["report_state"], "INCOMPLETE")
        self.assertIn("r2", result["non_ok_reports"])

    def test_agreement_version_mismatch_blocks_payment(self):
        result = reconcile(base_case(reports=(
            Report("r1", "OK", "v0", "sync-a", "synchronizer-a"),
            Report("r2", "OK", "v0", "sync-b", "synchronizer-b"),
        )))
        self.assertEqual(result["agreement_state"], "MISMATCH")
        self.assertEqual(result["payment_state"], "BLOCKED_AGREEMENT_MISMATCH")

    def test_not_yet_due_tranche_is_not_misclassified_as_shortfall(self):
        # Gross liability may be 10, but only 4 is due at evaluation time.
        case = base_case(
            obligations=(Obligation("sync-a", 4, "v1", synchronizer_id="synchronizer-a"),),
            allocations=(Allocation("a1", "burn-1", "sync-a", 4),),
        )
        result = reconcile(case)
        self.assertEqual(result["payment_state"], "RECONCILED")

    def test_overdue_amount_is_short_paid(self):
        case = base_case(
            obligations=(Obligation("sync-a", 10, "v1", synchronizer_id="synchronizer-a"),),
            allocations=(Allocation("a1", "burn-1", "sync-a", 4),),
        )
        result = reconcile(case)
        self.assertEqual(result["payment_state"], "SHORT_PAID")
        self.assertEqual(result["short_obligations"], ["sync-a"])

    def test_duplicate_allocation_identifier_is_disputed(self):
        case = base_case(allocations=(
            Allocation("same", "burn-1", "sync-a", 3),
            Allocation("same", "burn-1", "sync-b", 3),
        ))
        result = reconcile(case)
        self.assertEqual(result["allocation_state"], "INVALID")
        self.assertEqual(result["payment_state"], "DISPUTED_ALLOCATION")

    def test_overallocation_of_public_burn_is_disputed(self):
        case = base_case(allocations=(
            Allocation("a1", "burn-1", "sync-a", 7),
            Allocation("a2", "burn-1", "sync-b", 4),
        ))
        result = reconcile(case)
        self.assertEqual(result["overallocated_burns"], ["burn-1"])
        self.assertEqual(result["payment_state"], "DISPUTED_ALLOCATION")

    def test_missing_reward_record_does_not_rewrite_payment_result(self):
        result = reconcile(base_case(reward_record_ids=()))
        self.assertEqual(result["payment_state"], "RECONCILED")
        self.assertEqual(result["reward_state"], "MISSING")
        self.assertEqual(result["overall_state"], "REWARD_PENDING")

    def test_distinct_agreement_versions_are_checked_per_obligation(self):
        case = base_case(
            reports=(
                Report("r1", "OK", "agreement-A", "sync-a", "synchronizer-a"),
                Report("r2", "OK", "agreement-B", "sync-b", "synchronizer-b"),
            ),
            obligations=(
                Obligation("sync-a", 6, "agreement-A", synchronizer_id="synchronizer-a"),
                Obligation("sync-b", 4, "agreement-B", synchronizer_id="synchronizer-b"),
            ),
        )
        result = reconcile(case)
        self.assertEqual(result["agreement_state"], "MATCHED")
        self.assertEqual(result["payment_state"], "RECONCILED")

    def test_report_bound_to_wrong_synchronizer_is_disputed(self):
        case = base_case(reports=(
            Report("r1", "OK", "v1", "sync-a", "synchronizer-b"),
            Report("r2", "OK", "v1", "sync-b", "synchronizer-b"),
        ))
        result = reconcile(case)
        self.assertEqual(result["agreement_state"], "INVALID_BINDING")
        self.assertEqual(result["payment_state"], "DISPUTED_REPORT_BINDING")
        self.assertIn("r1", result["synchronizer_binding_mismatches"])

    def test_report_with_wrong_obligation_agreement_version_is_blocked(self):
        case = base_case(reports=(
            Report("r1", "OK", "v2", "sync-a", "synchronizer-a"),
            Report("r2", "OK", "v1", "sync-b", "synchronizer-b"),
        ))
        result = reconcile(case)
        self.assertEqual(result["agreement_state"], "MISMATCH")
        self.assertEqual(result["report_version_mismatches"], ["r1"])
        self.assertEqual(result["payment_state"], "BLOCKED_AGREEMENT_MISMATCH")

    def test_source_measurement_completeness_is_not_claimed(self):
        result = reconcile(base_case())
        self.assertEqual(
            result["measurement_completeness"],
            "NOT_ESTABLISHED_BY_THIS_MODEL",
        )


if __name__ == "__main__":
    unittest.main()
