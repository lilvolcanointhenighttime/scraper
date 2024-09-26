bash
#!/bin/sh

minikube image load praktika_leto-fastapi_scraper:latest
minikube image load praktika_leto-fastapi_oauth:latest
minikube image load praktika_leto-nodejs:latest
minikube image load praktika_leto-nginx:latest
minikube image load postgres:latest
minikube image load rabbitmq:3-management-alpine

declare -A docker_images
docker_images=(
    ["praktika_leto-fastapi_scraper:latest"]="./src/backend/docker/Dockerfile.fastapi_scraper"
    ["praktika_leto-fastapi_oauth:latest"]="./src/backend/docker/Dockerfile.fastapi_oauth"
    ["praktika_leto-nodejs:latest"]="./src/frontend/docker/Dockerfile.nodejs"
    ["praktika_leto-nginx:latest"]="/src/backend/docker/Dockerfile.nginx"
)

for key in "${!docker_images[@]}"
do
    docker build -t "$key" -f "${docker_images[$key]}" .
    echo "$key was built"
done