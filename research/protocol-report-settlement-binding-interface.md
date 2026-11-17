# Protocol Report and Settlement Binding Interface

**Status:** Synthetic interface implementation.  
**Date:** 17 November 2026.

## Purpose

Separate what the proposed protocol reports from the commercial metadata used to calculate and settle an off-ledger obligation.

## Records

### ProtocolTrafficReport

Contains only protocol/reporting evidence:
- report and interval identifiers;
- interval boundaries and receipt time;
- report status;
- aggregate traffic bytes when status is OK;
- correction revision and supersession lineage.

It does not contain a synchronizer commercial obligation, agreement version, invoice, or burn ID.

### SettlementBinding

Contains the separate off-ledger mapping:
- binding ID;
- interval ID;
- synchronizer ID;
- obligation ID;
- agreement version;
- authority reference for the mapping.

The authority reference is a synthetic provenance field. It does not itself authenticate the referenced document or prove that the signer had authority.

## Join and validation

The adapter joins each protocol report to a separately supplied binding. It rejects missing, duplicate, ambiguous or incomplete bindings. It rejects non-OK reports carrying chargeable byte values and OK reports without a non-negative integer byte count.

The current experiment assumes exactly one settlement binding per expected interval. That is a deliberately explicit simplifying constraint, not a statement about CIP-0132. The model does not yet support splitting one interval across multiple obligations or one binding covering multiple intervals.

The tariff's unit in this synthetic adapter is one model unit per reported byte. This is purely a test convention; it is not a Canton tariff or pricing proposal.

## What this separation establishes

It allows the experiment to distinguish:
1. integrity/completeness of the protocol report;
2. authority and integrity of the off-ledger settlement mapping;
3. tariff calculation;
4. matching liability to public CC burn allocations.

A successful reconciliation still does not prove the underlying traffic measurement is complete or truthful. The authority reference is supplied as data and is not cryptographically verified.

## Tests and limitations

Five tests cover a valid join, missing binding, ambiguous binding, invalid non-OK payload and invalid OK byte count. They are authored but not executed.

This is an implementation-neutral synthetic research interface, not a production Canton integration.
