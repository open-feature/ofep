---
date: 2023-05-19
title: Dispose Functionality To API
status: Approved
authors: [Todd Baert ,Weyert de Boer]
tags: [api, sdk]

---
# 009-OFEP-Add dispose functionality to API

## State: APPROVED

The goal of this OFEP is to enhance the OpenFeature API to allow authors to cleanly dispose of any resources consumed by OpenFeature providers.

## Background

When implementing OpenFeature providers, you sometimes need to register event handlers, or timers or similar functionality to
correctly handle functionality of the vendor library. Some vendor libraries might also have analytics, or debugging functionality
that can be enabled and might get flushed to the vendor platform when the library gets stopped or disposed off.

Currently, you aren't able to cleanly handle these use cases in OpenFeature providers.

## Proposal

To allow clean disposal of resources consumed by OpenFeature providers, I would like to propose a function that can be called by OpenFeature SDK that allow to cleanup these resources.
The OpenFeature provider will implement a similar function that will be called internally by the OpenFeature SDK.
The function may be synchronous or asynchronous, as SDK practicalities and language idioms dictate.
In order to facilitate resource disposal paradigms of the implementing language, the precise name of the function won't be specified.
 
### Example Implementation

The `Provider` interfaces gets extended (in a non-breaking way) to include the following function:

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
