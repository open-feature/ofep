## OFEP - Expose flag metadata to applications

## State: DRAFTING

OpenFeature specification focuses on the evaluation of feature flags. To further enhance the application author
experience, flag metadata can be exposed to the application layer. This metadata then can be used by application authors 
for various purposes. For example, cross-validations of flags used by an application using unit tests without 
the need for evaluation API or a connection to the flag management system.

## Background

At the time of writing this document, OpenFeature API supports metadata for providers and client. With a similar 
approach, it is desirable to expose flag metadata to the application layer. This metadata then can be used for
validations, tooling and other potential improvements.

## Proposal

The content of metadata payload can vary from provider to provider. However, from OpenFeature specification perspective,
it should be possible to enforce the following details, 

- flag key 
- flag type 

From a JSON representation, this payload could look as below,

```json
{
  "key" : "MyFlag",
  "type": "boolean"
}
```

Flag metadata is exposed from the `client` through dedicated methods. There are two variants of metadata that can be
exposed,

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
identify metadata related to all the flags exposed by a **specific client**. Ideally, it should be flags belongs to the
application.

Invoking of the client can look like below,

```java
Client client = OpenFeature.getClient();

List<FlagMetadata> flagMetadata = client.getAllMetadata()
```

## Limitations

Similar to [OFEP-007: Surfacing flag metadata](/007-OFEP-provider-flag-metadata.md), metadata exposed from client must
be immutable.