"""Explicit separation of protocol traffic reports and off-ledger settlement bindings.

The protocol record contains interval/status/aggregate-byte evidence only.
Commercial identity and tariff metadata live in SettlementBinding.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Mapping

from interval_coverage import IntervalReport
from integrated_interval_reconciliation import reconcile_with_interval_coverage
from agreement_verification import verify_signed_agreement


@dataclass(frozen=True)
class ProtocolTrafficReport:
    report_id: str
    interval_id: str
    start: datetime
    end: datetime
    received_at: datetime
    status: str
    traffic_consumed_bytes: int | None
    revision: int = 0
    supersedes_report_id: str | None = None


@dataclass(frozen=True)
class SettlementBinding:
    binding_id: str
    interval_id: str
    synchronizer_id: str
    obligation_id: str
    agreement_version: str
    authority_reference: str
    signer_key_id: str
    signature_b64: str


def reconcile_protocol_evidence(
    case,
    expected_intervals,
    protocol_reports: Iterable[ProtocolTrafficReport],
    settlement_bindings: Iterable[SettlementBinding],
    pricing_agreements: Mapping,
    prior_settlements=(),
    allow_late_reports=False,
    trusted_signers=None,
):
    """Join protocol evidence to separately authorised commercial bindings.

    Current model cardinality: exactly one binding per expected interval.
    This is an explicit synthetic constraint, not a CIP-0132 guarantee.
    """
    protocol_reports = tuple(protocol_reports)
    bindings = tuple(settlement_bindings)
    expected_by_id = {x.interval_id: x for x in expected_intervals}
    expected_ids = set(expected_by_id)
    if trusted_signers is None:
        return _blocked('TRUSTED_SIGNER_REGISTRY_REQUIRED')

    binding_ids = [x.binding_id for x in bindings]
    if len(binding_ids) != len(set(binding_ids)):
        return _blocked("DUPLICATE_BINDING_ID")
    by_interval = {}
    for binding in bindings:
        if binding.interval_id not in expected_ids:
            return _blocked("UNEXPECTED_BINDING_INTERVAL")
        if not all((binding.synchronizer_id, binding.obligation_id,
                    binding.agreement_version, binding.authority_reference)):
            return _blocked("INCOMPLETE_SETTLEMENT_BINDING")
        if binding.interval_id in by_interval:
            return _blocked("AMBIGUOUS_INTERVAL_BINDING")
        pricing = pricing_agreements.get(binding.agreement_version)
        if pricing is None:
            return _blocked("UNKNOWN_PRICING_AGREEMENT_VERSION")
        if pricing.version_id != binding.agreement_version or pricing.agreement_id != binding.obligation_id:
            return _blocked("AGREEMENT_BINDING_MISMATCH")
        signed_document = {
            "agreement_id": pricing.agreement_id,
            "version": pricing.version_id,
            "effective_from": pricing.effective_from,
            "effective_until": pricing.effective_until,
            "bands": [
                {"upper_units_exclusive": band.upper_units_exclusive,
                 "price_cc_per_unit": band.price_cc_per_unit}
                for band in pricing.bands
            ],
            "fixed_fee_cc": pricing.fixed_fee_cc,
            "discount_basis_points": pricing.discount_basis_points,
            "rounding": pricing.rounding,
        }
        verification = verify_signed_agreement(
            signed_document, binding.signature_b64, binding.signer_key_id,
            trusted_signers, expected_by_id[binding.interval_id].end,
        )
        if not verification["verified"]:
            return _blocked("AGREEMENT_SIGNATURE_" + verification["reason"])
        by_interval[binding.interval_id] = binding

    reports_by_interval = {}
    for report in protocol_reports:
        if report.interval_id not in expected_ids:
            return _blocked("UNEXPECTED_REPORT_INTERVAL")
        reports_by_interval.setdefault(report.interval_id, []).append(report)

    # Missing bindings are not treated as zero or as valid payment evidence.
    for interval_id, versions in reports_by_interval.items():
        if interval_id not in by_interval:
            return _blocked("MISSING_SETTLEMENT_BINDING")
        binding = by_interval[interval_id]
        for report in versions:
            if report.status == "OK":
                if not isinstance(report.traffic_consumed_bytes, int) or report.traffic_consumed_bytes < 0:
                    return _blocked("INVALID_TRAFFIC_BYTE_COUNT")
            elif report.traffic_consumed_bytes is not None:
                return _blocked("NON_OK_REPORT_MUST_NOT_CARRY_CHARGEABLE_BYTES")

    # A binding is required for every expected interval in this version of
    # the model, even when the report is missing, so absence is distinguishable
    # from a deliberately unbound interval.
    if set(by_interval) != expected_ids:
        return _blocked("INCOMPLETE_BINDING_COVERAGE")

    linked_reports = []
    for report in protocol_reports:
        binding = by_interval[report.interval_id]
        linked_reports.append(IntervalReport(
            report_id=report.report_id,
            interval_id=report.interval_id,
            start=report.start,
            end=report.end,
            received_at=report.received_at,
            status=report.status,
            revision=report.revision,
            supersedes_report_id=report.supersedes_report_id,
            agreement_version=binding.agreement_version,
            consumed_units=report.traffic_consumed_bytes,
            obligation_id=binding.obligation_id,
            synchronizer_id=binding.synchronizer_id,
        ))

    return reconcile_with_interval_coverage(
        case, expected_intervals, linked_reports, prior_settlements,
        allow_late_reports, pricing_agreements,
    )


def _blocked(reason):
    coverage = {"state": "INVALID", "reason": reason}
    return {
        "coverage": coverage,
        "payment_state": "BLOCKED_SETTLEMENT_BINDING",
        "overall_state": "BLOCKED_SETTLEMENT_BINDING",
        "adjustments": [],
    }
