.PHONY: default install_new install_pipfile run shell shell_clean test test_verbose

default: test

docker_build: install_freeze
	DOCKER_BUILDKIT=1 docker build -t archiveso .

docker_clean:
	docker image prune -f

docker_run: docker_build docker_clean
	docker run --rm -d -p 80:8080 --name=objArchiveso archiveso

install_freeze:
	pip3 install pipreqs
	pipreqs --ignore tests . --force
	pip3 uninstall -y pipreqs
	
install_new: 
	pipenv install archivebox==0.6.2 flask==1.0.2
	pipenv install --dev pytest==6.2.4 pytest-flask==1.2.0

install_pipfile:
	pipenv install --dev

run: 
	FLASK_ENV=development FLASK_APP=main PYTHONPATH=./:./src/archiveso python3 -m flask run --host=0.0.0.0 --port=8080

shell:
	pipenv shell

shell_clean:
	pipenv --rm

test: 
	PYTHONPATH=.:./src/archiveso pytest

test_verbose: 
	PYTHONPATH=.:./src/archiveso pytest -v -s