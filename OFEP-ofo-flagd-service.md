## flagd service deployment driven by OpenFeature Operator

## State: DRAFTING

Currently, OpenFeature Operator (OFO) manages the deployment of flagd by appending it to a pod's containers (sidecar pattern), thereby allowing containers within the pod to route to it. This OFEP campaigns for the extension of OFO to manage the deployment of externally accessible flagd (e.g. from client side applications, or even server side applications that don't want to use the sidecar pattern).

## Background

The driving force behind this is to simplify the deployment of flagd for use by client side applications. An [OFEP was drafted](./OFEP-ofo-flagd-client-support.md) to achieve this but subsequently withdrawn (reasons noted within). This OFEP recognises the limitations of the previous, presenting a modular solution with a broader scope.

## Proposal

Introduce a FlagdService custom resource definition (CRD) and controller.
The controller uses the configuration defined within the custom resource (CR) to create a Service and a Deployment of flagd (backed by the Service) in the same namespace as the CR. This is a common deployment pattern permitting access by any component that routes to the created Service (e.g. Ingress/Load Balancer). OFO already manages the [sidecar deployment pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/sidecar) to achieve the goal of internally routable flagd. In contrast, the described FlagdService pattern permits externally routable flagd.

### RBAC

OFO already has RBAC to Deployments but not Services so the following is required.

```
- apiGroups:
  - ""
  resources:
  - services
  verbs:
  - create
  - delete
  - get
  - list
  - patch
  - update
  - watch
```
