docker login
LAST_COMMIT=$(git rev-parse --short HEAD)
DOCKER_TAG=ilyaorson/symbolic_regression:$LAST_COMMIT
docker build --no-cache -t $DOCKER_TAG -f Dockerfile_from_scratch .
docker push $DOCKER_TAG
echo "FROM $DOCKER_TAG" >> Dockerfile
