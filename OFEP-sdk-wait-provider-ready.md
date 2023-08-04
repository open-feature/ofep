## OFEP-sdk-wait-provider-ready

## State: DRAFTING
Implement a mechanism to wait for the provider to be in a ready state.

## Background

Provider can now define a `initialize` function called by the SDK when Openfeature users call the function `setProvider(...)`. 
The `initialize` function is called asynchronously and it is possible to get the information that the provider is ready while awaiting an initial ready event.

In some languages such as `javascript` waiting for the event could be one line of code, but on other languages it could need way more boiler plate code to do that.
```javascript
Openfeature.setProvider(my-provider)
const client = Openfeature.getClient()
await new Promise((resolve) => client.on(‘ready’, resolve))
```

```java
OpenFeatureAPI.getInstance().setProvider("test", g);
Client cli = OpenFeatureAPI.getInstance().getClient("test");
CompletableFuture<EventDetails> completableFuture = new CompletableFuture<>();
OpenFeatureAPI.getInstance().onProviderReady(new Consumer<EventDetails>() {
    @Override
    public void accept(EventDetails eventDetails) {
        completableFuture.complete(eventDetails);
    }
});
completableFuture.get();
```

## Proposal
It would be great to have a way in the SDKs to wait for the provider to be ready.


## Alternatives

### Alternative 1: make `setProvider` synchronous
Probably not the most ideal solution but we could change the behavior of `setProvider` to wait for the initialize function to throw or return.  
*It is a breaking change from the actual implementation.*

### Alternative 2: Add a waiting function in the SDKs to wait for the provider to be ready
Adding a waiting function will allow to block the SDK until the provider is ready.  
This new function will wait for a `ready` event or a timelimit for the provider to be ready.  

```javascript
Openfeature.setProvider(myprovider)
const client = Openfeature.getClient()
await client.isReady()
```

### Alternative 3: Chain `waitReady()` with `setProvider(...)`
Add a chain function to `setProvider(...)` to wait until the intialization is done.
It will wait for the `initialize` function to throw or return.

```javascript
await Openfeature.setProvider(myprovider).waitReady()
const client = Openfeature.getClient()
```
