## OFEP: Pluggable OpenFeature providers for flagd evaluation engine

## State: DRAFTING

This OFEP proposes to introduce an adapter mechanism for plugging in OpenFeature providers as the evaluation engine for flagd.
Being a Go project, flagd would be capable of utilizing any OpenFeature provider written in Go as its evaluation engine. This
allows the benefits of the flagd architecture and cloud-native solutions like the open-feature-operator to be used in tandem
with the agnostic backend offering of OpenFeature providers.

## Background

Flagd is the exemplar OpenFeature solution, being a required provider for all OpenFeature SDKs for all languages, thus offering the best support for getting started with OpenFeature.

In the Go ecosystem, OpenFeature provides support for a number of feature flagging systems.

While flagd itself is accessible by OpenFeature SDKs with the provider implementation, the flagd backend itself has independent implementations for evaluation logic with the `IEvaluator` interface.

## Proposal

I propose a plugin mechanism or adapter pattern for OpenFeature `Provider` implementations to be used as an `IEvaluator` for flagd to allow configurable backends.

### Implementation

TODO: Go builds static binaries, but as of 1.17 they introduced support for plugins loading from shared objects. Let's cover some options:

1. Refactor to a plugin-oriented architecture with flagd, dynamically loading a configured shared object. The existing built-in configuration options would skip the plugin entirely so current evaluators would continue to work as expected.
2. Independent builds per provider. This means we would have the original `flagd` binary, and now also `flagd-split`, `flagd-cloudbees`, etc.