[![Actions Status](https://github.com/ReYaNOW/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/ReYaNOW/python-project-52/actions)
[![Linter and Tests](https://github.com/ReYaNOW/python-project-52/actions/workflows/pyci.yml/badge.svg)](https://github.com/ReYaNOW/python-project-52/actions/workflows/pyci.yml) [
![Maintainability](https://api.codeclimate.com/v1/badges/f6133a440607757eed8c/maintainability)](https://codeclimate.com/github/ReYaNOW/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/f6133a440607757eed8c/test_coverage)](https://codeclimate.com/github/ReYaNOW/python-project-52/test_coverage)
![Static Badge](https://img.shields.io/badge/Lines_of_Code-1.3k-blue)
<p align="center">
  <img src="https://github.com/ReYaNOW/ReYaNOW/blob/main/task_manager_logo_blue.png?raw=true" alt="image"/>
</p>

<p align="center"><b>EN</b> | <a href="https://github.com/ReYaNOW/python-project-52/blob/main/README_RU.md"><b>RU</b></a></p>


Task Manager is a task management system similar
to [Redmine](http://www.redmine.org/).
It allows you to set tasks, assign performers and change their statuses.
Registration and authentication are required to work with the system.

# Usage


 - Open deployed on render.com [test example](https://task-manager-hexlet.onrender.com/)
 - [Deploy an application with Docker](#How-to-deploy-app-with-Docker)  
 - [Deploy an application without Docker](#Как-развернуть-приложение-без-Docker)

![demo image](https://github.com/ReYaNOW/ReYaNOW/blob/main/task_manager_preview.png?raw=true)

## How to deploy app with Docker
1. Clone repository

```
git clone https://github.com/ReYaNOW/python-project-52.git
```

2. Install dependencies and apply migrations to the database
  
```
make compose-setup
```
3. Start with ``make compose-start`` for development
or using ``make compose-deploy`` for deployment to production

## How to deploy app without Docker

1. Clone repository

```
git clone https://github.com/ReYaNOW/python-project-52.git
```

2. If you need to use your own PostgreSQL db, then you have to create
   database url.
   Below is the format of such a link.

```
postgresql://[user][:password]@[hostname][:port][/dbname]
```

Otherwise, django will create the SQLite3 db itself.

3. Create a .env file in the root directory of the project with something like
   this content.
    - If you are not using your own database, then the DATABASE_URL can be omitted
    - You can specify ROLLBAR_ACCESS_TOKEN, which you can get from
      [Rollbar](https://rollbar.com/), to track errors in
      production environment

```dotenv
DATABASE_URL=postgres://user:password@localhost:5432/dbname
ROLLBAR_ACCESS_TOKEN=yourtoken
SECRET_KEY=yoursecretkey
DEBUG=True
```  

Install dependencies and apply django migrations to the DB

```
make install
```

Launch a local server for development

```
make dev
```  

or deploy the project using the gunicorn server locally or for example,
on [render.com](https://render.com/)

```
make start
```  

### Minimum Requirements:

- [Python^3.10](https://www.python.org/)
- [Poetry](https://python-poetry.org/)

#### Python libraries:

- [Django](https://pypi.org/project/Django/)
- [Psycopg2-binary](https://pypi.org/project/psycopg2-binary/)
- [Gunicorn](https://pypi.org/project/gunicorn/)
- [Whitenoise](https://pypi.org/project/whitenoise/)
- [Rollbar](https://pypi.org/project/rollbar/)
- [Django-bootstrap5](https://pypi.org/project/django-bootstrap5/)
- [dj-database-url](https://pypi.org/project/dj-database-url/)
- [Django-filter](https://pypi.org/project/django-filter/)
- [Django-extensions](https://pypi.org/project/django-extensions/)
- [Django-bootstrap5](https://pypi.org/project/django-bootstrap5/)

#### For development:

- [Python-dotenv](https://pypi.org/project/python-dotenv/)
- [Flake8](https://pypi.org/project/flake8/)
- [Coverage](https://pypi.org/project/coverage/)
- [Pygount](https://pypi.org/project/pygount/)

