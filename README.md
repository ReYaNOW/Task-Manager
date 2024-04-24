[![Actions Status](https://github.com/ReYaNOW/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/ReYaNOW/python-project-52/actions)
[![Linter and Tests](https://github.com/ReYaNOW/python-project-52/actions/workflows/pyci.yml/badge.svg)](https://github.com/ReYaNOW/python-project-52/actions/workflows/pyci.yml) [
![Maintainability](https://api.codeclimate.com/v1/badges/f6133a440607757eed8c/maintainability)](https://codeclimate.com/github/ReYaNOW/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/f6133a440607757eed8c/test_coverage)](https://codeclimate.com/github/ReYaNOW/python-project-52/test_coverage)
![Static Badge](https://img.shields.io/badge/Lines_of_Code-1.3k-blue)
<p align="center">
  <img src="https://github.com/ReYaNOW/ReYaNOW/blob/main/task_manager_logo.png?raw=true" alt="image"/>
</p>


Task Manager – система управления задачами,
подобная [Redmine](http://www.redmine.org/).
Она позволяет ставить задачи, назначать исполнителей и менять их статусы.
Для работы с системой требуется регистрация и аутентификация

![demo image](https://github.com/ReYaNOW/ReYaNOW/blob/main/task_manager_preview.png?raw=true)

# Использование

Открыть задеплоенный на render.com
[тестовый вариант](https://task-manager-hexlet.onrender.com/)

### Либо развернуть приложение локально

1. Склонировать репозиторий

```
git clone https://github.com/ReYaNOW/python-project-52.git
```

2. Если необходимо использовать свою БД PostgreSQL, тогда нужно составить
   database url.
   Ниже представлен формат такой ссылки.

```
postgresql://[user][:password]@[hostname][:port][/dbname]
```

В ином случае django сам создаст БД SQLite3

3. Создать файл .env в корневой директории проекта примерно c таким содержанием.   
   - Если не используете свою БД, то DATABASE_URL можно не указывать
   - Можно указать ROLLBAR_ACCESS_TOKEN с сайта [Rollbar](https://rollbar.com/), для отслеживания ошибок в production среде  

```dotenv
DATABASE_URL=postgres://user:password@localhost:5432/dbname
ROLLBAR_ACCESS_TOKEN=yourtoken
SECRET_KEY=yoursecretkey
DEBUG=True
```  

Установить зависимости и применить django миграции к БД

```
make install
```

Запустить локальный сервер для разработки

```
make dev
```  

Либо задеплоить проект при помощи сервера gunicorn локально или например,
на [render.com](https://render.com/)

```
make start
```  

### Минимальные требования:

- [Python^3.10](https://www.python.org/)
- [Poetry](https://python-poetry.org/)

#### Библиотеки Python:

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

##### Для разработки
- [Python-dotenv](https://pypi.org/project/python-dotenv/)
- [Flake8](https://pypi.org/project/flake8/)
- [Coverage](https://pypi.org/project/coverage/)
- [Pygount](https://pypi.org/project/pygount/)

