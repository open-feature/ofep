## 005-OFEP-flagd-update-subscribers

## State: DRAFTING

Using gRPC streams we can create subscribers to allow for client side updates to be driven from flag value changes in situations where a flag will not be re-evaluated, such as those involved in startup.

## Issues

1. What is the process that will be used to subscribe to changes on a flag - will multiple client connections be spun up or will one connection handle all updates?
2. What will the schema look like for the subscription requests and updates - will these changes be incorporated into the existing interface or will they sit on a separate one?
3. If we choose to implement this in the rest interface of flagd, how will this be done? (websockets, server push or not at all?)

## Design

To aid with the simplicity of both the client and server implementations for the subscribers I propose that a single grpc stream is opened for each flag. This will reduce the requirement of routing the received flag values on the client side, the downside of this is an increased number of open connections.

![image](https://user-images.githubusercontent.com/75740990/178506014-e6cefc43-4a44-4158-a2e2-86f84797d817.png)

In this example the context is sent with the subscription request and will be used in the flag evaluation once an updated flag value is received, a state Is also stored to ensure only deltas are sent - preventing repeated values being received client side.

![image](https://user-images.githubusercontent.com/75740990/178506204-1496289f-d729-4a22-b352-6173cb01823e.png)

In this example no context is present, this may be required when the context value is likely to change following the subscription to a given flag key. In this example the client receives a notification of change and can then request the new flag value via the standard grpc/rest interfaces.

Its likely that both of these will need to be present and the interface will contain pairs of subscribers, such as SubscribeToBoolean and SubscribeToBooleanNoContext 