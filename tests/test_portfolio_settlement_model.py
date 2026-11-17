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
    def test_one_burn_can_be_partitioned_across_two_synchronizers(self):
        obligations, burns, allocations = example_portfolio()
        result = validate_portfolio(obligations, burns, allocations, 250)
        self.assertEqual(result["status"], "valid")
        self.assertEqual(result["obligations"]["O-A"], "reconciled")
        self.assertEqual(result["obligations"]["O-B"], "reconciled")

    def test_not_yet_due_is_not_short_paid(self):
        obligations, burns, allocations = example_portfolio()
        result = validate_portfolio(obligations, burns, allocations, 150)
        self.assertEqual(result["obligations"]["O-A"], "not_yet_due")

    def test_overallocation_of_shared_burn_is_rejected(self):
        obligations, burns, _ = example_portfolio()
        allocations = (
            Allocation("burn-portfolio-1", "O-A", D("10")),
            Allocation("burn-portfolio-1", "O-B", D("6")),
        )
        self.assertEqual(validate_portfolio(obligations, burns, allocations, 250)["status"],
                         "invalid")

    def test_short_payment_after_due_date_is_detected(self):
        obligations, burns, _ = example_portfolio()
        allocations = (
            Allocation("burn-portfolio-1", "O-A", D("8")),
            Allocation("burn-portfolio-1", "O-B", D("6")),
        )
        result = validate_portfolio(obligations, burns, allocations, 250)
        self.assertEqual(result["obligations"]["O-A"], "short_paid")

    def test_agreement_version_change_is_retained_per_interval(self):
        obligations, _, _ = example_portfolio()
        versions = [x.agreement_version for x in obligations[0].intervals]
        self.assertEqual(versions, ["v1", "v2"])

    def test_due_schedule_must_equal_expected_liability(self):
        obligations, burns, allocations = example_portfolio()
        o = obligations[0]
        bad = Obligation(o.obligation_id, o.paymaster_id, o.synchronizer_id,
                         o.intervals, (DueTranche(100, D("8")),))
        result = validate_portfolio((bad, obligations[1]), burns, allocations, 250)
        self.assertEqual(result["status"], "invalid")

    def test_unknown_burn_reference_is_rejected(self):
        obligations, _, allocations = example_portfolio()
        result = validate_portfolio(obligations, (), allocations, 250)
        self.assertEqual(result["status"], "invalid")

    def test_allocation_must_match_paymaster(self):
        obligations, burns, allocations = example_portfolio()
        wrong = Burn("burn-portfolio-1", D("15"), "PM-OTHER")
        result = validate_portfolio(obligations, (wrong,), allocations, 250)
        self.assertEqual(result["status"], "invalid")


if __name__ == "__main__":
    unittest.main()
