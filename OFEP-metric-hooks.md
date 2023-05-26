## OFEP-hook-for-metrics

## State: PENDING REVIEW

This OFEP proposes to introduce an OpenFeature hook for OpenTelemetry metrics.

## Background

We already have OpenTelemetry Span support through hooks. Similarly, we can provide a dedicated hook for OpenTelemetry
metrics. Providing an easy method to collect standardized telemetry data will make OpenFeature attractive for both users and vendors.

## Proposal

The proposal here is to define a set of metrics that can be used with different hook stages. For example, error metrics
can be collected at the hook's `error` stage. Going with this background, I propose the following metrics.

## Metrics

All metrics defined through this proposal carry OpenTelemetry semantic conventions defined attributes(dimensions)[1].

- feature_flag.key: The unique identifier of the feature flag
- feature_flag.provider_name: The name of the service provider that performs the flag evaluation
- feature_flag.variant: SHOULD be a semantic identifier for a value. If one is unavailable, a stringified version of
  the value can be used

Given below is the list of metrics proposed and their usage,

### feature_flag.evaluation_request_total

A counter[2] based metric to calculate the number of flag evaluation requests. This is recorded at `before` stage of
the hook.

This metric is useful to understand flag evaluation requests received through OpenFeature SDK.

### feature_flag.evaluation_success_total

A counter[2] based metric to calculate the number of successful flag evaluations. This is recorded at `after` stage of
the hook.

This metric is useful for understanding successful flag evaluations. This metric contains the following extra dimension(s),

- reason : evaluation reason extracted from flag resolution details[3]

### feature_flag.evaluation_error_total

A counter[2] based metric to calculate the number of failed flag evaluations. This is recorded at the `error` stage of
the hook.

This metric is useful for understanding flag evaluation errors. This metric contains the following extra dimension(s),

- exception : error/exception message extracted from the evaluation error

### feature_flag.evaluation_active_count

An UpDownCounter[4] based metric to calculate the number of active flag evaluations currently going through
OpenFeature SDK. This is increased at `before` stage and decreased at `finally` stage.

Given the evaluation is fast, the value observed here can be 0. However, when there are bottlenecks or provider
slowdowns, this will be a non-zero value.

## Expansion options

Given below are future expansions that can be build on top of the metrics hook. These options will not be
implemented as they require further discussions and agreements from the community.

### Metric to measure latency

credits - Justin Abrahms

Flag evaluation latency can be calculated with time measurements between `finally` and `before` stages. However,
this requires time measurement to be shared between two stages, which require either a context propagation or a shared
variable (potentially a map). Alternatively, SDK could mark the evaluation start timestamp to enhance the accuracy
of the measurement

### Scope dimension

credits - Michael Beemer

It is possible to add an additional dimension representing the configuration of the feature flag being evaluated. A
feature flag usually has a scope such as a project, workspace, namespace, or application. This can be further
expanded to environment-specific configurations such as dev, hardening, and production or the cloud provider such as
AWS, Azure or GCP. Adding this dimension through an agreed attribute name (suggested name - `scope`) benefits metric
evaluations (ex:- drill down to cloud provider specific flag evaluations)


## Example

Consider following coding example in Go for usage of the hook.

```go

// Reader should be derived or injected 
var reader metric.Reader

// Derive metric hook from reader
metricsHook := hooks.NewMetricsHook(reader)

// Register OpenFeature API hooks
openfeature.AddHooks(metricsHook)
```

Injected `metric.Reader` will perform the metric export and API is simple enough for developers.

### References

[1] - https://opentelemetry.io/docs/specs/otel/logs/semantic_conventions/feature-flags/

[2] - https://opentelemetry.io/docs/specs/otel/metrics/api/#counter

[3] - https://openfeature.dev/specification/types#resolution-details

[4] - https://opentelemetry.io/docs/specs/otel/metrics/api/#updowncounter