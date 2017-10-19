init: Pipfile
	pip install --user pipenv
	pipenv install

test: pytest.ini
	pytest

admin: rose-admin
	rose-admin

server: rose-server
	rose-server

client: rose-client
	rose-client
