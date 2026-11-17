import unittest
from datetime import datetime,timedelta,timezone
from interval_coverage import IntervalReport,build_expected_intervals,evaluate_coverage

UTC=timezone.utc
START=datetime(2026,11,17,12,0,tzinfo=UTC)
END=START+timedelta(hours=1)

def make_reports(expected,received=None):
    received=received or END
    return tuple(IntervalReport(f"r{i}",x.interval_id,x.start,x.end,received,"OK") for i,x in enumerate(expected))

class IntervalCoverageTests(unittest.TestCase):
    def setUp(self):
        self.expected=build_expected_intervals(START,END,timedelta(minutes=10),timedelta(minutes=5))
    def test_hour_has_six_intervals(self):
        self.assertEqual(len(self.expected),6)
    def test_complete(self):
        self.assertEqual(evaluate_coverage(self.expected,make_reports(self.expected),END)["state"],"COMPLETE")
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
        rs.append(IntervalReport("r0-c1",r.interval_id,r.start,r.end,END+timedelta(minutes=2),"OK",1,"r0"))
        out=evaluate_coverage(self.expected,rs,END+timedelta(minutes=3))
        self.assertEqual(out["intervals"][0]["state"],"CORRECTED")
        self.assertEqual(out["intervals"][0]["latest_report_id"],"r0-c1")
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
