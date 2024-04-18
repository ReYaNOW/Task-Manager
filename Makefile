install:
	poetry install

dev:
	poetry run python manage.py runserver

start:
	gunicorn task_manager.wsgi

shell:
	python3 manage.py shell_plus --ipython

lint:
	poetry run flake8 task_manager

test:
	poetry run python3 manage.py test

test-coverage:
	poetry run coverage run manage.py test
	poetry run coverage report -m --include=task_manager/* --omit=task_manager/settings.py,*/migrations/*,*/tests/*,tests.py
	poetry run coverage xml --include=task_manager/* --omit=task_manager/settings.py,*/migrations/*,*/tests/*,tests.py

check:
	make lint
	make test

messages:
	django-admin makemessages -l ru
	django-admin makemessages -l en

compilemessages:
	django-admin compilemessages --ignore=.venv || true

migrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

collectstatic:
	python3 manage.py collectstatic
