.PHONY: default docker_build docker_clean docker_run docker_prod docker_stop docker_tunnel front_dev install_new install_pipfile run shell shell_clean test test_verbose

default: run_prod

docker_build: install_freeze
	DOCKER_BUILDKIT=1 docker build -t archiveso .

docker_clean: docker_stop
	docker image prune -f

docker_exec:
	docker exec -it objArchiveso /bin/bash

docker_logs:
	docker logs -f objArchiveso

docker_run: docker_build docker_clean
	docker run -d -p 8080:8080 --env-file=../front/.env -v /Users/dennislwm/Downloads/asset-box:/data -w /app --name=objArchiveso archiveso:latest

docker_prod: docker_stop
	docker run -d -p 8080:8080 --env-file=../front/.env -v /Users/dennislwm/Downloads/asset-box:/data -w /app --name objArchiveso dennislwm/archiveso:$${APP_VERSION}

docker_test: docker_build docker_clean
	docker-compose -f docker-compose.yml up -d
	docker-compose -f docker-compose-test.yml up -d

# ignore errors with prefix '-'
docker_stop:
	-docker container stop objArchiveso
	-docker container rm objArchiveso

docker_tunnel: 
	cloudflared tunnel --config ~/.cloudflared/config-archiveso.yml run

front_build:
	cd ../front/ && npx lowdefy@latest build

front_dev: front_build
	cd ../front/ && npx lowdefy@latest dev

front_prod: docker_prod front_build
	cd ../front/ && npx lowdefy@latest dev

install_freeze:
	pip3 install pipreqs
	pipreqs --ignore tests . --force
	echo "pytest==6.2.4" >> ./requirements.txt
	echo "pytest-flask==1.2.0" >> ./requirements.txt
	echo "prospector==1.6.0" >> ./requirements.txt
	echo "requests==2.27.1" >> ./requirements.txt
	pip3 uninstall -y pipreqs
	
install_new: 
	pipenv install archivebox==0.6.2 flask==1.0.2 flask_httpauth==4.5.0 Werkzeug==2.0.2
	pipenv install --dev pytest==6.2.4 pytest-flask==1.2.0 requests==2.27.1

install_pipfile:
	pipenv install --dev

run: docker_stop
	set -a && source ../front/.env && set +a && ARCHIVEBOX_PATH=/Users/dennislwm/Downloads/asset-box FLASK_ENV=development FLASK_APP=main PYTHONPATH=./:./src/archiveso python3 -m flask run --host=0.0.0.0 --port=8080

shell:
	pipenv shell

shell_clean:
	pipenv --rm

test: 
	PYTHONPATH=.:./src/archiveso pytest

test_verbose: 
	PYTHONPATH=.:./src/archiveso pytest -v -s