import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
from comparative_assurance_matrix import (
    Scenario, assess_public_burn, assess_signed_reconciliation,
    assess_confidential_audit, assess_cryptographic_proof, run_experiment,
)


class ComparativeAssuranceTests(unittest.TestCase):
    def test_experiment_has_twelve_assessments(self):
        self.assertEqual(len(run_experiment()), 12)

    def test_public_burn_cannot_verify_private_liability(self):
        s = Scenario("accurate", 100, 100, 10.0, True, True)
        result = assess_public_burn(s)
        self.assertIn("unverified", result.outcome)

    def test_signed_reconciliation_does_not_detect_consistent_underreport(self):
        s = Scenario("underreport", 100, 80, 8.0, True, True)
        result = assess_signed_reconciliation(s)
        self.assertEqual(result.outcome, "reconciled to submitted report")

    def test_independent_audit_detects_underreport_with_source_evidence(self):
        s = Scenario("underreport", 100, 80, 8.0, True, True)
        result = assess_confidential_audit(s)
        self.assertEqual(result.outcome, "measurement discrepancy detected")

    def test_audit_is_inconclusive_without_source_evidence(self):
        s = Scenario("underreport", 100, 80, 8.0, True, False)
        result = assess_confidential_audit(s)
        self.assertIn("inconclusive", result.outcome)

    def test_proof_accepts_arithmetically_valid_underreported_input(self):
        s = Scenario("underreport", 100, 80, 8.0, True, True)
        result = assess_cryptographic_proof(s)
        self.assertEqual(result.outcome, "proof verifies submitted-input calculation")

    def test_missing_report_is_incomplete_for_signed_reconciliation(self):
        s = Scenario("missing", 100, None, None, False, True)
        result = assess_signed_reconciliation(s)
        self.assertEqual(result.outcome, "incomplete: missing report")

    def test_proof_requires_completeness_manifest_to_identify_absence(self):
        s = Scenario("missing", 100, None, None, False, True)
        with_manifest = assess_cryptographic_proof(s, completeness_manifest=True)
        without_manifest = assess_cryptographic_proof(s, completeness_manifest=False)
        self.assertIn("proof failure", with_manifest.outcome)
        self.assertIn("not identifiable", without_manifest.outcome)


if __name__ == "__main__":
    unittest.main()
