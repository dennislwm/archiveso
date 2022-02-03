# Create a Dockerfile and test it locally

<!-- TOC -->

- [Create a Dockerfile and test it locally](#create-a-dockerfile-and-test-it-locally)
- [Constraint](#constraint)
    - [Hill chart](#hill-chart)
- [Place, Affordance, Connection](#place-affordance-connection)
- [Create a Dockerfile](#create-a-dockerfile)

<!-- /TOC -->

# Constraint

Base time: 1 workday (Max: 2)

## Hill chart
```
 .
. +
0-1
```

# Place, Affordance, Connection

* Places users can navigate
  * Docker Flask server on a port `8080`, e.g. `https://base.url:8080`
    * Status endpoint `/`
    * Application endpoint `/api/archiveso`
  
* Affordance users can act
  * App version `GET https://base.url:8080/`
  * List all `GET https://base.url:8080/api/archiveso`

* Connection users are taken to
  * Postman --> `GET https://base.url:8080/` --> Docker --> `main.py` --> HTTP response
  * Postman --> `GET https://base.url:8080/api/archiveso` --> Docker --> `main.py` --> `clsArchiveso.py` --> `/path/to/archivebox` --> `archivebox.cli.list()` --> String --> HTTP response

# Create a Dockerfile

1. Create a file `Docker` in the `app` folder. Add the following lines to the file:

```Dockerfile
FROM python:3.7-slim
RUN apt-get update

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

ENV FLASK_ENV=development
ENV FLASK_APP=main
ENV PYTHONPATH=./:./src/archiveso
CMD ["python3", "main.py"]
```

> Note: We are not using multi-stage Docker build because Python is an interpreted language, unlike Java, that is a compiled language which produces an executable file from code.

2. Generate `requirements.txt` file.

The `requirements.txt` file is generated each time we run the `make docker_build` command. Edit the file `Makefile` and insert the following lines of code:

```makefile
docker_build: install_freeze
	DOCKER_BUILDKIT=1 docker build -t archiveso .

docker_clean:
	docker image prune -f

docker_run: docker_build docker_clean
	docker run --rm -d -p 80:8080 --name=objArchiveso archiveso
...
install_freeze:
	pip3 install pipreqs
	pipreqs --ignore tests . --force
	pip3 uninstall -y pipreqs
```

According to [Krav2022], `pipreqs` generates a `requirements.txt` file based on imports in the project. The number of dependencies may not be the same as the `Pipfile` or `pip3 freeze`, i.e. `pip3 freeze` > `Pipfile` >= `pipreqs`.

3. Edit `main.py` file.

Edit the file `main.py` and replace the line `app = create_app()` with the `__main__` block as follows:

```py
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080)
```