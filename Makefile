init:
	pip install -r rose/client/requirements.txt
	pip install -r rose/server/requirements.txt

dev-init: init
	pip install -r rose/client/requirements-dev.txt
	pip install -r rose/server/requirements-dev.txt

lint:
	make -C rose/client lint
	make -C rose/server lint

lint-fix:
	make -C rose/client lint-fix
	make -C rose/server lint-fix

test:
	make -C rose/client test
	make -C rose/server test

clean:
	-find . -name '.coverage' -exec rm {} \;
	-find . -name 'htmlcov' -exec rmdir {} \;
	-find . -name '*.pyc' -exec rm {} \;
	-find . -name '__pycache__' -exec rmdir {} \;
	-find . -name '.pytest_cache' -exec rmdir {} \;

