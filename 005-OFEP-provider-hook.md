## 005-OFEP-provider-hook.md

## State: DRAFTING

As a part of the Provider implementation by the Flag Management Systen, there is a need to have standardized support for hooks specific to the Provider. The 
Provider Hook(s) should be specific to the provider implementation and implement the various defined stages of the Hook interface as applicable to the 
specific provider. 

## Assumptions

The Provider Hook is transparent to the application developer. The Provider may choose to document certain default behavior/feature in specific stages of the 
Provider Hook as relevant to the application and the application developer may be allowed to override the default feature. 

## Example Use Case

Flag Management System X provides the option to add Experimentation as an extension of Feature Flag. The user creates a Feature Flag, runs basic on/off 
evaluations of the Feature targeting specific audience and then wants to run A/B tests and hence adds the Experimentation aspects to the Feature Flag.

The Provider needs to generate event specific to the Experimentation implementation  on successful flag evaluation. The system wants to use a Provider Hook 
to do the following for each evaluation  
1. Run initialization operations (Use the _before_ stage of the Hook)
2. Run an event publish operation on successful flag evaluation operation (Use the _after_ stage of the Hook)
3. Provide the option to the application developer to override the event publish operation 
   1. The application developer may choose not to immediately publish the event on evaluation, but decide to publish it (or not) later based on other 
      application specific logic

For applications not required to override the default behavior, there is no extra step needed to add any other hooks. The Provider Hook is transparent to 
the application developer.

## Example Workflow

1. At the time of registering the provider (OpenFeature.setProvider), Provider implementation can register one or more Provider Hook(s)
2. Provider Hook implements the _before_ and _after_ and any other relevant stages to run the relevant provider logic.
3. Provider documents the relevant default behavior (e.g. automatic publish of Experimentation event on successful evaluation)
4. Provider provides an implementation of an Invocation Hook to override this default behavior as a part of the Provider SDK. 
5. If needed, the application developer uses the invocation hook to override specific default behavior of the provider by using Hook Hints e.g. turn off 
   default event publish behavior

## Hook Ordering

The Hooks should be executed in specific order.

* before: API, Client, Provider, Invocation
  * Provider does initialization before Invocation
* after:  Invocation, Provider, Client, API  
  * Provider runs after Invocation so that it can turn off default behavior if the application chooses to override it
* error (if applicable): Provider, Invocation, Client, API
* finally: Provider, Invocation, Client, API

