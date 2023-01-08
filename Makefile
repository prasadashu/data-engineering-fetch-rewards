ifeq (, $(shell which python))
	$(error "python was not found in $(PATH). For installation instructions go to https://www.python.org/downloads/.")
endif

ifeq (, $(shell which docker))
	$(error "docker was not found in $(PATH). For installation instructions go to https://docs.docker.com/get-docker/.")
endif

ifeq (, $(shell which docker-compose))
	$(error "docker-compose was not found in $(PATH). For installation instructions go to https://docs.docker.com/compose/install/.")
endif

.PHONY: dependencies
pip-install:
	pip install -r requirements.txt
aws-configure:
	bash aws_configure.sh

.PHONY: docker
start:
	docker-compose up -d
stop:
	docker-compose down --remove-orphans
clean:
	docker system prune -f

.PHONY: python
perform-etl:
	python ETL_process.py --endpoint-url http://localhost:4566 --queue-name login-queue --max-messages 25