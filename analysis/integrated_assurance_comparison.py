"""Integrated qualitative comparison of accounting-assurance architectures.

Ratings are analytical judgments, not measured performance or probabilities.
"""
ARCHITECTURES = {
    "public_burn_only": {
        "measurement_assurance": "none",
        "payment_completeness": "none",
        "allocation_assurance": "none",
        "reward_attribution": "none_without_external_mapping",
        "public_disclosure": "low",
        "auditor_disclosure": "none_required_in_this_tier",
        "residual_trust": "operator_measurement_and_off_ledger_agreement",
        "implementation_burden": "low",
        "latency": "low_incremental_latency",
        "dispute_resolution": "weak",
    },
    "signed_reconciliation": {
        "measurement_assurance": "limited_to_provenance_and_internal_consistency",
        "payment_completeness": "checkable_if_agreement_and_due_schedule_are_authoritative",
        "allocation_assurance": "checkable_from_manifest_and_burn_reference",
        "reward_attribution": "checkable_if_reward_mapping_is_included",
        "public_disclosure": "low_if_manifest_details_are_restricted",
        "auditor_disclosure": "high",
        "residual_trust": "source_meter_operator_and_auditor_independence",
        "implementation_burden": "medium",
        "latency": "low_to_medium",
        "dispute_resolution": "moderate_with_retained_evidence",
    },
    "independent_confidential_audit": {
        "measurement_assurance": "stronger_if_source_records_are_complete_and_independent",
        "payment_completeness": "strong_if_agreement_due_dates_and_burns_are_reconciled",
        "allocation_assurance": "strong_if_all_obligations_and_burns_are_in_scope",
        "reward_attribution": "strong_if_reward_rules_and_inputs_are_audited",
        "public_disclosure": "low_if_only_attestation_is_published",
        "auditor_disclosure": "very_high",
        "residual_trust": "auditor_competence_independence_and_source_record_integrity",
        "implementation_burden": "medium_to_high",
        "latency": "medium_or_high_due_to_review_cycle",
        "dispute_resolution": "stronger_with_workpapers_and_appeal_process",
    },
    "cryptographic_proof": {
        "measurement_assurance": "none_for_source_completeness_without_trusted_measurement",
        "payment_completeness": "strong_for_encoded_rules_over_committed_inputs",
        "allocation_assurance": "strong_for_encoded_uniqueness_and_sum_constraints",
        "reward_attribution": "strong_for_encoded_reward_formula_over_committed_inputs",
        "public_disclosure": "low_to_medium_depending_on_outputs_and_metadata",
        "auditor_disclosure": "medium_to_high_for_circuit_and_input_validation",
        "residual_trust": "input_completeness_key_security_circuit_correctness_and_governance",
        "implementation_burden": "high",
        "latency": "medium_to_high_until_benchmarked",
        "dispute_resolution": "moderate_for_proved_predicates_external_for_input_truth",
    },
}
DIMENSIONS = tuple(next(iter(ARCHITECTURES.values())).keys())


def validate_matrix() -> dict:
    expected = set(DIMENSIONS)
    mismatches = {
        name: sorted(expected - set(values) | set(values) - expected)
        for name, values in ARCHITECTURES.items()
        if set(values) != expected
    }
    return {
        "architecture_count": len(ARCHITECTURES),
        "dimension_count": len(DIMENSIONS),
        "valid": not mismatches,
        "mismatches": mismatches,
    }


def get_assessment(architecture: str, dimension: str) -> str:
    if architecture not in ARCHITECTURES:
        raise KeyError(f"Unknown architecture: {architecture}")
    if dimension not in DIMENSIONS:
        raise KeyError(f"Unknown dimension: {dimension}")
    return ARCHITECTURES[architecture][dimension]


if __name__ == "__main__":
    print(validate_matrix())
    for name, assessment in ARCHITECTURES.items():
        print(name, assessment)
