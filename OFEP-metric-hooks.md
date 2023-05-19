## OFEP-single-context-paradigm

## State: PENDING REVIEW

This OFEP propose to introduce OpenFeature hook for OpenTelemetry metrics.

## Background

We already have OpenTelemetry Span support through hooks. Similarly, we can provide a dedicated hook for 
OpenTelemetry 
metrics. Providing telemetry data out of the box will make OpenFeature attractive for both users and vendors. 

## Proposal

The proposal here is to define a set of metrics that can be used with different hook stages. For example, error metrics 
can e collected at hook's `error` stage. Going with this background, I propose the following metrics.

### evaluationRequests

A counter[1] based metric to calculate the number of flag evaluation requests. This is recorded at `before` stage of 
the hook.

### evaluationSuccess

A counter[1] based metric to calculate the number of successful flag evaluations. This is recorded at `after` stage of 
the hook.

### evaluationError

A counter[1] based metric to calculate the number of failed flag evaluations. This is recorded at `error` stage of
the hook.

### evaluationActive

An UpDownCounter[2] based metric to calculate the number of active flag evaluations currently going through 
OpenFeature SDK. This is increased at `before` stage and decreased at `finally` stage. Given the evaluation is fast,
the value observed here can be 0. However, when there are bottlenecks or provider slowdowns, this will be a 
non-zero value. 

### Semantic conventions 

All above metrics should carry OpenTelemetry semantic convention defined attributes [3] so that any metric processor 
can reliably process metrics produced by the hook.

## Example

Consider following coding example in Go. 

```go

    // Reader should be derived or injected 
	var reader metric.Reader

	// Derive metric hook from reader
	metricsHook, := hooks.NewMetricsHook(reader)

	// Register OpenFeature API hooks
	openfeature.AddHooks(metricsHook)
```

### References

[1] - https://opentelemetry.io/docs/specs/otel/metrics/api/#counter

[2] - https://opentelemetry.io/docs/specs/otel/metrics/api/#updowncounter

[3] - https://opentelemetry.io/docs/specs/otel/logs/semantic_conventions/feature-flags/ 