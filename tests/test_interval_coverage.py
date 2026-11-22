import unittest
from datetime import datetime,timedelta,timezone
from interval_coverage import (
    ExpectedInterval,IntervalReport,ScheduleAnchor,build_expected_intervals,evaluate_coverage,
)

UTC=timezone.utc
START=datetime(2026,11,17,12,0,tzinfo=UTC)
END=START+timedelta(hours=1)

def make_reports(expected,received=None):
    return tuple(
        IntervalReport(
            f"r{i}",x.interval_id,x.start,x.end,
            received if received is not None else x.end,"OK"
        )
        for i,x in enumerate(expected)
    )

class IntervalCoverageTests(unittest.TestCase):
    def setUp(self):
        self.expected=build_expected_intervals(START,END,timedelta(minutes=10),timedelta(minutes=5))
    def test_hour_has_six_intervals(self):
        self.assertEqual(len(self.expected),6)
    def test_complete(self):
        self.assertEqual(evaluate_coverage(self.expected,make_reports(self.expected),END)["state"],"COMPLETE")
    def test_complete_schedule_is_marked_unanchored_without_anchor(self):
        out=evaluate_coverage(self.expected,make_reports(self.expected),END)
        self.assertEqual(out["schedule_validation"]["state"],"INTERNALLY_CONSISTENT_UNANCHORED")
        self.assertEqual(out["schedule_validation"]["anchor_authority"],"NOT_ESTABLISHED")
    def test_empty_expected_schedule_is_invalid(self):
        out=evaluate_coverage((),(),END)
        self.assertEqual(out["reason"],"EMPTY_EXPECTED_SCHEDULE")
    def test_empty_and_duplicate_expected_ids_are_invalid(self):
        first=self.expected[0]
        empty_id=ExpectedInterval("",first.start,first.end,first.report_deadline)
        duplicate_id=ExpectedInterval(first.interval_id,first.end,first.end+timedelta(minutes=10),
            first.end+timedelta(minutes=15))
        self.assertEqual(evaluate_coverage((empty_id,),(),END)["reason"],
                         "EXPECTED_INTERVAL_ID_MISSING")
        self.assertEqual(evaluate_coverage((first,duplicate_id),(),END)["reason"],
                         "DUPLICATE_EXPECTED_INTERVAL_ID")
    def test_naive_expected_boundaries_and_deadline_are_invalid(self):
        item=self.expected[0]
        naive_start=item.start.replace(tzinfo=None)
        naive_end=item.end.replace(tzinfo=None)
        naive_deadline=item.report_deadline.replace(tzinfo=None)
        variants=(
            ExpectedInterval(item.interval_id,naive_start,item.end,item.report_deadline),
            ExpectedInterval(item.interval_id,item.start,naive_end,item.report_deadline),
            ExpectedInterval(item.interval_id,item.start,item.end,naive_deadline),
        )
        for invalid in variants:
            with self.subTest(interval=invalid):
                self.assertEqual(evaluate_coverage((invalid,),(),END)["reason"],
                                 "EXPECTED_INTERVAL_NAIVE_TIMESTAMP")
    def test_non_positive_expected_interval_is_invalid(self):
        item=self.expected[0]
        invalid=ExpectedInterval(item.interval_id,item.start,item.start,item.report_deadline)
        self.assertEqual(evaluate_coverage((invalid,),(),END)["reason"],
                         "EXPECTED_INTERVAL_NON_POSITIVE")
    def test_deadline_before_interval_end_is_invalid(self):
        item=self.expected[0]
        invalid=ExpectedInterval(item.interval_id,item.start,item.end,item.end-timedelta(seconds=1))
        self.assertEqual(evaluate_coverage((invalid,),(),END)["reason"],
                         "EXPECTED_DEADLINE_BEFORE_INTERVAL_END")
    def test_expected_schedule_gap_is_invalid(self):
        first,second=self.expected[:2]
        gap=ExpectedInterval("gap",first.end+timedelta(seconds=1),
            second.end,second.report_deadline)
        self.assertEqual(evaluate_coverage((gap,first),(),END)["reason"],
                         "EXPECTED_SCHEDULE_GAP")
    def test_expected_schedule_overlap_is_invalid(self):
        first,second=self.expected[:2]
        overlap=ExpectedInterval("overlap",first.end-timedelta(seconds=1),
            second.end,second.report_deadline)
        self.assertEqual(evaluate_coverage((overlap,first),(),END)["reason"],
                         "EXPECTED_SCHEDULE_OVERLAP")
    def test_duplicate_temporal_intervals_under_different_ids_are_invalid(self):
        first=self.expected[0]
        duplicate=ExpectedInterval("different-id",first.start,first.end,first.report_deadline)
        self.assertEqual(evaluate_coverage((first,duplicate),(),END)["reason"],
                         "DUPLICATE_EXPECTED_TEMPORAL_INTERVAL")
    def test_expected_intervals_are_validated_and_reported_chronologically(self):
        reversed_expected=tuple(reversed(self.expected))
        reversed_reports=tuple(reversed(make_reports(self.expected)))
        out=evaluate_coverage(reversed_expected,reversed_reports,END)
        self.assertEqual(out["state"],"COMPLETE")
        self.assertEqual([row["interval_id"] for row in out["intervals"]],
                         [item.interval_id for item in self.expected])
    def test_anchor_matches_complete_expected_schedule(self):
        anchor=ScheduleAnchor(START,END,timedelta(minutes=10),timedelta(minutes=5))
        out=evaluate_coverage(self.expected,make_reports(self.expected),END,schedule_anchor=anchor)
        self.assertEqual(out["state"],"COMPLETE")
        self.assertEqual(out["schedule_validation"]["anchor_comparison"],"MATCHED")
        self.assertEqual(out["schedule_validation"]["anchor_authority"],
                         "NOT_ESTABLISHED_BY_VALIDATOR")
    def test_truncated_contiguous_schedule_requires_external_anchor_to_detect(self):
        truncated=self.expected[:3]
        reports=make_reports(truncated)
        unanchored=evaluate_coverage(truncated,reports,END)
        anchored=evaluate_coverage(
            truncated,reports,END,
            schedule_anchor=ScheduleAnchor(START,END,timedelta(minutes=10),timedelta(minutes=5)),
        )
        self.assertEqual(unanchored["state"],"COMPLETE")
        self.assertEqual(unanchored["schedule_validation"]["state"],
                         "INTERNALLY_CONSISTENT_UNANCHORED")
        self.assertEqual((anchored["state"],anchored["reason"]),
                         ("INVALID","SCHEDULE_ANCHOR_MISMATCH"))
    def test_missing_before_deadline_pending(self):
        self.assertEqual(evaluate_coverage(self.expected,make_reports(self.expected[:-1]),END)["state"],"INCOMPLETE_PENDING")
    def test_missing_after_deadline_overdue(self):
        t=END+timedelta(minutes=6)
        self.assertEqual(evaluate_coverage(self.expected,make_reports(self.expected[:-1]),t)["state"],"INCOMPLETE_OVERDUE")
    def test_non_ok_is_not_zero(self):
        rs=list(make_reports(self.expected)); r=rs[0]
        rs[0]=IntervalReport(r.report_id,r.interval_id,r.start,r.end,r.received_at,"UNDETERMINED")
        self.assertEqual(evaluate_coverage(self.expected,rs,END)["state"],"INCOMPLETE_NON_OK")
    def test_late_report_is_visible(self):
        t=END+timedelta(minutes=6)
        self.assertEqual(evaluate_coverage(self.expected,make_reports(self.expected,t),t)["state"],"COMPLETE_WITH_LATE_REPORTS")
    def test_valid_correction_chain(self):
        rs=list(make_reports(self.expected)); r=rs[0]
        correction_time=r.end+timedelta(minutes=2)
        rs.append(IntervalReport("r0-c1",r.interval_id,r.start,r.end,correction_time,"OK",1,"r0"))
        out=evaluate_coverage(self.expected,rs,correction_time+timedelta(minutes=1))
        self.assertEqual(out["intervals"][0]["state"],"CORRECTED")
        self.assertEqual(out["intervals"][0]["latest_report_id"],"r0-c1")
    def test_multiple_corrections_accept_arbitrary_report_order(self):
        item=self.expected[0]
        reports=(
            IntervalReport("r2",item.interval_id,item.start,item.end,item.end+timedelta(minutes=3),
                           "OK",2,"r1"),
            IntervalReport("r0",item.interval_id,item.start,item.end,item.end,"OK"),
            IntervalReport("r1",item.interval_id,item.start,item.end,item.end+timedelta(minutes=2),
                           "OK",1,"r0"),
        )
        reports += tuple(
            IntervalReport(f"other-{index}",item.interval_id,item.start,item.end,item.end,"OK")
            for index,item in enumerate(self.expected[1:],start=1)
        )
        out=evaluate_coverage(self.expected,reports,END+timedelta(minutes=4))
        self.assertEqual(out["state"],"COMPLETE")
        self.assertEqual(out["intervals"][0]["latest_report_id"],"r2")
        self.assertEqual(out["intervals"][0]["revision"],2)
    def test_two_report_ids_cannot_claim_same_revision(self):
        item=self.expected[0]
        reports=(
            IntervalReport("r0",item.interval_id,item.start,item.end,item.end,"OK"),
            IntervalReport("r0-alt",item.interval_id,item.start,item.end,item.end,"OK"),
        )
        out=evaluate_coverage(self.expected,reports,END)
        self.assertEqual((out["state"],out["reason"]),
                         ("INVALID","DUPLICATE_REPORT_REVISION"))
    def test_two_corrections_cannot_supersede_the_same_report(self):
        item=self.expected[0]
        reports=(
            IntervalReport("r0",item.interval_id,item.start,item.end,item.end,"OK"),
            IntervalReport("r1",item.interval_id,item.start,item.end,item.end+timedelta(minutes=1),
                           "OK",1,"r0"),
            IntervalReport("r1-alt",item.interval_id,item.start,item.end,item.end+timedelta(minutes=2),
                           "OK",2,"r0"),
        )
        out=evaluate_coverage(self.expected[:1],reports,END+timedelta(minutes=3))
        self.assertEqual((out["state"],out["reason"]),("INVALID","SUPERSESSION_BRANCH"))
    def test_supersession_cycle_is_rejected(self):
        item=self.expected[0]
        reports=(
            IntervalReport("r0",item.interval_id,item.start,item.end,item.end,"OK",0,"r1"),
            IntervalReport("r1",item.interval_id,item.start,item.end,item.end+timedelta(minutes=1),
                           "OK",1,"r0"),
        )
        out=evaluate_coverage(self.expected[:1],reports,END+timedelta(minutes=2))
        self.assertEqual((out["state"],out["reason"]),("INVALID","CORRECTION_CHAIN_CYCLE"))
    def test_missing_correction_revision_is_invalid(self):
        item=self.expected[0]
        reports=(
            IntervalReport("r0",item.interval_id,item.start,item.end,item.end,"OK"),
            IntervalReport("r2",item.interval_id,item.start,item.end,item.end+timedelta(minutes=2),
                           "OK",2,"r0"),
        )
        out=evaluate_coverage(self.expected,reports,END+timedelta(minutes=3))
        self.assertEqual((out["state"],out["reason"]),("INVALID","REVISION_GAP"))
    def test_broken_correction_predecessor_is_invalid(self):
        item=self.expected[0]
        reports=(
            IntervalReport("r0",item.interval_id,item.start,item.end,item.end,"OK"),
            IntervalReport("r1",item.interval_id,item.start,item.end,item.end+timedelta(minutes=2),
                           "OK",1,"not-r0"),
        )
        out=evaluate_coverage(self.expected,reports,END+timedelta(minutes=3))
        self.assertEqual((out["state"],out["reason"]),
                         ("INVALID","BROKEN_CORRECTION_CHAIN"))
    def test_report_boundaries_must_match_expected_interval(self):
        item=self.expected[0]
        report=IntervalReport("r0",item.interval_id,item.start+timedelta(seconds=1),
                              item.end,item.end,"OK")
        out=evaluate_coverage(self.expected,(report,),END)
        self.assertEqual((out["state"],out["reason"]),
                         ("INVALID","INTERVAL_BOUNDARY_MISMATCH"))
    def test_broken_correction_chain_invalid(self):
        rs=list(make_reports(self.expected)); r=rs[0]
        rs.append(IntervalReport("r0-c1",r.interval_id,r.start,r.end,END+timedelta(minutes=2),"OK",1,"wrong"))
        out=evaluate_coverage(self.expected,rs,END+timedelta(minutes=3))
        self.assertEqual((out["state"],out["reason"]),("INVALID","BROKEN_CORRECTION_CHAIN"))
    def test_unexpected_interval_invalid(self):
        rs=list(make_reports(self.expected)); r=rs[0]
        rs[0]=IntervalReport(r.report_id,"unknown",r.start,r.end,r.received_at,"OK")
        self.assertEqual(evaluate_coverage(self.expected,rs,END)["reason"],"UNEXPECTED_INTERVAL")
    def test_naive_timestamps_rejected(self):
        with self.assertRaises(ValueError):
            build_expected_intervals(datetime(2026,11,17),END,timedelta(minutes=10))

if __name__=="__main__": unittest.main()
