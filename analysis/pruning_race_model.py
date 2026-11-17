"""Conceptual model of a pruning/read race; not Canton implementation code."""
from dataclasses import dataclass
from enum import Enum

class ReadResult(str, Enum):
    OK_CORRECT = "ok_correct"
    CANNOT_PROVIDE = "cannot_provide"
    ERROR = "error"
    OK_STALE = "ok_stale"

@dataclass(frozen=True)
class Scenario:
    name: str
    pruning_moves_after_check: bool
    requested_snapshot_available_at_read: bool
    implementation_returns_stale_snapshot: bool = False

def classify(s: Scenario) -> ReadResult:
    if not s.pruning_moves_after_check:
        return ReadResult.OK_CORRECT
    if s.requested_snapshot_available_at_read:
        return ReadResult.OK_CORRECT
    if s.implementation_returns_stale_snapshot:
        return ReadResult.OK_STALE
    return ReadResult.CANNOT_PROVIDE

def settlement_effect(expected_bytes: int, reported_bytes: int, price_per_byte: int) -> int:
    return (expected_bytes - reported_bytes) * price_per_byte
