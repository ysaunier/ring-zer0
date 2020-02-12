GIT_DESCRIBE_TAG = $(shell git describe --always --tag)
VERSION = $(GIT_DESCRIBE_TAG)
PY_FILES:=$(shell find . -name '*.py' -not -path '*/node_modules/*' -not -path './.venv/*')

install:
	pipenv install

clean:
	@find . -type f -name '*.py[co]' -delete -print -o -type d -name __pycache__ -delete >/dev/null
	@find . -name '.coverage' -delete >/dev/null
	@rm -rf .pytest_cache

ab:
	@echo $(PY_FILES)

codestyle:
	@flake8
	@pylint --rcfile=pylint.ini $(PY_FILES)

version:
	@echo $(VERSION)

test: clean
	@pytest --random --disable-warnings
