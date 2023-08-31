---
date: 2022-07-12
title: CUE Upstream
status: Draft
authors: [Alex Jones]
tags: [flagd, spec]

---
# CUE upstream

## State: DRAFTING

As flagD evolves, it will be presented on different types of services with a variety of protocols.
Many of these protocols have client libraries that can be generated for convenience.
For example, we use openapi to enable us to create a golang server implementation.
This is great because a) it's fast and easy b) it matches the specification files promises exactly - validation/matching for free.

Given we are looking to now expand to offer new generated server support for gRPC, we are in a predicament about whether to a) derive the implementation from OpenAPI b) have a new source of truth as .proto files c) have some sort of composite between the two.

My proposal here would be to choose a new top-level DSL to define the specifications required to drive generated server code implementations. As such, cue offers integration with YAML/JSON & protobuf directly.
This would mean we could use a single file(s) and toolchain to generate all of the automatically created code for flagD.
The benefit here would be a single source of truth, ease of contribution, ease of extension and simplified build process.

![unlabelled_image](images/003-01.png "unlabelled_image")



By switching to CUE, we can use a single build chain to produce the OpenAPI spec as a generated file that is convenient to users who want to build against flagD ( possible code-generating their own client libraries). Though we would not need to use the generated OpenAPI spec through any further generator. Instead, the protoc-http tool will allow for generation from protobuf files as per @James-Milligan initial investigation.

Next steps:
If we have agreement on this, I would propose looking at a top level CUE file(s) to replace the current OpenAPI YAML file that is generated from. At this point we will be able to prove it can become the new top-of-chain build step, enabling us to then replace the downstream components.