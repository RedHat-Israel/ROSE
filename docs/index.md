---
title: ROSE Project
tagline:
description: This project is a game that has been developed in order to help teach kids Python
---

# ROSE Project

[![Build Status](https://travis-ci.org/RedHat-Israel/ROSE.svg?branch=master)](https://travis-ci.org/RedHat-Israel/ROSE)

This project is a game that has been developed in order to help teach kids python.
The students need to code the behavior of the car in order to achieve the best score.

Here is video of a race, using drivers coded by students:<br/>
(Click on it to play the video)

<a href="http://www.youtube.com/watch?feature=player_embedded&v=BEV-CcqTOnw
" target="_blank"><img src="rose-video-preview.jpg"
alt="ROSE Race Car Game" width="860" height="720" border="10" /></a>

In this game, two race cars compete to achieve the most points.
The race car has to recognize the race track, the obstacles, and the bonus areas;
calculate the best path to take to avoid the pitfalls; and collect bonus points.
The cars move autonomously on the screen within the race track game with no interference
from the students. No joystick or mouse would be used.

In order to control the car movements, the students need to implement a 'driver'.
This code is controlling the car and will decide what will be the next action of the car.

For each type of obstacles there is a different action, and different points.

See [materials](materials.md) for our course materials.

See [examples/driver](examples/driver.md) for explanation on how to write a driver module.

See [development](development.md) for details on getting started
