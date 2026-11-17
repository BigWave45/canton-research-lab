import unittest
from dataclasses import dataclass
from datetime import datetime,timedelta,timezone
from interval_coverage import IntervalReport,ScheduleAnchor,build_expected_intervals
from reconciliation_state_machine import Allocation,Burn,Case,Obligation,Report
from integrated_interval_reconciliation import (
    PriorSettlement,reconcile_with_interval_coverage,
)

UTC=timezone.utc
START=datetime(2026,11,17,12,0,tzinfo=UTC)
END=START+timedelta(minutes=10)

@dataclass(frozen=True)
class CaseWithLiabilities:
    expected_report_ids: tuple
    reports: tuple
    obligations: tuple
    burns: tuple
    allocations: tuple
    evaluation_time: str
    reward_required: bool=True
    reward_record_ids: tuple=("reward-1",)
    liability_by_report_id: dict=None

def setup_case(liabilities=None):
    return CaseWithLiabilities(
        ("r0",),
        (Report("r0","OK","v1","o1","s1"),),
        (Obligation("o1",10,"v1",synchronizer_id="s1"),),
        (Burn("b1",10),),
        (Allocation("a1","b1","o1",10),),
        "2026-11-17T12:10:00+00:00",
        liability_by_report_id=liabilities or {},
    )

class IntegratedIntervalReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.expected=build_expected_intervals(START,END,timedelta(minutes=10),timedelta(minutes=5))
        self.report=IntervalReport("r0",self.expected[0].interval_id,START,END,END,"OK")
    def test_complete_coverage_allows_reconciliation(self):
        out=reconcile_with_interval_coverage(setup_case(),self.expected,(self.report,))
        self.assertEqual(out["payment_state"],"RECONCILED")
        self.assertEqual(out["coverage"]["schedule_validation"]["state"],
                         "INTERNALLY_CONSISTENT_UNANCHORED")
    def test_strict_mode_requires_schedule_anchor(self):
        out=reconcile_with_interval_coverage(
            setup_case(),self.expected,(self.report,),require_schedule_anchor=True
        )
        self.assertEqual(out["payment_state"],"BLOCKED_INVALID_INTERVAL_EVIDENCE")
        self.assertEqual(out["coverage"]["reason"],"SCHEDULE_ANCHOR_REQUIRED")
    def test_strict_mode_accepts_matching_schedule_anchor(self):
        anchor=ScheduleAnchor(START,END,timedelta(minutes=10),timedelta(minutes=5))
        out=reconcile_with_interval_coverage(
            setup_case(),self.expected,(self.report,),
            schedule_anchor=anchor,require_schedule_anchor=True,
        )
        self.assertEqual(out["payment_state"],"RECONCILED")
        self.assertEqual(out["coverage"]["schedule_validation"]["anchor_comparison"],"MATCHED")
    def test_strict_mode_rejects_truncated_schedule_against_anchor(self):
        full_end=END+timedelta(minutes=10)
        anchor=ScheduleAnchor(START,full_end,timedelta(minutes=10),timedelta(minutes=5))
        full=build_expected_intervals(START,full_end,timedelta(minutes=10),timedelta(minutes=5))
        truncated=full[:1]
        report=IntervalReport("r0",truncated[0].interval_id,truncated[0].start,
                              truncated[0].end,truncated[0].end,"OK")
        out=reconcile_with_interval_coverage(
            setup_case(),truncated,(report,),
            schedule_anchor=anchor,require_schedule_anchor=True,
        )
        self.assertEqual(out["payment_state"],"BLOCKED_INVALID_INTERVAL_EVIDENCE")
        self.assertEqual(out["coverage"]["reason"],"SCHEDULE_ANCHOR_MISMATCH")
    def test_empty_or_invalid_schedule_never_reaches_payment_reconciliation(self):
        empty=reconcile_with_interval_coverage(setup_case(),(),())
        invalid=reconcile_with_interval_coverage(
            setup_case(),(self.expected[0],self.expected[0]),(self.report,)
        )
        self.assertEqual(empty["payment_state"],"BLOCKED_INVALID_INTERVAL_EVIDENCE")
        self.assertEqual(empty["coverage"]["reason"],"EMPTY_EXPECTED_SCHEDULE")
        self.assertEqual(invalid["payment_state"],"BLOCKED_INVALID_INTERVAL_EVIDENCE")
        self.assertEqual(invalid["coverage"]["reason"],"DUPLICATE_EXPECTED_INTERVAL_ID")
    def test_missing_report_blocks_payment(self):
        out=reconcile_with_interval_coverage(setup_case(),self.expected,())
        self.assertEqual(out["payment_state"],"BLOCKED_INTERVAL_COVERAGE")
    def test_late_report_blocks_by_default(self):
        late=IntervalReport("r0",self.expected[0].interval_id,START,END,END+timedelta(minutes=6),"OK")
        out=reconcile_with_interval_coverage(setup_case(),self.expected,(late,))
        self.assertEqual(out["payment_state"],"BLOCKED_INTERVAL_COVERAGE")
    def test_late_report_can_be_allowed_explicitly(self):
        late=IntervalReport("r0",self.expected[0].interval_id,START,END,END+timedelta(minutes=6),"OK")
        out=reconcile_with_interval_coverage(setup_case(),self.expected,(late,),allow_late_reports=True)
        self.assertEqual(out["payment_state"],"RECONCILED")
    def test_correction_without_liability_calculation_is_blocked(self):
        correction=IntervalReport("r1",self.expected[0].interval_id,START,END,END+timedelta(minutes=2),"OK",1,"r0")
        prior=(PriorSettlement("settle-1",self.expected[0].interval_id,"r0",10),)
        out=reconcile_with_interval_coverage(setup_case(),self.expected,(self.report,correction),prior)
        self.assertEqual(out["payment_state"],"BLOCKED_CORRECTION_LIABILITY")
    def test_correction_creates_append_only_adjustment(self):
        correction=IntervalReport("r1",self.expected[0].interval_id,START,END,END+timedelta(minutes=2),"OK",1,"r0")
        prior=(PriorSettlement("settle-1",self.expected[0].interval_id,"r0",10),)
        out=reconcile_with_interval_coverage(setup_case({"r1":12}),self.expected,(self.report,correction),prior)
        self.assertEqual(out["adjustments"][0]["adjustment_cc"],2)
        self.assertEqual(out["adjustments"][0]["status"],"REQUIRES_SEPARATE_SETTLEMENT")
        self.assertEqual(out["correction_policy"],"APPEND_ONLY_ADJUSTMENT")
    def test_downward_correction_creates_negative_adjustment(self):
        correction=IntervalReport("r1",self.expected[0].interval_id,START,END,END+timedelta(minutes=2),"OK",1,"r0")
        prior=(PriorSettlement("settle-1",self.expected[0].interval_id,"r0",10),)
        out=reconcile_with_interval_coverage(setup_case({"r1":8}),self.expected,(self.report,correction),prior)
        self.assertEqual(out["adjustments"][0]["adjustment_cc"],-2)
    def test_invalid_correction_chain_blocks(self):
        correction=IntervalReport("r1",self.expected[0].interval_id,START,END,END+timedelta(minutes=2),"OK",1,"wrong")
        out=reconcile_with_interval_coverage(setup_case(),self.expected,(self.report,correction))
        self.assertEqual(out["payment_state"],"BLOCKED_INVALID_INTERVAL_EVIDENCE")

if __name__=="__main__": unittest.main()
