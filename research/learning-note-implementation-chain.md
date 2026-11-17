# Learning note: the current paymaster implementation in plain language

The system has three jobs.

## Job 1: measure usage

The synchronizer keeps cumulative traffic counters. The report code reads a counter at the start of a ten-minute interval and again at the end. It subtracts the first reading from the second.

Example:
- At 10:00 the counter reads 1,000 bytes.
- At 10:10 it reads 1,350 bytes.
- The interval consumed 350 bytes.

This is a measurement calculation. It is not yet a bill.

## Job 2: pay for usage

The registered paymaster can make a traffic purchase by burning CC. The merged purchase code checks that the payer is the registered paymaster and that the purchase refers to the correct synchronizer.

But the code does not automatically compare the burn with the amount the traffic report says is owed. The payment can be valid as a purchase while still being lower than the contractual liability. That gap is explicitly described in tracker issue #155.

## Job 3: assign rewards

A traffic purchase can be used to calculate app and asset activity weights for the paymaster. The code that records this activity through the ActivityRecorder hook is still a follow-up in the inspected implementation state.

## The missing connection

The intended chain is:

Traffic measured → report delivered → amount owed calculated → CC burned → payment checked against amount owed → reward activity recorded.

The code has parts of this chain, but it has not yet demonstrated the complete sequence in one end-to-end test.

## One distinction to remember

A successful CC burn does not automatically mean the correct amount was paid.

It proves that a particular amount was burned. To know whether it was enough, we need the report, the applicable agreement, the due date and a reconciliation check.
