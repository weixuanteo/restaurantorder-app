# IS213 ESD Project - Restaurant Ordering System

### Table of Contents
- [Local Development Setup](#local-development-setup)
  * [Enabling Kubernetes on Docker Desktop](#enabling-kubernetes-on-docker-desktop)
  * [Deploying MariaDB](#deploying-mariadb)
  * [Deploying Owner Service](#deploying-owner-service)
  * [Deploying NGINX Ingress](#deploying-nginx-ingress)
  * [Port Forward MariaDB](#port-forward-mariadb)
  * [Test Owner Serivce](#test-owner-serivce)
- [Kubernetes Cheatsheet](#kubernetes-cheatsheet)
  * [Some basic commands](#some-basic-commands)

### Local Development Setup
This local setup should be applicable to MacOS (ARM64, AMD64), Windows

See [Kubernetes Components](https://kubernetes.io/docs/concepts/overview/components/) for the overview of what makes up Kubernetes

#### Enabling Kubernetes on Docker Desktop

Open Docker Desktop, go to Settings, enable Kubernetes
![dropbox screenshot](https://uc356e5dbe496753a1e7e7db7f00.previews.dropboxusercontent.com/p/thumb/ABF2dQSeMOKQFb8oSobYnChLP0gxcDGWxlvqk7NJAm5btv24rkOpumbiRXZWIY72-eLmPNYsHykoZwq0ixWXjqZftlfqyZLGCDwx7z_zp4O5krHUpCnqeFbc_J_6hzu2pHoHIHN0VKA9HK1msfmPTVl_WAPf_xdaTooFEQlKfGKGTysMgBy6x5YCwYB1Bu4MsPz3qAsE8n9ys_-D22tMiFlW4CuyKW2jbChEcAjlX7dfbNPHTrhdeuqR57_2bXRDxSIyf9yBplWbFXtG07hOoATU5qR9cBz1aeKNiurfOMSDsz_tds1FBnPYjCNNJNgBj-SJNvvPh43H9mDuNd1VJ8jXJLgwsYL1EmZ8pA5hqIRwKzHnEZREA0yU8NuldbaIMTLJ2_81dCEcCDByi6p-71dO/p.png)

Select "Apply & Restart", Docker will take some time to install Kubernetes.

#### Deploying MariaDB
When a Pod is destroyed, all data will be lost stored on the container will be lost. To avoid this, [Persistent Volume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) is used so regardless of the container running MariaDB, the data will not be lost.

Go to the project directory of k8s
```bash
kubectl create -f mariadb-pv.yaml
```
```bash
kubectl create -f mariadb-definition.yaml
```

#### Deploying Owner Service
```bash
kubectl create -f owner-definition.yaml
```

#### Deploying NGINX Ingress
Containers inside of Kubernetes cluster are by default not accessible outside of the Kubernetes cluster. To access the container services, a load balancer is required to expose the internal container services to the outside world. NGINX Ingress Controller is a open source project that can be used as a load balancer inside a Kubernetes cluster.

See: https://kubernetes.github.io/ingress-nginx/deploy/
```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v0.44.0/deploy/static/provider/cloud/deploy.yaml
```

The YAML file below configures the load balancer and creates a route to owner service at /owner/registration
```bash
kubectl apply -f ingress.yaml
```

#### Port Forward MariaDB
To gain access to the database instance inside the Kubernetes cluster, port forwarding is required to expose the MariaDB to the local machine.
Replace the mariadb service name with your mariadb name, you can get this by running `kubectl get pods`
```bash
kubectl port-forward mariadb-775cdb9467-qjhln 3306:3306
```

Install MySQLWorkbench
In MySQLWorkbench, create a connection to MariaDB with 127.0.0.1:3306, both username and password are root.

Run the following MySQL Statement. This is needed because Flask-SQLAlchemy by default does not create the database/schema.

```mysql
CREATE DATABASE owner;
```

#### Test Owner Serivce
Open up Postman and create a POST request to localhost/owner/registration to create a new owner

![postman screenshot](https://uc079f5d8e62da4d9720a608eba9.previews.dropboxusercontent.com/p/thumb/ABFQLWIDHSvJuzAgj3oQZeRENlitvIHAunr0UAHHJSVt44xIUczkIRcqSTTNoW7B4GUZxrHXWsspnfAaakIBlHer5IbzwZl24R0Rnli8lep8c3x8N7Rm91OKLGSBIpcq1z4KnJEymcI_KOMh2jO68Nh0KgqBtcxMzqBDKqTaVHDAbunfAKtt01mEZJ_BB26XZBWy7hRIrfFlE2sqLtlJKfW4dqzvyLU8O5otxhgdjGJ3yAebhE_SjvDPv-3Bcky_rFMbe1jQmpe54ZywwCeETlJoz_bRF5bg7RYvkljwi-_Qa2a8AMu-WNyHC5iU6P9T8xmRrihoh0jXlWZW1mkWBr8QQA0jm-Vmb-eiIzaM8yrAUV-PhUEEJxPVovo5hX2KbJ7PY5eI3TGc7KFdx8Y6qWqr/p.png)

Set a JSON request body in Postman with the the POST request. The request is a success if the a similiar message to the one above appears

### Kubernetes Cheatsheet

`kubcectl` is the main command to interact with a Kubernetes cluster, just like `docker` command is used to interact with Docker Desktop. Check out the cheatsheet below for the command syntax of some that are commonly used 


[Kubernetes Command Cheatsheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)


#### Some basic commands
Get nodes (machine that runs Kubernetes on)
```bash
kubectl get nodes
```

Get all running pods (container)
```
kubectl get pods
```

Get all running services
```bash
kubectl get svc
```

Create container/service
```bash
kubectl create -f <some yaml file here>.yaml
```
```bash
kubectl apply -f <some yaml file here>.yaml
```

Replace or Update container/service
```bash
kubectl replace -f <some yaml file here>.yaml
```

Delete a container/service
```bash
kubectl delete -f <some yaml file here>.yaml
```
