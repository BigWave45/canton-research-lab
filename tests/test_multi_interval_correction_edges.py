import unittest
from datetime import datetime,timedelta,timezone
from interval_coverage import IntervalReport,build_expected_intervals
from pricing_liability import PriceBand,PricingAgreement
from reconciliation_state_machine import Allocation,Burn,Case,Obligation,Report
from integrated_interval_reconciliation import PriorSettlement,reconcile_with_interval_coverage
UTC=timezone.utc
START=datetime(2026,11,17,12,0,tzinfo=UTC)
CADENCE=timedelta(minutes=10)
def tariff():
    return PricingAgreement("agreement-A","v1","2026-11-01T00:00:00+00:00",None,(PriceBand(None,1),))
def case(report_ids,due,burn,allocations):
    reports=tuple(Report(r,"OK","v1","o1","sync-A") for r in report_ids)
    return Case(tuple(report_ids),reports,(Obligation("o1",due,"v1",synchronizer_id="sync-A"),),
        (Burn("burn-1",burn),),tuple(allocations),"2026-11-17T12:30:00+00:00",reward_required=False)
def alloc(amount):
    return Allocation("allocation-1","burn-1","o1",amount)
class MultiIntervalCorrectionEdgeTests(unittest.TestCase):
    def setUp(self):
        self.expected=build_expected_intervals(START,START+2*CADENCE,CADENCE,timedelta(minutes=5))
        self.r0=IntervalReport("r0",self.expected[0].interval_id,self.expected[0].start,self.expected[0].end,
            self.expected[0].end,"OK",agreement_version="v1",consumed_units=10,
            obligation_id="o1",synchronizer_id="sync-A")
        self.r1=IntervalReport("r1",self.expected[1].interval_id,self.expected[1].start,self.expected[1].end,
            self.expected[1].end,"OK",agreement_version="v1",consumed_units=10,
            obligation_id="o1",synchronizer_id="sync-A")
    def test_two_intervals_sum_into_single_obligation(self):
        c=case(("r0","r1"),20,20,(alloc(20),))
        out=reconcile_with_interval_coverage(c,self.expected,(self.r0,self.r1),pricing_agreements={"v1":tariff()})
        self.assertEqual(out["pricing_results"]["r0"]["liability_cc"],10)
        self.assertEqual(out["pricing_results"]["r1"]["liability_cc"],10)
        self.assertEqual(out["payment_state"],"RECONCILED")
    def test_missing_synchronizer_identity_is_rejected(self):
        bad=IntervalReport("r0",self.expected[0].interval_id,self.expected[0].start,self.expected[0].end,
            self.expected[0].end,"OK",agreement_version="v1",consumed_units=10,obligation_id="o1")
        c=case(("r0",),10,10,(alloc(10),))
        out=reconcile_with_interval_coverage(c,(self.expected[0],),(bad,),pricing_agreements={"v1":tariff()})
        self.assertEqual(out["payment_state"],"BLOCKED_REPORT_BINDING")
    def test_downward_correction_emits_negative_adjustment(self):
        corrected=IntervalReport("r0-c1",self.expected[0].interval_id,self.expected[0].start,self.expected[0].end,
            self.expected[0].end+timedelta(minutes=1),"OK",revision=1,supersedes_report_id="r0",
            agreement_version="v1",consumed_units=8,obligation_id="o1",synchronizer_id="sync-A")
        c=case(("r0",),10,10,(alloc(10),))
        prior=(PriorSettlement("settle-1",self.expected[0].interval_id,"r0",10),)
        out=reconcile_with_interval_coverage(c,(self.expected[0],),(self.r0,corrected),prior,
            pricing_agreements={"v1":tariff()})
        self.assertEqual(out["adjustments"][0]["adjustment_cc"],-2)
        self.assertEqual(out["adjustments"][0]["status"],"REQUIRES_SEPARATE_SETTLEMENT")
    def test_wrong_synchronizer_is_rejected_even_when_obligation_matches(self):
        bad=IntervalReport("r0",self.expected[0].interval_id,self.expected[0].start,self.expected[0].end,
            self.expected[0].end,"OK",agreement_version="v1",consumed_units=10,
            obligation_id="o1",synchronizer_id="sync-B")
        c=case(("r0",),10,10,(alloc(10),))
        out=reconcile_with_interval_coverage(c,(self.expected[0],),(bad,),pricing_agreements={"v1":tariff()})
        self.assertEqual(out["payment_state"],"BLOCKED_REPORT_BINDING")
if __name__=="__main__": unittest.main()
