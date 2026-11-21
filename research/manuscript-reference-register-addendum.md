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

## Resolution status

The earlier open issues in this addendum have been adjudicated in `research/manuscript-audit-resolution-2026-11-18.md`.

- **PR #103 versus PR #111:** use PR #111 for the participant-departure implementation observation. PR #103 is historical context only.
- **I-10:** the full reward-attribution checklist is not supported as an implemented I-10 model. The formal property register contains P1–P8; P6 is a narrower reward-budget bound. Describe the full checklist as a proposed validation requirement and cite the narrower code/tests only for the checks they actually perform.
- **ICU cost figures:** the four numerical architecture totals and break-even values have no reproducible model in the inspected repository snapshot. Remove them from the manuscript and use qualitative cost drivers unless the missing model is recovered and committed.

The main reference register has been updated to reflect these decisions. This addendum remains the source record for references [20]–[24].

## Revised citation map additions

| Manuscript section | Add references | Purpose |
|---|---|---|
| 2. Protocol model | [20], [21], [23], [24] | Distinguish merged purchase-path code from incomplete report and reward integration |
| 4. Measurement assurance | [22] | Report API acceptance criteria and their unverified status |
| 5. Settlement assurance | [20], [21] | Purchase-path implementation context |
| 6.1 Reward attribution | [23], [24] | End-to-end and ActivityRecorder integration status |
| 9.1 Implementation limitations | [20]–[24] | Snapshot-based evidence status |

