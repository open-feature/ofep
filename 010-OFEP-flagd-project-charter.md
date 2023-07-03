## Make flagD a full sub-project of OpenFeature

## State: PENDING REVIEW


This OFEP proposes to make flagD a full subproject of OpenFeature. The project will get a dedicated website, documentation, roadmap and charter. 

## Background

flagD started as small reference implementation for a developer-focussed feature evaluation mechanism, enabling OpenFeature SDK users to experiment with an end-to-end solution. Over time the project has grown in functionality and become stable and is now also used in production settings. 

In the past there was also some misunderstanding of the relationship of OpenFeature and flagD. 

Therefore, the project should become a full sub-project of open feature. 

## Proposal

flagD will become a dedicated sub project of the OpenFeature project. Documentation for flagD and all examples for OpenFeature will be moved to a dedicted space under the newly created domain ``openfeature.dev``.

The sub project gets it's own dedicated charter to ensure the project has clearly defined goals and scope. As a sub project flagD will have its own maintainers but will still be under the governance of the OpenFeature project. 

Below is the charter for flagD as defined by the OpenFeature governance board. 


### Charter

FlagD is an open-source project which provides a portable, lightweight, production-ready, and OpenFeature-compliant feature flag evaluation daemon, along with a supporting k8s operator and set of OpenFeature SDK providers.

The flagD project aims to provide a developer-focused, cloud-native, lightweight and extensible feature evaluation engine.

* **Developer-focused** means that flagD is configured in a declarative approach using “flags-as-code”
* **Cloud-native** means it focuses on seamless, standardised integration with cloud-native tools and practices like GitOps. * These components - like the operator - make the integration easy but are not required. 
* **Lightweight** means that flagD provides a compact and executable binary with a design focus on simplicity and ultra-fast, low-latency execution. flagD is implemented as a stateless, highly-scalable service which only requires a local flag definition or a configured endpoint to acquire the definition. 
* **Extensible** means that other projects and feature management tools can integrate easily using well-defined interfaces for rule evaluation requests and rule set definition. 
* **OpenFeature compliance** means flagd serves as a production-ready reference implementation of the OpenFeature specification and demonstrates the value of an open standard for feature flagging.

The following topics are out of scope for the flagD projects:
* Identity, storage, and attestation mechanisms
* Distributed architecture ( High availability quorum, voting, leader/follower, failover mechanics)
* Vendor modules dependencies
* A feature management and/or analytics solution (but could provide the foundations for one). The project will highlight open-source and commercial implementations which provide these capabilities and are OpenFeature compliant. 
