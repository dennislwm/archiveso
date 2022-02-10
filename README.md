# archiveso
<!--- See https://shields.io for others or to customize this set of shields.  --->

[![Netlify Status](https://api.netlify.com/api/v1/badges/60c66ba8-d468-4257-86eb-188faf80e2f0/deploy-status)](https://app.netlify.com/sites/archiveso/deploys)
![Docker Pulls](https://img.shields.io/docker/pulls/dennislwm/archiveso.svg)
![Docker Build](https://img.shields.io/docker/image-size/dennislwm/archiveso.svg)
![Docker Build](https://img.shields.io/docker/v/dennislwm/archiveso.svg)
[![dennislwm](https://circleci.com/gh/dennislwm/archiveso.svg?style=shield)](https://app.circleci.com/pipelines/github/dennislwm/archiveso)
![GitHub last commit](https://img.shields.io/github/last-commit/dennislwm/archiveso?color=red&style=plastic)

This project is an end-to-end application, using the Shape Up metholodogy, that consist of (1) static no-code front-end; (2) stateless back-end that serves request to and from an instance of ArchiveBox; and (3) CI pipeline to test and deploy a custom Docker image.

<!-- TOC -->

- [archiveso](#archiveso)
- [Things to learn and research](#things-to-learn-and-research)
- [Place, Affordance, Connection](#place-affordance-connection)
- [Usage](#usage)
  - [Prerequisites](#prerequisites)
- [Shaping](#shaping)
- [Building](#building)
- [Limitation](#limitation)
- [Methodology](#methodology)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Reference](#reference)

<!-- /TOC -->

---
# Things to learn and research

In no particular order, my plan is to use the following resources to learn and research. 

| Title | Author | Publisher Date [Short Code]
|---|---|---|
| E-Book: [Hands-On Docker for Microservices with Python](https://github.com/PacktPublishing/Hands-On-Docker-for-Microservices-with-Python) | Jaime Buelta | Packt 2019 [Buel2019]
| E-Book: Shape Up | Ryan Singer | Basecamp 2021 [Sing2021]
| [Lowdefy Documentation](https://docs.lowdefy.com/introduction) | Lowdefy | 2022 [Lowd2022]
| [Python API Usage - ArchiveBox Documentation](https://docs.archivebox.io/en/latest/Usage.html#python-api-usage) | ArchiveBox | 2022 [Arch2022]

# Place, Affordance, Connection

* Places users can navigate
  * Lowdefy app e.g. `https://archiveso.netlify.app`
  * Python Flask server (with cloudflared as a service) e.g. `https://archiveso.markit.work` 
  * Docker Hub e.g. `https://hub.docker.com/repository/docker/dennislwm/archiveso`
  
* Affordance users can act
  * Docker pull `docker pull dennislwm/archiveso:latest`

---
# Usage

## Prerequisites

Before running the Lowdefy app on your local workstation, you need the following:

- Configure a [MongoDB cluster](doc/build01.md#create-a-mongodb-cluster).
- Configure an [OpenID Connect provider](doc/build01.md#create-an-auth0-openid-connect-provider).
- Configure the [Lowdefy environment](doc/build01.md#configure-the-lowdefy-environment).

<details>
    <summary>Click here to <strong>get started.</strong></summary>

1. Open a new terminal and run a Docker container with the Python Flask server on your local workstation. This command pulls the image from Docker Hub if it doesn't exist.

```sh
docker run --rm -d -p 8080:8080 --name objArchiveso dennislwm/archiveso:latest
```

2. Run the `cloudflared` tunnel to expose your Docker container on port `8080` to a custom domain, e.g. `https://archiveso.mydomain.com`. 

```sh
cloudflared tunnel --config ~/.cloudflared/config-archiveso.yml run
```

> The tunnel remains opened as long as your don't terminate (CTRL-C) the connection.

3. Open a new terminal and build the Lowdefy app.

```sh
cd front
npx lowdefy@latest build
```

4. Run the Lowdefy app on your local workstation.

```sh
npx lowdefy@latest dev
```
</details>

![Getting Started](img/usage.gif)

---
# Shaping

As shaping and building have independent cycles, we will define shaping as any work that does not involve implementation of code. This work may include evaluation, feasibility, comparison, research, etc.

We set a time constraint of 9 workdays, for shaping, and an additional 9 workdays for building. Hence, the total time for this project is approximately 20 workdays with a cool-down of 2 workdays.

- [X] [Create a single REST endpoint with Python](doc/shape01.md#create-a-single-rest-endpoint-with-python) (2)
  - [Create a virtual environment](doc/shape01.md#create-a-virtual-environment)
  - [Install dependencies](doc/shape01.md#install-dependencies)
  - [Create a Makefile](doc/shape01.md#create-a-makefile)
  - [Create a Main Application](doc/shape01.md#create-a-main-application)
- [X] [Create test cases for each REST endpoint with Python](doc/shape02.md#create-test-cases-for-each-rest-endpoint-with-python) (1)
  - [Test Driven Development](doc/shape02.md#test-driven-development)
  - [Install developer dependencies](doc/shape02.md#install-developer-dependencies)
  - [Create a test file](doc/shape02.md#create-a-test-file)
- [X] [Create a Dockerfile and test it locally](doc/shape03.md#create-a-dockerfile-and-test-it-locally) (1)
  - [Create a Dockerfile](doc/shape03.md#create-a-dockerfile)
- [X] [Require status checks to pass before merging PR](doc/shape04.md#require-status-checks-to-pass-before-merging-pr) (1)
  - [Status Checks](doc/shape04.md#status-checks)
  - [Continuous Integration](doc/shape04.md#continuous-integration)
  - [CircleCI](doc/shape04.md#circleci)
  - [Travis CI](doc/shape04.md#travis-ci)
- [X] [Build, test, tag and upload our web app image using CI](doc/shape05.md#build-test-tag-and-upload-our-web-app-image-using-ci) (1)
  - [Workflows](doc/shape05.md#workflows)
  - [Sequential job execution with dependency](doc/shape05.md#sequential-job-execution-with-dependency)
  - [Create an access token for Docker Hub](doc/shape05.md#create-an-access-token-for-docker-hub)
- [X] [Create a front-end for our web service](doc/shape06.md#create-a-lowdefy-front-end-for-our-web-service) (2)
  - [Lowdefy Structure](doc/shape06.md#lowdefy-structure)
  - [Deploy to Netlify](doc/shape06.md#deploy-to-netlify)
    - [Requirements](doc/shape06.md#requirements)
    - [Running on a Local Server](doc/shape06.md#running-on-a-local-server)
- [X] [Expose our web app using Cloudflare Tunnel](doc/shape07.md#expose-our-web-app-using-cloudflare-tunnel) (1)
  - [Prerequisites](doc/shape07.md#prerequisites)
  - [Deploy container on local workstation](doc/shape07.md#deploy-container-on-local-workstation)
  - [Set up cloudflared](doc/shape07.md#set-up-cloudflared)
  - [Run cloudflared](doc/shape07.md#run-cloudflared)

This project started on 26-Jan-2022 and the shaping cycle was completed on 8-Feb-2022 (8 days). The expected completion date for building is 24-Feb-2022, which includes a 2-day cooldown period.

---
# Building

- [X] [Lowdefy user authentication](doc/build01.md#lowdefy-user-authentication) (1)
  - [Requirements](doc/build01.md#requirements)
  - [Configure the Lowdefy environment](doc/build01.md#configure-the-lowdefy-environment)
  - [Modify Lowdefy root schema](doc/build01.md#modify-lowdefy-root-schema)
  - [Build Lowdefy action pages](doc/build01.md#build-lowdefy-action-pages)
  - [Build Lowdefy reusable components](doc/build01.md#build-lowdefy-reusable-components)
  - [Build a Javascript login script](doc/build01.md#build-a-javascript-login-script)
  - [Create a MongoDB cluster](doc/build01.md#create-a-mongodb-cluster)
  - [Create an Auth0 OpenID Connect provider](doc/build01.md#create-an-auth0-openid-connect-provider)
  - [Secure the Auth0 connections](doc/build01.md#secure-the-auth0-connections)
- [ ] Python Flask server tokenization (1)

This steps are repeatable, i.e. expose an endpoint and build a page to allow user interaction.
- [ ] Build a Lowdefy page to allow user interaction (1)
- [ ] Build an API endpoint to execute an ArchiveBox CLI command and return its response (1)
- [ ] Build test cases to verify the API endpoint (1)

---
# Limitation

* The CI pipeline does not perform the last mile delivery, i.e deploy the Docker container Python Flask server app after it has been tagged and pushed to Docker Hub. The Continuous Delivery ["CD"] pipeline is not implemented. 
* Currently, I'm hosting the Docker container on my local workstation, i.e. http://localhost:8080 and using Cloud Tunnel to access it via https://archiveso.mydomain.com.

---
# Methodology

- Shaping and building have independent cycles. 
- Shaping requires a level of abstraction that is neither too concrete (wireframe) nor too abstract (words).
- Time constraint as an appetite for both shaping and building.
- Integrate one slice from UI to backend during shaping.
- Make a bet for what to build and honor it.
- Choose either a base, bull or bear cycle length with cool-down.
- Break a project into independent scopes, each with a smaller period, on a hill chart.
- Each independent scope should include details such as places a user can navigate (S3 bucket), affordances a user can act (/api/upload), and connections a user are taken to (api/upload -> S3 bucket).
- Integrate all scopes to form a minimal intentional product [MIP].

---
# Project Structure

```
root
|- README.md                                  <-- This README markdown file
|- .gitignore                                 <-- Git ignore file
+- doc/                                       <-- Holds documentation files
+- img/
   |- shape.drawio
+- app/
   |- Pipfile                                 <-- Requirements file for app
   |- Pipfile.lock
   |- Makefile                                <-- Makefile for app, image and dependency
   |- main.py                                 <-- Python file for app
   |- Dockerfile                              <-- Dockerfile for app
   |- docker-compose.yml                      <-- YAML file for CI static-analysis
   +- src/
      +- archiveso/
         |- __init__.py
         |- clsArchiveso.py
   +- test/
+- .circleci/                                 <-- Holds CircleCI files
   |- config.yml                              <-- Config file for CI pipeline implementation
+- front/                                     <-- Holds Lowdefy front-end static files
   |- lowdefy.yaml                            <-- YAML file for Lowdefy root schema
   +- auth0/
   +- components/                             <-- Holds YAML files for Lowdefy reusable components
   +- pages/                                  <-- Holds YAML files for Lowdefy pages
```

# Troubleshooting

1. Argo Tunnel error

Your cloudflared tunnel is not running as a service.

```sh
cloudflared tunnel --config ~/.cloudflared/config-archiveso.yml run
```

# Reference

The following resources were used as a single-use reference.

| Title | Author | Publisher Date [Short Code]
|---|---|---|
| GitHub Repo: [Flask Ticket](https://github.com/dennislwm/flask_ticket) | Dennis Lee | 2021 [Dlee2021]
| [Creating a Python Makefile - Earthly Blog](https://earthly.dev/blog/python-makefile) | Aniket Bhattacharyea | 2021 [Bhat2021]
| [Command Line Interface - Flask Documentation](https://flask.palletsprojects.com/en/2.0.x/cli) | Flask | 2022 [Flas2022]
| [About fixtures - Full pytest documentation](https://docs.pytest.org/en/latest/explanation/fixtures.html) | pytest | 2022 [pyte2022]
| GitHub Repo: [Flask tutorial](https://github.com/pallets/flask/tree/fdac8a5404e3e3a316568107a293f134707c75bb/examples/tutorial) | Pallets Projects | 2022 [Pall2022]
| [pipreqs 0.4.11 - Project description](https://pypi.org/project/pipreqs) | Vadim Kravcenko | 2022 [Krav2022]
| [Autodocumenting Makefiles](https://daniel.feldroy.com/posts/autodocumenting-makefiles) | Daniel Greenfeld | 2022 [Gree2022]
| [GitHub CI/CD tutorial: Setting up continuous integration](https://circleci.com/blog/setting-up-continuous-integration-with-github) | Stanley Ndagi | 2022 [Ndag2022]
| [Python static code analysis tools](https://pawamoy.github.io/posts/python-static-code-analysis-tools) | Timothy Mazzucotelli | 2017 [Mazz2017]
| [Build and Deploy only on PR request Accept](https://discuss.circleci.com/t/build-and-deploy-only-on-pr-request-accept/38846) | CircleCI | 2021 [Circ2021]
| [Using CircleCI workflows to replicate Docker Hub automated builds](https://circleci.com/blog/using-circleci-workflows-to-replicate-docker-hub-automated-builds/) | Jonathan Cardoso | 2020 [Card2020]
| GitHub Repo: [lowdefy-example-openid-connect](https://github.com/lowdefy/lowdefy-example-openid-connect) | lowdefy | 2021 [Lowd2021]