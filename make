docs:
	python make_docs.py
	mkdocs build

serve:
	python make_docs.py
	mkdocs serve