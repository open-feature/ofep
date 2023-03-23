## flag service deployment driven by OpenFeature Operator

## State: APPROVED

Currently, OpenFeature Operator (OFO) manages the deployment of a flag provider (e.g. flagd) by appending it to a pod's containers (sidecar pattern), thereby allowing containers within the pod to route to it. This OFEP campaigns for the extension of OFO to manage flag providers by abstracting a Kubernetes Deployment resource.

## Background

The driving force behind this is to simplify the deployment of flag providers for use by client side applications. An [OFEP was drafted](./OFEP-ofo-flagd-client-support.md) to achieve this but subsequently withdrawn (reasons noted within). This OFEP recognises the limitations of the previous, presenting a modular solution with a broader scope.

## Proposal

Introduce a FlagService custom resource definition (CRD) and controller.
The controller uses the configuration defined within the custom resource (CR) to create a Service (in OFO's namespace) and a Deployment of a flag provider (backed by the Service) in the same namespace as the CR. This is a common deployment pattern permitting access by any component that routes to the created Service (e.g. Ingress/Load Balancer). OFO already manages the [sidecar deployment pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/sidecar) to achieve the goal of an internally routable flag provider. In contrast, the described FlagService pattern permits an externally routable flag provider.

### RBAC

OFO already has RBAC to Deployments but not Services so (at minimum) the following is required.

```
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  creationTimestamp: null
  name: manager-role
  namespace: open-feature-operator-system
rules:
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

This restricts OFO's Service mutation scope to within its namespace.
