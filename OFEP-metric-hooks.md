## OFEP-hook-for-metrics

## State: PENDING REVIEW

This OFEP propose to introduce OpenFeature hook for OpenTelemetry metrics.

## Background

We already have OpenTelemetry Span support through hooks. Similarly, we can provide a dedicated hook for OpenTelemetry
metrics. Providing telemetry data out of the box will make OpenFeature attractive for both users and vendors.

## Proposal

The proposal here is to define a set of metrics that can be used with different hook stages. For example, error metrics
can be collected at the hook's `error` stage. Going with this background, I propose the following metrics.

## Metrics

All metrics defined through this proposal carry OpenTelemetry semantic conventions defined attributes(dimensions)[1].

- feature_flag.key: The unique identifier of the feature flag
- feature_flag.provider_name: The name of the service provider that performs the flag evaluation
- feature_flag.variant:    SHOULD be a semantic identifier for a value. If one is unavailable, a stringified version of
  the value can be used

Given below is the list of metrics proposed and their usage,

### feature_flag.evaluation_requests

A counter[2] based metric to calculate the number of flag evaluation requests. This is recorded at `before` stage of
the hook.

This metric is useful to understand flag evaluation requests received through OpenFeature SDK.

### feature_flag.evaluation_success

A counter[2] based metric to calculate the number of successful flag evaluations. This is recorded at `after` stage of
the hook.

This metric is useful to understand successful flag evaluations. This metric contain following extra dimension(s),

- reason : evaluation reason extracted from flag resolution details[3]

### feature_flag.evaluation_error

A counter[2] based metric to calculate the number of failed flag evaluations. This is recorded at `error` stage of
the hook.

This metric is useful to understand flag evaluation errors. This metric contain following extra dimension(s),

- exception : error/exception message extracted from the evaluation error

### feature_flag.evaluation_active

An UpDownCounter[4] based metric to calculate the number of active flag evaluations currently going through
OpenFeature SDK. This is increased at `before` stage and decreased at `finally` stage.

Given the evaluation is fast, the value observed here can be 0. However, when there are bottlenecks or provider
slowdowns, this will be a non-zero value.

## Example

Consider following coding example in Go.

```go

// Reader should be derived or injected 
var reader metric.Reader

// Derive metric hook from reader
metricsHook := hooks.NewMetricsHook(reader)

// Register OpenFeature API hooks
openfeature.AddHooks(metricsHook)
```

### References

[1] - https://opentelemetry.io/docs/specs/otel/logs/semantic_conventions/feature-flags/

[2] - https://opentelemetry.io/docs/specs/otel/metrics/api/#counter

[3] - https://openfeature.dev/specification/types#resolution-details

[4] - https://opentelemetry.io/docs/specs/otel/metrics/api/#updowncounter