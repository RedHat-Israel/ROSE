.PHONY: lint lint-fix build-image

IMAGE_NAME ?= quay.io/rose/rose-common

# By default, run both linting and tests
all: lint

lint:
	@echo "Running flake8 linting..."
	flake8 --show-source --statistics .
	black --check --diff .

lint-fix:
	@echo "Running lint fixing..."
	@black --verbose --color .

build-image:
	@echo "Building container image ..."
	podman build -t $(IMAGE_NAME) .
