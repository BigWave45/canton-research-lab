"""Ed25519 verification for off-ledger commercial agreement records.

This verifies document integrity and a signature against a separately trusted
key registry. It does not establish legal authority unless that registry is
itself governed and authenticated outside this module.
"""
import base64
import hashlib
import json
from datetime import datetime


def canonical_agreement_bytes(document):
    if not isinstance(document, dict) or not document:
        raise ValueError("Agreement document must be a non-empty object")
    try:
        return json.dumps(
            document, sort_keys=True, separators=(",", ":"),
            ensure_ascii=False, allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ValueError("Agreement document must contain canonical JSON values") from exc


def agreement_digest(document):
    return hashlib.sha256(canonical_agreement_bytes(document)).hexdigest()


def verify_signed_agreement(
    document, signature_b64, signer_key_id, trusted_signers, verification_time,
):
    """Return a structured verification result; never silently trust unknown keys."""
    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    except ImportError as exc:
        raise RuntimeError(
            "Install the cryptography package to verify Ed25519 signatures"
        ) from exc

    try:
        when = _parse_time(verification_time)
    except (TypeError, ValueError):
        return _fail("INVALID_VERIFICATION_TIME")

    signer = trusted_signers.get(signer_key_id)
    if signer is None:
        return _fail("UNKNOWN_SIGNER_KEY")
    if signer.get("authorised") is not True:
        return _fail("SIGNER_NOT_AUTHORISED")
    if signer.get("revoked_at"):
        revoked = _parse_time(signer["revoked_at"])
        if when >= revoked:
            return _fail("SIGNER_KEY_REVOKED")

    if signer.get("valid_from") and when < _parse_time(signer["valid_from"]):
        return _fail("SIGNER_KEY_NOT_YET_VALID")
    if signer.get("valid_until") and when > _parse_time(signer["valid_until"]):
        return _fail("SIGNER_KEY_EXPIRED")

    try:
        public_key = Ed25519PublicKey.from_public_bytes(
            base64.b64decode(signer["public_key_b64"], validate=True)
        )
        signature = base64.b64decode(signature_b64, validate=True)
        payload = canonical_agreement_bytes(document)
    except (KeyError, TypeError, ValueError):
        return _fail("MALFORMED_KEY_SIGNATURE_OR_DOCUMENT")

    try:
        public_key.verify(signature, payload)
    except InvalidSignature:
        return _fail("INVALID_SIGNATURE")

    return {
        "verified": True,
        "reason": "SIGNATURE_VALID",
        "agreement_sha256": hashlib.sha256(payload).hexdigest(),
        "signer_key_id": signer_key_id,
    }


def _parse_time(value):
    if isinstance(value, datetime):
        result = value
    elif isinstance(value, str):
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    else:
        raise ValueError("Timestamp must be a datetime or ISO-8601 string")
    if result.tzinfo is None or result.utcoffset() is None:
        raise ValueError("Timestamp must be timezone-aware")
    return result


def _fail(reason):
    return {"verified": False, "reason": reason}
