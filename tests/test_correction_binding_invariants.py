import unittest
from datetime import datetime,timedelta,timezone
from interval_coverage import IntervalReport,build_expected_intervals,evaluate_coverage
UTC=timezone.utc
START=datetime(2026,11,17,12,0,tzinfo=UTC)
END=START+timedelta(minutes=10)
class CorrectionBindingTests(unittest.TestCase):
    def setUp(self):
        self.expected=build_expected_intervals(START,END,timedelta(minutes=10),timedelta(minutes=5))
        self.interval=self.expected[0]
    def report(self,rid,revision=0,supersedes=None,sync="sync-A",obligation="obligation-A",
               agreement="v1",units=10,paymaster="paymaster-A"):
        return IntervalReport(rid,self.interval.interval_id,START,END,END+timedelta(minutes=revision),
            "OK",revision,supersedes,agreement,units,obligation,sync,paymaster)
    def test_correction_preserves_accounting_identity(self):
        out=evaluate_coverage(self.expected,(self.report("r0"),self.report("r1",1,"r0",units=12)),END+timedelta(minutes=2))
        self.assertEqual(out["state"],"COMPLETE")
        self.assertEqual(out["intervals"][0]["latest_report_id"],"r1")
    def test_correction_cannot_change_synchronizer(self):
        out=evaluate_coverage(self.expected,(self.report("r0"),self.report("r1",1,"r0",sync="sync-B")),END+timedelta(minutes=2))
        self.assertEqual(out["state"],"INVALID")
        self.assertEqual(out["reason"],"CORRECTION_BINDING_CHANGED")
    def test_correction_cannot_change_paymaster(self):
        out=evaluate_coverage(self.expected,(
            self.report("r0"),
            self.report("r1",1,"r0",units=12,paymaster="paymaster-B")
        ),END+timedelta(minutes=2))
        self.assertEqual(out["reason"],"CORRECTION_BINDING_CHANGED")
    def test_correction_cannot_change_obligation(self):
        out=evaluate_coverage(self.expected,(self.report("r0"),self.report("r1",1,"r0",obligation="obligation-B")),END+timedelta(minutes=2))
        self.assertEqual(out["reason"],"CORRECTION_BINDING_CHANGED")
    def test_correction_cannot_change_agreement_version(self):
        out=evaluate_coverage(self.expected,(self.report("r0"),self.report("r1",1,"r0",agreement="v2")),END+timedelta(minutes=2))
        self.assertEqual(out["reason"],"CORRECTION_BINDING_CHANGED")
    def test_second_correction_must_preserve_original_binding(self):
        out=evaluate_coverage(self.expected,(
            self.report("r0"),
            self.report("r1",1,"r0",units=12),
            self.report("r2",2,"r1",units=11,sync="sync-C")
        ),END+timedelta(minutes=3))
        self.assertEqual(out["reason"],"CORRECTION_BINDING_CHANGED")
if __name__=="__main__": unittest.main()
