import base64
import unittest
from datetime import datetime,timezone
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from agreement_verification import agreement_digest,verify_signed_agreement,canonical_agreement_bytes

NOW="2026-11-17T12:00:00+00:00"
class AgreementVerificationTests(unittest.TestCase):
    def setUp(self):
        self.private=Ed25519PrivateKey.generate()
        public=self.private.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
        self.registry={"sv-key-1":{
            "public_key_b64":base64.b64encode(public).decode(),
            "authorised":True,
            "valid_from":"2026-01-01T00:00:00+00:00",
            "valid_until":"2027-01-01T00:00:00+00:00",
        }}
        self.document={
            "agreement_id":"agreement-A","version":"v2",
            "effective_from":"2026-11-01T00:00:00+00:00",
            "effective_until":None,"price_per_unit_cc":1,
            "smoothing_days":7,
        }
        self.signature=base64.b64encode(
            self.private.sign(canonical_agreement_bytes(self.document))
        ).decode()
    def verify(self,document=None,signature=None,key="sv-key-1",registry=None,when=NOW):
        return verify_signed_agreement(
            self.document if document is None else document,
            self.signature if signature is None else signature,
            key,self.registry if registry is None else registry,when,
        )
    def test_valid_authorised_signature(self):
        result=self.verify()
        self.assertTrue(result["verified"])
        self.assertEqual(result["agreement_sha256"],agreement_digest(self.document))
    def test_modified_agreement_rejected(self):
        changed={**self.document,"price_per_unit_cc":2}
        self.assertEqual(self.verify(document=changed)["reason"],"INVALID_SIGNATURE")
    def test_unknown_key_rejected(self):
        self.assertEqual(self.verify(key="unknown")["reason"],"UNKNOWN_SIGNER_KEY")
    def test_unauthorised_key_rejected(self):
        registry={**self.registry,"sv-key-1":{**self.registry["sv-key-1"],"authorised":False}}
        self.assertEqual(self.verify(registry=registry)["reason"],"SIGNER_NOT_AUTHORISED")
    def test_revoked_key_rejected_after_revocation(self):
        registry={**self.registry,"sv-key-1":{**self.registry["sv-key-1"],"revoked_at":"2026-11-01T00:00:00+00:00"}}
        self.assertEqual(self.verify(registry=registry)["reason"],"SIGNER_KEY_REVOKED")
    def test_expired_key_rejected(self):
        registry={**self.registry,"sv-key-1":{**self.registry["sv-key-1"],"valid_until":"2026-11-01T00:00:00+00:00"}}
        self.assertEqual(self.verify(registry=registry)["reason"],"SIGNER_KEY_EXPIRED")
    def test_naive_verification_time_rejected(self):
        self.assertEqual(self.verify(when="2026-11-17T12:00:00")["reason"],"INVALID_VERIFICATION_TIME")
if __name__=="__main__": unittest.main()
