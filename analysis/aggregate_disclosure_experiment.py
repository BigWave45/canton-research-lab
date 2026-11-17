"""Synthetic aggregate-disclosure differencing experiment.

This is a privacy-risk demonstration, not a Canton traffic dataset or attack
against a live Canton deployment.
"""
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class AggregateRelease:
    release_id: str
    members: frozenset[str]
    total_bytes: int


def release_for(members: Iterable[str], usage: dict[str, int], release_id: str):
    cohort = frozenset(members)
    return AggregateRelease(release_id, cohort, sum(usage[p] for p in cohort))


def find_single_member_differences(
    releases: Iterable[AggregateRelease], minimum_cohort: int
) -> list[dict]:
    """Find nested cohort releases whose difference isolates one member."""
    releases = tuple(releases)
    findings = []
    for i, left in enumerate(releases):
        for right in releases[i + 1:]:
            if len(left.members) < minimum_cohort or len(right.members) < minimum_cohort:
                continue
            if left.members < right.members:
                larger, smaller = right, left
            elif right.members < left.members:
                larger, smaller = left, right
            else:
                continue
            difference = larger.members - smaller.members
            if len(difference) == 1:
                findings.append({
                    "larger_release": larger.release_id,
                    "smaller_release": smaller.release_id,
                    "isolated_member": next(iter(difference)),
                    "inferred_bytes": larger.total_bytes - smaller.total_bytes,
                    "both_cohorts_meet_threshold": True,
                })
    return findings


def run_experiment():
    usage = {"P1": 40, "P2": 30, "P3": 20, "P4": 10, "P5": 50}
    whole = release_for(usage, usage, "whole-synchronizer")
    cohort_a = release_for(("P1", "P2", "P3", "P4"), usage, "cohort-A")
    cohort_b = release_for(("P2", "P3", "P4"), usage, "cohort-B")
    assert whole.total_bytes == 150
    assert cohort_a.total_bytes == 100
    assert cohort_b.total_bytes == 60
    findings = find_single_member_differences((cohort_a, cohort_b), 3)
    assert findings == [{
        "larger_release": "cohort-A", "smaller_release": "cohort-B",
        "isolated_member": "P1", "inferred_bytes": 40,
        "both_cohorts_meet_threshold": True,
    }]
    print("whole synchronizer total:", whole.total_bytes)
    print("k=3 overlapping cohort releases:", findings[0])
    print("finding: minimum cohort size alone does not prevent differencing")


if __name__ == "__main__":
    run_experiment()
