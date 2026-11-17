# Accounting-Invariant Validation Matrix

**Prepared:** 18 November 2026  
**Branch:** `circleci-project-setup`  
**Status:** research validation plan mapped to existing prototype coverage; not a Canton conformance certification.

## 1. Purpose

This matrix connects the proposed accounting guarantees to (a) the public Canton evidence currently available, (b) the research prototype that models the guarantee, and (c) the evidence still required. It deliberately separates a property enforced by our synthetic validator from a property established by Canton source or a live deployment.

The Scan API access check on 18 November retrieved no live records. The matrix therefore contains no observed TestNet accounting results.

## 2. Validation matrix

| ID | Invariant / question | Canton evidence currently available | Existing research artefact and test coverage | Current result | Remaining validation |
|---|---|---|---|---|---|
| I-01 | Every required interval is represented exactly once; gaps and overlaps cannot silently become zero usage | CIP-0132 describes aligned ten-minute reports; PR #111 is open and its report API is not a deployed feed | `analysis/interval_coverage.py`; `tests/test_integrated_interval_reconciliation.py`; `tests/test_settlement_manifest_validator.py` cover missing report, late report, uncovered window and interval gap | Prototype checks exist; Canton report completeness not established | Add/confirm explicit duplicate, overlap and out-of-order report cases; compare against an independent interval partition oracle |
| I-02 | Non-OK / unavailable reports never become billable zero or chargeable bytes | PR #111 defines Ok, Undetermined and CannotProvide states in an open PR | `tests/test_protocol_settlement_interface.py` tests non-OK report with bytes and invalid OK byte count; manifest tests missing/CannotProvide | Prototype rejects these malformed states | Confirm every model path preserves unavailable vs zero; source review remains PR-level |
| I-03 | Report provenance and immutability are verifiable | PR #111 uses JWT API authentication; reviewed patch does not establish a report-level signature or public attestation | Protocol report model has no report signature field; interface specification proposes canonical report signature and digest | Not implemented in current prototype interface | Add a report-attestation model/test if this mechanism remains a selected architecture; separately test canonical encoding, digest tampering, signer rotation/revocation |
| I-04 | Agreement version effective at the interval is selected and its authority is established | CIP-0132 places commercial terms off-ledger; actual bilateral agreements are unavailable | Agreement verification and pricing models check signed agreement document and signer registry; protocol interface tests unknown/revoked signer and agreement-version mismatch paths indirectly through code | Agreement document signature checks are modelled; legal authority and real operator authority remain assumptions | Test effective-time boundaries and authorised-party role binding; distinguish signer identity from authority to bind a specific synchronizer/obligation |
| I-05 | Report-to-obligation binding is authenticated independently of agreement terms | No such on-ledger binding mechanism is specified in CIP-0132 Phase 1 | `analysis/protocol_settlement_interface.py`; test `test_agreement_signature_does_not_authenticate_binding_metadata` deliberately alters authority_reference while reusing agreement signature and still reconciles | **Known prototype gap demonstrated** | Add separate binding-attestation signature over report digest, interval, synchronizer, obligation, agreement version and authority reference; reject altered fields, wrong signer role and replay |
| I-06 | Liability is deterministic and independently reproducible from report plus applicable agreement | CIP-0132 leaves price/discount/smoothing terms to off-ledger agreement | Pricing, agreement schedule and liability modules; deterministic synthetic calculations | Modelled, not verified against actual operator contracts | Add independent second implementation or golden vectors; obtain anonymised agreement examples only if an operator can provide them |
| I-07 | Amount paid is evaluated against amount due at time t, including discounts and smoothing | CIP-0132 permits discounts and delayed/smoothed settlement; issue #155 says purchase path does not compare paid amount to report amount | Reconciliation state machine and agreement schedule models include due-date/smoothing scenarios | Synthetic temporal accounting is modelled; no actual agreement or settlement history | Confirm no path classifies NOT_YET_DUE as SHORT_PAID; test partial tranche, grace-period expiry, late burn and correction after due date |
| I-08 | Burn evidence is unique and cannot be allocated beyond its public amount | Public CC burn evidence exists in principle; no paired live data retrieved in this access attempt | `tests/test_settlement_manifest_validator.py` covers duplicate burn and burn claimed by another settlement; allocation model tests cover allocation controls | Prototype checks exist | Add property-based or exhaustive small-state tests for many-to-many allocation, duplicate allocation IDs, split burns, rounding and amendment replay |
| I-09 | Each obligation receives sufficient eligible allocations, without double counting across obligations | CIP-0132 permits off-ledger commercial reconciliation; no complete public report-to-burn link established | Reconciliation and manifest validators model obligation coverage and allocation | Synthetic state-machine property only | Verify cumulative multi-obligation allocations and carry-forward rules against explicit agreement semantics |
| I-10 | Reward attribution traces to eligible paid activity and the correct rule version | CIP-0132 describes CIP-0104 activity hook; reviewed PR #8449 was draft/open and issue #163 open at 17 Nov snapshot | Reward attribution model and tests exist in repository; no full end-to-end Canton test evidenced | Research prototype only; public implementation flow incomplete in reviewed snapshot | Recheck upstream status; test wrong epoch, wrong weight version, unbacked eligible bytes, duplicate activity record and distinction between validator reward and app distribution |
| I-11 | Corrections preserve history and produce auditable adjustments | PR #111's report retention design is on-demand and depends on sequencer counter history; no durable report archive in reviewed patch | `tests/test_integrated_interval_reconciliation.py` covers correction chain, missing liability calculation and append-only positive/negative adjustments | Prototype correction semantics tested in source | Add replay/idempotency tests and define correction authority, maximum correction window and dispute freeze semantics |
| I-12 | Public disclosure does not leak confidential participant or commercial data through aggregate composition | Scan exposes DSO-party view, not all private application transactions; no live data collected | Synthetic aggregate leakage experiments and privacy analysis exist | Synthetic leakage examples only | Validate against realistic query/adversary assumptions; do not claim a Canton privacy incident or formal differential-privacy guarantee |

## 3. Evidence-level classification

Use these labels when reporting outcomes:

- **E0 — Specification:** requirement is stated in a research specification or CIP.
- **E1 — Public implementation observation:** behaviour is visible in a named source revision or pull request.
- **E2 — Prototype test:** our code enforces or rejects a constructed case.
- **E3 — Reproducible local experiment:** the test/model is executed at a recorded commit with environment and outputs preserved.
- **E4 — Independent network/operator experiment:** an authorised TestNet or operator environment produces records that can be independently compared.
- **E5 — Production assurance:** operator records, independent source evidence and production controls support the claim.

A result at one level must not be described as a higher level. In particular, E2 does not establish Canton conformance; E3 does not establish live-network behaviour; public burn evidence alone does not establish private metering completeness.

## 4. Priority order

1. **Close I-05 first.** The existing prototype test demonstrates that agreement-signature verification does not authenticate settlement-binding metadata. Implement a distinct binding attestation in the research prototype and test field tampering, replay, signer authorisation and report-digest substitution.
2. **Strengthen I-01 and I-08.** Add duplicate/overlap/out-of-order interval cases and allocation invariants across multiple obligations. These are local deterministic tests and do not require Scan access.
3. **Run existing deterministic tests locally.** Preserve the exact commit SHA, Python version, command, complete output and exit status. The CircleCI pass is user-confirmed, but its tested SHA was not recorded; it does not prove that subsequent commits or every new test have run.
4. **Recheck upstream source status before publication.** In particular CIP-0132, PR #111, PR #8449, issues #152, #159 and #163. Treat the 17 November audit as a dated snapshot.
5. **Keep E4 optional.** Only pursue TestNet access if an SV/operator provides an authorised endpoint, VPN or export. Do not infer data from the SV directory or bypass access controls.

## 5. Claims currently supportable

- The public proposal and implementation work describe separate measurement, off-ledger agreement and CC purchase stages; the reviewed source snapshot did not establish an end-to-end verified report-to-burn-to-reward pipeline.
- The research prototype contains tests for several interval, status, signature, allocation and correction invariants.
- The prototype has a demonstrated binding-authentication gap: changing an authority reference while reusing the agreement signature still reconciles.
- The Scan API access attempt returned 403 from two browser requests; no live network accounting records were retrieved.

## 6. Claims not currently supportable

- That Canton TestNet has under-reported traffic, underpaid synchronizer operators or misallocated rewards.
- That the proposed CIP-0132 model works end-to-end on TestNet or MainNet.
- That all public Scan APIs are inaccessible, or that the observed 403s prove a universal access policy.
- That any proposed signature, audit or proof architecture has been deployed or independently validated in Canton.
- That synthetic costs, detection rates or scenario values estimate real Canton operating costs or failure probabilities.
