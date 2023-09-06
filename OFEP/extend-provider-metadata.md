---
date: 2023-09-06
title: Extend Provider Metadata
status: Approved
authors: [Michael Beemer]
tags: [spec]

---
## Extend provider metadata

## State: APPROVED

This proposal lays out a mechanism for flag providers to surface arbitrary metadata about themselves to OpenFeature, and for hooks to access this metadata.
It's similar in concept to flag metadata but works at the provider level.
This is an ideal location to store information about the provider that's common across all flag evaluations.

## Background

OpenFeature supports [flag metadata](./007-OFEP-provider-flag-metadata.md) which allows for arbitrary information to be associated with a flag evaluation.
This works well for data that specific to an individual flag that was successfully evaluated.
However, it's useful to access arbitrary provider information outside of a successful flag evaluation.

In many flag management tools, there are ways to group related flag configurations.
A non-exhaustive list includes `organization`, `namespace`, `project`, and `environment`.
As an example, a `flag key` may have different configurations per `environment`.
OpenFeature needs a way to capture provider specific metadata so that it can be leveraged by hooks.
This will allow hooks to provide better troubleshooting and telemetry support.

As with flag metadata, different providers will expose different kinds of metadata, and different Application Integrators will want to consume that metadata in different ways.
As such, the goal of this proposal is to provide a simple way for the OpenFeature runtime to pass generic metadata from a provider to a hook, without OpenFeature itself understanding the semantics of that metadata.

## Non-goals

In the future we may wish to standardize the semantics of some key metadata attributes which are common amongst many providers (e.g. `organization`, `project`, `environment`) so that provider-agnostic hooks can be created to consume these standard attributes, but that is explicitly NOT in the scope of this OFEP - we would prefer to see which common attributes naturally emerge and then "pave those cow paths".

## Proposal

Extend the [provider metadata](https://openfeature.dev/specification/sections/providers#requirement-211) to allow for a bag of immutable metadata attributes related to the provider itself.
This bag will be a set of key-value pairs, where the key will be a string and the value will be a small set of primitive values.

`ProviderMetadata` is already defined in the spec.
It currently has a single readonly property `name`.
This requirement would remain, but the `ProviderMetadata` interface would be extended to allow for a type like `Record<string,string|boolean|number>` in typescript, where the key is the metadata attribute and the value is the metadata value.
These values would be mutable by the provider only.

### Code examples

```ts
interface ProviderMetadata extends Metadata {
  readonly name: string;
}

interface Metadata {
  [key: string]: string | boolean | number;
}
```

```java
public interface Metadata {
    String getName();
    // Add attributes accessor
    Map<String, Object> getAttributes();
}
```

> Since evaluation context is already available to hooks, they already have access to the [provider metadata](https://openfeature.dev/specification/sections/hooks#requirement-412).
