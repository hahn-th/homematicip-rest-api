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
	python scripts/gen_api_docs.py
	zensical build

serve:
	cp CHANGELOG.md ./docs/changelog.md
	python scripts/gen_api_docs.py
	zensical serve

publish:
	cp CHANGELOG.md ./docs/changelog.md
	python scripts/gen_api_docs.py
	zensical build

clean:
	rm -rf site