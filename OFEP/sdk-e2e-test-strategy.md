---
date: 2023-07-25
title: SDK end-to-end test strategy
status: Approved
authors: [Michael Beemer, Todd Baert, Kavindu Dodanduwa, Justin Abrahms]
tags: [specification, sdk, flagd]

---
# SDK end-to-end test strategy

## State: APPROVED

This OFEP proposes to introduce a simplified process to write SDK end-to-end(e2e) tests

## Background

SDKs are at the core of OpenFeature as they contain language specific implementations of the OpenFeature specification [^1]

For testing of the SDKs, current approach uses gherkin step definitions [^2] contained in OpenFeature/test-harness [^3] repository.
And the test implementations use a real instance of flagd [^4] to validate test rules.

The current approach however comes with a problem. As SDK tests rely on flagd, these tests rely on SDK contributions [^5].
This means:

- SDK cannot introduce tests until flagd contribution is there
- Breaking changes require disabling e2e tests until
  - Changes propagate to respective SDK contribution repository
  - flagd implements the breaking change
- Cannot write tests till
  - flagd implements the feature

Besides, there is a circular dependency among `Go SDK` - `Go SDK Contribution` - `flagd` [^6] which will become harder to maintain in the long run.

## Proposal

Given OpenFeature has a lot of community interest and SDKs, I am proposing to introduce a simplified e2e test strategy.
The test strategy must comply with the following:

- Tests must not use mocks and must run against an OpenFeature compliant provider
- Tests must be self-contained except for test definitions which are common to all SDKs
- Tests must verify error scenarios 

To fulfill these needs, I am proposing a simple in-memory provider to be built into the SDK and maintained alongside the SDK implementation. 

## In-memory provider

In-memory provider should be bundled with SDK and must not have any unique external dependencies, other than the ones coming from SDK itself. 
While it mainly serves SDK testing, SDK consumers may use it for their use cases. Hence, the packaging, naming and access modifiers must be set appropriately.

With this background, I am proposing following features for the in-memory provider,

- Flag structure definition will be based on test requirements and must be minimal
- Provider is initiated with a pre-defined set of flags provided to constructor
- EvaluationContext support should be provided through callbacks/lambda expressions to minimize implementation
- Must provide SDK contract implementations where needed (ex:- consider `NoOpProvider` [^7])
- Must continue to support new spec enhancements. For example, support for events

[^1]: https://openfeature.dev/specification/
[^2]: https://cucumber.io/docs/gherkin/reference/#steps
[^3]: https://github.com/open-feature/test-harness/tree/main
[^4]: https://github.com/open-feature/flagd/tree/main 
[^5]: https://github.com/open-feature/java-sdk/blob/main/src/test/java/dev/openfeature/sdk/e2e/StepDefinitions.java#L3
[^6]: https://github.com/open-feature/flagd/blob/main/flagd/go.mod#L69
[^7]: https://github.com/open-feature/java-sdk/blob/main/src/main/java/dev/openfeature/sdk/NoOpProvider.java#L8
