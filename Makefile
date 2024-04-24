PORT ?= 8080


install:
	poetry install --no-dev
	make migrate

install_no_dev:
	poetry install --no-dev
	make migrate

dev:
	poetry run python3 manage.py runserver $(PORT)

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi:application

shell:
	poetry run python3 manage.py shell_plus --ipython

lint:
	poetry run flake8 task_manager

test:
	poetry run python3 manage.py test

test-coverage:
	poetry run coverage run manage.py test
	poetry run coverage report -m
	poetry run coverage xml

check:
	make lint
	make test

messages:
	poetry run django-admin makemessages -l ru
	poetry run django-admin makemessages -l en

compilemessages:
	poetry run django-admin compilemessages --ignore=.venv || true

migrations:
	poetry run python3 manage.py makemigrations

migrate:
	poetry run python3 manage.py migrate

collectstatic:
	poetry run python3 manage.py collectstatic

get_loc:
	pygount --folders-to-skip="[...]migrations,static,locale" -f summary task_manager/