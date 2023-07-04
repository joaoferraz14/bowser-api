.PHONY: install-precommit setup-hooks

install-precommit:
	pip install pre-commit

setup-hooks:
	pre-commit install

all: install-precommit setup-hooks

