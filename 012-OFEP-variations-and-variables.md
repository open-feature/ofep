## Variations and Variables

## State: DRAFTING

Introduce two new kinds of evaluations under individual features called **variations** and **variables**, next to feature flag's own value. This will allow OpenFeature SDKs to support a wider range of feature management use cases with already existing tools.

## Background

The SDK API currently exposes various type-specific methods for evaluating a feature flag's single value:

```js
import { OpenFeature } from "@openfeature/web-sdk";

OpenFeature.setProvider(new YourProviderOfChoice());

const client = OpenFeature.getClient();

// evaluation
const isEnabled = client.getBooleanValue("my_feature", false);
```

The evaluated value could have been of other types as well, including:

- `String`
- `Number`
- `Object`

## Proposal

This proposal aims to look at feature management as a broad topic, where flags are one of the implementations.

OpenFeature, in its current form, is designed to support feature flags alone with their own single value.

In real world implementations of various different tools (both Open Source and SaaS), we notice that the feature flags go beyond just a single value, even if that single value can be of various different primitive types for different use cases.

This is where we introduce the concept of **Variations** and **Variables**.

## Kinds of evaluations

### Flags

This is solely for checking if the feature flag itself is enabled or not, and is always of `Boolean` type.

Example:

```js
const featureKey = "my_feature";
const defaultState = false;

const isEnabled = client.isEnabled(featureKey, defaultState);
```

### Variations

We now enter the realm of A/B testing and experimentation.

An experiment consists of different variations (which are usually of `String` type), and the user is consistently bucketed (assigned) into one of its variations, irrespective of the device or session the user is in.

You can think of an experiment named `my_experiment`, that can have two variations:

- `control`: the default behaviour
- `treatment`: the new behaviour that we wish to test

A user will be bucketed into one of these variations, and will stay in that variation for the duration of the experiment.

Example:

```js
const featureKey = "my_experiment";
const defaultVariation = "control";

const variation = client.getVariation(featureKey, defaultVariation);
```

#### Weights

Each variation is also associated with a weight, which is a number between 0 (0%) and 1 (100%), and represents the probability of the user being bucketed into that variation. The total weight of all variations in an experiment must be 1.

This level of details is something to be handled at Provider level, and not the OpenFeature SDKs.

#### Measuring success

Applications will be tracking various different conversion goals (like successful user sign ups, purchases, etc). Based on the variation the user is bucketed into, we will be able to track the conversion goal events against each variation of the experiment over a period of time, and decide which variation is the winner.

OpenFeature SDKs will not be involved here.

### Variables

Feature management can go beyond just on/off values for the flag itself and supporting a mechanism for a/b testing with variations.

We may also want to support the concept of variables for supporting configuration to be deployed independently of our applications, which are values that can be changed over time.

These values can be of various different primitive types for different use cases.

You can think of a feature named `my_feature`, that can have several variables scoped under it:

- `showSidebar`: boolean
- `buttonColor`: string
- `allowSignup`: boolean

The variable values can be evaluated against the context that already exists in the SDK, and can also react further based on the bucketed variation if there's an experiment involved.

Example:

```js
const featureKey = "my_feature";
const variableKey = "showSidebar";
const defaultValue = false;

const showSidebar = client.getVariableBoolean(featureKey, variableKey, defaultValue);
```

## Summarizing the feature model

Three different kinds of values under a single feature:

- Flag status (`Boolean`)
- Variation (`String`)
- Variables:
  - key (`String`)
  - Value (`Boolean`, `String`, `Number`, `Object`)

**Note**: It is worthwhile to expand the `Number` type into more explicit types like `Integer` and `Double`, especially when dealing with SDKs in strongly typed languages.

## API directions

With the new kinds of evaluations scoped under a single feature, we can consider the following API allowing more tools to create Providers targeting OpenFeature SDKs in various languages:

```js
import { OpenFeature } from "@openfeature/web-sdk";

OpenFeature.setProvider(new YourProviderOfChoice({
  // purely up to Providers to define this API
  onActivation: () => console.log("handle experiment activation for tracking purposes")
}));

const client = OpenFeature.getClient();

client.setContext({
  userId: "123",
  country: "nl",
});

const featureKey = "my_feature";
const variableKey = "showSidebar";

// feature flag's own status (always a boolean)
const isEnabled = client.isEnabled(featureKey, false);

// variation for a/b testing (always a string)
const variation = client.getVariation(featureKey, "control");

// variables (could be various different types)
const showSidebar = client.getVariableBoolean(featureKey, variableKey, false);
```

## Additional notes

The proposal is primarily motivated for integrating [Featurevisor](https://featurevisor.com) with OpenFeature SDKs, which is an open source Git-based feature management tool supporting the proposed model.

If approved, this model can be used by other tools as well opening up OpenFeature's adoption to even a wider community.

Regarding the proposed API, you can refer to documentation of Featurevisor SDK for getting a feel of real-world usage:

- [`isEnabled`](https://featurevisor.com/docs/sdks/#checking-if-enabled)
- [`getVariation`](https://featurevisor.com/docs/sdks/#getting-variations)
- [`getVariable`](https://featurevisor.com/docs/sdks/#getting-variables)
