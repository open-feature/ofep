## OFEP - Expose flag metadata to applications

## State: DRAFTING

OpenFeature specification focuses on the evaluation of feature flags. To further enhance the application author
experience, this proposal focuses on exposing flag metadata through dedicated client methods.


## Background

At the time of writing this document, OpenFeature API supports metadata for providers and client. With a similar 
approach, it is desirable to expose flag metadata to the application layer.

This metadata can then be used by application authors for various purposes such as validation, tooling and testing.
For example, cross-validations of flags used by an application using unit tests without the need for evaluation API 
or a direct connection to the flag management system.

## Proposal

The content of metadata payload can vary from provider to provider. However, from OpenFeature specification perspective,
it should be possible to enforce the following, 

- flag key 
- flag type 

Other vendor specific, non-sensitive data can also be present and they can be included in a dedicated `data` segment.

From a JSON representation, this payload could look like below,

```json
{
  "key" : "MyFlag",
  "type": "boolean",
  "data" : {
    "key" : "value"
  }
}
```

When it comes to API, flag metadata is exposed from the `client` through dedicated methods. 

There are two variants of metadata that can be exposed,

- Metadata of an individual flag
- Metadata of all flags 

### Metadata of an individual flag

Goal here is to identify metadata of an individual flag. Invoking of the client can look like below,

```java
Client client = OpenFeature.getClient();

FlagMetadata myFlagMetadata = client.getFlagMetadata("MyFlag")
```

`FlagMetadata` then can expose core metadata entries (ex:- key, type) and other metadata as required by implementation
through key-value pairs.

### Metadata of all flags

This could be optional due to security/performance concerns but still desired by an application author. Goal here is to
identify metadata related to all the flags exposed by a **specific client**. Ideally, it should be flags used by the
application.

Invoking of the client can look like below,

```java
Client client = OpenFeature.getClient("AppClient");

List<FlagMetadata> flagMetadata = client.getAllFlagMetadata()
```

## Limitations

Similar to [OFEP-007: Surfacing flag metadata](/007-OFEP-provider-flag-metadata.md), metadata exposed from client must
be immutable. 

Further, provider authors can ignore the implementation due to various reasons. This should give us the flexibility 
of maintaining the core focus (flag evaluation) and keeps flag metadata exposure as an add-on feature.