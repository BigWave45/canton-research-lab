import unittest
from datetime import datetime,timedelta,timezone
from protocol_settlement_interface import (
    ProtocolTrafficReport,SettlementBinding,reconcile_protocol_evidence
)
from interval_coverage import build_expected_intervals
from pricing_liability import PriceBand,PricingAgreement
from reconciliation_state_machine import Allocation,Burn,Case,Obligation,Report

UTC=timezone.utc
START=datetime(2026,11,17,12,0,tzinfo=UTC)
END=START+timedelta(minutes=10)

def agreement():
    return PricingAgreement("agreement-A","v1","2026-11-01T00:00:00+00:00",None,(PriceBand(None,1),))

def make_case(due=10):
    return Case(("r0",),(Report("r0","OK","v1","o1","sync-A"),),
        (Obligation("o1",due,"v1",synchronizer_id="sync-A"),),
        (Burn("burn-1",10),),(Allocation("alloc-1","burn-1","o1",10),),
        "2026-11-17T12:10:00+00:00",reward_required=False)

class ProtocolSettlementSeparationTests(unittest.TestCase):
    def setUp(self):
        self.expected=build_expected_intervals(START,END,timedelta(minutes=10),timedelta(minutes=5))
        self.report=ProtocolTrafficReport("r0",self.expected[0].interval_id,START,END,END,"OK",10)
        self.binding=SettlementBinding("b0",self.expected[0].interval_id,"sync-A","o1","v1","agreement-authority:doc-1")
    def run_case(self,reports=None,bindings=None):
        return reconcile_protocol_evidence(make_case(),self.expected,
            (self.report,) if reports is None else reports,
            (self.binding,) if bindings is None else bindings,
            {"v1":agreement()})
    def test_separate_protocol_and_binding_reconcile(self):
        out=self.run_case()
        self.assertEqual(out["payment_state"],"RECONCILED")
        self.assertEqual(out["pricing_results"]["r0"]["consumed_units"],10)
    def test_missing_binding_blocks(self):
        out=self.run_case(bindings=())
        self.assertEqual(out["payment_state"],"BLOCKED_SETTLEMENT_BINDING")
        self.assertEqual(out["coverage"]["reason"],"INCOMPLETE_BINDING_COVERAGE")
    def test_ambiguous_multiple_bindings_block(self):
        second=SettlementBinding("b1",self.expected[0].interval_id,"sync-A","o2","v1","authority:2")
        out=self.run_case(bindings=(self.binding,second))
        self.assertEqual(out["coverage"]["reason"],"AMBIGUOUS_INTERVAL_BINDING")
    def test_non_ok_report_cannot_claim_chargeable_bytes(self):
        bad=ProtocolTrafficReport("r0",self.expected[0].interval_id,START,END,END,"UNDETERMINED",10)
        out=self.run_case(reports=(bad,))
        self.assertEqual(out["coverage"]["reason"],"NON_OK_REPORT_MUST_NOT_CARRY_CHARGEABLE_BYTES")
    def test_ok_report_requires_nonnegative_integer_bytes(self):
        bad=ProtocolTrafficReport("r0",self.expected[0].interval_id,START,END,END,"OK",None)
        out=self.run_case(reports=(bad,))
        self.assertEqual(out["coverage"]["reason"],"INVALID_TRAFFIC_BYTE_COUNT")
if __name__=="__main__": unittest.main()
