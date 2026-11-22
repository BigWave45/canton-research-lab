import unittest
import base64
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from agreement_verification import canonical_agreement_bytes
from datetime import datetime,timedelta,timezone
from protocol_settlement_interface import (
    ProtocolTrafficReport,SettlementBinding,reconcile_protocol_evidence,
    protocol_report_set_digest,canonical_binding_document,
)
from interval_coverage import build_expected_intervals
from pricing_liability import PriceBand,PricingAgreement
from reconciliation_state_machine import Allocation,Burn,Case,Obligation,Report
from integrated_interval_reconciliation import PriorSettlement

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
        self.agreement_private=Ed25519PrivateKey.generate()
        agreement_public=self.agreement_private.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,format=serialization.PublicFormat.Raw)
        self.binding_private=Ed25519PrivateKey.generate()
        binding_public=self.binding_private.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,format=serialization.PublicFormat.Raw)
        self.trusted={
            "key-agreement":{"public_key_b64":base64.b64encode(agreement_public).decode(),
            "authorised":True,"roles":["agreement"],
            "valid_from":"2026-01-01T00:00:00+00:00",
            "valid_until":"2027-01-01T00:00:00+00:00"},
            "key-binding":{"public_key_b64":base64.b64encode(binding_public).decode(),
            "authorised":True,"roles":["settlement_binding"],
            "valid_from":"2026-01-01T00:00:00+00:00",
            "valid_until":"2027-01-01T00:00:00+00:00"}}
        self.signed_document={"agreement_id":"agreement-A","version":"v1",
            "effective_from":"2026-11-01T00:00:00+00:00","effective_until":None,
            "bands":[{"upper_units_exclusive":None,"price_cc_per_unit":1}],
            "fixed_fee_cc":0,"discount_basis_points":0,"rounding":"CEILING"}
        signature=base64.b64encode(self.agreement_private.sign(canonical_agreement_bytes(self.signed_document))).decode()
        unsigned=SettlementBinding("b0",self.expected[0].interval_id,"sync-A","o1","agreement-A","v1",
            "agreement-authority:doc-1","key-agreement",signature,
            protocol_report_set_digest((self.report,)),"","key-binding","paymaster-A")
        binding_signature=base64.b64encode(self.binding_private.sign(canonical_agreement_bytes(
            canonical_binding_document(unsigned)))).decode()
        self.binding=SettlementBinding(unsigned.binding_id,unsigned.interval_id,unsigned.synchronizer_id,
            unsigned.obligation_id,unsigned.agreement_id,unsigned.agreement_version,
            unsigned.authority_reference,unsigned.signer_key_id,unsigned.signature_b64,
            unsigned.report_set_digest,binding_signature,unsigned.binding_signer_key_id,
            unsigned.paymaster_id)
    def run_case(self,reports=None,bindings=None,registry=None,pricing_agreements=None,
                 prior_settlements=()):
        return reconcile_protocol_evidence(make_case(),self.expected,
            (self.report,) if reports is None else reports,
            (self.binding,) if bindings is None else bindings,
            {"v1":agreement()} if pricing_agreements is None else pricing_agreements,
            prior_settlements=prior_settlements,
            trusted_signers=self.trusted if registry is None else registry)
    def binding_for(self, reports):
        digest=protocol_report_set_digest(reports)
        unsigned=SettlementBinding("b0",self.expected[0].interval_id,"sync-A","o1","agreement-A","v1",
            "agreement-authority:doc-1","key-agreement",self.binding.signature_b64,digest,"","key-binding",
            "paymaster-A")
        signature=base64.b64encode(self.binding_private.sign(canonical_agreement_bytes(
            canonical_binding_document(unsigned)))).decode()
        return SettlementBinding(unsigned.binding_id,unsigned.interval_id,unsigned.synchronizer_id,
            unsigned.obligation_id,unsigned.agreement_id,unsigned.agreement_version,
            unsigned.authority_reference,unsigned.signer_key_id,unsigned.signature_b64,
            digest,signature,unsigned.binding_signer_key_id,unsigned.paymaster_id)
    def altered_binding(self, **changes):
        values={name:getattr(self.binding,name) for name in self.binding.__dataclass_fields__}
        values.update(changes)
        return SettlementBinding(**values)
    def test_valid_separate_agreement_and_binding_attestations_reconcile(self):
        out=self.run_case()
        self.assertEqual(out["payment_state"],"RECONCILED")
        self.assertEqual(out["pricing_results"]["r0"]["consumed_units"],10)
    def test_authority_reference_tampering_blocks(self):
        out=self.run_case(bindings=(self.altered_binding(authority_reference="attacker-ref"),))
        self.assertEqual(out["coverage"]["reason"],"SETTLEMENT_BINDING_SIGNATURE_INVALID_SIGNATURE")
    def test_correction_cannot_change_prior_authority_reference(self):
        correction=ProtocolTrafficReport(
            "r1",self.report.interval_id,START,END,END+timedelta(minutes=1),"OK",11,1,"r0"
        )
        reports=(self.report,correction)
        changed=self.altered_binding(
            authority_reference="replacement-authority",
            report_set_digest=protocol_report_set_digest(reports),
        )
        signature=base64.b64encode(self.binding_private.sign(canonical_agreement_bytes(
            canonical_binding_document(changed)))).decode()
        changed=self.altered_binding(
            authority_reference="replacement-authority",
            report_set_digest=protocol_report_set_digest(reports),
            binding_signature_b64=signature
        )
        prior=(PriorSettlement("settle-1",self.expected[0].interval_id,"r0",10,
                               authority_reference="agreement-authority:doc-1",
                               paymaster_id="paymaster-A"),)
        out=self.run_case(reports=reports,bindings=(changed,),prior_settlements=prior)
        self.assertEqual(out["coverage"]["reason"],"CORRECTION_AUTHORITY_CHANGED")
    def test_correction_cannot_change_prior_paymaster(self):
        correction=ProtocolTrafficReport(
            "r1",self.report.interval_id,START,END,END+timedelta(minutes=1),"OK",11,1,"r0"
        )
        reports=(self.report,correction)
        changed=self.altered_binding(
            paymaster_id="paymaster-B",report_set_digest=protocol_report_set_digest(reports)
        )
        signature=base64.b64encode(self.binding_private.sign(canonical_agreement_bytes(
            canonical_binding_document(changed)))).decode()
        changed=self.altered_binding(
            paymaster_id="paymaster-B",report_set_digest=protocol_report_set_digest(reports),
            binding_signature_b64=signature
        )
        prior=(PriorSettlement("settle-1",self.expected[0].interval_id,"r0",10,
                               paymaster_id="paymaster-A"),)
        out=self.run_case(reports=reports,bindings=(changed,),prior_settlements=prior)
        self.assertEqual(out["coverage"]["reason"],"CORRECTION_BINDING_CHANGED")
    def test_obligation_tampering_blocks(self):
        out=self.run_case(bindings=(self.altered_binding(obligation_id="other-obligation"),))
        self.assertEqual(out["coverage"]["reason"],"SETTLEMENT_BINDING_SIGNATURE_INVALID_SIGNATURE")
    def test_synchronizer_tampering_blocks(self):
        out=self.run_case(bindings=(self.altered_binding(synchronizer_id="other-sync"),))
        self.assertEqual(out["coverage"]["reason"],"SETTLEMENT_BINDING_SIGNATURE_INVALID_SIGNATURE")
    def test_agreement_version_tampering_blocks(self):
        pricing_agreements={
            "v1":agreement(),
            "v2":PricingAgreement("agreement-B","v2","2026-11-01T00:00:00+00:00",None,(PriceBand(None,1),)),
        }
        out=self.run_case(
            bindings=(self.altered_binding(agreement_version="v2"),),
            pricing_agreements=pricing_agreements,
        )
        self.assertEqual(out["coverage"]["reason"],"AGREEMENT_BINDING_MISMATCH")
    def test_report_digest_substitution_blocks(self):
        out=self.run_case(bindings=(self.altered_binding(report_set_digest="0"*64),))
        self.assertEqual(out["coverage"]["reason"],"SETTLEMENT_BINDING_REPORT_DIGEST_MISMATCH")
    def test_report_content_tampering_blocks(self):
        altered=ProtocolTrafficReport("r0",self.report.interval_id,START,END,END,"OK",11)
        out=self.run_case(reports=(altered,))
        self.assertEqual(out["coverage"]["reason"],"SETTLEMENT_BINDING_REPORT_DIGEST_MISMATCH")
    def test_missing_binding_attestation_blocks(self):
        out=self.run_case(bindings=(self.altered_binding(binding_signature_b64=""),))
        self.assertEqual(out["coverage"]["reason"],"SETTLEMENT_BINDING_ATTESTATION_REQUIRED")
    def test_invalid_binding_signature_blocks(self):
        out=self.run_case(bindings=(self.altered_binding(binding_signature_b64="AAAA"),))
        self.assertEqual(out["coverage"]["reason"],"SETTLEMENT_BINDING_SIGNATURE_INVALID_SIGNATURE")
    def test_unknown_binding_signer_blocks(self):
        out=self.run_case(bindings=(self.altered_binding(binding_signer_key_id="unknown"),))
        self.assertEqual(out["coverage"]["reason"],"SETTLEMENT_BINDING_SIGNATURE_UNKNOWN_SIGNER_KEY")
    def test_legacy_binding_without_binding_signer_is_rejected(self):
        legacy=SettlementBinding(
            self.binding.binding_id,self.binding.interval_id,self.binding.synchronizer_id,
            self.binding.obligation_id,self.binding.agreement_id,self.binding.agreement_version,
            self.binding.authority_reference,self.binding.signer_key_id,self.binding.signature_b64,
            self.binding.report_set_digest,self.binding.binding_signature_b64,"",
            self.binding.paymaster_id,
        )
        registry={
            "key-agreement":{
                **self.trusted["key-agreement"],
                "roles":["agreement","settlement_binding"],
            },
            "key-binding":self.trusted["key-binding"],
        }
        out=self.run_case(bindings=(legacy,),registry=registry)
        self.assertEqual(out["coverage"]["reason"],"SETTLEMENT_BINDING_SIGNER_ID_MISSING")
    def test_signer_without_binding_role_blocks(self):
        registry={
            "key-agreement":self.trusted["key-agreement"],
            "key-binding":{**self.trusted["key-binding"],"roles":["agreement"]},
        }
        out=self.run_case(registry=registry)
        self.assertEqual(out["coverage"]["reason"],"SETTLEMENT_BINDING_SIGNATURE_SIGNER_ROLE_NOT_AUTHORISED")
    def test_revoked_binding_signer_blocks(self):
        registry={
            "key-agreement":self.trusted["key-agreement"],
            "key-binding":{**self.trusted["key-binding"],"revoked_at":"2026-11-17T12:05:00+00:00"},
        }
        out=self.run_case(registry=registry)
        self.assertEqual(out["coverage"]["reason"],"SETTLEMENT_BINDING_SIGNATURE_SIGNER_KEY_REVOKED")
    def test_duplicate_binding_id_blocks(self):
        out=self.run_case(bindings=(self.binding,self.binding))
        self.assertEqual(out["coverage"]["reason"],"DUPLICATE_BINDING_ID")
    def test_missing_binding_blocks(self):
        out=self.run_case(bindings=())
        self.assertEqual(out["payment_state"],"BLOCKED_SETTLEMENT_BINDING")
        self.assertEqual(out["coverage"]["reason"],"MISSING_SETTLEMENT_BINDING")
    def test_ambiguous_multiple_bindings_block(self):
        second=self.altered_binding(binding_id="b1")
        out=self.run_case(bindings=(self.binding,second))
        self.assertEqual(out["coverage"]["reason"],"AMBIGUOUS_INTERVAL_BINDING")
    def test_non_ok_report_cannot_claim_chargeable_bytes(self):
        bad=ProtocolTrafficReport("r0",self.expected[0].interval_id,START,END,END,"UNDETERMINED",10)
        # Binding is also rebuilt for this exact report so the status invariant is tested independently.
        out=self.run_case(reports=(bad,),bindings=(self.binding_for((bad,)),))
        self.assertEqual(out["coverage"]["reason"],"NON_OK_REPORT_MUST_NOT_CARRY_CHARGEABLE_BYTES")
    def test_ok_report_requires_nonnegative_integer_bytes(self):
        bad=ProtocolTrafficReport("r0",self.expected[0].interval_id,START,END,END,"OK",None)
        out=self.run_case(reports=(bad,),bindings=(self.binding_for((bad,)),))
        self.assertEqual(out["coverage"]["reason"],"INVALID_TRAFFIC_BYTE_COUNT")

if __name__=="__main__": unittest.main()
