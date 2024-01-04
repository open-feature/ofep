## Flag Evaluation Wire Protocol

## State: DRAFTING

Create a wire protocol for RPC-based flag evaluation compliant with the OpenFeature specification.

## Background

OpenFeature offers a vendor-agnostic SDK that works across various open source and commercial offerings.
Developers can choose the provider they want to use and include it in their codebase.
This works well when a high-quality provider exists, and it's acceptable to include a vendor-specific dependency.
However, that's not always the case.
For example, many open source applications could benefit from having a standardized means of including feature flags.
A flag evaluation wire protocol would allow developers to choose the architecture that best fits their needs.

## In-process vs Remote Evaluation

Many feature flag vendors offer SDKs that perform flag evaluation in-process.
This provides fast and consistent flag evaluations with no additional deployment complexities.
Remote evaluation logic can be written in a single language and be used interchangeably with any system complying with the wire protocol.
That makes it ideal for open source projects that need a vendor-agnostic solution for feature flags.

## Action items

- Review the [existing proto schema](https://github.com/open-feature/schemas/blob/main/protobuf/schema/v1/schema.proto) to identify ways to make it provider agnostic.
- Create a new proto schema that defines a general RPC-based flag evaluation based on the OpenFeature provider specification.
- Publish the proto schema to the [Buf registry](https://buf.build/open-feature)
- Create RPC providers for every OpenFeature SDK
- Create reference flag evaluation server implementations
  - flagd
  - Go Feature Flag
- Write documentation on how to create a new flag evaluation server.
- Support feature flag vendors in creating a flag evaluation service.
- Extend the OpenFeature ecosystem registry to include flag evaluation server implementations.
- Integrate with various open source projects looking to include feature flags.

## Prior art and alternatives

### Alternative 1: Use the existing flagd proto schema

As an alternative to creating a new proto schema, we could reuse the existing flagd schema.
This schema already complies with the OpenFeature specification and provides a working end-to-end implementation.

The drawbacks to this alternative are:

- The schema contains references to flagd
- The schema was not designed to be provider agnostic

## Open source projects that may be interested in a wire protocol

- OpenTelemetry demo application
- Jenkins
- Quarkus
  - https://github.com/quarkusio/quarkus/issues/28032
- Dapr
