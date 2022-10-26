# Mutating Webhook no CPU limit

Kubernetes Dynamic Admission Control which removes CPU limits when creating pods

## Introduction
This chart creates a [Dynamic Admission Control](https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/) which removes any  CPU limit from the container specs from pods which are being created.

## Prerequisites
- Kubernetes 1.19+
- Helm 3.2.0+

## Installing the Chart

To install the chart with the release name `my-release`:

```console
$ helm repo add deepworx https://deepworx.github.io/helm-charts
$ helm install my-release deepworx/mutating-webhook-no-cpu-limit
```

These commands deploy mutating-webhook-no-cpu-limit on the Kubernetes cluster in the default configuration.

> **Tip**: List all releases using `helm list`

## Uninstalling the Chart

To uninstall/delete the `my-release` deployment:

```console
$ helm delete my-release
```

The command removes all the Kubernetes components associated with the chart and deletes the release.
