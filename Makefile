.PHONY: run
run:
	which docker-machine >/dev/null 2>/dev/null && eval $$(docker-machine env default); \
		docker-compose up -d elasticsearch; \
		sleep 10; \
		docker-compose up -d server

.PHONY: docker-stop
docker-stop:
	which docker-machine >/dev/null 2>/dev/null && eval $$(docker-machine env default); \
		docker-compose stop; \
		docker-compose rm -f
