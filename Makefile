compilemessages:
	django-admin compilemessages --ignore=.venv || true

install:
	poetry install

dev:
	python manage.py runserver

start:
	gunicorn task_manager.wsgi

