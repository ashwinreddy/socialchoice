init:
	pip install -r requirements.txt

test:
	py.test test_voting.py

.PHONY: init test