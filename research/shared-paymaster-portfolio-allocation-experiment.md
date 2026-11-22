# Shared-Paymaster Portfolio Allocation Experiment

**Status:** Synthetic accounting model; not an empirical study of Canton paymasters.  
**Model:** `analysis/portfolio_allocation_model.py`  
**Comparative experiment tests:** `tests/test_portfolio_allocation_model.py`
**Portfolio accounting validator:** `analysis/portfolio_settlement_model.py`
**Validator tests:** `tests/test_portfolio_settlement_model.py`

## Question

If one paymaster burns CC for several synchronizers, how can the same public burn be partitioned across obligations without double-counting or creating unsupported payment claims?

## Core distinction

One burn may legitimately fund multiple obligations. The requirement is not “one burn, one synchronizer.” The requirement is that every allocation is uniquely identified, references the correct burn, and that total allocations do not exceed the burn. Allocations must also cover the amounts contractually due for the obligations they claim to settle.

For a burn (b), with public amount (B_b), and allocations (a_{b,s}) to synchronizers (s):

[
sum_s a_{b,s} leq B_b
]

For each synchronizer obligation (s), across its eligible burn allocations:

[
sum_b a_{b,s} geq D_s(t)
]

where (D_s(t)) is the amount due by evaluation time (t). The model also requires unique allocation identifiers and correct burn references.

## Synthetic scenarios

| Scenario | Public burn | Obligation due | Claimed allocation | Expected result |
|---|---:|---:|---:|---|
| Valid partition | 10 CC | A: 6, B: 4 | A: 6, B: 4 | Reconciled |
| Duplicate claim | 10 CC | A: 6, B: 4 | Allocation ID reused | Reject duplicate claim |
| Over-allocation | 10 CC | A: 7, B: 5 | A: 7, B: 5 | Reject: 12 CC claimed against 10 CC |
| Partial allocation | 10 CC | A: 6, B: 4 | A: 6, B: 2 | B remains 2 CC short |

The duplicate-claim case deliberately reuses an allocation identifier. The over-allocation case uses distinct identifiers but claims 12 CC against a 10 CC burn. These are different failure conditions.

## Architecture comparison

| Architecture | Valid partition | Duplicate / over-allocation | Partial obligation shortfall |
|---|---|---|---|
| Public burn only | Sees 10 CC burn, cannot verify allocation | Cannot see private claims or due obligations | Cannot determine which synchronizer remains unpaid |
| Signed reconciliation | Checks signed allocation manifest against burn ID and amount | Detects duplicate IDs and total allocation above burn | Detects obligation-level shortfall if due schedule is included |
| Independent confidential audit | Recomputes allocations against agreements and source records | Detects exceptions, subject to complete auditor access | Detects shortfall and can inspect underlying obligation evidence |
| Cryptographic proof | Can prove unique allocation and bounded sum over committed data | Rejects proof if uniqueness or sum constraints fail | Can prove due-amount coverage or reveal a failed predicate without disclosing each amount |

A proof only establishes the encoded constraints over committed inputs. It does not prove that the obligation list is complete or that the underlying agreements are authoritative unless those inputs are independently anchored.

## What the model establishes

1. **A single burn can legitimately be partitioned.** Rejecting every many-to-one relationship would be unnecessarily restrictive.
2. **Uniqueness and aggregate bounds are separate checks.** Reusing an allocation identifier is invalid even if the arithmetic total happens not to exceed the burn. Distinct allocations can also over-claim the same burn.
3. **Portfolio reconciliation must remain obligation-aware.** A correct aggregate burn total can coexist with one synchronizer being underpaid and another being over-allocated.
4. **Public burn observability is not portfolio reconciliation.** Without obligation and allocation evidence, the public burn does not reveal which synchronizer it settles.
5. **Selective disclosure is plausible.** A public verifier could receive a proof of unique allocation and aggregate bounds while an authorised auditor retains the exact per-synchronizer allocation and agreement data. This is a candidate design, not a demonstrated deployed feature.

## Limitations

- The model assumes the burn event ID and amount are correctly identified from public ledger evidence.
- It assumes a canonical obligation identifier and an authoritative due amount for each synchronizer.
- It does not model multiple burns, cross-epoch carry-forward, reversals, refunds or disputed agreement amendments.
- It does not measure proof generation cost, audit effort, privacy leakage or reconciliation latency.
- The four architecture results describe evidence capability under the stated assumptions, not measured detection probabilities.

## Validation

Eight unit tests cover the 16 scenario/architecture combinations, valid partitioning, duplicate identifiers, over-allocation, partial shortfall and the limits of public burn-only evidence.

Run from the repository root:

```bash
python -m unittest discover -s tests -p 'test_portfolio_allocation_model.py' -v
python analysis/portfolio_allocation_model.py
```

## Next step

Integrate the portfolio results with the earlier 24 comparisons, then move to privacy and operational trade-offs: what must be disclosed to a public verifier, what can remain auditor-restricted, and what evidence must stay confidential.

## Portfolio validator extension: I-08/I-09

The portfolio accounting validator now models distinct allocation IDs, rejects duplicate burn evidence and missing burn/obligation references, and permits many-to-many partitions while enforcing aggregate burn limits and paymaster identity. It combines prior committed allocations with new amendment claims, so allocation IDs cannot be replayed and existing burn credit remains consumed. Per-obligation status checks compare eligible credit with due tranches at the evaluation time and retain the distinction between `short_paid` and `not_yet_due`.

The validator uses finite `Decimal` amounts only and performs exact comparisons without float conversion or quantization. The CC precision/rounding policy remains unspecified. Its tests demonstrate the encoded rules over synthetic input, not correctness or completeness of real burn evidence, the full obligation portfolio, or agreement-defined due/eligibility/amendment semantics.
