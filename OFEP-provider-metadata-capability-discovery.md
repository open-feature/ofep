---
date: 2023-04-15
title: Provider-Metadata-Capability-Discovery
status: Approved
authors: [Todd Baert]
tags: [specification, sdk]

---
# 016-OFEP-provider-metadata-capability-discovery

## State: APPROVED

This OFEP proposes a solution for "capability discovery" in the context of providers, in order to signal to the SDK and `application authors` what functionality is available in a particular provider.

## Background

As the OpenFeature specification evolves, it's to be expected that some components may not be able to support certain functionality. For instance, some providers may not support flag change events (as described in https://github.com/open-feature/ofep/pull/25). 

## Proposal

This OFEP proposes that the [`provider metadata`](https://openfeature.dev/docs/specification/sections/providers#requirement-211) be extended to include optional properties that denote which functions are available on the implementing provider. The SDK can then make intelligent decisions and log warnings if capabilities that are not supported by the provider in question, are used. For example, if an `application author` adds an event handler but the registered provider doesn't support events, the SDK can log a warning.

### Example Implementation

```typescript

import { Provider, Capabilities } from '@openfeature/js-sdk';

/**
 * The following provider supports `SomeFeature`, `ProviderEvents`, but not `SomeOtherFeature`, which are defined by the SDK.
 */
class SomeFeatureProvider implements Provider {
  readonly metadata = {
    name: 'Some Feature Provider',
    capabilities: {
      [Capabilities.SomeFeature]: true,
      [Capabilities.ProviderEvents]: true,
      [Capabilities.SomeOtherFeature]: false,
    }
  };

  // ...implementation...
}
```
