clean:
	pipenv --rm
coverage:
	pipenv run py.test -s --verbose --cov-report term-missing --cov-report xml --cov=eufy_security tests
init:
	pip3 install --upgrade pip pipenv
	pipenv lock
	pipenv install --three --dev
	pipenv run pre-commit install
lint:
	pipenv run flake8 eufy_security
	pipenv run pydocstyle eufy_security
	pipenv run pylint eufy_security
publish:
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload dist/*
	rm -rf dist/ build/ .egg eufy_security.egg-info/
test:
	pipenv run py.test
typing:
	pipenv run mypy --ignore-missing-imports eufy_security
