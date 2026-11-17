import unittest

from comparative_assurance_model import assess, comparison_matrix


class ComparativeAssuranceModelTests(unittest.TestCase):
    def test_matrix_has_three_scenarios_for_four_architectures(self):
        self.assertEqual(len(comparison_matrix()), 12)

    def test_signed_report_does_not_detect_under_reporting(self):
        result = assess("under_reporting", "signed_reconciliation")
        self.assertFalse(result["exception_detected"])
        self.assertFalse(result["measurement_assured"])
        self.assertTrue(result["payment_reconciled"])

    def test_independent_audit_detects_under_reporting(self):
        result = assess("under_reporting", "independent_confidential_audit")
        self.assertTrue(result["exception_detected"])
        self.assertTrue(result["measurement_assured"])
        # The burn still matches the understated contractual calculation.
        self.assertTrue(result["payment_reconciled"])

    def test_missing_interval_detected_when_expected_schedule_is_known(self):
        for architecture in (
            "signed_reconciliation",
            "independent_confidential_audit",
            "cryptographic_proof",
        ):
            with self.subTest(architecture=architecture):
                self.assertTrue(
                    assess("missing_interval", architecture)["exception_detected"]
                )

    def test_public_burn_only_cannot_establish_missing_interval(self):
        result = assess("missing_interval", "public_burn_only")
        self.assertFalse(result["exception_detected"])
        self.assertIsNone(result["payment_reconciled"])

    def test_proof_does_not_detect_false_but_consistent_source_input(self):
        result = assess("under_reporting", "cryptographic_proof")
        self.assertFalse(result["exception_detected"])
        self.assertFalse(result["measurement_assured"])
        self.assertTrue(result["payment_reconciled"])


if __name__ == "__main__":
    unittest.main()
