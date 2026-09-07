.PHONY: demo test node help

PYTHONPATH := .

help:
	@echo "make demo  - run the local demo"
	@echo "make test  - run the light tests"
	@echo "make node  - start the node on port 5000"

demo:
	PYTHONPATH=$(PYTHONPATH) python3 blockchain/run.py

test:
	PYTHONPATH=$(PYTHONPATH) python3 -m unittest tests.test_basic -v

node:
	PYTHONPATH=$(PYTHONPATH) python3 blockchain/cli.py node --port 5000
