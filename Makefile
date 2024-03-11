compilemessages:
	django-admin compilemessages --ignore=.venv

install:
	poetry install
	make compilemessages


dev:
	python manage.py runserver

start:
	gunicorn task_manager.wsgi