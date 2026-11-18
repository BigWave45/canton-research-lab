# Manuscript Reference Register — Addendum

**Prepared:** 18 November 2026  
**Applies to:** `research/manuscript-reference-register.md`  
**Research repository snapshot:** `ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c`

This addendum extends the working register with implementation sources that the first pass identified in the end-to-end verification audit. It also records two corrections required before manuscript citations are inserted.

## Additional implementation references

### [20] Canton Network. Pull request #100 — Paymaster traffic purchase support
Canton Network, `splice-multi-sync`. Pull request #100.  
https://github.com/canton-network/splice-multi-sync/pull/100  
**Supports:** merged source changes for the Daml paymaster traffic-purchase path and registration-gated purchase support.  
**Use:** Sections 2 and 5.  
**Qualification:** merged source is not proof of deployment to a long-running network or MainNet.

### [21] Canton Network. Pull request #104 — Scan and SV registered-synchronizer handling
Canton Network, `splice-multi-sync`. Pull request #104.  
https://github.com/canton-network/splice-multi-sync/pull/104  
**Supports:** Scan/SV integration for registered synchronizers and paymaster MemberTraffic handling.  
**Use:** Sections 2 and 5.  
**Qualification:** the audit states that #100 and #104 were intended to be deployed together; neither merged status alone establishes network deployment.

### [22] ChainSafe. Issue #152 — Traffic report API acceptance criteria
ChainSafe, `canton-extending-mainnet`. Issue #152.  
https://github.com/ChainSafe/canton-extending-mainnet/issues/152  
**Supports:** acceptance criteria for ten-minute interval reporting, completed-interval semantics, multi-operator consistency and retention across pruning/upgrades.  
**Use:** Sections 4 and 9.  
**Qualification:** acceptance criteria are requirements, not proof that the criteria passed.

### [23] ChainSafe. Issue #159 — End-to-end paymaster flow test
ChainSafe, `canton-extending-mainnet`. Issue #159.  
https://github.com/ChainSafe/canton-extending-mainnet/issues/159  
**Supports:** the requested end-to-end test sequence from registration and participant traffic through report retrieval, paymaster burn and activity records.  
**Use:** Sections 2, 6.1 and 9.  
**Qualification:** an open test issue is evidence that the end-to-end test was still outstanding in the 17 November 2026 audit snapshot, not evidence of a passing test.

### [24] ChainSafe. Issue #163 — ActivityRecorder integration
ChainSafe, `canton-extending-mainnet`. Issue #163.  
https://github.com/ChainSafe/canton-extending-mainnet/issues/163  
**Supports:** the tracked integration gap between paymaster purchase and recording app/asset activity through the CIP-0104 extension hook.  
**Use:** Sections 2, 6.1 and 9.  
**Qualification:** cite the issue's state and audit date. Do not describe the integration as complete based on a tracked follow-up.

## Corrections and unresolved points

### Section 4.3: use PR #111 for the participant-departure behaviour

The current repository file `research/traffic-report-implementation-audit.md` explicitly attributes the implementation semantics to PR #111. It says PR #111 replaces PR #103 and describes the current implementation as an on-demand reader using sequencer counter snapshots. It also says the calculation iterates participants present in the end-of-interval state and excludes participants absent at interval end, even if present at interval start.

Therefore, the manuscript's existing sentence attributing this observation to PR #103 is inconsistent with the current audit record. Unless the source-code diff establishes that the same exact behaviour was already present in PR #103, change the manuscript attribution to PR #111 and identify the 17 November 2026 source snapshot. Retain the caveat that this was an open pull request, not deployed production behaviour.

### Section 6.1: I-10 has not been located in the current register

The inspected `research/accounting-properties-and-threat-model.md` defines eight properties, P1–P8. The current repository tree and targeted search did not locate an authoritative twelve-invariant register or a definition of I-10. This does not prove no such document exists outside the inspected tree, but the current paper citation cannot be supported from the located register.

Before publication, either locate and cite the exact I-01–I-12 source file and verify I-10's definition, or remove the I-10 label and describe the validation checks directly. Do not silently map I-10 onto P6 or another property.

### Section 7.2: ICU model remains untraceable

The located scripts `analysis/comparative_assurance_model.py` and `analysis/integrated_assurance_comparison.py` do not reproduce the 28.0, 59.5, 105.0 and 141.5 ICU values. The separate `analysis/synchronizer_economics_scenarios.py` models a different USD/MB pricing and collateral question, so it is not a source for the Section 7.2 assurance-cost table.

The manuscript needs the exact cost-model inputs, formulae, units, script or spreadsheet, and output. If the values were manually constructed, label them as an illustrative scenario and show enough arithmetic to reproduce them. Do not cite an unrelated model.

## Revised citation map additions

| Manuscript section | Add references | Purpose |
|---|---|---|
| 2. Protocol model | [20], [21], [23], [24] | Distinguish merged purchase-path code from incomplete report and reward integration |
| 4. Measurement assurance | [22] | Report API acceptance criteria and their unverified status |
| 5. Settlement assurance | [20], [21] | Purchase-path implementation context |
| 6.1 Reward attribution | [23], [24] | End-to-end and ActivityRecorder integration status |
| 9.1 Implementation limitations | [20]–[24] | Snapshot-based evidence status |

