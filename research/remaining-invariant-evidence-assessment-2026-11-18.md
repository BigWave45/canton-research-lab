# Remaining invariant evidence assessment

**Prepared:** 18 November 2026  
**Branch:** `circleci-project-setup`  
**Scope:** I-02, I-03, I-04, I-06 and I-07  
**Purpose:** Decide whether remaining invariant gaps justify more prototype implementation. This is a source/code inspection, not a fresh test run or Canton conformance assessment.

## Assessment

| Invariant | Existing evidence | What the prototype establishes | Actual unresolved gap | Decision |
|---|---|---|---|---|
| I-02 — Non-OK reports are not billable zero | CIP-0132 reporting proposal and open PR #111 define `Ok`, `Undetermined` and `CannotProvide` states. | The interval coverage path preserves `NON_OK` as incomplete; the protocol adapter rejects non-OK reports carrying chargeable bytes; pricing rejects non-OK reports. | The report API remains proposed/open in the reviewed snapshot. There is no deployed feed or production-path evidence. | No more code now. Existing prototype coverage is adequate for the research claim. Retain upstream implementation/deployment as an external evidence gap. |
| I-03 — Report provenance and immutability | PR #111's reviewed API uses JWT authentication; the reviewed patch did not establish a report-level operator signature. | The settlement binding signs a digest of the report set. This detects changes relative to that signed digest if the binding signer and key registry are trusted. | The report set is not independently attested by the reporting operator. A settlement-binding signature proves that the binding signer committed to a digest; it does not prove which operator generated the report or that it originated from the meter. | Architecture decision required, not immediate coding. If signed operator reports are selected, add a distinct operator attestation and define key authority/rotation. Do not describe the existing binding signature as operator report provenance. |
| I-04 — Effective agreement version and authority | CIP-0132 leaves commercial terms to off-ledger agreement. Actual bilateral agreements are unavailable. | The interface verifies the agreement document signature, signer key status and generic `agreement` role at the expected interval end; pricing checks that the agreement covers the full report interval. | A generic role in a caller-supplied registry does not prove authority to bind this specific synchronizer, paymaster or obligation. No real agreement or independently governed signer registry is available. | No further implementation until policy is specified. Define authority scope and effective-time policy first; otherwise tests would encode invented legal semantics. |
| I-06 — Deterministic liability | CIP-0132 does not supply actual bilateral tariff, discount or smoothing terms. | The pricing model uses deterministic integer arithmetic, explicit bands, discounts and rounding. Agreement schedules use explicit timestamps and integer CC amounts. | There is only one implementation path and synthetic inputs. Determinism within one implementation is not independent reproducibility. No anonymised operator agreement, tariff vector or independently computed expected result is available. | Do not build a second pricing engine yet. Golden vectors become useful if actual or explicitly hypothetical tariff rules are fixed. |
| I-07 — Paid versus due at time t | CIP-0132 allows off-ledger discounts/smoothing; issue #155 documented no purchase-side comparison between paid amount and report amount in the reviewed snapshot. | The schedule calculator distinguishes future, due, within-grace and past-grace tranches; it models FIFO allocation, explicit carry-forward and unapplied payment. | The model aggregates allocated payment by evaluation time but does not retain a timestamp/finality point for each burn allocation. A burn occurring after a historical due/grace deadline could be counted when reconstructing that earlier evaluation unless the caller pre-filters allocations. | Specific modelling gap, but defer code. Document this as an evidence limitation. Implement timestamped/finality-aware payment events only if historical as-of reconciliation becomes a required deliverable. |

## Important distinctions

### I-02: unavailable is not zero

The current model distinguishes a valid zero-traffic `OK` report, a non-OK report with no chargeable byte value, and missing/unavailable evidence. A valid zero is a measured value; unavailable is an absence of an authoritative value. This is a sound model-level distinction, not proof of upstream production behavior.

### I-03: digest commitment is not source provenance

The report digest is included in a signed settlement binding. This supports tamper-evidence after the binding signer commits to the digest. It does not provide an operator-origin signature over the report. A JWT-authenticated API request is also not equivalent to a durable, independently verifiable report attestation. The paper must name the signer and the exact claim being authenticated.

### I-04: cryptographic identity is not contractual authority

The signer registry is an explicit trust root. A key marked with the generic `agreement` role is not thereby authorised to sign for every synchronizer or paymaster. Authority must be scoped to entities, agreement identifiers, validity periods and permitted actions, and governed outside the verifier. Without a source contract or agreed policy, further code would merely formalise assumptions.

### I-06: deterministic does not mean independently verified

Integer arithmetic and deterministic rounding make the same inputs reproducible by the same implementation. Independent reproducibility requires separately calculated expected values or a second implementation that does not share the same logic. No actual Canton tariff data is available, so the existing model should remain explicitly synthetic.

### I-07: payment timing is not just payment quantity

A snapshot of total allocations at evaluation time can establish a cumulative amount only if the snapshot is complete and correctly scoped. Historical payment status additionally needs the burn's event time and finality time, plus a rule for which timestamp determines contractual payment. Current allocation records do not encode that temporal evidence.

## Work decision

- I-02: retain existing tests and source-status caveat.
- I-03: keep as a named architecture gap; do not claim operator-origin provenance.
- I-04: keep authority scope and contract interpretation as external assumptions until real policy evidence exists.
- I-06: retain deterministic synthetic model; defer independent golden vectors.
- I-07: record missing event-time/finality-aware as-of accounting; defer implementation.

No additional code is recommended at this stage. No CI or local tests were run for this assessment. It is based on inspection of committed source and tests plus the previously recorded public-source snapshot. Recheck upstream statuses and source references before publication.
