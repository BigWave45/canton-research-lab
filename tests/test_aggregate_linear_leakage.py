import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
from aggregate_linear_leakage import matrix_rank, uniquely_identifiable_participants


class LinearLeakageTests(unittest.TestCase):
    def test_one_aggregate_does_not_identify_individuals(self):
        self.assertEqual(uniquely_identifiable_participants([[1, 1, 1, 1, 1]]), [])

    def test_two_overlapping_k_three_cohorts_isolate_one_member(self):
        rows = [[1, 1, 1, 1, 0], [0, 1, 1, 1, 0]]
        self.assertEqual(uniquely_identifiable_participants(rows), [0])

    def test_multiple_releases_are_composed(self):
        rows = [[1, 1, 1, 1, 0], [0, 1, 1, 1, 0], [0, 1, 1, 0, 1]]
        self.assertEqual(uniquely_identifiable_participants(rows), [0])

    def test_nonidentifiable_variables_remain_hidden(self):
        rows = [[1, 1, 1, 1, 0], [0, 1, 1, 1, 0]]
        self.assertNotIn(1, uniquely_identifiable_participants(rows))

    def test_matrix_rank_exact(self):
        self.assertEqual(matrix_rank([[1, 2], [2, 4]]), 1)
        self.assertEqual(matrix_rank([[1, 0], [0, 1]]), 2)

    def test_invalid_matrix_width_rejected(self):
        with self.assertRaises(ValueError):
            matrix_rank([[1, 0], [1]])


if __name__ == "__main__":
    unittest.main()
