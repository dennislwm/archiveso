# Create a single REST endpoint with Python

<!-- TOC -->

- [Create a single REST endpoint with Python](#create-a-single-rest-endpoint-with-python)
- [Constraint](#constraint)
    - [Hill chart](#hill-chart)
- [Place, Affordance, Connection](#place-affordance-connection)
- [Create a virtual environment](#create-a-virtual-environment)
- [Install dependencies](#install-dependencies)
- [Create a Makefile](#create-a-makefile)
- [Create a Main Application](#create-a-main-application)

<!-- /TOC -->

# Constraint

Base time: 2 workday (Max: 4)

## Hill chart
```
  .
 . .
.   +
0-1-2
```

# Place, Affordance, Connection

* Places users can navigate
  * Python Flask server on a port `8080`, e.g. `https://base.url:8080`
    * Status endpoint `/`
    * Application endpoint `/api/archiveso`

* Affordance users can act
  * App version `GET https://base.url:8080/`
  * List all `GET https://base.url:8080/api/archiveso`

* Connection users are taken to
  * `GET https://base.url:8080/` --> `main.py` --> HTTP response
  * `GET https://base.url:8080/api/archiveso` --> `main.py` --> `clsArchiveso.py` --> `/path/to/archivebox` --> `archivebox.cli.list()` --> String --> HTTP response

# Create a virtual environment

We will start by navigating to our `app` folder. This is the root folder of our virtual environment.

Then, we will install `pipenv` and create a Python 3 virtual environment for this project.

```sh
cd app
pip3 install --user pipenv
pipenv --python $(which python3)
```

# Install dependencies

1. Workstation

Before we can run our app, we need to activate virtual environment and install any dependencies. Ensure that you are in the `app` folder.

```sh
pipenv shell
```

This command creates both the `Pipfile` and `Pipfile.lock` in your current folder. To add any dependencies under the `[packages]` section, type the following command:

```sh
pipenv install archivebox==0.6.2 flask==1.0.2
```

To uninstall any dependency.

```sh
pipenv uninstall archivebox
```

To deactivate the virtual environment.

```sh
exit
```

2. Verify the installation

Create a file `help.py` in the `app` folder. Add the following lines to the file:

```py
import archivebox.cli as cli
import os
os.chdir('/path/to/your/archivebox')
cli.help()
```

In the terminal, run the command `python3 help.py` and you should see the output below. You may delete the `help.py` file after verification.

```sh
ArchiveBox v0.6.2: The self-hosted internet archive.

Active data directory:
    /Users/dennislwm/Downloads/asset-box

Usage:
    archivebox [command] [--help] [--version] [...args]

Commands:
    help                 Print the ArchiveBox help message and usage
    version              Print the ArchiveBox version and dependency information

    init                 Initialize a new ArchiveBox collection in the current directory
    config               Get and set your ArchiveBox project configuration values
    setup                Automatically install all ArchiveBox dependencies and extras

    add                  Add a new URL or list of URLs to your archive
    remove               Remove the specified URLs from the archive
    update               Import any new links from subscriptions and retry any previously failed/skipped links
    list                 List, filter, and export information about archive entries
    status               Print out some info and statistics about the archive collection

    shell                Enter an interactive ArchiveBox Django shell
    server               Run the ArchiveBox HTTP server
    manage               Run an ArchiveBox Django management command
    oneshot              
    Create a single URL archive folder with an index.json and index.html, and all the archive method outputs.
    You can run this to archive single pages without needing to create a whole collection with archivebox init.
    
    schedule             Set ArchiveBox to regularly import URLs at specific times using cron

Example Use:
    mkdir my-archive; cd my-archive/
    archivebox init
    archivebox status

    archivebox add https://example.com/some/page
    archivebox add --depth=1 ~/Downloads/bookmarks_export.html
    
    archivebox list --sort=timestamp --csv=timestamp,url,is_archived
    archivebox schedule --every=day https://example.com/some/feed.rss
    archivebox update --resume=15109948213.123

Documentation:
    https://github.com/ArchiveBox/ArchiveBox/wiki
```

# Create a Makefile

You can use `make` to automate different parts of developing a Python app, like running tests, cleaning builds, and installing dependencies. To use `make` in your project, you need to have a file named `Makefile` at the root of your project.

1. Create a file `Makefile` in the `app` folder. Add the following lines to the file:

```makefile
.PHONY: default install install_pipfile shell shell_clean

default: test

install:
	pipenv install archivebox==0.6.2 flask==1.0.2

install_pipfile:
	pipenv install --dev

shell:
	pipenv shell

shell_clean:
	pipenv --rm
```

Each rule consists of 3 parts: a target, a list of pre-requisities, and a recipe. The follow this format:

```makefile
target: pre-req1 pre-req2 pre-req3
  recipes
```

The `target` represents a file that needs to be created in your build. The pre-requisites list tells `make` what dependencies are required, which can be a file or another target. Finally the recipes are a list of shell commands that will be executed.

The `.PHONY` line declares a target that does not exist. As Python is an interpreted language, there is no build file.

# Create a Main Application

1. Create a file `main.py` in the `app` folder. Add the following lines to the file:

```py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def root():
  return "App-version: 0.1.0"
```

2. Edit the file `Makefile` and insert a target `run` to the `.PHONY` declaration. Then declare the target `run` with the following lines of code:

```makefile
run:
	FLASK_ENV=development FLASK_APP=main PYTHONPATH=./:./src/archiveso python3 -m flask run --host=0.0.0.0 --port=8080
```

There are three environment variables used in the `run` command:
* `FLASK_ENV` sets an environment, such as `development`. The default is `production`.
* `FLASK_APP` has three parts: an optional path that sets the current working directory. If the name is a factory, it can optionally be followed by arguments in parentheses. Examples:
  * `FLASK_APP=src/main`: Sets the current working directory to `src` then imports `main.py`.
  * `FLASK_APP=src.main`: Imports the path `src/main.py`.
  * `FLASK_APP=main:app2`: Uses the `app2` Flask instance in `main.py`.
  * `FLASK_APP="main:create_app('dev')"`: The `create_app` factory in `main.py` is called with an argument.
* `PYTHON_PATH` sets the path for your custom imports.

3. Run the make command:

```sh
make run
FLASK_ENV=development FLASK_APP=main PYTHONPATH=./:./src/archiveso python3 -m flask run --host=0.0.0.0 --port=8080
 * Serving Flask app "main" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on all addresses.
   WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://192.168.86.26:8080/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 646-438-933
```
