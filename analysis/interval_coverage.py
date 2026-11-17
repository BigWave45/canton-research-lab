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
    return value.tzinfo is not None and value.utcoffset() is not None

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

def evaluate_coverage(expected: Iterable[ExpectedInterval], reports: Iterable[IntervalReport], evaluation_time):
    if not _aware(evaluation_time):
        raise ValueError("Evaluation time must be timezone-aware")
    expected, reports = tuple(expected), tuple(reports)
    if len({x.interval_id for x in expected}) != len(expected):
        return {"state":"INVALID","reason":"DUPLICATE_EXPECTED_INTERVAL"}
    expected_by_id = {x.interval_id:x for x in expected}
    report_ids = [r.report_id for r in reports]
    if len(set(report_ids)) != len(report_ids):
        return {"state":"INVALID","reason":"DUPLICATE_REPORT_ID"}
    grouped = {}
    for r in reports:
        item = expected_by_id.get(r.interval_id)
        if item is None:
            return {"state":"INVALID","reason":"UNEXPECTED_INTERVAL","report_id":r.report_id}
        if (r.start,r.end)!=(item.start,item.end):
            return {"state":"INVALID","reason":"INTERVAL_BOUNDARY_MISMATCH","report_id":r.report_id}
        if not all(_aware(x) for x in (r.start,r.end,r.received_at)):
            return {"state":"INVALID","reason":"NAIVE_TIMESTAMP","report_id":r.report_id}
        if r.status not in {"OK","UNDETERMINED","CANNOT_PROVIDE"} or r.revision < 0:
            return {"state":"INVALID","reason":"INVALID_REPORT_FIELDS","report_id":r.report_id}
        grouped.setdefault(r.interval_id,[]).append(r)
    rows=[]
    for item in expected:
        versions=sorted(grouped.get(item.interval_id,[]),key=lambda x:x.revision)
        if not versions:
            state="AWAITING" if evaluation_time <= item.report_deadline else "MISSING_OVERDUE"
            rows.append({"interval_id":item.interval_id,"state":state})
            continue
        previous=None
        for n,r in enumerate(versions):
            if r.revision != n:
                return {"state":"INVALID","reason":"REVISION_GAP","interval_id":item.interval_id}
            if (n==0 and r.supersedes_report_id is not None) or (n>0 and r.supersedes_report_id != previous):
                return {"state":"INVALID","reason":"BROKEN_CORRECTION_CHAIN","interval_id":item.interval_id}
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
    return {"state":overall,"intervals":rows,"measurement_completeness":"NOT_ESTABLISHED"}
