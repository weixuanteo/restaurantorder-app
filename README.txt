# INSTALLATION AND SETUP GUIDE FOR ESD TEAM B Restaurant Ordering System
# This installation includes both MacOS and Windows setup instructions as some of the steps will defer due to the OS.


## Kubernetes installation
Using Docker Desktop, go to Preferences, select Kubernetes, Enable Kubernetes, Apply & Restart.
After some time, Kubernetes should be installed successfully. Open Terminal/CMD, type `kubectl get nodes` to verify that docker-desktop is listed.



## NGINX Ingress Controller installation
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v0.44.0/deploy/static/provider/cloud/deploy.yaml



## RabbitMQ Installation
kubectl apply -f "https://github.com/rabbitmq/cluster-operator/releases/latest/download/cluster-operator.yml"

-- Check that it created successfully
kubectl get all -n rabbitmq-system

-- Create an instance of RabbitMQ in Kubernetes
At project root folder,
cd k8s
kubectl apply -f rabbitmq.yaml

-- Create "serviceuser" in RabbitMQ Management Console (serviceuser is used by order and notification service to publish and retrieve messages on queue)
Credentials retrieved from Kubernetes needs to be decoded to base64. 

[MACOS]
username="$(kubectl get secret esd-rabbitmq-default-user -o jsonpath='{.data.username}' | base64 --decode)"
echo "username: $username"
password="$(kubectl get secret esd-rabbitmq-default-user -o jsonpath='{.data.password}' | base64 --decode)"
echo "password: $password"

[WINDOWS]
kubectl get secret esd-rabbitmq-default-user -o jsonpath='{.data.username}'
kubectl get secret esd-rabbitmq-default-user -o jsonpath='{.data.password}'

To decode the credentials to base64, go to https://www.base64decode.net/
Copy paste the output onto the website to get the username and password for RabbitMQ

-- Port Forward RabbitMQ to local computer
kubectl port-forward "service/esd-rabbitmq" 15672

-- Create serviceuser
1. Access the RabbitMQ at localhost:15672 and login with the username and password from the output generated from `kubectl get secret`
2. Once login, go to Admin tab. 
3. Under Add a User, set the username as serviceuser and password as serviceuser. Set the Tags as Admin and select "Add user"
4. Once created, click on the created serviceuser.
5. Set the default permission for Permissions (Virtual Host: /, Configure regexp: .*, Write regexp: .*, Read regexp: .*)
6. Set the default permission for Topic permissions (Virtual Host: /, Exchange: (AMQP Default), Write regexp: ,*, Read regexp: .*)



## Skaffold Installation
[MACOS]
curl -Lo skaffold https://storage.googleapis.com/skaffold/releases/latest/skaffold-darwin-amd64 && \
sudo install skaffold /usr/local/bin/

[WINDOWS]
1. Download Skaffold at https://storage.googleapis.com/skaffold/releases/latest/skaffold-windows-amd64.exe
2. Create a folder called Skaffold and place the skaffold-windows-amd64.exe inside
3. Rename skaffold-windows-amd64.exe to skaffold.exe
4. Hit Windows Key, type Edit environment variables for your account and select it
5. Under User variables for user , select Path and click Edit
6. Select "Browse" and navigate to the Skaffold folder created in Step 2
7. Select "OK" and select "OK" again



## Deploying microservices to Kubernetes Cluster
1. Open Terminal or CMD
2. Go to the project root folder
3. Type in and enter: skaffold run

-- Alternative
skaffold dev

`skaffold dev` will trigger a watch loop build (see container logs) and deploy to Kubernetes with cleanup on exit

## Setup MariaDB
-- Find the mariadb pod name
kubectl get pods

-- Port-forward mariadb (replace mariadb pod name with yours)
kubectl port-forward mariadb-xxxxx 3306:3306

-- Apply load.sql to MariaDB with MySQLWorkBench
1. Open up MySQLWorkBench, setup a connection to the MariaDB
[Connection Details]
Hostname: 127.0.0.1
Port: 3306
Username: root
Password: root

2. Apply load.sql (insider sql folder)



## Run AdminUI and ClientUI docker containers

docker run --name clientui -p 5500:80 -d weixuantepo/clientui
docker run --name adminui -p 5501:80 -d weixuantepo/adminui

[URLs]
ClientUI: localhost:5500/index.html
AdminUI: localhost:5501/index.html



## Login Credentials and Additional Details

[Restaurant Owner Login Credentials]
Username: john@esd.sg
Password: password

[Customer UI]
localhost:5500/index.html

[Restaurant UI]
localhost:5501/index.html

[Card Payments]
The Stripe API is configured to be in a test environment so as to stimulate an "actual order payment"
For any order payments, use the following card details to pay.

Card: 4242 4242 4242 4242
Expiry: 11/21
CVC: 111



## Cleanup if skaffold dev option is not used
skaffold delete