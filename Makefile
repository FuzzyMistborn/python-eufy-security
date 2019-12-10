clean:
	.venv/bin/pre-commit uninstall
	rm -rf .venv/
coverage:
	.venv/bin/py.test -s --verbose --cov-report term-missing --cov-report xml --cov=eufy_security tests
format:
	.venv/bin/black eufy_security
	.venv/bin/black tests
	.venv/bin/docformatter -ir eufy_security
init:
	python3 -m venv .venv
	.venv/bin/pip3 install poetry
	.venv/bin/poetry lock
	.venv/bin/poetry install
	.venv/bin/pre-commit install
lint:
	.venv/bin/black --check --fast eufy_security
	.venv/bin/flake8 eufy_security
	.venv/bin/docformatter -r -c eufy_security
	.venv/bin/pylint eufy_security
publish:
	.venv/bin/poetry build
	.venv/bin/poetry publish
	rm -rf dist/ build/ .egg *.egg-info/
test:
	.venv/bin/py.test
typing:
	.venv/bin/mypy --ignore-missing-imports eufy_security
