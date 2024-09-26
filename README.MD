## Quick Start
1. Fill all .env.example and rename it to .env

2. Deployment:

docker-compose deployment
```
docker-compose up -d
```

k8s deployment(minikube)

```
kubectl create secret generic env --from-env-file=.env
kubectl create secret generic scraper-pg.env --from-env-file=scraper_pg.env
kubectl create secret generic oauth-pg.env --from-env-file=oauth_pg.env

kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.11.1/deploy/static/provider/cloud/deploy.yaml

minikube start
minikube addons enable ingress
minikube addons enable ingress-dns
```

Build docker images
```
chmod +x ./docker_build.sh
./docker_build.sh

minikube image load praktika_leto-fastapi_scraper:latest
minikube image load praktika_leto-fastapi_oauth:latest
minikube image load praktika_leto-nodejs:latest
minikube image load praktika_leto-nginx:latest
minikube image load postgres:latest
minikube image load rabbitmq:3-management-alpine
```

```
kubectl apply -f ./src/ops/.kube/
kubectl get ing
```

Edit your local dns(hosts) pasting "domain ADDRESS" value

```
minikube tunnel
```
