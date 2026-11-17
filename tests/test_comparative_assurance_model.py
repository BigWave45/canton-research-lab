import unittest

from comparative_assurance_model import ARCHITECTURES, assess, comparison_matrix


class ComparativeAssuranceModelTests(unittest.TestCase):
    def test_matrix_has_six_scenarios_for_four_architectures(self):
        self.assertEqual(len(comparison_matrix()), 24)

    def test_signed_report_does_not_detect_under_reporting(self):
        result = assess("under_reporting", "signed_reconciliation")
        self.assertFalse(result["exception_detected"])
        self.assertFalse(result["measurement_assured"])
        self.assertTrue(result["payment_reconciled"])

    def test_independent_audit_detects_under_reporting(self):
        result = assess("under_reporting", "independent_confidential_audit")
        self.assertTrue(result["exception_detected"])
        self.assertTrue(result["measurement_assured"])
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

    def test_authoritative_agreement_version_mismatch_detected(self):
        for architecture in (
            "signed_reconciliation",
            "independent_confidential_audit",
            "cryptographic_proof",
        ):
            with self.subTest(architecture=architecture):
                result = assess("agreement_version_mismatch", architecture)
                self.assertTrue(result["exception_detected"])
                self.assertTrue(result["agreement_assured"])
                self.assertFalse(result["payment_reconciled"])

    def test_public_burn_cannot_detect_agreement_version_mismatch(self):
        result = assess("agreement_version_mismatch", "public_burn_only")
        self.assertFalse(result["exception_detected"])
        self.assertIsNone(result["payment_reconciled"])

    def test_smoothing_is_not_misclassified_as_shortfall(self):
        for architecture in ARCHITECTURES[1:]:
            with self.subTest(architecture=architecture):
                result = assess("smoothing_not_yet_due", architecture)
                self.assertFalse(result["exception_detected"])
                self.assertTrue(result["payment_reconciled"])
                self.assertEqual(result["result"], "smoothed_payment_current")

    def test_overdue_smoothing_shortfall_is_detected(self):
        for architecture in ARCHITECTURES[1:]:
            with self.subTest(architecture=architecture):
                result = assess("smoothing_overdue_shortfall", architecture)
                self.assertTrue(result["exception_detected"])
                self.assertFalse(result["payment_reconciled"])
                self.assertEqual(result["result"], "overdue_shortfall_detected")


if __name__ == "__main__":
    unittest.main()
