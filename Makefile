init: Pipfile
	python -m pip install pipenv --user
	pipenv install

dev-init: Pipfile
	python -m pip install pipenv --user
	pipenv install --dev

test: pytest.ini
	pipenv run pytest

admin: rose-admin
	pipenv run ./rose-admin

server: rose-server
	pipenv run ./rose-server

client: rose-client
	pipenv run ./rose-client

container-image:
	podman build --build-arg DEV=True -t rose_dev .
