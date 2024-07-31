bash
#!/bin/sh

declare -A docker_images
docker_images=(
    ["fastapi_app:slim"]="./src/backend/docker/Dockerfile.fastapi"
    ["nodejs_app:alpine"]="./src/frontend/docker/Dockerfile.nodejs"
    ["nginx"]="/src/backend/docker/Dockerfile.nginx"
)

for key in "${!docker_images[@]}"
do
    docker build -t "$key" -f "${docker_images[$key]}" .
    echo "$key was built"
done