---
date: 2023-05-19
title: Single Context Paradigm
status: Approved
authors: [Todd Baert]
tags: [sdk]

---
# Single-context Paradigm

## State: APPROVED

This draft outlines a "single-context" paradigm - an alternative pattern and set of APIs supporting client use-cases.

## Background

In contrast with server-side or other service-type applications, client side apps typically operate in the context of a single user.
Most feature flagging SDKs for these applications have been designed with this in mind.
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

Providers may need a mechanism to understand when their cache of evaluated flags must be invalidated or updated. An `on-context-set` handler can be defined which performs whatever operations are needed to reconcile the evaluated flags with the new context. The OpenFeature SDK calls this handler when the global context is modified.

```typescript

interface Provider {
  //...

  // a handler called by the SDK when context is modified
  onContextSet?(oldContext: EvaluationContext, newContext: EvaluationContext): Promise<void>

  //...
}
```

While the `on-context-set` handler is executing, the cache of resolved flags may be considered "stale". `Provider authors` and `application authors` should understand the consequences of evaluating flags in this state.

#### Initialize function

Providers may need access to the static context when they start up.
Passing this in the provider constructor is not always possible, and ergonomics are improved by separating configuration and evaluation.

An `initialize` function can be optionally implemented by a provider, which defines an parameter for the static context.

interface Provider {
  //...

  // a function called by the SDK when the provider becomes active
  initialize?(context: EvaluationContext): Promise<void>

  //...
}
```

> NOTE: The provider interface will retain the context parameter.
The parameter will be supplied by the SDK from the global context.

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

### Hook changes

#### Remove return value from before stage

Context cannot be modified at evaluation, so `before` stage 

```typescript

export interface Hook<T extends FlagValue = FlagValue> {
  //...

  // before handler no longer optionally returns an EvaluationContext
  before?(hookContext: BeforeHookContext, hookHints?: HookHints): void;

  //...
}

```
