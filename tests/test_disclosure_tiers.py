import unittest

from disclosure_tiers import (
    claim_support,
    disclosure_matrix,
    public_minimisation_check,
)


class DisclosureTierTests(unittest.TestCase):
    def test_matrix_covers_three_roles_and_six_claims(self):
        self.assertEqual(len(disclosure_matrix()), 18)

    def test_public_can_verify_burn_and_allocation_proof(self):
        self.assertTrue(claim_support("public_verifier", "burn_exists")["supported"])
        self.assertTrue(
            claim_support("public_verifier", "allocation_constraints_hold")["supported"]
        )

    def test_public_cannot_reconcile_exact_per_synchronizer_amounts(self):
        result = claim_support(
            "public_verifier", "per_synchronizer_payment_reconciles"
        )
        self.assertFalse(result["supported"])
        self.assertIn("exact_obligation_amounts", result["missing_evidence"])

    def test_auditor_can_check_measurement_against_source_records(self):
        self.assertTrue(
            claim_support(
                "independent_auditor", "measurement_matches_source_records"
            )["supported"]
        )

    def test_public_tier_excludes_exact_private_values_and_payloads(self):
        self.assertTrue(public_minimisation_check()["passes"])
        self.assertEqual(
            public_minimisation_check()["prohibited_fields_exposed"], []
        )

    def test_no_role_needs_payloads_for_accounting_claims_except_payload_content(self):
        for claim in (
            "burn_exists",
            "allocation_constraints_hold",
            "correct_agreement_version_used",
            "per_synchronizer_payment_reconciles",
            "measurement_matches_source_records",
        ):
            self.assertNotIn(
                "private_transaction_payloads",
                __import__("disclosure_tiers").CLAIMS[claim],
            )


if __name__ == "__main__":
    unittest.main()
