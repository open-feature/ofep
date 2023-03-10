## OFEP: Pluggable OpenFeature providers for flagd evaluation engine

## State: DRAFTING

This OFEP proposes to introduce an adapter mechanism for plugging in OpenFeature providers as the evaluation engine for flagd.
Being a Go project, flagd would be capable of utilizing any OpenFeature provider written in Go as its evaluation engine. This
allows the benefits of the flagd architecture and cloud-native solutions like the open-feature-operator to be used in tandem
with the agnostic backend offering of OpenFeature providers.

## Background

Flagd is the exemplar OpenFeature solution for feature flagging, being a required provider for all OpenFeature SDKs for all languages, thus offering the best support for getting started with OpenFeature.

In the Go ecosystem, OpenFeature provides support for a number of feature flagging systems.

While flagd itself is accessible by OpenFeature SDKs with the provider implementation, the flagd backend itself has independent implementations for evaluation logic with the `IEvaluator` interface.

## Proposal

I propose a plugin mechanism or adapter pattern for OpenFeature `Provider` implementations to be used as an `IEvaluator` for flagd to allow configurable backends.

### Implementation

Go builds static binaries, but as of 1.17 they introduced support for plugins loading from shared objects. Let's cover some options:

1. PENDING REVIEW: Refactor to a plugin-oriented architecture with flagd, dynamically loading a configured shared object. The existing built-in configuration options would skip the plugin entirely so current evaluators would continue to work as expected.
2. TODO: Independent builds per provider. This means we would have the original `flagd` binary, and now also `flagd-split`, `flagd-cloudbees`, etc. 

#### Plugins

There are two sides to this:

1. The flagd plugin implementation
2. The flagd plugin loader

The two of these would require a shared interface definition that the plugin exports an implementation of, and the plugin loader would load and validate that export.

If a valid `IEvaluator` is defined, for example, we can utilize that directly for the flagd evaluation engine.

If an OpenFeature `Provider` is defined, we could utilize an adapter on this to automatically support any OpenFeature `Provider` at runtime.

ℹ️ We could also provide an OpenFeature `Client` adapter, which would allow a combination of providers and hooks to be utilized to automatically instrument metrics and more as part of the flagd evaluation engine. This case showcases how the versatility of the plugin architecture would allow teams to utilize flagd for their environment and use cases. An example of this would be an OpenFeature `Client` wired up with custom StatsD, event dispatcher, and OTel hooks executing against an in-house feature flagging system's `Provider` definition.

Go has plugin support with the [plugin][go-plugin-docs] package. You can use this to load a compiled plugin and access its exported properties and functions. Build constraints may also be useful as part of our build process, but not necessary like our export types.

##### Example

The providers can define their own plugin definition, or a lightweight wrapper could be written in flagd. A custom `IEvaluator` implementation could be provided which could utilize hooks and providers.

**An example with an existing Provider**

```go
// go:build openfeature-plugin
package main

import (
	fromEnv "github.com/open-feature/go-sdk-contrib/providers/from-env/pkg"
    "github.com/open-feature/go-sdk/pkg/openfeature"
)

const Plugin *openfeature.Provider = &fromEnv.Provider{}
```

Now for flagd, the implementation for loading plugins and utilizing these directly for the evaluation engine would look like this (sans adapter boilerplate):

```go
import (
    "errors"
    "github.com/open-feature/go-sdk/pkg/openfeature"
)

func loadEvaluatorPlugin(pluginName string) (*IEvaluator, error) {
    p, err := plugin.Open(pluginName)
    if err != nil {
        return nil, err
    }

    plugin, err := p.Lookup("Plugin")
    if err != nil {
        return nil, err
    }

	typeEvaluator, ok := plugin.(*IEvaluator)
	if ok {
		return typeEvaluator, nil
	}

    typeProvider, ok := plugin.(*openfeature.Provider)
    if ok {
        return ProviderEvaluatorAdapter{typeProvider}, nil
    }

    typeClient, ok := plugin.(*openfeature.Client)
    if ok {
        return ClientEvaluatorAdapter{typeClient}, nil
    }

    return nil, errors.New(fmt.Sprintf("Plugin %s type was invalid", pluginName))
}
```

Since Go can also validate that type casting is successful, this allows us to ensure we are receiving valid plugins before passing them into their relevant adapter. This has been done in other projects using plugins like go-ipfs. See [an example][go-ipfs-plugin-example] from their repository.


### Independent Bundled Builds

TODO: Provide more information on bundle build approach.

<!-- References -->
[go-plugin-docs]: https://pkg.go.dev/plugin@master 
[go-ipfs-plugin-example]: https://github.com/FatProteins/go-ipfs/blob/v0.4.19/plugin/loader/load_linux.go#L52-L68
