import sys
import unittest
from decimal import Decimal as D
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
from settlement_manifest_validator import (
    BurnEvidence, IntervalEvidence, SettlementManifest,
    example_manifest, validate_manifest,
)


class SettlementManifestTests(unittest.TestCase):
    def changed(self, m, intervals=None, burns=None, end=None):
        return SettlementManifest(
            m.settlement_id, m.synchronizer_id, m.window_start,
            m.window_end if end is None else end,
            m.intervals if intervals is None else intervals,
            m.expected_cc, m.burns if burns is None else burns, m.tolerance_cc
        )

    def test_valid_complete_manifest_reconciles(self):
        result = validate_manifest(example_manifest())
        self.assertEqual(result.status, "reconciled")
        self.assertEqual(result.total_reported_bytes, 2500)

    def test_missing_interval_is_not_zero(self):
        m = example_manifest()
        intervals = (m.intervals[0],
                     IntervalEvidence(600, 1200, "CannotProvide", None, "agreement-v3", "r2"))
        self.assertEqual(validate_manifest(self.changed(m, intervals=intervals)).status,
                         "incomplete_or_invalid")

    def test_interval_gap_is_rejected(self):
        m = example_manifest()
        intervals = (m.intervals[0],
                     IntervalEvidence(700, 1200, "Ok", 1500, "agreement-v3", "r2"))
        self.assertEqual(validate_manifest(self.changed(m, intervals=intervals)).status,
                         "incomplete_or_invalid")

    def test_duplicate_burn_within_manifest_is_rejected(self):
        m = example_manifest()
        self.assertEqual(validate_manifest(self.changed(m, burns=m.burns * 2)).status,
                         "incomplete_or_invalid")

    def test_burn_claimed_by_another_settlement_is_rejected(self):
        self.assertEqual(validate_manifest(example_manifest(), {"burn-001"}).status,
                         "incomplete_or_invalid")

    def test_wrong_settlement_assignment_is_rejected(self):
        m = example_manifest()
        wrong = BurnEvidence("burn-x", D("9"), "another-settlement")
        self.assertEqual(validate_manifest(self.changed(m, burns=(wrong,))).status,
                         "incomplete_or_invalid")

    def test_payment_mismatch_is_detected(self):
        m = example_manifest()
        wrong = BurnEvidence("burn-y", D("8.50"), m.settlement_id)
        result = validate_manifest(self.changed(m, burns=(wrong,)))
        self.assertEqual(result.status, "payment_mismatch")
        self.assertEqual(result.residual_cc, D("0.50"))

    def test_uncovered_window_is_rejected(self):
        m = example_manifest()
        self.assertEqual(validate_manifest(self.changed(m, end=1800)).status,
                         "incomplete_or_invalid")

    def test_agreement_version_required(self):
        m = example_manifest()
        intervals = (IntervalEvidence(0, 600, "Ok", 1000, "", "r1"), m.intervals[1])
        self.assertEqual(validate_manifest(self.changed(m, intervals=intervals)).status,
                         "incomplete_or_invalid")

    def test_digest_presence_required(self):
        m = example_manifest()
        intervals = (IntervalEvidence(0, 600, "Ok", 1000, "agreement-v3", ""), m.intervals[1])
        self.assertEqual(validate_manifest(self.changed(m, intervals=intervals)).status,
                         "incomplete_or_invalid")


if __name__ == "__main__":
    unittest.main()
