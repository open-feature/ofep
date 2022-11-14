## ??-OFEP-provider-metadata-feature-discovery

## State: DRAFTING

This OFEP proposes a solution for "feature discovery" in the context of providers, in order to signal to the SDK and `application authors` what features are available in a particular provider.

## Background

As the OpenFeature specification evolves, it's to be expected that some components may not be able to support certain features. For instance, some providers may not support flag change events (as described in https://github.com/open-feature/ofep/pull/25). 

## Proposal

This OFEP proposes that the [`provider metadata`](https://docs.openfeature.dev/docs/specification/sections/providers#requirement-211) be extended to include optional properties that denote which features are available on the implementing provider. The SDK can then make intelligent decisions and log warnings if features that are not supported by the provider in question, are used. For example, if an `application author` adds an event handler but the registered provider doesn't support events, the SDk can log a warning.

### Example Implementation

```typescript

import { Provider, Functions } from '@openfeature/js-sdk';

/**
 * The following provider supports `SomeFeature`, `ProviderEvents`, and `SomeOtherFeature`, which are defined by the SDK.
 */
class SomeFeatureProvider implements Provider {
  readonly metadata = {
    name: 'Some Feature Provider',
		features: {
			[Functions.SomeFeature]: true,
			[Functions.ProviderEvents]: true,
			[Functions.SomeOtherFeature]: false,
		}
  };

	// ...implementation...
}
```