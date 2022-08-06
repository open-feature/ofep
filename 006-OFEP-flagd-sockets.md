## NAME

## State: ( DRAFTING )

Often when flagD is required to talk to another application within the same pod, it is far faster to use a unix socket 
than the full TCP/IP stack. There are also permission benefits around using a socket in terms of file ownership.
This OFEP outlines an approach to use gRPC over Unix sockets to enable this.


## Background

It is possible within golang to use a unix socket as a `*net.Conn`
The following illustration exemplifies how it can be used to create the underlying gRPC transport.

```
conn, err := net.DialUnix("unix", nil, "unix://proc/flagD.sock")
	return conn, err

conn, err := grpc.Dial(server_file, grpc.WithInsecure(), grpc.WithDialer(UnixConnect))
	if err != nil {
		log.Fatal("did not connect: %v", err)
	}
	defer conn.Close()
```

This shows how the machinery is already present to enable IPC through this interface.

## Proposal

I propose that we introduce an additional layer of gRPC options in the `grpc_service.go` in flagD.
This would allow a new `serveSocket` method to be created and facilitate the IPC functionality.
_Note this wouldn't be a TLS enabled transport_

## Sections

From this point onwards, the sections and headers are generally freeform depending on the OFEP. Sections are styled as "Heading 2". Try to organize your information into self-contained sections that answer some critical question, and organize your sections into an order that builds up knowledge necessary (rather than forcing a reader to jump around to gain context).

Sections often are split further into sub-sections styled "Heading 3". These sub-sections just further help to organize data to ease reading and discussion.

### [Example] Implementation

Many OFEPs have an "implementation" section which details how the implementation will work. This section should explain the rough API changes (internal and external), package changes, etc. The goal is to give an idea to reviews about the subsystems that require change and the surface area of those changes. 

This knowledge can result in recommendations for alternate approaches that perhaps are idiomatic to the project or result in less packages touched. Or, it may result in the realization that the proposed solution in this OFEP is too complex given the problem.

For the OFEP author, typing out the implementation in a high-level often serves as "rubber duck debugging" and you can catch a lot of issues or unknown unknowns prior to writing any real code.
