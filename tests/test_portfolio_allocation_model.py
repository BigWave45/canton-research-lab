import unittest

from portfolio_allocation_model import (
    ARCHITECTURES,
    SCENARIOS,
    assess,
    comparison_matrix,
    validate_allocations,
)


class PortfolioAllocationTests(unittest.TestCase):
    def test_matrix_has_four_scenarios_for_four_architectures(self):
        self.assertEqual(len(comparison_matrix()), 16)

    def test_valid_partition_allows_one_burn_to_cover_two_obligations(self):
        result = validate_allocations(SCENARIOS["valid_partition"])
        self.assertTrue(result["valid"])
        self.assertEqual(result["allocated_total_cc"], 10)

    def test_duplicate_allocation_identifier_is_rejected(self):
        result = validate_allocations(SCENARIOS["duplicate_claim"])
        self.assertFalse(result["valid"])
        self.assertEqual(result["duplicate_allocation_ids"], ["alloc-A"])

    def test_aggregate_over_allocation_is_rejected(self):
        result = validate_allocations(SCENARIOS["over_allocation"])
        self.assertFalse(result["valid"])
        self.assertEqual(result["over_allocated_cc"], 2)

    def test_partial_allocation_reports_obligation_shortfall(self):
        result = validate_allocations(SCENARIOS["partial_allocation_shortfall"])
        self.assertFalse(result["valid"])
        self.assertEqual(result["shortfalls_cc"], {"sync-B": 2})

    def test_public_burn_only_cannot_verify_private_allocation(self):
        result = assess("over_allocation", "public_burn_only")
        self.assertIsNone(result["portfolio_reconciled"])
        self.assertFalse(result["exception_detected"])

    def test_all_manifest_aware_architectures_detect_invalid_allocation(self):
        for scenario in ("duplicate_claim", "over_allocation", "partial_allocation_shortfall"):
            for architecture in ARCHITECTURES[1:]:
                with self.subTest(scenario=scenario, architecture=architecture):
                    result = assess(scenario, architecture)
                    self.assertTrue(result["exception_detected"])
                    self.assertFalse(result["portfolio_reconciled"])

    def test_all_manifest_aware_architectures_accept_valid_partition(self):
        for architecture in ARCHITECTURES[1:]:
            with self.subTest(architecture=architecture):
                result = assess("valid_partition", architecture)
                self.assertFalse(result["exception_detected"])
                self.assertTrue(result["portfolio_reconciled"])


if __name__ == "__main__":
    unittest.main()
