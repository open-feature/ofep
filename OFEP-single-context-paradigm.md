## OFEP-single-context-paradigm

## State: DRAFTING

This draft outlines a "single-context" paradigm - an alternative pattern and set of APIs supporting client use-cases.

## Background

In contrast with server-side or other service-type applications, client side apps typically operate in the context of a single user.
Most feature flagging for these applications have been designed with this in mind.
In summary, most client/web SDKs operate something like this:

- an initialization occurs, which fetches evaluated flags in bulk for a given context (user)
- the evaluated flags are cached in the SDK
- flag evaluations take place against this cache, without a need to provide context (context was already used to evaluate flags in bulk)
- Functions/methods are exposed on the SDK that signal the cache is no longer valid, and must be reconciled based on a context change. This frequently involves a network request or I/O operation.

This paradigm doesn't fit well with the existing SDK, which, like most server-side SDKs, emphasizes realtime evaluation and context-per-evaluation.

Though not all client side SDKs function in this way, those that do allow context per evaluation can conform to this model fairly easily.

## Design

To better support the "single-context" paradigm we need to define some additional handlers and add some flexibility to current APIs.
In short, the application author now sets context globally using the existing global context mutator on the OpenFeature API object.
This single context is used by providers for initialization and fetching evaluated flag values in bulk.
All evaluations functions are "context-less".
When the context is changed, providers are signalled to update their cache of evaluated flags.

### Provider changes

#### On-context-set handler

Providers must have a mechanism to understand when their cache of evaluated flags must be invalidated or updated. An `on-context-set` handler can be defined which performs whatever operations are needed to reconcile the evaluated flags with the new context. The OpenFeature SDK calls this handler when the global context is modified.

```typescript

interface Provider {
  //...

  // a handler called by the SDK when context is modified
  onContextChange?(oldContext: EvaluationContext, newContext: EvaluationContext): Promise<void>

  //...
}
```

#### Remove evaluation-context parameter on resolvers

With all evaluation context represented in the global context, resolvers no longer need it as a parameter. Providers that require context at evaluation can simply access the global evaluation context for use in their evaluation.

```typescript

interface Provider {
  //...
  
  // context parameter is removed from resolver
  resolveBooleanEvaluation(flagKey: string, defaultValue: boolean): ResolutionDetails<boolean>;

  //...
}
```

### Client changes

#### Remove evaluation-context parameter on evaluation functions

Similarly to the changes in the provider, the evaluator functions on the client do not accept a context.

```typescript
interface Client {
  //...

  // context parameter is removed from evaluation API
  getBooleanValue(flagKey: string, defaultValue: boolean, options?: FlagEvaluationOptions): boolean;
  getBooleanDetails(flagKey: string, defaultValue: boolean, options?: FlagEvaluationOptions): EvaluationDetails<boolean>;

  //...
}
```

#### Remove context mutator

The global context has a one-to-one correspondence to the providers cache of evaluated flags. It's unreasonable or impossible to reconcile multiple client-level contexts with this state. The context mutator of the client must be removed.
