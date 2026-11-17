import unittest
from datetime import datetime,timedelta,timezone
from interval_coverage import IntervalReport,build_expected_intervals
from pricing_liability import PriceBand,PricingAgreement
from reconciliation_state_machine import Allocation,Burn,Case,Obligation,Report
from integrated_interval_reconciliation import PriorSettlement,reconcile_with_interval_coverage
UTC=timezone.utc
START=datetime(2026,11,17,12,0,tzinfo=UTC)
END=START+timedelta(minutes=10)
def make_case():
    return Case(("r0",),(Report("r0","OK","v1","o1","sync-A"),),
        (Obligation("o1",10,"v1",synchronizer_id="sync-A"),),
        (Burn("burn-1",10),),(Allocation("alloc-1","burn-1","o1",10),),
        "2026-11-17T12:10:00+00:00",reward_required=False)
def tariff():
    return PricingAgreement("agreement-A","v1","2026-11-01T00:00:00+00:00",
        None,(PriceBand(None,1),))
class PricingCorrectionIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.expected=build_expected_intervals(START,END,timedelta(minutes=10),timedelta(minutes=5))
        self.original=IntervalReport("r0",self.expected[0].interval_id,START,END,END,"OK",
            agreement_version="v1",consumed_units=10,obligation_id="o1",synchronizer_id="sync-A")
        self.prior=(PriorSettlement("settle-1",self.expected[0].interval_id,"r0",10),)
    def test_original_report_is_priced_and_reconciles(self):
        out=reconcile_with_interval_coverage(make_case(),self.expected,(self.original,),
            pricing_agreements={"v1":tariff()})
        self.assertEqual(out["pricing_results"]["r0"]["liability_cc"],10)
        self.assertEqual(out["payment_state"],"RECONCILED")
    def test_upward_correction_reprices_and_creates_adjustment(self):
        corrected=IntervalReport("r1",self.expected[0].interval_id,START,END,END+timedelta(minutes=2),"OK",
            revision=1,supersedes_report_id="r0",agreement_version="v1",consumed_units=12,
            obligation_id="o1",synchronizer_id="sync-A")
        out=reconcile_with_interval_coverage(make_case(),self.expected,(self.original,corrected),self.prior,
            pricing_agreements={"v1":tariff()})
        self.assertEqual(out["pricing_results"]["r1"]["liability_cc"],12)
        self.assertEqual(out["adjustments"][0]["adjustment_cc"],2)
        self.assertEqual(out["adjustments"][0]["status"],"REQUIRES_SEPARATE_SETTLEMENT")
        self.assertEqual(out["payment_state"],"SHORT_PAID")
    def test_wrong_synchronizer_binding_blocks_pricing(self):
        bad=IntervalReport("r0",self.expected[0].interval_id,START,END,END,"OK",
            agreement_version="v1",consumed_units=10,obligation_id="o1",synchronizer_id="sync-B")
        out=reconcile_with_interval_coverage(make_case(),self.expected,(bad,),
            pricing_agreements={"v1":tariff()})
        self.assertEqual(out["payment_state"],"BLOCKED_REPORT_BINDING")
if __name__=="__main__": unittest.main()
