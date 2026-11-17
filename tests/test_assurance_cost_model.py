import unittest
from decimal import Decimal

from assurance_cost_model import ARCHITECTURES, cost_breakdown, compare_architectures


def synthetic_inputs(scale=1):
    """Constructed test values only; not measured operating costs."""
    return {
        "implementation_cost": 100 * scale,
        "interval_count": 10,
        "report_cost_per_interval": 2 * scale,
        "exception_count": 2,
        "investigation_cost_per_exception": 5 * scale,
        "review_hours": 3,
        "loaded_hourly_rate": 4 * scale,
        "evidence_storage_gb": 2,
        "storage_cost_per_gb": 1 * scale,
        "delay_cost": 6 * scale,
        "currency": "TEST_UNITS",
        "evaluation_period": "synthetic-period",
    }


class AssuranceCostModelTests(unittest.TestCase):
    def test_cost_components_and_total_are_separated(self):
        result = cost_breakdown(synthetic_inputs())
        self.assertEqual(result["one_time_implementation_cost"], Decimal("100"))
        self.assertEqual(result["report_processing_cost"], Decimal("20"))
        self.assertEqual(result["exception_investigation_cost"], Decimal("10"))
        self.assertEqual(result["human_review_cost"], Decimal("12"))
        self.assertEqual(result["evidence_storage_cost"], Decimal("2"))
        self.assertEqual(result["delay_cost"], Decimal("6"))
        self.assertEqual(result["recurring_cost"], Decimal("50"))
        self.assertEqual(result["total_cost"], Decimal("150"))
        self.assertFalse(result["residual_expected_loss_included"])

    def test_missing_inputs_are_rejected(self):
        incomplete = synthetic_inputs()
        del incomplete["loaded_hourly_rate"]
        with self.assertRaisesRegex(ValueError, "loaded_hourly_rate"):
            cost_breakdown(incomplete)

    def test_negative_and_non_finite_inputs_are_rejected(self):
        for value in (-1, "NaN", "Infinity"):
            with self.subTest(value=value):
                params = synthetic_inputs()
                params["delay_cost"] = value
                with self.assertRaises(ValueError):
                    cost_breakdown(params)

    def test_counts_must_be_non_negative_integers(self):
        params = synthetic_inputs()
        params["interval_count"] = 1.5
        with self.assertRaisesRegex(ValueError, "interval_count"):
            cost_breakdown(params)

    def test_comparison_reports_delta_and_break_even_threshold(self):
        inputs = {
            name: synthetic_inputs(scale=index + 1)
            for index, name in enumerate(ARCHITECTURES)
        }
        result = compare_architectures(inputs)
        baseline = result["results"]["public_burn_only"]
        signed = result["results"]["signed_reconciliation"]
        self.assertEqual(baseline["delta_vs_baseline"], Decimal("0"))
        self.assertEqual(signed["delta_vs_baseline"], Decimal("150"))
        self.assertEqual(signed["break_even_avoided_loss_per_interval"], Decimal("15"))
        self.assertEqual(result["evidence_status"], "PARAMETERISED_INPUTS_ONLY")

    def test_all_architectures_are_required(self):
        with self.assertRaisesRegex(ValueError, "cryptographic_proof"):
            compare_architectures({
                name: synthetic_inputs()
                for name in ARCHITECTURES[:-1]
            })

    def test_comparison_rejects_incomparable_evaluation_period(self):
        inputs = {name: synthetic_inputs() for name in ARCHITECTURES}
        inputs["cryptographic_proof"]["evaluation_period"] = "different-period"
        with self.assertRaisesRegex(ValueError, "evaluation_period"):
            compare_architectures(inputs)

    def test_comparison_rejects_different_interval_counts(self):
        inputs = {name: synthetic_inputs() for name in ARCHITECTURES}
        inputs["independent_confidential_audit"]["interval_count"] = 11
        with self.assertRaisesRegex(ValueError, "interval_count"):
            compare_architectures(inputs)


if __name__ == "__main__":
    unittest.main()
