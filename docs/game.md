---
title: ROSE Project
tagline: Materials
description: This project is a game that has been developed in order to help teach kids Python
---

# Game

## Introduction

### Getting the source

```
git clone https://github.com/RedHat-Israel/ROSE.git
```

install pipenv

```
pip install --user pipenv
```

installing using pipenv
```
pipenv install
```

Using pipenv shell
```
pipenv shell
```

### Running the server
Each student should run his server on a different server port and a different web port, we will let you know in which ports you should use.

```
./rose-server --server-port 1234 --web-port 8881
```

### Viewing the game UI in a browser


```
http://localhost:8881/
```

The port used here is the web port (what was used in --web-port when starting the server).

### Run example driver
You should run the client with the same server port you used to run the server:

```
./rose-client examples/random-driver.py --server-port 1234
```

## Writing your driver

### Writing your own None driver

Create a new python file 'yourname.py', and write the following lines:

```
from rose.common import obstacles, actions

driver_name = "Michael Schumacher"

def drive(world):
    return actions.NONE
```

In order to run your driver, use:

Don't forget to add the server port when running the server and client.
If you want to connect to your friend's server, you should run the client with the same server port he used.


```
./rose-client yourname.py --server-port 1234 
```

### Print your car location
```
x = world.car.x
y = world.car.y

print ("Current location is: (%d,%d)" % (x ,y))
```

### Print the obstacle a head
```
obstacle = world.get((x, y - 1))

print (obstacle)
```

### Restarting after exceptions
After getting an exception, make sure to re-run your driver:
```
./rose-client yourname.py
```
### Handling PENGUIN

### Handling WATER

### Handling CRACK

### Handling other obstacles

### Running multiple drivers

## Improving drivers

### Moving out to track

### Choosing best move (RIGHT or LEFT)

### Driving in other car lane

### Remembering your lane

### Looking more than one penguin a head

### Competing with your classmates' drivers

- Finding ip address<br>
Look for an address that starts with 10.35
```
ip addr
```
- Connecting rose-client to remote machine<br>
For example, in order to compete with client `foo.py` on `10.35.1.2`:
```
./rose-client -s 10.35.1.2 foo.py
```
