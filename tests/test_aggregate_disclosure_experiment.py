import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
from aggregate_disclosure_experiment import find_single_member_differences, release_for


class AggregateDisclosureTests(unittest.TestCase):
    def setUp(self):
        self.usage = {"P1": 40, "P2": 30, "P3": 20, "P4": 10, "P5": 50}

    def test_overlapping_cohorts_defeat_k_threshold(self):
        a = release_for(("P1", "P2", "P3", "P4"), self.usage, "A")
        b = release_for(("P2", "P3", "P4"), self.usage, "B")
        findings = find_single_member_differences((a, b), 3)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["isolated_member"], "P1")
        self.assertEqual(findings[0]["inferred_bytes"], 40)

    def test_threshold_suppresses_small_cohort(self):
        a = release_for(("P1", "P2", "P3", "P4"), self.usage, "A")
        b = release_for(("P2", "P3"), self.usage, "B")
        self.assertEqual(find_single_member_differences((a, b), 3), [])

    def test_disjoint_cohorts_do_not_create_nested_difference(self):
        a = release_for(("P1", "P2", "P3"), self.usage, "A")
        b = release_for(("P4", "P5"), self.usage, "B")
        self.assertEqual(find_single_member_differences((a, b), 2), [])

    def test_identical_cohorts_do_not_isolate_member(self):
        a = release_for(("P1", "P2", "P3"), self.usage, "A")
        b = release_for(("P1", "P2", "P3"), self.usage, "B")
        self.assertEqual(find_single_member_differences((a, b), 3), [])


if __name__ == "__main__":
    unittest.main()
