# Parameterised Assurance Cost Model

**Status:** Executable research calculator with synthetic unit tests. It is not a cost benchmark and contains no Canton operating-cost estimates.

## Purpose

The calculator makes the cost equation in the quantitative evaluation plan executable while preventing missing evidence from being replaced by arbitrary defaults.

For each architecture and evaluation period:

```
total cost =
    one-time implementation cost
  + interval count × marginal report-processing cost
  + exception count × marginal investigation cost
  + review hours × loaded hourly rate
  + retained evidence volume × storage rate
  + evidenced delay cost
```

The module keeps one-time implementation cost separate from recurring costs. It does not amortise implementation cost because a defensible service life and discount rate have not been supplied. It excludes expected residual loss because no supportable incident probabilities and loss severities are available.

## Inputs

Each architecture requires:
- implementation cost;
- interval count and marginal report-processing cost;
- exception count and marginal investigation cost;
- human review hours and loaded hourly rate;
- retained evidence volume and storage rate;
- delay cost for the evaluation period.

The caller must use one currency and the same evaluation period across all architectures. The model validates non-negative finite numeric values and integer event counts. It rejects missing inputs.

## Outputs

- one-time implementation cost;
- recurring cost components;
- total cost over the supplied evaluation period;
- incremental cost relative to public-burn-only;
- break-even avoided loss per interval.

The break-even threshold is incremental cost divided by comparable interval count. It answers how much avoided loss per interval would be required to offset incremental cost, assuming interval counts are comparable. It does not claim that any loss is actually avoided.

## Synthetic test fixture

The unit tests use deliberately constructed values to verify arithmetic and validation. Their TEST_UNITS are not prices, labour rates, storage rates or Canton measurements. The fixture must never be copied into the paper as an empirical result.

## Reproduction

From the repository root:

```bash
python -m unittest discover -s tests -p 'test_assurance_cost_model.py' -v
python analysis/assurance_cost_model.py
```

The module prints a usage notice rather than an illustrative cost result when run without supplied inputs. To produce a substantive comparison, populate all four architecture input sets from measured prototype runs, documented vendor rates, a defined time-and-motion protocol, or clearly labelled scenario assumptions.

## Worked scenario

See [Illustrative Assurance-Cost Scenario Analysis](illustrative-assurance-cost-scenario.md) for one explicitly synthetic input set, calculated results and sensitivity checks. Its ICU values are not Canton estimates and must not be cited as empirical costs.

## Interpretation limits

- This is a cost-accounting framework, not a weighted architecture score.
- Cost estimates are only as credible as the supplied inputs.
- A zero delay cost means the caller supplied zero; it must not imply delay has no economic consequence.
- Proof costs remain unmeasured until an actual proof circuit and verifier exist.
- Auditor effort remains unmeasured until a defined audit workflow is timed.
- The calculator does not quantify privacy risk or assurance effectiveness. Those remain separate exhibits.
