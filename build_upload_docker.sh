docker login
LAST_COMMIT=$(git rev-parse --short HEAD)
BASE_TAG=ilyaorson/symbolic_regression
DOCKER_TAG=ilyaorson/symbolic_regression:$LAST_COMMIT
docker build --no-cache -t $BASE_TAG -f Dockerfile_from_scratch .
docker tag $BASE_TAG $BASE_TAG:$LAST_COMMIT
docker push --all-tags $BASE_TAG
echo "FROM $DOCKER_TAG" > Dockerfile # this will always be one commit behind...
