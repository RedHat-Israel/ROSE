# ROSE Project

## Requirements

To install the requirements, run:

    pip install -r requirements.txt

You can also install packages from your distribution.


## Running the game

Start the server on some machine:

    ./rose-server

Start up to 2 clients:

    ./rose-client mydriver.py

For drive modules, see the examples direcotory.

To start a race, use rose-admin tool on any machine:

    ./rose-admin <server-address> start

To stop a race, use rose-admin tool on any machine:

    ./rose-admin <server-address> stop

To modify the game rate, you can use set-rate command. The following command
would change game rate to 10 frames per second:

    ./rose-admin <server-address> set-rate 10


## Creating a tarball

    python setup.py sdist


## Developing

Before submitting patches, please run the tests:

    pytest

Creating coverage report in html format:

    pytest --cov-report html
    xdg-open htmlcov/index.html
