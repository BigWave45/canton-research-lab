# Scan API Access Check and Evidence Boundary

**Checked:** 18 November 2026  
**Environment:** User-operated iPhone browser; no validator node, SV sponsor, VPN or allowlisted validator egress IP established.  
**Purpose:** Record the result of attempting to retrieve public Scan API data for the dedicated-synchronizer paymaster accounting study.

## 1. Attempts and observed result

The user confirmed that the official Canton Foundation Super Validator network-status directory opened successfully and supplied its TestNet SV list. The list included 13 TestNet Scan URLs and advertised software versions between 0.10.0 and 0.10.1.

Two direct API requests were then attempted in the user's mobile browser:

| Network | Scan instance | Request | User-observed result |
|---|---|---|---|
| MainNet | Global Synchronizer Foundation | `GET /api/scan/v0/scans` | HTTP 403 Forbidden |
| TestNet | Global Synchronizer Foundation | `GET /api/scan/v0/scans` | HTTP 403 Forbidden |

No response body, server diagnostic, request ID or headers were captured. The reason for either refusal is therefore not independently established. The repeated 403 responses are evidence of failed access from this browser/network context, not proof that all Scan instances or all Scan endpoints are inaccessible.

## 2. Relevant official API semantics

The official Splice Scan documentation describes Scan as an application hosted by Super Validator nodes. Scan ingests the SV participant's view as the DSO party and exposes that view through APIs. It includes Canton Coin transfers and governance operations, but excludes most application transactions that do not involve the DSO party. The documentation says a consumer can query one SV's Scan API or compare multiple SV Scan APIs.

The Scan OpenAPI reference documents:

- `GET /v0/scans`: returns synchronizer IDs and associated Scan URLs.
- `GET /v0/domains/{domain_id}/members/{member_id}/traffic-status`: returns traffic status as reported by the sequencer according to ledger state at request time. The documented response includes `actual.total_consumed`, `actual.total_limit` and `target.total_purchased`.

These fields are useful network-state observations, but they do not expose the underlying private ten-minute dedicated-synchronizer traffic report or prove that its source measurement is complete. In particular, a traffic-credit status endpoint must not be treated as a substitute for the proposed CIP-0132 operator report.

Official references:
- Scan API overview: https://docs.global.canton.network.sync.global/app_dev/scan_api/index.html
- Scan OpenAPI reference: https://docs.global.canton.network.sync.global/app_dev/scan_api/scan_openapi.html
- Current CC and synchronizer traffic API: https://docs.global.canton.network.sync.global/app_dev/scan_api/scan_current_state_api.html
- Splice API overview and authentication: https://docs.global.canton.network.sync.global/app_dev/overview/splice_app_apis.html

## 3. Access-control interpretation

The official validator-onboarding documentation describes connecting through a validator's allowlisted egress IP and notes that access to the Scan web UI may require an SV-operated VPN. This is consistent with the access problem encountered here. However, the two 403 responses alone do not identify the specific access-control rule that rejected the requests. Do not state that the API is universally private or that every SV endpoint necessarily requires identical access.

Official reference:
- Validator onboarding: https://github.com/canton-network/splice/blob/main/docs/src/validator_operator/validator_onboarding.rst

## 4. Consequence for the research

No live Scan response has been collected. The project therefore has **no observed public-network dataset** from these attempts. Do not use the supplied SV directory as if it were transaction or traffic data.

The following work remains feasible without privileged network access:

1. Use official CIPs, public Splice source code, pull requests, issues and tests for dated documentary and implementation analysis.
2. Run the research repository's deterministic models and tests locally in Codespaces.
3. Use synthetic event streams to test report coverage, agreement-version selection, liability calculation, due-date treatment, burn allocation, duplicate handling and reward traceability.
4. If an operator later provides an authorised Scan endpoint or report export, collect a bounded, provenance-recorded sample and compare it with the corresponding public burn evidence where the records can legitimately be linked.

A successful Scan query, if obtained, would still establish only the fields and view exposed by that endpoint. It would not by itself validate source-meter completeness, off-ledger contractual liability, report-to-burn binding, or reward attribution.

## 5. Next validation route

Do not continue trying the same `/api/scan/v0/scans` route across the remaining SV hosts from the same browser context. The next research step is source-to-invariant validation against the public implementation and local prototype tests. Pursue direct Scan access only if an SV sponsor or authorised operator supplies the required network path and access permissions.

## 6. Evidence classification

- SV names, Scan URLs and advertised versions: user-supplied directory transcription; not independently re-fetched in this note.
- HTTP 403 outcomes: user-observed, two requests, no captured response metadata.
- API endpoint semantics and Scan visibility boundary: official Splice documentation.
- Cause of the 403 responses: unknown.
- Any claim about live traffic completeness, live paymaster accounting correctness or production end-to-end operation: not established by this access check.
