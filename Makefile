dev:
	poetry run flask --app page_analyzer:app run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

install:
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

lint:
	poetry run flake8 gendiff

test-coverage:
	poetry run pytest --cov=page_analyzer --cov-report xml

selfcheck:
	poetry check

check: selfcheck test lint

start-debug:
	poetry run flask --app page_analyzer/app --debug run