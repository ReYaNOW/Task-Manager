PORT ?= 8080


install:
	poetry install
	make migrate

install-no-dev:
	poetry install --only main
	make migrate

compose-setup:
	docker compose build
	docker compose run --rm web make migrate

compose-start:
	docker compose up --abort-on-container-exit || true

compose-prod:
	docker compose up --no-start
	docker compose run -p $(PORT):$(PORT) web make start || true
	make compose-stop

compose-down:
	docker compose down --remove-orphans || true

compose-stop:
	docker compose stop || true

enter-db:
	docker compose up --abort-on-container-exit --no-start
	docker compose start db
	docker compose exec -it db psql -U pguser -d pgdb psql

dev:
	poetry run python manage.py runserver 0.0.0.0:$(PORT)

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