import unittest
import base64
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from agreement_verification import canonical_agreement_bytes
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
        self.private=Ed25519PrivateKey.generate()
        public=self.private.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,format=serialization.PublicFormat.Raw)
        self.trusted={"key-1":{"public_key_b64":base64.b64encode(public).decode(),
            "authorised":True,"valid_from":"2026-01-01T00:00:00+00:00",
            "valid_until":"2027-01-01T00:00:00+00:00"}}
        self.signed_document={"agreement_id":"agreement-A","version":"v1",
            "effective_from":"2026-11-01T00:00:00+00:00","effective_until":None,
            "bands":[{"upper_units_exclusive":None,"price_cc_per_unit":1}],
            "fixed_fee_cc":0,"discount_basis_points":0,"rounding":"CEILING"}
        signature=base64.b64encode(self.private.sign(canonical_agreement_bytes(self.signed_document))).decode()
        self.binding=SettlementBinding("b0",self.expected[0].interval_id,"sync-A","o1","agreement-A","v1","agreement-authority:doc-1","key-1",signature)
    def run_case(self,reports=None,bindings=None):
        return reconcile_protocol_evidence(make_case(),self.expected,
            (self.report,) if reports is None else reports,
            (self.binding,) if bindings is None else bindings,
            {"v1":agreement()},trusted_signers=self.trusted)
    def test_separate_protocol_and_binding_reconcile(self):
        out=self.run_case()
        self.assertEqual(out["payment_state"],"RECONCILED")
        self.assertEqual(out["pricing_results"]["r0"]["consumed_units"],10)
    def test_missing_binding_blocks(self):
        out=self.run_case(bindings=())
        self.assertEqual(out["payment_state"],"BLOCKED_SETTLEMENT_BINDING")
        self.assertEqual(out["coverage"]["reason"],"MISSING_SETTLEMENT_BINDING")
    def test_ambiguous_multiple_bindings_block(self):
        second=SettlementBinding("b1",self.expected[0].interval_id,"sync-A","o1","agreement-A","v1","authority:2","key-1",self.binding.signature_b64)
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

    def test_invalid_signature_blocks_settlement(self):
        bad=SettlementBinding(self.binding.binding_id,self.binding.interval_id,
            self.binding.synchronizer_id,self.binding.obligation_id,self.binding.agreement_id,self.binding.agreement_version,
            self.binding.authority_reference,self.binding.signer_key_id,"AAAA")
        out=self.run_case(bindings=(bad,))
        self.assertEqual(out["payment_state"],"BLOCKED_SETTLEMENT_BINDING")
        self.assertEqual(out["coverage"]["reason"],"AGREEMENT_SIGNATURE_INVALID_SIGNATURE")
    def test_unknown_signer_blocks_settlement(self):
        bad=SettlementBinding(self.binding.binding_id,self.binding.interval_id,
            self.binding.synchronizer_id,self.binding.obligation_id,self.binding.agreement_id,self.binding.agreement_version,
            self.binding.authority_reference,"unknown",self.binding.signature_b64)
        out=self.run_case(bindings=(bad,))
        self.assertEqual(out["coverage"]["reason"],"AGREEMENT_SIGNATURE_UNKNOWN_SIGNER_KEY")
    def test_revoked_signer_blocks_settlement(self):
        registry={**self.trusted,"key-1":{**self.trusted["key-1"],
            "revoked_at":"2026-11-17T12:05:00+00:00"}}
        out=reconcile_protocol_evidence(make_case(),self.expected,(self.report,),
            (self.binding,),{"v1":agreement()},trusted_signers=registry)
        self.assertEqual(out["coverage"]["reason"],"AGREEMENT_SIGNATURE_SIGNER_KEY_REVOKED")
    def test_missing_registry_blocks_settlement(self):
        out=reconcile_protocol_evidence(make_case(),self.expected,
            (self.report,),(self.binding,),{"v1":agreement()})
        self.assertEqual(out["coverage"]["reason"],"TRUSTED_SIGNER_REGISTRY_REQUIRED")

if __name__=="__main__": unittest.main()
