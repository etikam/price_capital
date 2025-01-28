.PHONY: help install migrate run shell test clean collectstatic superuser lint format

help:
	@echo "Available commands:"
	@echo "install      - Install Python dependencies"
	@echo "migrate      - Run database migrations"
	@echo "run         - Run development server"
	@echo "shell       - Open Django shell"
	@echo "test        - Run tests"
	@echo "clean       - Remove Python file artifacts"
	@echo "collectstatic - Collect static files"
	@echo "superuser   - Create superuser"
	@echo "lint        - Check code style with flake8"
	@echo "format      - Format code with black"

install:
	pip install -r requirements.txt

migrate:
	python manage.py makemigrations
	python manage.py migrate

run:
	python manage.py runserver

shell:
	python manage.py shell

test:
	python manage.py test

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".coverage" -exec rm -r {} +

collectstatic:
	python manage.py collectstatic --noinput

superuser:
	python manage.py createsuperuser

lint:
	flake8 .

format:
	black .
