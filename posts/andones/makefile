build:
	python3 -m venv and_ones_env
	. and_ones_env/bin/activate
	pip3 install -r requirements.txt

cleanup:
	rm -rf and_ones_env/

.PHONY: test
test: build
	pytest

run: build
	python3 andones.py