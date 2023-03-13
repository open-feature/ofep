## Inline Evaluation of Flag Rules

## State: APPROVED

This OFEP seeks to find a solution for near-zero latency flag evaluation for server-side contexts (e.g. not mobile).

## Background

Today, most flag providers make API calls to backing services to understand if a given flag should return e.g. `true` or `false`. Even if that API call is going to a kubernetes sidecar like the flagD case, it introduces latency which may not be acceptable in high scale use-cases. The flag's rules are often evaluated on another service because determining whether the provided context matches a given set of rules requires computation which may be non-trivial or may take into account data not known by the caller.

## Proposal

To address this, I'd like to define a mechanism by which the rules can be returned to the openfeature client, and it can determine the answer of which value to return. The intent is to update these rules outside of the scope of the request lifecycle, such as at startup and/or on an interval basis.

## Updated Provider API

We would offer a stock `RuleEvaluatingProvider` that would implement the `getBooleanEvaluation` et al methods given a rule state. That rule state would be fetched by a `RuleFetcher`, which provider authors would implement. That fetcher would, for instance, download the rules from the data store and set up an appropriate update interval in the background.

When "provider ready" events are in use, `RuleEvaluatingProvider` will not emit ready until the `RuleFetcher` emits ready.

## Rule Format

The rule format use [JsonLogic](https://jsonlogic.com/), which is already setup in `flagD` and has broad support for various languages.

### What it might look like

```java
public class MyRulesProvider implements RuleFetcher {
  @Override
  public JsonLogic fetch() {
    // your code to get the flags and their rules and convert it to jsonlogic goes here
  }
}

// in your app setup code..
OpenFeature.getInstance().setProvider(new RuleEvaluatingProvider(new MyRulesProvider(API_KEY)))
```
