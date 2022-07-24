# ROSE Project

![CI WorkFlow](https://github.com/RedHat-Israel/ROSE/actions/workflows/ci.yml/badge.svg)


This project is a game that has been developed to assist in teaching
kids python.  The students need to code the behavior of a car to achieve
the best score.

Here is a video of a race (running code from students):
(Click on the screenshot to play the video)

<a href="http://www.youtube.com/watch?feature=player_embedded&v=BEV-CcqTOnw
" target="_blank"><img src="docs/rose-video-preview.jpg"
alt="ROSE Race Car Game" width="860" height="720" border="10" /></a>

In this game, two race cars compete to achieve the most points.  The
race car must recognize the race track, the obstacles, and the bonus
areas; then calculate the best path where the pitfalls are avoided and
all the bonus points are collected.  The cars move autonomously on the
screen within the race track game with no interference from the
students. No joystick or mouse shall be used.

In order to control the car movements, the students needs to implement a
'driver'.  This code  controls the car and will decide what the next
action of the car will be.

For each type of obstacles there is a different action and different
points assigned.

See [examples/README.md](examples/README.md) for an explanation on how
to write a driver module.

## GitHub pages

Refer to our GitHub pages for the course materials and additional resources:
[https://redhat-israel.github.io/ROSE/](https://redhat-israel.github.io/ROSE/)

## Talks and presentations

- [Read](http://www.pc.co.il/news/252820/) an interview with Miki Kenneth
  on [People and Computers](http://www.pc.co.il)
- [Read](http://schd.ws/hosted_files/osseu17/b9/BringingPeopleTogetherWithOpenSource.pdf)
  [Fred Rolland](https://github.com/rollandf) and [Ori Rabin](https://github.com/orrabin)'s presentation
  at [Open Source Summit Europe 2017](http://events.linuxfoundation.org/events/archive/2017/open-source-summit-europe-/)
- [Read](http://ap.hamakor.org.il/2017/tracks.html#main-f1015) [Fred Rolland](https://github.com/rollandf)
  and [Ori Rabin](https://github.com/orrabin)'s presentation at
  [August Penguin 2017](http://ap.hamakor.org.il/2017/)
- [Watch](https://www.youtube.com/watch?v=41oxZr43Ih0) [Fred Rolland](https://github.com/rollandf)
  and [Ori Rabin](https://github.com/orrabin)'s talk at
  [PyCon Israel 2017](https://pycon.org.il/2017/)
- [Read](https://opensource.com/education/15/9/open-source-education-israel)
  an article by Laura Novich on [opensource.com](https://opensource.com)

## Requirements

Once we're in the ROSE directory, we need to verify we have pipenv
installed.  In order to make sure we have pipenv installed:

    pipenv --version

If you don't have it installed, the best way is to install it only for
your user:

    python -m pip install --user pipenv

## Getting started

The following commands should be performed only once; after creating the
environment you will be connecting to the same environment each time you
open a new session.

Use pipenv to create a virtual environment and to install the rest of
the dependencies:

    pipenv install

You can also install development packages by running:

    pipenv --dev install

After creating the environment, we want to activate and enter our
environment (make sure you're in the ROSE directory):

    pipenv shell

Indication that you are inside the environment, the prompt line will
look like this:

    (ROSE) [username@hostname ROSE]$

## Running the server

If you are not in your virtual environment, please run it:

    pipenv shell

Start the server on some machine:

    ./rose-server

For running the same track for all drivers (instead or random) start the
server using:

    ./rose-server -t same

Open a browser at http://{server-address}:8880 to view and control the
game.

### Running the server in Podman

Build the Docker image:

    podman build -t rose_server .

Run the Docker image on port 8880:

    podman run -it --rm --name=rose_server -p 8880:8880 rose_server python ./rose-server

If you don't want to see the log of the run in the current window,
replace `-it` with `-d`.

Open a browser at http://{server-address}:8880 to view and control the
game.

### Tunneling the UI server to your browser

You can use SSH tunneling when running the server on your remote VM, so
you can view the game in you local browser:

    ssh -L 8880:127.0.0.1:8880 {user}@{server-address}

After starting the server (as mentioned above), open a browser at
http://127.0.0.1:8880/ to view and control the game.

### Opening firewall ports

You can also open ports 8880 and 8888 on the remote VM running the
server, and browse from a local machine in case port 8880 or 8888 are
blocked by [firewalld](https://firewalld.org/):

    sudo firewall-cmd --add-port=8880/tcp --permanent
    sudo firewall-cmd --add-port=8888/tcp --permanent
    sudo firewall-cmd --reload

## Running a driver

In a new window, open your virtual environment:

    pipenv shell

Create your driver file:

    cp examples/none.py mydriver.py

Edit the file mydriver.py and change the driver_name variable to your
name.

Start up the client, using your driver file:

    ./rose-client mydriver.py

The server address can be specified that way (Replace '10.20.30.44' with
your server address):

    ./rose-client -s 10.20.30.44 mydriver.py

For running the driver on the Docker container use:

    docker exec -it rose_server python ./rose-client examples/random-driver.py

For driver modules, see the [examples](examples) directory.

You can run the game with just 1 driver!

To let 2 drivers compete, repeat these commands in 2 terminals.

## Command line interface

You can control the game from the command line using the rose-admin
tool.

To start a race, use the rose-admin tool on any machine:

    ./rose-admin {server-address} start

To stop a race, use the rose-admin tool on any machine:

    ./rose-admin {server-address} stop

To modify the game rate, you can use the "set-rate" command. The
following command would change game rate to 10 frames per second:

    ./rose-admin {server-address} set-rate 10

## Using tmux / screen

`./rose-server` and `./rose-client {driver name}` do not return, but
continue running, in order to run both server and drivers a user need to
run them in separate shells, Each driver will run it it's own pipenv
shell. `tmux` may be useful in this case.

Example `tmux` commands:

| Command | Description              |
|---------|--------------------------|
| Ctrl+c  | Create a new window      |
| Ctrl+n  | Toggle to next window    |
| Ctrl+w  | List open windows        |

## Creating a tarball

    python setup.py sdist

## Developing

Should you want to contribute to the project, please read the
[Code of Conduct](docs/code-of-conduct.md).

To install development requirements:

    pipenv install --dev

To open a shell for development, use:

    pipenv shell

For development in docker, use:

    docker build --build-arg DEV=True -t rose_dev .

Before submitting patches, please run the tests:

    flake8
    pytest

Creating coverage report in html format:

    pytest --cov-report html
    xdg-open htmlcov/index.html
