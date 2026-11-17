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
    def test_shared_paymaster_burns_reconcile_two_synchronizers(self):
        obligations, burns, allocations = example_portfolio()
        result = validate_portfolio(obligations, burns, allocations, 250)
        self.assertEqual(result["status"], "valid")
        self.assertEqual(result["obligations"], {"O-A": "reconciled", "O-B": "reconciled"})

    def test_not_yet_due_is_not_short_paid(self):
        obligations, burns, allocations = example_portfolio()
        result = validate_portfolio(obligations, burns, allocations, 150)
        self.assertEqual(result["obligations"]["O-A"], "not_yet_due")

    def test_overallocation_of_burn_is_rejected(self):
        obligations, burns, _ = example_portfolio()
        allocations = (Allocation("burn-1", "O-A", D("4")),
                       Allocation("burn-1", "O-B", D("6")),
                       Allocation("burn-2", "O-A", D("6")))
        self.assertEqual(validate_portfolio(obligations, burns, allocations, 250)["status"],
                         "invalid")

    def test_short_payment_after_due_date_is_detected(self):
        obligations, burns, _ = example_portfolio()
        allocations = (Allocation("burn-1", "O-A", D("2")),
                       Allocation("burn-1", "O-B", D("6")),
                       Allocation("burn-2", "O-A", D("6")))
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


if __name__ == "__main__":
    unittest.main()
