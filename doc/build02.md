# Python Flask server authentication

<!-- TOC -->

- [Python Flask server authentication](#python-flask-server-authentication)
- [Constraint](#constraint)
  - [Hill chart](#hill-chart)
- [HTTP Basic Authentication](#http-basic-authentication)
- [Requirements](#requirements)
- [Set up authorization in the Lowdefy app](#set-up-authorization-in-the-lowdefy-app)
- [Protect the Python Flask server routes with HTTP Basic authentication](#protect-the-python-flask-server-routes-with-http-basic-authentication)
- [Retrieve secrets during test and run](#retrieve-secrets-during-test-and-run)

<!-- /TOC -->

# Constraint

Base time: 1 workday (Max: 2)

## Hill chart
```
 .
. +
0-1
```

# HTTP Basic Authentication

We are using HTTP basic authentication for our Python Flask server. This is to prevent any unauthorized persons to access our API endpoints, which are available via a public domain.

# Requirements

* [Flask-HTTPAuth](https://flask-httpauth.readthedocs.io/en/latest/)

# Set up authorization in the Lowdefy app

The Lowdefy **Secrets** object is an object that can be used to securely store sensitive information. Secrets can be accessed using the `_secret` operator.

The secrets object only exists on the backend server, and therefore the `_secret` operator can only be used in `connections` and `requests`. Secrets can only be set with environment variables.

Secrets created as an environment variable must be prefixed with `LOWDEFY_SECRET_`. The remaining part of the key is the name of the variable used within the Lowdefy app.

For example, if the environment variable `LOWDEFY_SECRET_API_USERNAME` is set to `super`, then `API_USERNAME` will return `super`.

1. Edit the `.env` file in the path `front/`. Append the following lines:

```
LOWDEFY_SECRET_API_USERNAME=YOUR_API_USERNAME
LOWDEFY_SECRET_API_PASSWORD=YOUR_API_PASSWORD
```

2. Edit the file `lowdefy.yaml` in the path `front/`. Insert the following code:

```yml
...
connections:
  - id: conn_my_api
      ...
      baseURL: https://dev.to/api
      auth:
        username:
          _secret: API_USERNAME
        password:
          _secret: API_PASSWORD
```

3. Configure your [Netlify](https://app.netlify.com) deployment. Click **Site Settings** --> **Build & deploy**.

Under the **Environment** section, add the environment variables for your Lowdefy app.

# Protect the Python Flask server routes with HTTP Basic authentication

1. Edit the `main.py` file in the path `app/`. Modify the source code as follows:

```py
...
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

def create_app():
    app = Flask(__name__)
    auth = HTTPBasicAuth()

    API_USERNAME = os.getenv('LOWDEFY_SECRET_API_USERNAME', '')
    API_PASSWORD = os.getenv('LOWDEFY_SECRET_API_PASSWORD', '')

    users = {
        API_USERNAME: generate_password_hash(API_PASSWORD),
    }

    @auth.verify_password
    def verify_password(username, password):
        if username in users:
            return check_password_hash(users.get(username), password)
        return False

    @app.route("/")
    @auth.login_required
    def root():
    ...
```

# Retrieve secrets during test and run

There are many methods of storing and retrieving secrets. However, in this build we will only be covering the use of environment variables.

We need to ensure that the secrets are set in the environment variables on:

- a Python flask server when testing and running locally
- a Docker container server when testing and running locally
- a Docker container server when testing and running in our CI pipeline
- a Docker container server when testing and running in our production instance 

1. Edit the `Makefile` file in the path `app/`. Insert the following code:

Both the `make` rules `docker_run` and `docker_prod`, which are used to run a Docker container locally and in our production instance, respectively, accept an argument `--env-file` that specifies the environment variables file.

The `make run` rule loads the environment variable file using `source` before running the Python Flask app locally.

```makefile
...
docker_run: docker_build docker_clean
	docker run --rm -d -p 8080:8080 --env-file=../front/.env --name=objArchiveso archiveso

docker_prod: docker_stop
	docker run --rm -d -p 8080:8080 --env-file=../front/.env --name objArchiveso dennislwm/archiveso:latest
...
run: 
	set -a && source ../front/.env && set +a && FLASK_ENV=development FLASK_APP=main PYTHONPATH=./:./src/archiveso python3 -m flask run --host=0.0.0.0 --port=8080
```

2. Edit the `docker-compose.yml` file in the path `app/`. Append the following code:

The `docker-compose.yml` file accepts the environment variables from the host, which in our case is the CircleCI pipeline. We have to add these key-value pairs as environment variables in our CircleCI project settings.

```yml
...
services:
  archiveso:
    image: archiveso:latest
    environment:
      - LOWDEFY_SECRET_API_USERNAME
      - LOWDEFY_SECRET_API_PASSWORD
      ...
```