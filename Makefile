init: Pipfile
	pip install --user pipenv
	pipenv install

test: pytest.ini
	pytest

admin: rose-admin
	pipenv run ./rose-admin

server: rose-server
	pipenv run ./rose-server

client: rose-client
	pipenv run ./rose-client
