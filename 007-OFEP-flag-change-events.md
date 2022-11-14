## 007-OFEP-flag-change-events

## State: DRAFTING

Some flag SDKs support listening for flag value changes or general configuration changes ([launchdarkly](https://docs.launchdarkly.com/sdk/features/flag-changes), [cloudbees](https://docs.cloudbees.com/docs/cloudbees-feature-management/latest/reporting/configuration-fetched-handler), flagd). This can allow us to use an event-based paradigm for consuming flags. Client apps may use feature flags for characteristics that aren't specifically tied to a user-action, making imperative flag evaluation a less-than-ideal solution. A server application could listen to a flag that changes some operational behavior.

Examples:

- A web client's banner color could be updated when an associated flag is changed, without any user action or a page reload.
- A service could subscribe to a flag that controls its global log-level.
- A subsystem could be restarted with the new flag value.

## Design

The provider interface and the OpenFeature client would be extended to have new functionality to register handlers for a set of events defined by the SDK (`ProviderEvents`). When a _application author_ registers a handler on a client, the client the client maintains this handler. The provider emits events or runs a callback indicating that it received a certain event, optionally providing data associated with that event. The callbacks registered with the client are then invoked with this data (`EventData`).

In the case of the aforementioned flag systems, flags are not actually evaluated when configurations are changed. One reason is that no dynamic context can be reasonably provided in the case of events, since the event is driven by a change in the flag management system, not a user-action. In these cases, the `EventData` would not contain flag values and the application author would have to evaluate flags in the registered handler. This is consistent with the event APIs already existing in those systems.

How it looks implemented in a Provider:

```ts
import { Provider, EventingProvider, ProviderEvents } from './types';

/**
 * The No-op provider is set by default, and simply always returns the default value.
 */
class MyEventingProvider implements Provider, EventingProvider {
  readonly metadata = {
    name: 'My Eventing Provider',
  } as const;

  // ...

  // the SDK listens for events, and fires associated handlers the application-author adds.
  readonly events = new EventEmitter();

  // pollDataSource a conceptual method specific to this provider that fires a callback if the flag source-of-truth of this provider changes.
  this.pollDataSource((newFlagData) => this.events.emit(ProviderEvents.ConfigurationChanged, newFlagData))

  // ...

```

How it looks for an `application author`:

```ts
OpenFeature.setProvider(new MyEventingProvider());

const client = OpenFeature.getClient();

// subscribe to ProviderEvents.ConfigurationChanged events
client.addHandler(ProviderEvents.ConfigurationChanged, (eventData: EventData | undefined) => {

  // the exact structure of the EventData is not covered in this OFEP
  if (eventData.changes.myFlag) {
    onMyFlagChange();
  }
  onAnyChange();
});
```

## Benefits

Ability to use event-based flag evaluation paradigms; attaching event handlers for specific occurrences. This is particularly useful for reacting to configuration changes, provider readiness, and errors. Such event-based models are particularly useful for web frameworks such as React and Angular.

## Caveats

- Not all providers can reasonably implement this... some SDKs don't support subscriptions, for example. Should these providers simply never fire events? I've attempted to partially address this with: https://github.com/open-feature/ofep/pull/36
- We may need a way to "shutdown" providers, cancelling all handlers - this is addressed by: https://github.com/open-feature/ofep/pull/30

## Demo

[Proposed JS-SDK implementation](https://github.com/open-feature/js-sdk/pull/316)
[Proposed usage in flagd-web provider](https://github.com/open-feature/js-sdk-contrib/pull/142)
