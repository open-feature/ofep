## OFEP-flag-evaluator-identification

## State: DRAFTING 

OpenFeature feature flag evaluations are invoked by an application on top of the evaluation API. In the current specification,
evaluation API defines a mechanism to obtain a client with an optional client identifier.

```
OpenFeature.getClient({
  name: "my-openfeature-client",
});
```

However, this client identifier is not communicated down the line to the provider nor to the flag management system. Further,
there is no other generic identification for the application that invokes the evaluation.

In my opinion, it is possible to utilize a unique evaluator identifier to,

- Allow flag evaluation audits
- Access control mechanism at evaluation API

## Background

There are a wide variety of use cases for feature flags in applications. If focused on application deployments, they can
be mainly divided to front-end (AKA client-side) and back-end (server-side) applications. From OpenFeature spec
perspective, these deployments are aggregated as applications. However, the actual deployment of applications bring
their own challenges.

A front-end application usually runs on a browser that require evaluation API to be exposed as an HTTP endpoint.
For a such deployment, evaluation API could require access control to the API based on an application identifier.
Similarly, in a backend system with multiple services, there could be the need to isolate feature flags based on the
evaluating service. In general, this boils down to authentication of the application and authorization to evaluate.

From flag management system perspective, a key consideration could be to identify the application that invoked the 
feature flag evaluation. This could be a requirement of compliance (ex:- GDPR if a personal context is involved in the evaluation)
or a policy requirement of a specific organization.

All above use cases, it shows the importance of having a unique evaluator identification.

## Proposal

I propose to introduce or extend the existing client identifier as a unique identifier of the application, so that
it allows evaluation API, providers and flag management systems to build various extra features around the identifier.


### Implementation

This proposal may be implemented as an extension on `feature provider` interface. Or it could be possible to extend 
the `evaluation context` if it is not being misused for the purpose.

In either case, the identifier of the evaluator (application), should get propagates from evaluation API to provider and
to the flag management system.

### Generating and storing identifier

Generating process of an evaluator identifier is out of the scope of the specification. Same is true for the storage of such an 
identifier. However, if such identifier is used for access control mechanism, then security of storage must be considered.
For example, in a front-end application, this unique identifier will get exposed to the end-users. Hence, if it is being 
used for access control, then there must be other security measures to prevent misuse. 