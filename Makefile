# Makefile for HomematicIP Cloud Rest API Wrapper

.PHONY: install test docs serve clean publish

install:
	pip install -r requirements.txt
	pip install -r requirements_dev.txt
	pip install -r requirements_docs.txt

test:
	pytest

docs:
	cp CHANGELOG.md ./docs/changelog.md
	mkdocs build

serve:
	cp CHANGELOG.md ./docs/changelog.md
	mkdocs serve

publish:
	cp CHANGELOG.md ./docs/changelog.md
	mkdocs gh-deploy --force

clean:
	rm -rf site