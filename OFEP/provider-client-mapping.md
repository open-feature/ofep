---
date: 2023-04-27
title: Provider-Client Mapping
status: Approved
authors: [Justin Abrahms]
tags: [spec]

---
# Provider to client mapping

## State: APPROVED

The goal of this OFEP is to describe a way that application authors can selectively determine which provider a given client uses. This means that they should be able to set a provider for a library that is different than what they use in their main app.

## Background

Today, we operate with [a single provider stored on a global singleton](https://github.com/open-feature/spec/blob/74c373e089ad77bf8cac84f3d93c00c945ff3a8a/specification/sections/01-flag-evaluation.md?plain=1#L25). Especially in large apps, which may have different provider needs, this is limiting. Teams could solve this in user-space with a sort of `MultiplexingProvider` which takes in N other providers. Sadly, this introduces latency (calling provider 1 before falling through to provider 2 isn't free) and waste. Additionally, when it comes to testing, the "there can be only one!" nature of global singletons makes things a giant pain.

## Proposal

To address that, we will allow application authors to provide mappings of client names to a provider of their choosing. This should allow a great degree of flexibility for app authors to choose the flag-config store that works for that particular use-case.

### Example Implementation

Authors may optionally use [a named client](https://github.com/open-feature/spec/blob/74c373e089ad77bf8cac84f3d93c00c945ff3a8a/specification/sections/01-flag-evaluation.md?plain=1#L60), which we already support. If they don't pick a name, it falls through to the configured "default" provider (or no provider if none are set).

```java
# example library code
var client = OpenFeature.getInstance().getClient('my-sweet-library')
if client.getBooleanValue('redesign-enabled?', false) {
  # ...
}
```

```
# application author
OpenFeature.setProvider(OpenFeature.DEFAULT_PROVIDER, new FlagDProvider())
OpenFeature.setProvider('my-sweet-library', new FileBasedProvider('path/to/myfile'))
```

At this point, things will use flagD by default. The example library will use a file-based provider.
