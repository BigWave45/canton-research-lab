# Comparative Assurance Experiment: Agreement Versions and Payment Smoothing

**Status:** Synthetic model extension; not an empirical study of Canton traffic or paymaster behaviour.  
**Model:** `analysis/comparative_assurance_model.py`  
**Tests:** `tests/test_comparative_assurance_model.py`

## Purpose

This extension adds agreement-version mismatch and due-date-aware payment smoothing to the first three scenarios. It tests whether reconciliation uses the authoritative contract version and whether it distinguishes a payment that is late from one that is simply not yet due.

## New assumptions

- The applicable agreement version for each interval is available to the authorised verifier through an authoritative, versioned agreement record.
- The applied version is included in the settlement evidence.
- The evaluation timestamp and contractual due schedule are known.
- Burn allocations are attributed to the obligation being evaluated; portfolio-wide allocation and double-claim checks are a later scenario.
- Independent audit can inspect the executed agreement and relevant source records.
- A cryptographic proof binds the authoritative agreement version, applied version, liability calculation, due schedule and burn allocation. It cannot establish that a submitted agreement is legally authoritative unless the authority and version registry are separately trusted.
- All figures are synthetic.

## New scenario inputs

| Scenario | Liability under applicable terms | Applied version | Burn | Amount due now |
|---|---:|---|---:|---:|
| Agreement-version mismatch | 10 CC | v1 instead of v2 | 8 CC | 10 CC |
| Smoothing, instalment not yet due | 10 CC | v2 | 4 CC | 4 CC |
| Smoothing, instalment overdue | 10 CC | v2 | 4 CC | 10 CC |

In the mismatch case, v1 calculates 8 CC while the authoritative v2 calculates 10 CC. The burn matches the stale calculation but not the current obligation.

In the first smoothing case, 6 CC remains outstanding but is not yet due. In the overdue case, the same 6 CC is already due.

## Results

| Scenario | Public burn only | Signed reconciliation | Independent confidential audit | Cryptographic proof |
|---|---|---|---|---|
| Agreement-version mismatch | Cannot identify applicable terms | Detects mismatch against authoritative version record | Detects by inspecting executed agreement | Detects if proof binds authoritative version and applied version |
| Smoothing, not yet due | Cannot assess liability or due date | Correctly treats 4 CC as current | Correctly treats 4 CC as current after contract review | Correctly proves due-date calculation if schedule is bound |
| Smoothing, overdue | Cannot establish shortfall | Detects 6 CC overdue | Detects 6 CC overdue | Detects 6 CC overdue if due schedule and allocation are bound |

The existing under-reporting result remains important: signed reconciliation and proof can still accept a self-consistent calculation over an incomplete source report.

## What this adds

1. **Agreement identity is a first-class accounting input.** Reconciliation is not meaningful unless it identifies which agreement version governs the interval.
2. **Burn-to-total-liability comparison is insufficient.** The correct comparison is between burn allocated by the evaluation time and the liability due by that time.
3. **Smoothing creates a temporal accounting obligation.** A settlement manifest needs due tranches, deadlines, and burn allocations, not merely one aggregate amount.
4. **Proofs inherit the trust model of their reference data.** A proof can enforce use of a version identifier, but a trusted mechanism must establish which version was authoritative and effective.

## Limitations

- The model assumes an authoritative agreement-version registry and due schedule. It does not specify a legal governance process for disputes over amendments, signatures, effective dates or retroactivity.
- The model does not yet allocate one burn across multiple synchronizers or test duplicate claims across obligations.
- No operational cost, privacy leakage or latency is measured in this extension.
- Results are scenario classifications, not statistical detection rates or claims about current Canton implementation.

## Validation

The expanded suite contains nine tests covering the 24 scenario/architecture combinations and the key distinctions above.

Run from the repository root:

```bash
python -m unittest discover -s tests -p 'test_comparative_assurance_model.py' -v
python analysis/comparative_assurance_model.py
```

## Next experiment

Extend the model to a shared paymaster with multiple synchronizer obligations and aggregate burns. Test duplicate allocation, over-allocation, partial allocation and whether a single burn can be transparently partitioned without revealing confidential per-synchronizer liabilities publicly.
