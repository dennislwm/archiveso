# Require status checks to pass before merging PR

<!-- TOC -->

- [Require status checks to pass before merging PR](#require-status-checks-to-pass-before-merging-pr)
- [Constraint](#constraint)
  - [Hill chart](#hill-chart)
- [Place, Affordance, Connection](#place-affordance-connection)
- [Status Checks](#status-checks)
- [Continuous Integration](#continuous-integration)
- [CircleCI](#circleci)
- [Travis CI](#travis-ci)

<!-- /TOC -->

# Constraint

Base time: 1 workday (Max: 2)

## Hill chart
```
    +
   . .
  .   .
 .     .
.       .
0-1-2-3-4
```

# Place, Affordance, Connection

# Status Checks

1. We will use the python package `prospector` to perform static analysis. 

Edit the file `Makefile` and insert the `echo` line under the `install_freeze` block of code:

```makefile
...
install_freeze:
	pip3 install pipreqs
	pipreqs --ignore tests . --force
	echo "prospector==1.6.0" >> ./requirements.txt
	pip3 uninstall -y pipreqs
```

Each time you run `make docker_build`, the `install_freeze` dependency is executed. This package is not included in the `Pipfile` because the application doesn't require it.

2. We will use `docker-compose` in our CI pipeline, with a `prospector` entrypoint that executes the static analysis.

Create a file `docker-compose` file in the path `app/` and enter the following:

```yml
version: '3.7'

services:
  # Pipeline actions
  archiveso:
    image: archiveso:latest
    entrypoint: /usr/local/bin/prospector
```

> Note: As the `docker-compose.yml` file depends on our custom image `archiveso:latest`, we need to ensure that `make docker_build` gets executed before it in our CI pipeline.

# Continuous Integration

The book Buel2019 suggests Travis CI ["TCI"] as a free service for public GitHub projects. However, TCI uses **OSS only** credits for public repos. The OSS credits are granted by TCI on a case-by-case assessment and may be assigned as a one-time pool or renewable pool.

# CircleCI

CircleCI ["CCI"] has a free plan that includes 30,000 free credits per month (or 6,000 build minutes per month).

<details>
  <summary>Configure CircleCI to check GitHub status.</summary><br>

1. Add your GitHub repo to CCI.

Navigate to [CCI web page](https://circleci.com) and login with your GitHub credentials.

Select **Organization Settings** --> **VCS** --> **Manage GitHub Checks**.

Select which repo you want to utilize checks and click the **Install** button.

2. Create a file `.config.yml` in the `.circleci/` folder of your repo. Add the following lines to the file:

```yml
# Use the latest 2.1 version of CircleCI pipeline process engine.
# See: https://circleci.com/docs/2.0/configuration-reference
version: 2.1

# Define a job to be invoked later in a workflow.
# See: https://circleci.com/docs/2.0/configuration-reference/#jobs
    # Specify the execution environment. You can specify an image from Dockerhub or use one of our Convenience Images from CircleCI's Developer Hub.
    # See: https://circleci.com/docs/2.0/configuration-reference/#docker-machine-macos-windows-executor
    # Add steps to the job
    # See: https://circleci.com/docs/2.0/configuration-reference/#steps
    # working_directory (Default: /home/circleci/project)
    #   root folder of repo
jobs:
  static-analysis:
    docker:
      - image: cimg/python:3.9.10
    steps:
      - checkout
      - setup_remote_docker:
          version: 19.03.13
      - run:
          name: "Build image"
          command: cd app && make docker_build
      - run:
          name: "Run static analysis"
          command: cd app && docker-compose up -d

# Invoke jobs via workflows
# See: https://circleci.com/docs/2.0/configuration-reference/#workflows
workflows:
  static-analysis-workflow:
    jobs:
      - static-analysis
```

The root of our repo is initially checked out to the default working directory `/home/circleci/project`. The step `setup_remote_docker` adds support for `docker-compose` and Docker BuildKit.

The first `run` builds our custom Docker image, while the second `run` executes the `docker-compose.yml` that performs the static-analysis.

3. To take full advantage of our configured CI system, we need to ensure that we check the build before merging it into the main branch.

Navigate to your GitHub repo, and click on the repo **Settings** --> **Branches** --> **Add Rule**. 

- In field **Branch name pattern**, enter `main`.
- Under **Protect matching branches** section:
  - Enable checkbox **Require a pull request before merging**
  - Enable checkbox **Require status checks to pass before merging** 
    - Enable checkbox **Require branches to be up to date before merging**
  - Enable checkbox **Require linear history**
- In the search box, type `ci`. Select the checks that are required.
- Click **Save changes** button.
</details>

Each time you make a PR for your repo, CCI automatically runs your `config.yml` file. If any steps fail, then you will not be able to merge your PR with the `main` branch.

# Travis CI

<details>
  <summary>The Travis CI has been superceded by CircleCI</summary><br>

1. Add your GitHub repo to TCI.

Navigate to [TCI web page](https://travis-ci.com) and login with your GitHub credentials.

Grant TCI access to GitHub by [activating it](https://app.travis-ci.com/account/repositories) for a selected repo. Select which repo you want to build.

2. Create a file `.travis.yml` in the `root` folder of your repo. Add the following lines to the file:

```yml
services:
    - docker
env:
    - DOCKER_COMPOSE_VERSION=1.23.2
before_install:
    - sudo rm /usr/local/bin/docker-compose
    - curl -L https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-`uname -s`-`uname -m` > docker-compose
    - chmod +x docker-compose
    - sudo mv docker-compose /usr/local/bin
    - docker --version
    - docker-compose version
script:
    - cd ci
    - docker-compose build db
    - docker-compose build static-analysis
    - docker-compose build test-postgresql
    - docker-compose run test-postgresql
    - docker-compose run static-analysis
```

The `before_install` block will be executed in all Travis VMs. The block `script` will build alll the images to use and then run the tests.

> Note: For the `db` container, the Travis VM does not allow us to open port `5432`. We removed `ports` in `docker-compose` for that. Internally, the containers can talk to each other through their internal network, as the `ports` are used externally for debugging purposes.

3. We can configure tests and static analysis to run in parallel, by replacing the `script` section with a `jobs` section.

```yml
...
jobs:
    include:
        - stage: tests
          name: "Unit Tests"
          script:
          - cd ci
          - docker-compose build db
          - docker-compose bulld test-postgresql
          - docker-compose run test-postgresql
        - stage: tests
          name: "Static Analysis"
          script:
          - cd ci
          - docker-compose build static-analysis
          - docker-compose run static-analysis
```

This section creates two parallel `jobs`, named `Unit Tests` and `Static Analysis`, in one stage `tests`. This division can not only speed up the build, but it can also clarify what the problems are.

4. To take full advantage of our configured CI system, we need to ensure that we check the build before merging it into the main branch.

Navigate to your GitHub repo, and click on the repo **Settings** --> **Branches** --> **Add Rule**. Then, we enable both the **Require status checks to pass before merging** and **Require branches to be up to date before merging** options with the status checks from TCI.

> Note: If you do not see the status check from TCI, you should wait at least 30 minutes after login in to TCI with your GitHub credentials, and activating TCI on your GitHub repo.
</details>
