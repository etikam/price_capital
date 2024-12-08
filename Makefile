PHONY:migrate
migrate:
	py manage.py makemigrations
	py manage.py migrate

PHONY: run
run:
	py manage.py runserver

