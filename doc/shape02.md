# Create test cases for each REST endpoint with Python

<!-- TOC -->

- [Create test cases for each REST endpoint with Python](#create-test-cases-for-each-rest-endpoint-with-python)
- [Constraint](#constraint)
    - [Hill chart](#hill-chart)
- [Place, Affordance, Connection](#place-affordance-connection)
- [Test Driven Development](#test-driven-development)
- [Install developer dependencies](#install-developer-dependencies)
- [Create a test file](#create-a-test-file)

<!-- /TOC -->

# Constraint

Base time: 1 workday (Max: 2)

## Hill chart
```
 +
. .
0-1
```

# Place, Affordance, Connection

* Places users can navigate
  * Not applicable as tests are automated

* Affordance users can act
  * Test `GET https://base.url:8080/` returns HTTP Status `200` and payload `App-version: *`
  * Test `GET https://base.url:8080/api/archiveso` returns HTTP Status `200`.

* Connection users are taken to
  * `GET https://base.url:8080/` --> `main.py` --> HTTP response
  * `GET https://base.url:8080/api/archiveso` --> `main.py` --> `clsArchiveso.py` --> `/path/to/archivebox` --> `archivebox.cli.list()` --> String --> HTTP response

# Test Driven Development

For this project, we're using `pytest` as our testing framework. 

# Install developer dependencies

1. Workstation

Before we can run our app, we need to activate virtual environment and install any dependencies. We use the flag `--dev` to specify that these packages are for development only.

```sh
cd app
pipenv shell
pipenv install --dev pytest==6.2.4 pytest-flask==1.2.0
```

To uninstall any dependency.

```sh
pipenv uninstall pytest
```

To deactivate the virtual environment.

```sh
exit
```

2. Create a `make` command.

Edit the file `Makefile` and insert both targets `test` and `test_verbose` to the `.PHONY` declaration. Then add the following lines of code:

```makefile
install:
  ...
	pipenv install --dev pytest==6.2.4 pytest-flask==1.2.0

test: 
	PYTHONPATH=.:./src/archiveso pytest

test_verbose: 
	PYTHONPATH=.:./src/archiveso pytest -v -s
```

# Create a test file

1. Before we can run tests, we have to create a function in `main.py` to allow it to be called as a function in test fixtures. Edit the `main.py` file and refactor the code as follows:

```py
from flask import Flask

def create_app():
    app = Flask(__name__)
    
    @app.route("/")
    def root():
      return "App-version: 0.1.0"

    return app

app = create_app()
```

In testing, a fixture provides a defined, reliable and consistent context for the tests. This could include environment or content. 

We can tell `pytest` that a particular function is a fixture by decorating it with `@pytest.fixture`. The return value of the fixture can be passed as a parameter in tests.

2. Create a `test` directory in the path `app/`. This is where we store our test files `test_*.py`, which will be auto-discoverable by `pytest`.

Create a special file `conftest.py` that holds all our fixtures, as `pytest` will auto-import these into all our tests. Add the following lines of code:

```py
import pytest

from main import create_app

@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture
def client(app):
    return app.test_client()
```

3. Create a file `test_app.py` and add the following lines of code:

```py
import pytest

def test_app(client):
    assert client.get("/").data == b"App-version: 0.1.0"
```

4. Verify that our test works with `make`.

```sh
PYTHONPATH=.:./src/archiveso pytest
====================================================== test session starts =======================================================
platform darwin -- Python 3.9.10, pytest-6.2.4, py-1.11.0, pluggy-0.13.1
rootdir: /Users/dennislwm/fx-git-pull/14shapeup_archiveso/app
plugins: flask-1.2.0
collected 1 item                                                                                                                 

tests/test_app.py .                                                                                                        [100%]

======================================================= 1 passed in 0.01s ========================================================
```