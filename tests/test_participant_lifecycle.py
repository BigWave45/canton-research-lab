import sys
import unittest
from decimal import Decimal as D
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
from participant_lifecycle_experiment import Participant, compare_policy


class ParticipantLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.participants = [
            Participant("continuing", D("100"), True),
            Participant("departed", D("40"), False),
            Participant("joined", D("25"), True),
        ]

    def test_departed_participant_is_omitted_by_end_state_aggregation(self):
        result = compare_policy(self.participants, True)
        self.assertEqual(result["reported_aggregate"], D("125"))
        self.assertEqual(result["economic_total_under_policy"], D("165"))
        self.assertEqual(result["uncounted_units"], D("40"))

    def test_explicit_exclusion_policy_removes_the_difference(self):
        result = compare_policy(self.participants, False)
        self.assertEqual(result["reported_aggregate"], D("125"))
        self.assertEqual(result["economic_total_under_policy"], D("125"))
        self.assertEqual(result["uncounted_units"], D("0"))

    def test_joining_participant_counts_from_zero(self):
        participants = [Participant("joined", D("25"), True)]
        result = compare_policy(participants, True)
        self.assertEqual(result["reported_aggregate"], D("25"))
        self.assertEqual(result["uncounted_units"], D("0"))

    def test_no_departures_means_no_lifecycle_gap(self):
        participants = [
            Participant("p1", D("100"), True),
            Participant("p2", D("25"), True),
        ]
        result = compare_policy(participants, True)
        self.assertEqual(result["uncounted_units"], D("0"))


if __name__ == "__main__":
    unittest.main()
