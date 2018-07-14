How to write a driver module
============================

First, you should import the obstacles and actions modules from rose.common
package:

    from rose.common import obstacles, actions

The obstacles modules is needed for detecting obstacles on the racing track.
The actions module is needed for the drive function.

Define the driver_name variable - this string is rendered below your car on
everyone's screen.

    driver_name = "Michael Schumacher"

Write a drive function. This function accepts a world object, which you can use
to find obstacles, and must return one of the actions constants in the actions
module.

Here is the simplest possible drive function:

    def drive(world):
        return actions.NONE

To find your car position, you can access the car.x and car.y of the world
object:

    x = world.car.x
    y = world.car.y

In the next game iteration, your car will be at x, y - 1. World coordinates
start at the top left of the screen. You would like to check if there is an
obstacle at this location, and return the best action for this obstacle.

To check for obstacles, use the world.get() function. This function
accept a tuple (x, y) with the required location.

    obstacle = world.get((x, y - 1))

Note that if you try to access a position which is out of the racing track,
this function will raise an IndexError. You must handle this exception when
checking for obstacles:

    try:
        obstacle = world.get((x, y - 1))
    except IndexError:
        # x, y - 1 is not a valid position
    else:
        # Choose the best action for obstacle

The game has 2 lanes and each lane has 3 routes in which you can drive.
On game start, each car starts at the center route of its lane.
The car can pass to other lane, but will be punished for collisions
with the lane owner.

    <------ Car#1 lane ------><------ Car#2 lane ---->

    |       |       |       |X|       |       |      |
    |       |       |       |X|       |       |      |
    |       |       |       |X|       |       |      |
    |       |       |       |X|       |       |      |
    |       |       |       |X|       |       |      |
    |       |       |       |X|       |       |      |
    |       |       |       |X|       |       |      |
    |       |       |       |X|       |       |      |
    |       |       |       |X|       |       |      |
    |       | car#1 |       |X|       | Car#2 |      |
    |       |       |       |X|       |       |      |
    |       |       |       |X|       |       |      |

Here are the possible obstacles and the action you should take when hitting
them:

* `obstacles.NONE`      there is no obstacle at this position. You can return any
                        action.
                        Score : 0

* `obstacles.PENGUIN`   return `actions.PICKUP` and move 1 step forward. You will
                        not move backward if you do not pick up the penguin.
                        Score : 10 for `PICKUP` otherwise 0

* `obstacles.WATER`     return `actions.BRAKE` if you want to continue forward.
                        return `actions.RIGHT` or `actions.LEFT` if you like to
                        bypass the obstacle. Any other action will cause you to
                        move backward.
                        Score: 4 for `BRAKE`, 0 for `LEFT`/`RIGHT` otherwise -10

* `obstacles.CRACK`     return `actions.JUMP` if you want to continue forward
                        return `actions.RIGHT` or `actions.LEFT` if you like to
                        bypass the obstacle. Any other action will cause you to
                        move backward.
                        Score: 5 for `JUMP`, 0 for `LEFT`/`RIGHT` otherwise -10

* `obstacles.TRASH`     you must return `actions.RIGHT` or `actions.LEFT` to bypass
                        the obstacle. Any other action will cause you to
                        move backward.
                        Score: 0 for `LEFT`/`RIGHT` otherwise -10

* `obstacles.BIKE`      you must return `actions.RIGHT` or `actions.LEFT` to bypass
                        the obstacle. Any other action will cause you to
                        move backward.
                        Score: 0 for `LEFT`/`RIGHT` otherwise -10

* `obstacles.BARRIER`   you must return `actions.RIGHT` or `actions.LEFT` to bypass
                        the obstacle. Any other action will cause you to
                        move backward.
                        Score: 0 for `LEFT`/`RIGHT` otherwise -10

NOTE : If you are driving out of your lane and have a collision with the lane
       owner, you will punished by -10 points and be moved to other free place.


Please check and test drive the examples drivers modules in this directory.
Then go ahead and write the fastest driver!
