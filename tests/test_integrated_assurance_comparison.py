import unittest

from integrated_assurance_comparison import (
    ARCHITECTURES, DIMENSIONS, get_assessment, validate_matrix,
)


class IntegratedAssuranceComparisonTests(unittest.TestCase):
    def test_four_architectures_share_same_dimensions(self):
        result = validate_matrix()
        self.assertTrue(result["valid"])
        self.assertEqual(result["architecture_count"], 4)
        self.assertEqual(result["dimension_count"], 10)

    def test_proof_does_not_claim_source_completeness(self):
        value = get_assessment("cryptographic_proof", "measurement_assurance")
        self.assertIn("none_for_source_completeness", value)

    def test_audit_measurement_claim_is_conditional(self):
        value = get_assessment("independent_confidential_audit", "measurement_assurance")
        self.assertIn("if_source_records_are_complete", value)

    def test_public_burn_only_has_no_payment_completeness(self):
        self.assertEqual(get_assessment("public_burn_only", "payment_completeness"), "none")

    def test_all_dimensions_are_nonempty(self):
        for architecture, values in ARCHITECTURES.items():
            for dimension in DIMENSIONS:
                with self.subTest(architecture=architecture, dimension=dimension):
                    self.assertTrue(values[dimension])


if __name__ == "__main__":
    unittest.main()
