"""Expected-interval coverage for synthetic synchronizer traffic reports."""
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Iterable

@dataclass(frozen=True)
class ExpectedInterval:
    interval_id: str
    start: datetime
    end: datetime
    report_deadline: datetime


@dataclass(frozen=True)
class ScheduleAnchor:
    """Caller-supplied settlement window and cadence; authority is external."""
    window_start: datetime
    window_end: datetime
    cadence: timedelta
    reporting_grace: timedelta = timedelta(0)


@dataclass(frozen=True)
class IntervalReport:
    report_id: str
    interval_id: str
    start: datetime
    end: datetime
    received_at: datetime
    status: str
    revision: int = 0
    supersedes_report_id: str | None = None
    agreement_version: str | None = None
    consumed_units: int | None = None
    obligation_id: str | None = None
    synchronizer_id: str | None = None

    @property
    def interval_start(self):
        return self.start.isoformat()

    @property
    def interval_end(self):
        return self.end.isoformat()

def _aware(value):
    return (
        isinstance(value, datetime)
        and value.tzinfo is not None
        and value.utcoffset() is not None
    )

def build_expected_intervals(window_start, window_end, cadence, reporting_grace=timedelta(0)):
    if not all(_aware(x) for x in (window_start, window_end)):
        raise ValueError("All timestamps must be timezone-aware")
    if cadence.total_seconds() <= 0 or reporting_grace.total_seconds() < 0:
        raise ValueError("Cadence must be positive and grace non-negative")
    duration = window_end - window_start
    steps = duration.total_seconds() / cadence.total_seconds()
    if duration.total_seconds() <= 0 or not steps.is_integer():
        raise ValueError("Window must be positive and exactly divisible by cadence")
    result, cursor = [], window_start
    while cursor < window_end:
        end = cursor + cadence
        result.append(ExpectedInterval(
            f"{cursor.isoformat()}_{end.isoformat()}", cursor, end,
            end + reporting_grace
        ))
        cursor = end
    return tuple(result)


def _validate_expected_schedule(expected, schedule_anchor, require_schedule_anchor):
    if not expected:
        return None, {"state": "INVALID", "reason": "EMPTY_EXPECTED_SCHEDULE"}

    for item in expected:
        if not isinstance(item.interval_id, str) or not item.interval_id.strip():
            return None, {"state": "INVALID", "reason": "EXPECTED_INTERVAL_ID_MISSING"}
    ordered_by_id = tuple(sorted(expected, key=lambda x: x.interval_id))
    for previous, current in zip(ordered_by_id, ordered_by_id[1:]):
        if previous.interval_id == current.interval_id:
            return None, {"state": "INVALID", "reason": "DUPLICATE_EXPECTED_INTERVAL_ID",
                          "interval_id": current.interval_id}
    for item in ordered_by_id:
        if not all(_aware(value) for value in (item.start, item.end, item.report_deadline)):
            return None, {"state": "INVALID", "reason": "EXPECTED_INTERVAL_NAIVE_TIMESTAMP",
                          "interval_id": item.interval_id}

    ordered = tuple(sorted(expected, key=lambda x: (x.start, x.end, x.interval_id)))
    temporal_intervals = set()
    for item in ordered:
        if item.end <= item.start:
            return None, {"state": "INVALID", "reason": "EXPECTED_INTERVAL_NON_POSITIVE",
                          "interval_id": item.interval_id}
        if item.report_deadline < item.end:
            return None, {"state": "INVALID", "reason": "EXPECTED_DEADLINE_BEFORE_INTERVAL_END",
                          "interval_id": item.interval_id}
        temporal = (item.start, item.end)
        if temporal in temporal_intervals:
            return None, {"state": "INVALID", "reason": "DUPLICATE_EXPECTED_TEMPORAL_INTERVAL",
                          "interval_id": item.interval_id}
        temporal_intervals.add(temporal)

    for previous, current in zip(ordered, ordered[1:]):
        if current.start > previous.end:
            return None, {"state": "INVALID", "reason": "EXPECTED_SCHEDULE_GAP",
                          "interval_id": current.interval_id}
        if current.start < previous.end:
            return None, {"state": "INVALID", "reason": "EXPECTED_SCHEDULE_OVERLAP",
                          "interval_id": current.interval_id}

    if schedule_anchor is None:
        if require_schedule_anchor:
            return None, {"state": "INVALID", "reason": "SCHEDULE_ANCHOR_REQUIRED"}
        return ordered, {
            "state": "INTERNALLY_CONSISTENT_UNANCHORED",
            "anchor_comparison": "NOT_PROVIDED",
            "anchor_authority": "NOT_ESTABLISHED",
        }

    if not isinstance(schedule_anchor, ScheduleAnchor):
        return None, {"state": "INVALID", "reason": "INVALID_SCHEDULE_ANCHOR"}
    try:
        anchored = build_expected_intervals(
            schedule_anchor.window_start,
            schedule_anchor.window_end,
            schedule_anchor.cadence,
            schedule_anchor.reporting_grace,
        )
    except (AttributeError, TypeError, ValueError, OverflowError):
        return None, {"state": "INVALID", "reason": "INVALID_SCHEDULE_ANCHOR"}
    supplied_shape = tuple(
        (x.interval_id, x.start, x.end, x.report_deadline) for x in ordered
    )
    anchored_shape = tuple(
        (x.interval_id, x.start, x.end, x.report_deadline) for x in anchored
    )
    if supplied_shape != anchored_shape:
        return None, {"state": "INVALID", "reason": "SCHEDULE_ANCHOR_MISMATCH"}
    return ordered, {
        "state": "INTERNALLY_CONSISTENT",
        "anchor_comparison": "MATCHED",
        "anchor_authority": "NOT_ESTABLISHED_BY_VALIDATOR",
    }


def evaluate_coverage(
    expected: Iterable[ExpectedInterval],
    reports: Iterable[IntervalReport],
    evaluation_time,
    schedule_anchor: ScheduleAnchor | None = None,
    require_schedule_anchor: bool = False,
):
    """Evaluate reports; an anchor comparison does not authenticate its authority."""
    expected = tuple(expected)
    ordered_expected, schedule_validation = _validate_expected_schedule(
        expected, schedule_anchor, require_schedule_anchor
    )
    if ordered_expected is None:
        return {
            "state": "INVALID",
            "reason": schedule_validation["reason"],
            "schedule_validation": schedule_validation,
        }
    if not _aware(evaluation_time):
        raise ValueError("Evaluation time must be timezone-aware")
    reports = tuple(reports)
    expected_by_id = {x.interval_id:x for x in expected}
    report_ids = sorted(r.report_id for r in reports)
    if len(set(report_ids)) != len(report_ids):
        return {"state":"INVALID","reason":"DUPLICATE_REPORT_ID",
                "schedule_validation":schedule_validation}
    grouped = {}
    for r in reports:
        item = expected_by_id.get(r.interval_id)
        if item is None:
            return {"state":"INVALID","reason":"UNEXPECTED_INTERVAL","report_id":r.report_id,
                    "schedule_validation":schedule_validation}
        if not all(_aware(x) for x in (r.start,r.end,r.received_at)):
            return {"state":"INVALID","reason":"NAIVE_TIMESTAMP","report_id":r.report_id,
                    "schedule_validation":schedule_validation}
        if (r.start,r.end)!=(item.start,item.end):
            return {"state":"INVALID","reason":"INTERVAL_BOUNDARY_MISMATCH","report_id":r.report_id,
                    "schedule_validation":schedule_validation}
        if r.status not in {"OK","UNDETERMINED","CANNOT_PROVIDE"} or r.revision < 0:
            return {"state":"INVALID","reason":"INVALID_REPORT_FIELDS","report_id":r.report_id,
                    "schedule_validation":schedule_validation}
        grouped.setdefault(r.interval_id,[]).append(r)
    rows=[]
    for item in ordered_expected:
        versions=sorted(grouped.get(item.interval_id,[]),key=lambda x:x.revision)
        if not versions:
            state="AWAITING" if evaluation_time <= item.report_deadline else "MISSING_OVERDUE"
            rows.append({"interval_id":item.interval_id,"state":state})
            continue
        revisions = [report.revision for report in versions]
        if len(revisions) != len(set(revisions)):
            return {"state":"INVALID","reason":"DUPLICATE_REPORT_REVISION",
                    "interval_id":item.interval_id,"schedule_validation":schedule_validation}
        previous=None
        original_binding=None
        for n,r in enumerate(versions):
            if r.revision != n:
                return {"state":"INVALID","reason":"REVISION_GAP","interval_id":item.interval_id,
                        "schedule_validation":schedule_validation}
            if (n==0 and r.supersedes_report_id is not None) or (n>0 and r.supersedes_report_id != previous):
                return {"state":"INVALID","reason":"BROKEN_CORRECTION_CHAIN",
                        "interval_id":item.interval_id,"schedule_validation":schedule_validation}
            binding=(r.synchronizer_id,r.obligation_id,r.agreement_version)
            if n==0:
                original_binding=binding
            elif binding!=original_binding:
                return {"state":"INVALID","reason":"CORRECTION_BINDING_CHANGED",
                        "interval_id":item.interval_id,"report_id":r.report_id,
                        "schedule_validation":schedule_validation}
            previous=r.report_id
        latest=versions[-1]
        if latest.status!="OK": state="NON_OK"
        elif latest.received_at>item.report_deadline: state="LATE"
        elif latest.revision>0: state="CORRECTED"
        else: state="COVERED"
        rows.append({"interval_id":item.interval_id,"state":state,
                     "latest_report_id":latest.report_id,"revision":latest.revision})
    states=[x["state"] for x in rows]
    if "MISSING_OVERDUE" in states: overall="INCOMPLETE_OVERDUE"
    elif "AWAITING" in states: overall="INCOMPLETE_PENDING"
    elif "NON_OK" in states: overall="INCOMPLETE_NON_OK"
    elif "LATE" in states: overall="COMPLETE_WITH_LATE_REPORTS"
    else: overall="COMPLETE"
    return {
        "state":overall,
        "intervals":rows,
        "measurement_completeness":"NOT_ESTABLISHED",
        "schedule_validation":schedule_validation,
    }
