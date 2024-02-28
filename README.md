I've called this project *FlaskWiki*, a Flask RESTful API that serves you data sourced from Wikitech's [Analytics/AQS/Pageviews](https://wikitech.wikimedia.org/wiki/Analytics/AQS/Pageviews) RESTful APIs with some extra functionality catered to the requests of the take-home. There is a Swagger UI that you can use to interact with the endpoints and documentation. I describe some of the steps of getting this web server up and running on your local, as well as notes (things like opportunities for improvement etcetera).
  
Author: Nachmi Kott

## **Abstract**:

* Create a web server with API endpoints that support the following features:
  * Retrieve a list of the most viewed articles for a week or a month (if an article is not listed on a given day, you can assume it has 0 views)
  * Retrieve the view count of a specific article for a week or a month
  * Retrieve the day of the month where an article got the most page views*

## Installation:

Prerequisites: A functioning version of `python3` and CLI.

* Because python3 is by default installed on Unix machines (and I assume this audience is an active developer) (or [freely installable on Windows](https://docs.python.org/3/using/windows.html#:~:text=Python%20will%20always%20be%20available,PowerShell%20session%20by%20typing%20python%20.)) a prerequisite to running these steps is to have python3 available on your local. Adding in a Dockerfile to create the environment is mentioned in Opportunities for Improvement.

Step 0: Clone This Repo

`git clone git@github.com:nachmikott/flask_wiki.git` (or HTTPS)

Step 1: change directories to the root of the project

`cd flask_wiki`

Step 2: Create Virtual Environment

`python3 -m venv .venv`

Step 3: Activate Virtual Environment

`. .venv/bin/activate`

Step 4: Install `requirements.txt`

`pip3 install --no-cache-dir -r requirements.txt`

## Run Server:

`flask --app app run`

* Optionally, add `--debug` to run in debug mode.

## Access Swagger

`http://127.0.0.1:5000/swagger`

## Run Tests:

`pytest`

## Notes

Tech Stack Decisioning:

* Flask + Python + Pytest + Swagger: I wanted something to use that was extensible but quick to running. Amongst the top frameworks/libraries in Python, both Flask and Django were amongst the two most popular and suggested. Flask seemed lighter-weight that was better suited for this project.

Assumptions:
* *Retrieve the view count of a specific article for a week or a month* <-- I maintained the `start_timestamp`, `end_timestamp` convention WikiTech had in the API params. I wanted to create an API that was expandable for further use-cases (What about bi-weekly, every 2 weeks?, every yearly quarter?). Using the`start_timestamp` & `end_timstamp` conventions for accessing the data allows us to *retrieve the view count of a specific article for a week, or a month*, or anything the user may need in the future.

  * Tradeoffs: An API parameterized endpoint like `/{weekly}/` or `/{monthly}/` could require less timeformatting of a date. I chose extensibility in this case, but future user feedback can allow us to add those.
* *Retrieve the day of the month where an article got the most page views* <-- I maintained the `start_timestamp`, `end_timestamp` pattern convention for similar reasons - to allow for extensibility to meet a requirement beyond weekly, or monthly. This API allows for a user to *retrieve the day of the month where an article got the most page views*.

Opportunities For Improvement:

* Validators as Decorators:

  * In code, I have validations as methods that throw (ex `TimestampException`) (that are then caught and dealt with. I would like to leverage a tool to make that a decorator. Often decorators can be offered using frameworks/libraries that treat RESTful API endpoints on Flask as the main objective. Examples include [Flask/Marshmellow](https://flask-smorest.readthedocs.io/en/latest/), [flask-restful](https://flask-restful.readthedocs.io/en/latest/)
* Continued coverage of Unit Testing.
* Logging/Telemetry. At this stage I have print statements in key places (status_code responses, calling external APIs), but using a logger to emmit telemetry and log exception with better formatting will make this application more easy to monitor. 
* Swagger UI Documentation in-line with python code docs. For now, its JSON. Theres opportunities to better co-locate the documentation and the code.
* Dockerized deliverable. A working installation of python3 is assumed, but having a Dockerfile that allows to build out a container for a deterministic environment to run FlaskWiki is ideal.

Potential Next Steps (Looking Ahead).

* Support for GraphQL.

  * WikiTech may be an only RESTful API, but FlaskWiki can support both RESTful and GraphQL! Example flask plugins like [flask-graphql](https://github.com/graphql-python/flask-graphql) can be a good start.
* Additional support for other aggregations of data offered by WikiTech.

  * Examples include view counts of an article _by country_, view counts for _all_ of wikipedia projects, etcetera.
* GitHub Actions and Pull Request Strategy (scaling _how_ to work).

  * I worked on this alone, so I was a bit more easy-going on the initial Pull Request Strategy, and _how_ we built up main, and other branched version. If ever multiple people were to work on this project, I'd leverage GitHub Actions and other conditionals to help facilitate working well together and ensuring best practices to contributing.
* CICD, IaC, E2E Testing.
