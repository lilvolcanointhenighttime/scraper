## Quick Start
1. Fill .env.example and rename it to .env

2. Deployment

docker-compose deployment
```
docker-compose up -d
```

k8s deployment(minikube)
```
kubectl create secret generic env --from-env-file=.env

kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.11.1/deploy/static/provider/cloud/deploy.yaml

minikube start
minikube addons enable ingress
minikube addons enable ingress-dns

kubectl apply -f ./src/ops/.kube/
kubectl get ing
```

edit your local dns(hosts) pasting "domain ADDRESS" value

```
minikube tunnel
```
