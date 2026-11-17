# Prototype Measurement Protocol

**Status:** Reproducible local microbenchmark harness. No benchmark output has yet been collected.  
**Scope:** Existing research prototypes only; synthetic workloads, not Canton production traffic.

## Question

How do report-manifest validation, shared-burn allocation validation and aggregate-disclosure analysis behave as synthetic input size increases?

This experiment measures three separate computational tasks. It does not measure end-to-end synchronizer performance, network latency, cryptographic proof generation, operator effort or production privacy.

## Implemented harness

Run from the repository root:

```bash
python analysis/research_benchmark.py --repeats 30 --sizes 10,50,100,250
```

The script prints a JSON record with:
- Python version and platform;
- fixture scale;
- compact UTF-8 JSON byte length for each fixture;
- validation/analysis median, p95, minimum and maximum runtime;
- peak traced Python allocation during repeated calls;
- privacy matrix rank and identified participant indices.

It performs up to three warm-up calls. Timing uses `perf_counter_ns`; memory uses `tracemalloc`. The p95 is a descriptive statistic over a small local sample, not a service-level percentile. The serialized sizes are schema-specific fixture sizes, not wire-protocol or network payload measurements.

## Workloads

### 1. Settlement manifest

Builds a contiguous sequence of 10-minute synthetic intervals, each with status OK, a traffic-byte count, agreement version and report digest. A single burn is compared with a fixed expected amount.

The validator's expected outcome is `reconciled`. The measured operations are serialization size and `validate_manifest` runtime/peak traced allocation.

This tests validator scaling over the interval list. It does not prove that the interval source measured all actual traffic.

### 2. Portfolio allocation

Builds one synthetic burn partitioned into N unique allocations, each assigned to a distinct obligation with a matching due amount. The expected result is valid allocation.

The measured operation is `validate_allocations`. The current implementation builds duplicate identifiers using repeated list counting; that construction may have quadratic growth. The benchmark is intended to test this suspected scaling property before any optimisation is proposed. Do not infer a production bottleneck from a local synthetic run.

### 3. Aggregate privacy

Builds two overlapping aggregate-release rows over N participants. The second row excludes participant zero, so the difference between aggregates isolates that participant's value under the constructed linear model.

The harness records matrix dimensions, serialized matrix size, exact matrix rank, identified participant index and analysis runtime/peak traced allocation.

This is an algebraic disclosure demonstration. It is not differential privacy, a production attack, or evidence of a Canton disclosure incident.

## Reproducibility record

When executed, preserve:
- exact Git commit SHA;
- command line;
- complete JSON output;
- device/CPU and memory context if available;
- Python version;
- whether other applications or workloads were active;
- any errors or discarded runs.

Run at least twice on the same environment before comparing code changes. Do not compare phone, laptop and cloud measurements as if they were controlled experiments. Do not report only the fastest run.

## Interpretation

The harness produces local computational measurements for synthetic inputs. Results can support claims such as "the validator took X milliseconds on this device for this N-interval fixture." They cannot support claims about Canton production latency, throughput, synchronizer costs or operator economics.

The allocation validator's duplicate-ID scan is a code-level candidate for optimisation. First collect a baseline. If measurements show growth that matters at plausible manifest sizes, replace the repeated counting with a linear-time frequency/set check and rerun the same workload. Preserve before/after outputs and verify identical validation semantics.

## Current status

The harness is committed as code, but it has not been executed in this environment. No timings, memory figures or measured payload sizes are claimed in this document.
