# cicd-assignment-FA23-BCT-054

**Zohaib Ahmad Tariq — FA23-BCT-054**
CSC418 Cloud Computing, Lab Assignment 3: an automated CI/CD pipeline for a web
application, built with GitHub, Docker, Jenkins and Selenium.

## Contents

| File | Purpose |
|---|---|
| `index.html` | The web page: student name, roll number, a message button and a text box with Submit |
| `Dockerfile` | Serves the page with nginx |
| `tests/Dockerfile` | Test agent image: Python, Selenium, pytest, Chromium and ChromeDriver |
| `tests/test_site.py` | 5 Selenium tests (title, heading, roll number, button click, text box input); one test saves a screenshot |
| `Jenkinsfile` | Multi-stage pipeline: Checkout → Package → Start Staging → Test → Deploy |

## Run it manually (Task 1)

```bash
# 1. Start the page in a container
docker build -t cicd-site .
docker run -d --name site -p 8080:80 cicd-site

# 2. Build the test agent and run the tests inside it
docker build -t cicd-tests tests/
docker run --rm --network host -e SITE_URL=http://localhost:8080 cicd-tests

# All 5 tests must pass.
```

## Jenkins pipeline (Task 2)

Create a **Pipeline** job with **Pipeline script from SCM** pointing at this
repository. The pipeline:

1. **Checkout** – clones this repository.
2. **Package** – builds the nginx Docker image, tagged with the build number.
3. **Start Staging** – starts the new image as a staging container on a private
   Docker network.
4. **Test** – builds the Selenium test-agent image and runs the tests against
   staging; results are published with `junit`. **If any test fails, the
   pipeline stops here.**
5. **Deploy** – only reached when every test passes: replaces the live
   container (port 8080) with the new build.

A GitHub webhook (`/github-webhook/`) triggers the pipeline automatically on
every push, so a change to the page goes live without clicking *Build Now* —
but only if it passes the tests (the quality gate).
