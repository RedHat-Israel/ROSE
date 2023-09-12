.PHONY: lint test lint-fix code-quality run build-image run-image clean

IMAGE_NAME ?= quay.io/rose/rose-server
PORT ?= 8880
WS_PORT ?= 8765

# Default driver when running on localhost
DRIVERS ?= http://127.0.0.1:8081

# By default, run both linting and tests
all: lint test

lint:
	@echo "Running linting..."
	flake8 --show-source --statistics .
	black --check --diff .

lint-fix:
	@echo "Running lint fixing..."
	black --verbose --color .

code-quality:
	@echo "Running static code quality checks..."
	radon cc .
	radon mi .

test:
	@echo "Running unittests..."
	pytest

run:
	@echo "Running driver logic server ..."
	python main.py --port $(PORT) --drivers $(DRIVERS)

build-image:
	@echo "Building container image ..."
	podman build -t $(IMAGE_NAME) .

run-image:
	@echo "Running container image ..."
	podman run --rm --network host -it $(IMAGE_NAME)

clean:
	-rm -rf .coverage
	-rm -rf htmlcov
	-find . -name '*.pyc' -exec rm {} \;
	-find . -name '__pycache__' -exec rmdir {} \;
