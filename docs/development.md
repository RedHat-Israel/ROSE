---
title: ROSE Project
tagline: Development
description: How to get started with development on the ROSE project
---
## Requirements

To install the dependencies, run:

    pipenv install

Or in the old-fashioned way

    pip install -r requirements.txt

You can also install packages from your distribution.

## Running the game

Start the server on some machine:

    ./rose-server

Open a browser at http://\<server-address\>:8880 to view and control the game.

Start up to 2 clients:

    ./rose-client mydriver.py

The server address can be specified that way (Replace '10.20.30.44' with your server address):

    ./rose-client -s 10.20.30.44 mydriver.py

For driver modules, see the examples directory.


Command line interface
----------------------

You can control the game from the command line using the rose-admin tool.

To start a race, use rose-admin tool on any machine:

    ./rose-admin <server-address> start

To stop a race, use rose-admin tool on any machine:

    ./rose-admin <server-address> stop

To modify the game rate, you can use `set-rate` command. The following command
would change game rate to 10 frames per second:

    ./rose-admin <server-address> set-rate 10


## Creating a tarball

    python setup.py sdist


## Developing

Before submitting patches, please run the tests:

    pytest

To create coverage report in html format:

    pytest --cov-report html
    xdg-open htmlcov/index.html
