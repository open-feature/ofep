## 007-OFEP-flag-change-events

## State: DRAFTING

Some flag SDKs support listening for flag value changes or general configuration changes ([launchdarkly](https://docs.launchdarkly.com/sdk/features/flag-changes), [cloudbees](https://docs.cloudbees.com/docs/cloudbees-feature-management/latest/reporting/configuration-fetched-handler), flagd). This can allow us to use an event-based paradigm for consuming flags. Client apps may use feature flags for characteristics that aren't specifically tied to a user-action, making imperative flag evaluation a less-than-ideal solution. A server application could listen to a flag that changes some operational behavior.

Examples:

- A web client's banner color could be updated when an associated flag is changed, without any user action.
- A web service could subscribe to a flag that controls its log-level.

## Design

The provider interface and the OpenFeature client would be extended to have new functionality to register handlers for a particular flag value or the configuration in general. When an _application author_ registers a handler, the provider would react by appropriately registering a listener on it's SDK, polling it's REST API, etc. If the flag (or configuration in general) is updated, the provider would call the registered handler. The handler might be called with the flag key, or perhaps some other metadata pertaining to the configuration update. **Flag values would not be provided to the handler**, the handler would simply run, indicating the associated configuration had changed. The _application author_ would then perform a flag evaluation for the changed flag. This is consistent with the aforementioned flag systems, which do not evaluate the flags when they've changed. One reason is that no dynamic context can be reasonably provided in the case of events, since the event is driven by a change in the flag management system, not a user-action.

Per-flag design:

```ts
const client = OpenFeature.getClient();

// subscribe to changes in a string flag called "hex-color", and evaluate it when it's updated
client.addHandler("hex-color", async (key) => {
  console.log(
    `Got update for ${key}, new value is ${await client.getStringValue(
      key,
      "000000"
    )}`
  );
});
```

General configuration change design:

```ts
const client = OpenFeature.getClient();

// subscribe to changes in the configuration in general, and evaluate flagd it when it's updated
// this might be easier to implement across vendors, since many don't allow subscription to a particular flag, but general configuration changes
client.on("configuration-change", async (changeMetadata) => {
  console.log(
    `Got update for configuration, new value for hex-color is ${await client.getStringValue(
      key,
      "000000"
    )}`
  );
});
```

## Benefits

Ability to use event-based flag evaluation paradigms.

## Caveats

- Not all providers can reasonably implement this... some SDKs don't support subscriptions or configuration change notifications, for example. Should these providers simply never fire events?
- Implementation in providers will likely be more divergent than imperative evaluation (based on demo work below).
- Re-evaluating a flag after the handler fires sometimes means another round-trip, but most of the time in this case, things are locally cached - really dependant on SDK implementation. This is the pattern used by some vendors though, so it's not unprecedented.
- Some SDKs can't identify individual flags have changed, so all registered handlers must fire (see cloudbees provider demo). This might not be such a big deal since they are likely no-ops.
- We may need a way to "shutdown" providers, cancelling all handlers.
- We may need a way to "move" handlers from one provider to another if the provider is changed (recreate them in the new provider).
- We should probably consider other events, like "SDK-READY" as well, which would fit well into design 2, above.

## Demo

[Proposed JS-SDK implementation](https://github.com/open-feature/js-sdk/pull/316)
[Proposed usage in flagd-web provider](https://github.com/open-feature/js-sdk-contrib/pull/142)
