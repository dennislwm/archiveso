# Build and test an API endpoint to execute a command and return its response

<!-- TOC -->

- [Build and test an API endpoint to execute a command and return its response](#build-and-test-an-api-endpoint-to-execute-a-command-and-return-its-response)
- [Constraint](#constraint)
  - [Hill chart](#hill-chart)
- [Place, Affordance, Connection](#place-affordance-connection)
- [Test driven development of API endpoint](#test-driven-development-of-api-endpoint)
- [Create test case](#create-test-case)
- [Configure build](#configure-build)
- [Build the API endpoint](#build-the-api-endpoint)

<!-- /TOC -->

# Constraint

Base time: 2 workday (Max: 4)

## Hill chart
```
  .
 . .
+   .
0-1-2
```

# Place, Affordance, Connection

* Places users can navigate
  * Lowdefy app e.g. `https://archiveso.netlify.app`
    * Add URL `/page_post_url`

* Affordance users can act
  * Test `POST https://base.url:8080/api/archiveso` returns HTTP Status `200`.

* Connection users are taken to
  * `POST https://base.url:8080/api/archiveso` --> `main.py` --> `clsArchiveso.py` --> `/path/to/archivebox` --> `archivebox add` --> stdout --> HTTP response

# Test driven development of API endpoint

When you approach coding using a test driven development ["TDD"], you start with a test case and then build your code around the test case. You can have have one or more test cases for each feature.

In our example, we are building an API endpoint that allows users to add URL(s) with the `POST` method. There are two cases that we test for:

- Archivebox index not found
- Empty user form

In our first test case, with reference to our connection where users are taken to, this fails if the `path/to/archivebox` is not configured as an environment variable `ARCHIVEBOX_PATH`.

The second test case, with reference to our places where users can navigate, this fails if the user form is empty and the body of the `POST` method does not contain the `url` field.

# Create test case

1. Edit the `test_app.py` file and append the following lines of code:

```py
...
def test_post_url_index_not_found(client, header):
    objResponse = client.post("/api/archiveso",
                              headers = header,
                              data={"url": "https://earthly.dev/blog/canary-deployment/"})
    assert objResponse.status_code == 503
    assert objResponse.data.find(b"Archivebox index not found") >= 0

def test_post_url_empty_form(client, header):
    objResponse = client.post("/api/archiveso", headers = header)
    assert objResponse.status_code == 400
    assert objResponse.data.find(b"Empty strUrl") >= 0
```

2. Edit the file `conftest.py` file that holds all our fixtures. Insert the following lines of code:

```py
...
import os
...
from requests.auth import _basic_auth_str
...
@pytest.fixture
def header():
    API_USERNAME = os.getenv('LOWDEFY_SECRET_API_USERNAME', '')
    API_PASSWORD = os.getenv('LOWDEFY_SECRET_API_PASSWORD', '')

    return {
        'Authorization': _basic_auth_str(API_USERNAME, API_PASSWORD)
    }
```

We define a fixture named `header` that contains the basic authentication required for our Flask server. Without this, you will get an `Unauthorized Access` response each time we make a request.

# Configure build

Before we can build and test our app, we need to configure our build by adding new environment variables and Python packages:
- environment variables: `ARCHIVEBOX_PATH`
- Python packages: `requests==2.27.1`

The environment variable is required in both development and production, but not in our testing stage. On the other hand, the Python packages are required in both development and testing, but not in our production stage.

1. Install Python packages

Before we can run our app, we need to activate virtual environment and install any dependencies. We use the flag `--dev` to specify that these packages are for development only.

```sh
cd app
pipenv shell
pipenv install --dev requests==2.27.1
```

2. Edit the `Makefile` file in the path `app/`. Then modify the following lines of code:

```makefile
...
docker_test: docker_build docker_clean
	docker-compose -f docker-compose-test.yml up -d
...
install_freeze:
  ...
	echo "pytest==6.2.4" >> ./requirements.txt
	echo "pytest-flask==1.2.0" >> ./requirements.txt
	echo "prospector==1.6.0" >> ./requirements.txt
	echo "requests==2.27.1" >> ./requirements.txt
	pip3 uninstall -y pipreqs

install_new: 
	...
	pipenv install --dev pytest==6.2.4 pytest-flask==1.2.0 requests==2.27.1
...
run: 
	set -a && source ../front/.env && set +a && ARCHIVEBOX_PATH=/Users/dennislwm/Downloads/asset-box FLASK_ENV=development FLASK_APP=main PYTHONPATH=./:./src/archiveso python3 -m flask run --host=0.0.0.0 --port=8080
...
```

3. Create a `docker-compose-test.yml` file in the path `app/`. Add the following lines of code:

```yml
version: '3.7'

services:
  # Pipeline actions
  archiveso:
    image: archiveso:latest
    environment:
      - LOWDEFY_SECRET_API_USERNAME
      - LOWDEFY_SECRET_API_PASSWORD
      - ARCHIVEBOX_PATH=./
    entrypoint: /usr/local/bin/pytest
```

4. Edit the `config.yml` file in the path `.circleci/`. Append the following lines of code to `jobs.static-analysis.steps` section:

```yml
jobs:
  static-analysis:
    ...
    steps:
      ...
      - run:
          name: "Run unit tests"
          command: cd app && docker-compose -f docker-compose-test.yml up -d
```

The test cases are configured to pass without a valid `ARCHIVEBOX_PATH`, as this environment variable is set both in development and production, but not in the testing stage.

# Build the API endpoint

With reference to our connection where users are taken to:
* `POST https://base.url:8080/api/archiveso` --> `main.py` --> `clsArchiveso.py` --> `/path/to/archivebox` --> `archivebox add` --> stdout --> HTTP response

When a user makes a `POST` request, the `main.py` file checks for both basic authentication and `url` form field. If the user is logged in and the form field isn't empty, then a call is made to the class method `add_url()` from the `clsArchiveso.py` file. Otherwise, it will return either:
- "Unauthorized Access"
- "Empty strUrl", `400`

The `add_url()` function encapsulates the `archivebox add` command-line and accepts one input string, `strUrl`, which specifies one or more URL(s) separated by space. There are three possible return values:
- `strResult`, `200`
- "Archivebox index not found", `503`
- "Archivebox not installed", `503`

1. Edit the `main.py` file in the path `app/`. Modify the following lines of code:

```py
...
from flask import Flask, request
...
from clsArchiveso import clsArchiveso

def create_app():
    ...
    API_PASSWORD = os.getenv('LOWDEFY_SECRET_API_PASSWORD', '')
    ARCHIVEBOX_PATH = os.getenv('ARCHIVEBOX_PATH', './')
    ab = clsArchiveso(ARCHIVEBOX_PATH)
    ...
    @app.route("/api/archiveso", methods = ['POST'])
    @auth.login_required
    def post_url():
        strUrl = request.form.get('url')
        if not strUrl:
            return "Empty strUrl", 400
        return ab.add_url(strUrl)
```

2. Edit the `clsArchiveso.py` file in the path `app/src/archiveso/`. Add the following lines of code:

```py
# pylint: disable=pointless-string-statement
import os
import subprocess

from archivebox import cli

#-----------------------
# Redirect stdout to buf
import io
from contextlib import redirect_stdout

"""--------+---------+---------+---------+---------+---------+---------+---------+---------|
|                                    M A I N   C L A S S                                   |
|----------+---------+---------+---------+---------+---------+---------+---------+-------"""
class clsArchiveso():

    """--------+---------+---------+---------+---------+---------+---------+---------+---------|
    |                                   C O N S T R U C T O R                                  |
    |----------+---------+---------+---------+---------+---------+---------+---------+-------"""
    def __init__(self, strPath):
        #----------------------------
        # initialize class _CONSTANTS
        self._init_meta()
        os.chdir(strPath)

    """--------+---------+---------+---------+---------+---------+---------+---------+---------|
    |                                 C L A S S   M E T H O D S                                |
    |----------+---------+---------+---------+---------+---------+---------+---------+-------"""
    def get_version(self):
        return self._strMETAVERSION

    def get_cli_version(self):
        #-----------------------
        # Redirect stdout to buf
        buf = io.StringIO()
        with redirect_stdout(buf):
            cli.version()
        return buf.getvalue().splitlines()[0]

    def add_url(self, strUrl):
        try:
            strCmd = 'archivebox add ' + strUrl
            strResult = subprocess.check_output(strCmd, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as e:
            strOutput = e.output.decode('utf-8')
            # directory not found
            if "archivebox init" in strOutput:
              return "Archivebox index not found", 503
            # command not found
            return "Archivebox not installed", 503

        return strResult.decode('utf-8'), 200

    """--------+---------+---------+---------+---------+---------+---------+---------+---------|
    |                                C L A S S   M E T A D A T A                               |
    |----------+---------+---------+---------+---------+---------+---------+---------+-------"""
    def _init_meta(self):
        """
        | _strMETACLASS, _strMETAVERSION, _strMETAFILE used to save() and load() members
        """
        self._strMETACLASS = str(self.__class__).split('.')[1][:-2]
        self._strMETAVERSION = "0.2.0"
        """
        | Filename "_Class_Version_"
        """
        self._strMETAFILE = "_" + self._strMETACLASS + "_" + self._strMETAVERSION + "_"
```