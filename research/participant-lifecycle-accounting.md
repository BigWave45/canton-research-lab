# Participant lifecycle accounting: synthetic sensitivity analysis

**Source-grounded aggregation rule:** the inspected TrafficReport implementation sums only participants present in the end-of-interval state. Participants absent at interval end are excluded; new participants present at interval end count from zero.

**Critical qualification:** this creates an accounting shortfall only if the intended agreement says traffic consumed before departure remains chargeable. The research has not yet verified that contractual rule.

## Worked example

Suppose the interval contains:
- Continuing participant: 100 units.
- Participant who leaves before interval end: 40 units consumed before departure.
- Participant who joins during the interval: 25 units.

The end-state aggregation returns 125 units (100 + 25). If the 40 units consumed before departure remain chargeable, the economic total is 165 units. The difference is 40 units.

| Departure usage | End-state aggregate | Economic total if departure use is chargeable | Difference |
|---:|---:|---:|---:|
| 10 | 125 | 135 | 10 |
| 40 | 125 | 165 | 40 |
| 80 | 125 | 205 | 80 |

The output is a sensitivity analysis over explicit synthetic values, not an estimate of actual Canton traffic.

## Policy interpretation

Two materially different policies are possible:

1. **Pre-departure usage remains chargeable.** The current end-state aggregation does not include the departed participant's interval consumption. A separate lifecycle-boundary record or final counter snapshot is needed to account for it.
2. **Departed participants' interval usage is intentionally excluded.** The aggregation is consistent with that policy, but the agreement and specification must state the exclusion clearly. The cost is that the chargeable population differs from total traffic consumed during the interval.

The implementation alone does not decide which policy is economically correct.

## Candidate mechanisms to compare

| Mechanism | Evidence added | Main cost / assumption |
|---|---|---|
| Signed departure snapshot | Final counter at participant exit, bound to interval and identity | Requires trusted/authenticated event capture; may reveal lifecycle metadata |
| Carry-forward counter | Preserve departed member's final cumulative counter until interval closes | Requires durable state and careful replay/idempotency handling |
| Event-driven boundary settlement | Close that participant's usage at departure time | More events and settlement complexity |
| Explicit exclusion rule | No additional evidence; policy defines excluded traffic | Accepts difference between consumed and billable traffic |

No mechanism is selected. The next step is to establish the actual charging semantics and then quantify assurance, privacy leakage, implementation complexity and dispute handling for each alternative.
