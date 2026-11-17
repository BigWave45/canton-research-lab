"""Linear-algebra audit for repeated aggregate releases."""
from fractions import Fraction
from typing import Iterable


def matrix_rank(rows: Iterable[Iterable[int | Fraction]]) -> int:
    matrix = [[Fraction(x) for x in row] for row in rows]
    if not matrix:
        return 0
    width = len(matrix[0])
    if any(len(row) != width for row in matrix):
        raise ValueError("matrix rows must have equal length")
    rank = 0
    for col in range(width):
        pivot = next((r for r in range(rank, len(matrix)) if matrix[r][col]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][col]
        matrix[rank] = [x / scale for x in matrix[rank]]
        for r in range(len(matrix)):
            if r != rank and matrix[r][col]:
                factor = matrix[r][col]
                matrix[r] = [a - factor*b for a, b in zip(matrix[r], matrix[rank])]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def uniquely_identifiable_participants(cohort_rows: list[list[int]]) -> list[int]:
    if not cohort_rows:
        return []
    n = len(cohort_rows[0])
    if any(len(row) != n for row in cohort_rows):
        raise ValueError("all cohort rows must use the same participant universe")
    base_rank = matrix_rank(cohort_rows)
    identifiable = []
    for i in range(n):
        unit = [1 if j == i else 0 for j in range(n)]
        if matrix_rank(cohort_rows + [unit]) == base_rank:
            identifiable.append(i)
    return identifiable


def run():
    nested = [[1, 1, 1, 1, 0], [0, 1, 1, 1, 0]]
    assert uniquely_identifiable_participants(nested) == [0]
    repeated = [
        [1, 1, 1, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 1, 1, 0, 1],
    ]
    assert uniquely_identifiable_participants(repeated) == [0]
    assert uniquely_identifiable_participants([[1, 1, 1, 1, 1]]) == []
    print("linear release audit passed: nested and composed releases identify P1")


if __name__ == "__main__":
    run()
