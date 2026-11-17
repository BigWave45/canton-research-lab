import sys
import unittest
from decimal import Decimal as D
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
from participant_lifecycle_mechanisms import (
    MemberInterval, current_end_state_total, deduplicate_departures,
    lifecycle_total, mechanism_comparison, example_rows,
)


class ParticipantLifecycleMechanismTests(unittest.TestCase):
    def test_current_api_population_excludes_departed_member(self):
        self.assertEqual(current_end_state_total(example_rows()), D("125"))

    def test_departure_inclusion_requires_exit_evidence(self):
        result = lifecycle_total(example_rows(), "charge_departures")
        self.assertEqual(result["total"], D("165"))
        self.assertEqual(result["departure_delta"], D("40"))

    def test_missing_exit_evidence_is_incomplete_not_zero(self):
        rows = [
            MemberInterval("continuing#1", D("50"), D("150")),
            MemberInterval("departed#1", D("20"), None),
            MemberInterval("joined#1", None, D("25")),
        ]
        result = lifecycle_total(rows, "charge_departures")
        self.assertEqual(result["status"], "incomplete")
        self.assertIsNone(result["total"])

    def test_explicit_exclusion_policy_is_complete_at_125(self):
        result = lifecycle_total(example_rows(), "exclude_departures")
        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["total"], D("125"))

    def test_mechanisms_reconcile_to_policy_dependent_totals(self):
        result = mechanism_comparison(example_rows())
        self.assertEqual(result["current_end_state"], D("125"))
        self.assertEqual(result["signed_departure_snapshot"], D("165"))
        self.assertEqual(result["carry_forward_counter"], D("165"))
        self.assertEqual(result["event_driven_boundary_settlement"], D("165"))
        self.assertEqual(result["explicit_exclusion_policy"], D("125"))

    def test_identical_departure_event_is_idempotent(self):
        rows = example_rows()
        unique, duplicates = deduplicate_departures(rows + [rows[1]])
        self.assertEqual(duplicates, 1)
        self.assertEqual(lifecycle_total(unique, "charge_departures")["total"], D("165"))

    def test_conflicting_departure_event_is_rejected(self):
        rows = example_rows()
        conflict = MemberInterval("departed#1", D("20"), None, D("61"), "exit-001")
        with self.assertRaises(ValueError):
            deduplicate_departures(rows + [conflict])


if __name__ == "__main__":
    unittest.main()
