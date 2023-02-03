## Add dispose functionality to API

## State: DRAFTING

The goal of this OFEP is to enhance the OpenFeature API to allow authors to cleanly dispose of any resources by consumed by OpenFeature providers.

## Background

When implementing OpenFeature providers, you sometimes need to register event handlers, or timers or similar functionality to
correctly handle functionality of the vendor library. Some vendor libraries might also have analytics, or debugging functionality
that can be enabled and might get flushed to the vendor platform when the library gets stopped or disposed off.

Currently, you aren't able to cleanly handle these use cases in OpenFeature providers.

## Proposal

To allow to cleanly dispose of resources consumed by OpenFeature providers, I would like to purpose a `dispose`-function that
can be called by OpenFeature SDK to allow to cleanup these resources. The OpenFeature provider will implement an async function
named `dispose` that can be called by the internal OpenFeature SDK.
 
### [Example] Implementation

The `Provider` type gets extended with the following function:

```typescript
dispose(): Promise<void>
```

The function can be called by the the `API` instance when it requests the resources that need to be disposed off, for this reason, 
the global API needs to be enhanced to also have the `dispose`-function:

```typescript
dispose(): Promise<void>
```

A potential implementation could be the following in the Node SDK:

```typescript
async dispose(): Promise<void> {
   await this.provider.dispose()
}
```
