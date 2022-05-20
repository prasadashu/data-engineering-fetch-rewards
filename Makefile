ifeq (, $(shell which python))
	$(error "python was not found in $(PATH). For installation instructions go to https://www.python.org/downloads/.")
endif

ifeq (, $(shell which pip))
	$(error "python's pip was not found in $(PATH). For installation run `python -m ensurepip --upgrade` in your terminal or run `make pip-install`.")
endif

ifeq (, $(shell which awslocal))
	$(error "awslocal was not found in $(PATH). To install run `pip install awscli-local` in your terminal or run `make pip-install`.")
endif

ifeq (, $(shell which docker))
	$(error "docker was not found in $(PATH). For installation instructions go to https://docs.docker.com/get-docker/.")
endif

ifeq (, $(shell which docker-compose))
	$(error "docker-compose was not found in $(PATH). For installation instructions go to https://docs.docker.com/compose/install/.")
endif


.PHONY: dependencies
pip-install:
	python -m ensurepip --upgrade && pip install -r requirements.txt

.PHONY: docker
start:
	docker-compose up -d
stop:
	docker-compose down --remove-orphans
clean:
	docker system prune -f
