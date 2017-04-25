# Docker Pets

Docker Pets is a simple application that's useful for testing out features of Docker Datacenter.

If you are interested in a guide on how to demo Docker Pets on the Universal Control Plane then check out [this tutorial](https://github.com/mark-church/docker-pets/blob/master/DEMO-DDC.md).


## Versioning

- `1.0` is the primary version that should be used for demos.
- `2.0` is a version with minor visual changes. Use this to demonstrate rolling updates from `1.0` to `2.0`
- `broken` is a version that reports a failed healthcheck. Use this version to demonstrate an unsucessful rolling update.

## Deploying Docker Pets on Kubernetes

To better compare Swarm and Kubernetes, this page illustrates how to deploy the same `docker-pets` application on Kubernetes using K8s Services and Deployments.

## Deploying Stateless Multi-Container Docker-Pets on K8s

```
$ git clone https://github.com/mark-church/docker-pets.git
$ cd docker-pets
$ git checkout k8s
$ kubectl create -f pets-web.yaml
deployment "pets-web" created
service "web" created
```
