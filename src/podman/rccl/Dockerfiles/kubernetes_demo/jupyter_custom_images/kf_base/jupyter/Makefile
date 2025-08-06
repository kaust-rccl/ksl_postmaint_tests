TAG=v1.5.0-rc.0-82-g5e09536f

docker-build-base:
	make docker-build -C ../base TAG=${TAG}

docker-build: docker-build-base
	docker build -t jupyter:${TAG} --build-arg BASE_IMG=base:${TAG} -f Dockerfile . 

docker-push:
	docker push jupyter:${TAG}
