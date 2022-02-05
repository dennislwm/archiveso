# archiveso

This project is an end-to-end application, using the Shape Up metholodogy, that consist of (1) static no-code front-end; (2) stateless Flask back-end that serves request to and from an instance of ArchiveBox; and (3) CI pipeline to test and deploy a custom Docker image.

<!-- TOC -->

- [archiveso](#archiveso)
- [Things to learn and research](#things-to-learn-and-research)
- [Shaping](#shaping)
- [Building](#building)
- [Methodology](#methodology)
- [Project Structure](#project-structure)
- [Reference](#reference)

<!-- /TOC -->

---
# Things to learn and research

In no particular order, my plan is to use the following resources to learn and research. 

| Title | Author | Publisher Date [Short Code]
|---|---|---|
| E-Book: [Hands-On Docker for Microservices with Python](https://github.com/PacktPublishing/Hands-On-Docker-for-Microservices-with-Python) | Jaime Buelta | Packt 2019 [Buel2019]
| E-Book: Shape Up | Ryan Singer | Basecamp 2021 [Sing2021]
| [Python API Usage - ArchiveBox Documentation](https://docs.archivebox.io/en/latest/Usage.html#python-api-usage) | ArchiveBox | 2022 [Arch2020]

---
# Shaping

As shaping and building have independent cycles, we will define shaping as any work that does not involve implementation of code. This work may include evaluation, feasibility, comparison, research, etc.

We set a time constraint of 10 workdays, for shaping, and an additional 9 workdays for building. Hence, the total time for this project is approximately 20 workdays with a cool-down of 2 workdays.

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
- [X] [Require status checks to pass before merging PR](doc/shape04.md#require-status-checks-to-pass-before-merging-pr) (2)
  - [Status Checks](doc/shape04.md#status-checks)
  - [Continuous Integration](doc/shape04.md#continuous-integration)
  - [CircleCI](doc/shape04.md#circleci)
  - [Travis CI](doc/shape04.md#travis-ci)
- [ ] [Build, test, tag and upload our web app image using CI](doc/shape05.md#build-test-tag-and-upload-our-web-app-image-using-ci) (1)
  - [Workflows](doc/shape05.md#workflows)
  - [Sequential job execution with dependency](doc/shape05.md#sequential-job-execution-with-dependency)
  - [Create an access token for Docker Hub](doc/shape05.md#create-an-access-token-for-docker-hub)
- [ ] Create a Lowdefy front-end for our web service (1)
- [ ] Expose our web app using Cloudflare Tunnel (1)

This project started on 26-Jan-2022 and is a work-in-progress. The expected completion date is 24-Feb-2022, with an expected shaping completion at 11-Feb-2022 (includes a 2-day cooldown).

---
# Building

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
|- README.md
+- doc
+- img
   |- shape.drawio
+- app
   |- Pipfile
   |- Pipfile.lock
   |- Makefile
   |- main.py
   +- src
      +- archiveso
         |- __init__.py
         |- clsArchiveso.py
   +- test
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