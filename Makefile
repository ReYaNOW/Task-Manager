install:
	poetry install

dev:
	python manage.py runserver

start:
	make collectstatic
	gunicorn task_manager.wsgi

lint:
	poetry run flake8 task_manager

test:
	python3 manage.py test

check:
	make lint
	make test

messages:
	django-admin makemessages -l ru
	django-admin makemessages -l en

compilemessages:
	django-admin compilemessages --ignore=.venv || true

makemigrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

collectstatic:
	python3 manage.py collectstatic
