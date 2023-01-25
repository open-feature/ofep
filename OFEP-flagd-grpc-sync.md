## OFEP: Add gRPC sync support to flagd

## State: DRAFTING

This OFEP proposes to introduce gRPC syncs to flagd. gRPC sync will act similar to existing remote HTTP URL syncs. But
going beyond periodic pulls, flagd can utilize gRPC server streaming to receive near real-time updates, pushed from a
flag management system.

## Background

gRPC server streaming allows clients to listen and react to server-pushed data. For flagd, this perfectly matches the
ISync interface and current sync mechanism implementations.

The gRPC schema will be defined by flagd and supporting flag management system(s) then will implement the contract.

<img src="images/ofep-fd-grpc-1.png" width="300">

Further, server push can be expanded to have `event types` such as flag updates, modifications and deletions, giving more
performant connectivity between flagd and flag management system.

<img src="images/ofep-fd-grpc-2.png" width="300">

### Taks

Following are the main tasks I am proposing for the implementation,

- [x] POC for the implementation and OFEP approval
- [ ] Introduce basic grpc sync, with minimal configuration options
- [ ] Introduce additional options, such as SSL certificates, token authentication on top of existing solution
