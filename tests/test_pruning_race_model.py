import unittest
from analysis.pruning_race_model import Scenario, ReadResult, classify, settlement_effect

class PruningRaceModelTests(unittest.TestCase):
    def test_no_race_returns_correct_value(self):
        self.assertEqual(classify(Scenario("no race", False, True)), ReadResult.OK_CORRECT)

    def test_pruning_does_not_always_invalidate_snapshot(self):
        self.assertEqual(classify(Scenario("still readable", True, True)), ReadResult.OK_CORRECT)

    def test_invalidated_snapshot_fails_closed(self):
        self.assertEqual(classify(Scenario("unavailable", True, False)), ReadResult.CANNOT_PROVIDE)

    def test_stale_ok_is_explicitly_a_hypothetical_danger_case(self):
        self.assertEqual(classify(Scenario("stale", True, False, True)), ReadResult.OK_STALE)

    def test_underreported_bytes_have_linear_settlement_effect(self):
        self.assertEqual(settlement_effect(150, 120, 2), 60)

if __name__ == "__main__":
    unittest.main()
