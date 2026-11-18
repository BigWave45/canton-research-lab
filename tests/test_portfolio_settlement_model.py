import sys
import unittest
from decimal import Decimal as D
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
from portfolio_settlement_model import (
    Allocation, Burn, DueTranche, Obligation, PricedInterval,
    example_portfolio, validate_portfolio,
)


class PortfolioSettlementTests(unittest.TestCase):
    def obligation(self, obligation_id, amount, paymaster_id="PM-1", due_at=100,
                   due_schedule=None):
        amount = D(amount)
        return Obligation(
            obligation_id, paymaster_id, f"sync-{obligation_id}",
            (PricedInterval(0, 10, "Ok", 100, "v1", amount),),
            ((DueTranche(due_at, amount),) if due_schedule is None else due_schedule),
        )

    def allocation(self, allocation_id, event_id, obligation_id, amount):
        return Allocation(event_id, obligation_id, D(amount), allocation_id)

    def test_shared_paymaster_burns_reconcile_two_synchronizers(self):
        obligations, burns, allocations = example_portfolio()
        result = validate_portfolio(obligations, burns, allocations, 250)
        self.assertEqual(result["status"], "valid")
        self.assertEqual(result["obligations"], {"O-A": "reconciled", "O-B": "reconciled"})

    def test_not_yet_due_is_not_short_paid(self):
        obligations, burns, _ = example_portfolio()
        allocations = (
            self.allocation("a1", "burn-1", "O-A", "3"),
            self.allocation("a2", "burn-1", "O-B", "6"),
        )
        result = validate_portfolio(obligations, burns, allocations, 150)
        self.assertEqual(result["obligations"]["O-A"], "not_yet_due")

    def test_overallocation_of_burn_is_rejected(self):
        obligations, burns, _ = example_portfolio()
        allocations = (self.allocation("a1", "burn-1", "O-A", "4"),
                       self.allocation("a2", "burn-1", "O-B", "6"),
                       self.allocation("a3", "burn-2", "O-A", "6"))
        self.assertEqual(validate_portfolio(obligations, burns, allocations, 250)["status"],
                         "invalid")

    def test_short_payment_after_due_date_is_detected(self):
        obligations, burns, _ = example_portfolio()
        allocations = (self.allocation("a1", "burn-1", "O-A", "2"),
                       self.allocation("a2", "burn-1", "O-B", "6"),
                       self.allocation("a3", "burn-2", "O-A", "6"))
        result = validate_portfolio(obligations, burns, allocations, 250)
        self.assertEqual(result["obligations"]["O-A"], "short_paid")

    def test_agreement_versions_retained_per_interval(self):
        obligations, _, _ = example_portfolio()
        self.assertEqual([x.agreement_version for x in obligations[0].intervals], ["v1", "v2"])

    def test_due_schedule_must_equal_expected_liability(self):
        obligations, burns, allocations = example_portfolio()
        o = obligations[0]
        bad = Obligation(o.obligation_id, o.paymaster_id, o.synchronizer_id,
                         o.intervals, (DueTranche(100, D("8")),))
        result = validate_portfolio((bad, obligations[1]), burns, allocations, 250)
        self.assertEqual(result["status"], "invalid")

    def test_unknown_burn_reference_is_rejected(self):
        obligations, _, allocations = example_portfolio()
        self.assertEqual(validate_portfolio(obligations, (), allocations, 250)["status"],
                         "invalid")

    def test_allocation_must_match_paymaster(self):
        obligations, burns, allocations = example_portfolio()
        wrong_burns = (Burn("burn-1", D("9"), "PM-X"), burns[1])
        self.assertEqual(validate_portfolio(obligations, wrong_burns, allocations, 250)["status"],
                         "invalid")

    def test_one_burn_can_be_split_across_three_obligations(self):
        obligations = tuple(self.obligation(name, amount) for name, amount in (
            ("O-A", "2"), ("O-B", "3"), ("O-C", "5"),
        ))
        burns = (Burn("b1", D("10"), "PM-1"),)
        allocations = tuple(
            self.allocation(f"a{i}", "b1", name, amount)
            for i, (name, amount) in enumerate((("O-A", "2"), ("O-B", "3"), ("O-C", "5")))
        )
        result = validate_portfolio(obligations, burns, allocations, 100)
        self.assertEqual(result["status"], "valid")
        self.assertEqual(set(result["obligations"].values()), {"reconciled"})

    def test_three_burns_can_fund_one_obligation(self):
        obligation = self.obligation("O-A", "10")
        burns = tuple(Burn(f"b{i}", D(amount), "PM-1") for i, amount in enumerate(
            ("2", "3", "5"), start=1
        ))
        allocations = tuple(
            self.allocation(f"a{i}", f"b{i}", "O-A", amount)
            for i, amount in enumerate(("2", "3", "5"), start=1)
        )
        self.assertEqual(validate_portfolio((obligation,), burns, allocations, 100)["status"],
                         "valid")

    def test_multiple_burns_can_fund_multiple_obligations(self):
        obligations = tuple(self.obligation(name, "4") for name in ("O-A", "O-B", "O-C"))
        burns = tuple(Burn(name, D(amount), "PM-1")
                      for name, amount in (("b1", "5"), ("b2", "4"), ("b3", "3")))
        allocations = tuple(self.allocation(*record) for record in (
            ("a1", "b1", "O-A", "2"), ("a2", "b1", "O-B", "3"),
            ("a3", "b2", "O-A", "2"), ("a4", "b2", "O-C", "2"),
            ("a5", "b3", "O-B", "1"), ("a6", "b3", "O-C", "2"),
        ))
        result = validate_portfolio(obligations, burns, allocations, 100)
        self.assertEqual(result["status"], "valid")
        self.assertEqual(set(result["obligations"].values()), {"reconciled"})

    def test_aggregate_allocations_may_equal_burn_amount_exactly(self):
        obligations = (self.obligation("O-A", "4"), self.obligation("O-B", "6"))
        burns = (Burn("b1", D("10"), "PM-1"),)
        allocations = (
            self.allocation("a1", "b1", "O-A", "4"),
            self.allocation("a2", "b1", "O-B", "6"),
        )
        self.assertEqual(validate_portfolio(obligations, burns, allocations, 100)["status"],
                         "valid")

    def test_fractional_overallocation_is_rejected_exactly(self):
        obligations = (self.obligation("O-A", "0.1"), self.obligation("O-B", "0.2001"))
        burns = (Burn("b1", D("0.3"), "PM-1"),)
        allocations = (
            self.allocation("a1", "b1", "O-A", "0.1"),
            self.allocation("a2", "b1", "O-B", "0.2001"),
        )
        result = validate_portfolio(obligations, burns, allocations, 100)
        self.assertIn("BURN_OVERALLOCATED:b1", result["errors"])

    def test_duplicate_allocation_id_across_obligations_is_rejected(self):
        obligations = (self.obligation("O-A", "1"), self.obligation("O-B", "1"))
        burns = (Burn("b1", D("2"), "PM-1"),)
        allocations = (
            self.allocation("same", "b1", "O-A", "1"),
            self.allocation("same", "b1", "O-B", "1"),
        )
        result = validate_portfolio(obligations, burns, allocations, 100)
        self.assertIn("DUPLICATE_ALLOCATION_ID:same", result["errors"])

    def test_duplicate_burn_evidence_is_rejected(self):
        obligation = self.obligation("O-A", "1")
        burns = (Burn("b1", D("1"), "PM-1"), Burn("b1", D("1"), "PM-1"))
        allocation = self.allocation("a1", "b1", "O-A", "1")
        result = validate_portfolio((obligation,), burns, (allocation,), 100)
        self.assertIn("DUPLICATE_BURN_EVENT_ID:b1", result["errors"])

    def test_missing_burn_and_obligation_references_are_rejected(self):
        obligation = self.obligation("O-A", "2")
        burns = (Burn("b1", D("1"), "PM-1"),)
        allocations = (
            self.allocation("a1", "missing-burn", "O-A", "1"),
            self.allocation("a2", "b1", "missing-obligation", "1"),
        )
        result = validate_portfolio((obligation,), burns, allocations, 100)
        self.assertIn("UNKNOWN_BURN_REFERENCE:missing-burn", result["errors"])
        self.assertIn("UNKNOWN_OBLIGATION_REFERENCE:missing-obligation", result["errors"])

    def test_allocation_id_must_be_nonempty(self):
        obligation = self.obligation("O-A", "1")
        burn = (Burn("b1", D("1"), "PM-1"),)
        result = validate_portfolio(
            (obligation,), burn, (Allocation("b1", "O-A", D("1")),), 100
        )
        self.assertIn("ALLOCATION_ID_MISSING", result["errors"])

    def test_negative_and_zero_allocations_are_rejected(self):
        obligation = self.obligation("O-A", "2")
        burn = (Burn("b1", D("2"), "PM-1"),)
        for value in ("-1", "0"):
            with self.subTest(amount=value):
                result = validate_portfolio(
                    (obligation,), burn,
                    (self.allocation("a1", "b1", "O-A", value),), 100,
                )
                self.assertIn("NON_POSITIVE_ALLOCATION:a1", result["errors"])

    def test_fractional_cc_uses_exact_decimal_arithmetic(self):
        obligations = (self.obligation("O-A", "0.1"), self.obligation("O-B", "0.2"))
        burns = (Burn("b1", D("0.3"), "PM-1"),)
        allocations = (
            self.allocation("a1", "b1", "O-A", "0.1"),
            self.allocation("a2", "b1", "O-B", "0.2"),
        )
        result = validate_portfolio(obligations, burns, allocations, 100)
        self.assertEqual(result["status"], "valid")

    def test_float_allocation_is_rejected_without_conversion(self):
        obligation = self.obligation("O-A", "0.1")
        burn = (Burn("b1", D("0.1"), "PM-1"),)
        allocation = Allocation("b1", "O-A", 0.1, "a1")
        result = validate_portfolio((obligation,), burn, (allocation,), 100)
        self.assertIn("INVALID_ALLOCATION_AMOUNT:a1", result["errors"])

    def test_one_obligation_can_be_paid_while_another_is_short(self):
        obligations = (self.obligation("O-A", "3"), self.obligation("O-B", "4"))
        burns = (Burn("b1", D("5"), "PM-1"),)
        allocations = (
            self.allocation("a1", "b1", "O-A", "3"),
            self.allocation("a2", "b1", "O-B", "2"),
        )
        result = validate_portfolio(obligations, burns, allocations, 100)
        self.assertEqual(result["obligations"], {"O-A": "reconciled", "O-B": "short_paid"})

    def test_not_yet_due_tranche_remains_distinct_from_short_paid(self):
        obligation = self.obligation(
            "O-A", "5", due_schedule=(DueTranche(100, D("2")), DueTranche(200, D("3")))
        )
        burn = (Burn("b1", D("2"), "PM-1"),)
        allocation = (self.allocation("a1", "b1", "O-A", "2"),)
        result = validate_portfolio((obligation,), burn, allocation, 150)
        self.assertEqual(result["obligations"]["O-A"], "not_yet_due")

    def test_prior_allocation_id_cannot_be_replayed(self):
        obligation = self.obligation("O-A", "2")
        burns = (Burn("b1", D("1"), "PM-1"),)
        prior = (self.allocation("committed-1", "b1", "O-A", "0.5"),)
        current = (self.allocation("committed-1", "b1", "O-A", "0.1"),)
        result = validate_portfolio(
            (obligation,), burns, current, 100, prior_allocations=prior
        )
        self.assertIn("ALLOCATION_ID_REPLAY:committed-1", result["errors"])

    def test_new_amendment_cannot_reuse_previously_consumed_burn_credit(self):
        obligation = self.obligation("O-A", "2")
        burns = (Burn("b1", D("1"), "PM-1"),)
        prior = (self.allocation("committed-1", "b1", "O-A", "0.6"),)
        current = (self.allocation("amend-1", "b1", "O-A", "0.4001"),)
        result = validate_portfolio(
            (obligation,), burns, current, 100, prior_allocations=prior
        )
        self.assertIn("BURN_OVERALLOCATED:b1", result["errors"])

    def test_prior_allocations_count_toward_obligation_coverage(self):
        obligation = self.obligation("O-A", "1")
        burns = (Burn("b1", D("1"), "PM-1"),)
        prior = (self.allocation("committed-1", "b1", "O-A", "1"),)
        result = validate_portfolio(
            (obligation,), burns, (), 100, prior_allocations=prior
        )
        self.assertEqual(result["obligations"]["O-A"], "reconciled")

    def test_input_order_does_not_change_validation_result(self):
        obligations = (self.obligation("O-A", "1"), self.obligation("O-B", "1"))
        burns = (Burn("b1", D("1"), "PM-1"), Burn("b2", D("1"), "PM-1"))
        allocations = (
            self.allocation("same", "b1", "O-A", "0.5"),
            self.allocation("same", "b2", "O-B", "0.5"),
        )
        original = validate_portfolio(obligations, burns, allocations, 100)
        reversed_inputs = validate_portfolio(
            tuple(reversed(obligations)), tuple(reversed(burns)),
            tuple(reversed(allocations)), 100,
        )
        self.assertEqual(original, reversed_inputs)


if __name__ == "__main__":
    unittest.main()
