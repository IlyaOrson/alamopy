docker login
docker build --no-cache -t ilyaorson/symbolic_regression -f Dockerfile_from_scratch .
docker push ilyaorson/symbolic_regression