## Surfacing flag metadata

## State: DRAFTING
This proposal lays out a mechanism for flag providers to surface arbitrary flag metadata to Open Feature, and for hooks to access this metadata.


## Background

Flag providers maintain metadata about a feature flag, and there are scenarios where a hook might benefit from being able to access this metadata. For example, a flag provider could surface a `management-url` attribute which an open-telemetry hook could then add to an otel span, allowing someone viewing a trace for a feature-flagged operation to easily navigate to a webpage describing that flag in detail.

Different providers will expose different kinds of metadata, and different Application Integrators will want to consume that metadata in different ways. As such, the goal of this proposal is to provide a simple way for the Open Feature runtime to pass generic metadata from a provider to a hook, without Open Feature itself understanding the semantics of that metadata.

## Non-goals

In the future we may wish to standardize the semantics of some key metadata attributes which are common amongst many providers (e.g. `expiration-date`, `owner`, `management-url`) so that provider-agnostic hooks can be created to consume these standard attributes, but that is explicitly NOT in the scope of this OFEP - we would prefer to see which common attributes naturally emerge and then "pave those cow paths".

## Proposal

The Open Feature spec will be extended in two ways:
- a flag provider will be able to provide a bag of metadata attributes for a feature flag. This bag will be a set of key-value pairs, where the key will be a string and the value will be a small set of primitive values.
- a hook will be able to access these metadata attributes

*note* what follows is a VERY rough strawman proposal for one way to extend the spec. Please poke holes!

### provider interface

We add a `getMetadataForFlag(flagKey:string):FlagMetadata` method to the provider interface. 

The `FlagMetadata` has a type like `Record<string,string|boolean|number>` in typescript, where the key is the metadata attribute and the value is the metadata value.

If called with an unrecognized `flagKey`, the method MUST return an empty FlagMetadata instance.

### hook interface

The HookContext interface will gain a `flagMetadata:FlagMetadata` field. 

The SDK is responsible for calling `getMetadataForFlag` during every flag evaluation, and passing whatever was provided into the HookContext.


### other details

The contents of `FlagMetadata` must be immutable once returned from `getMetadataForFlag`. We won't support adding/removing/editing metadata in hooks, for example.

Format of the metadata attribute is left up to the provider. Maybe we provide suggestions around formatting, and a namespacing prefix (e.g. `"flags-r-us.management-url"). Following otel conventions for span attributes might be smart.

The SDK will not cache the results of the `getMetadataForFlag` call, and must call it once during every flag evaluation.

## Open Questions

- Should we also expose flag metadata in the `FlagEvaluationDetails`, in case an OF client wants to consume them directly?
