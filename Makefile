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
	zensical build

serve:
	cp CHANGELOG.md ./docs/changelog.md
	zensical serve

publish:
	cp CHANGELOG.md ./docs/changelog.md
	zensical build

clean:
	rm -rf site