clean:
	pipenv --rm
coverage:
	pipenv run py.test -s --verbose --cov-report term-missing --cov-report xml --cov=aiowwlln tests
init:
	pip3 install --upgrade pip pipenv
	pipenv lock
	pipenv install --three --dev
	pipenv run pre-commit install
lint:
	pipenv run flake8 aiowwlln
	pipenv run pydocstyle aiowwlln
	pipenv run pylint aiowwlln
publish:
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload dist/*
	rm -rf dist/ build/ .egg aiowwlln.egg-info/
test:
	pipenv run py.test
typing:
	pipenv run mypy --ignore-missing-imports aiowwlln
