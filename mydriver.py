"""
This driver does not do any action.
"""
from rose.common import obstacles, actions  # NOQA

driver_name = "test"

find2 = True
goal = False
GoodList = [obstacles.PENGUIN,obstacles.CRACK,obstacles.WATER] #obstacles that earn points
ActionList = [actions.LEFT,actions.NONE,actions.RIGHT]
def worthcheck(world):
    return False


def drive(world):
    global find2
    global home
    vision = []
    if find2:
        find2 = False
        home = (world.car.x, world.car.y)
    pos = (world.car.x, world.car.y)
    #print(pos) #initial - x(1,4),y(6)
    # "scans"
    # for i in range(1, 4):  # i = line we're checking
    #     list = []
    #     for j in range(1 + 2 * (i)):  # j = square in line we're cheking
    #         if (pos[0] - i + j > 0) and (pos[0] - i + j < 5):
    #             list.append(world.get(pos[0] - i + j, pos[1] - i))
    #         else:
    #             list.append("B")
    #     vision.append(list)  # vision = list of all the obstacles in front of us

    for i in range(1, 4):
        list = []
        for j in range(3):
            num = (pos[0] + j - 1, pos[1] - i)
            if num[0] < 0 or num[0] > 5:
                list.append('B')
            else:
                list.append(world.get(num))
        vision.append(list)
    #print(vision)


    # add a worthy path finder

    worth = worthcheck(world)
    if worth:
        pass
    else:  # what to do if there isn't a worthy prize in sight(deafult)
        # point greedy
        print(vision)
        if vision[0][1] == obstacles.PENGUIN:
            return actions.PICKUP
        if vision[0][1] == obstacles.CRACK:
            return actions.JUMP
        if vision[0][1] == obstacles.WATER:
            return actions.BRAKE
        #obsitcale in front in the car
        if vision[0][1] != obstacles.NONE: #front of the car
            action =  findTheHighScoreWay(vision, pos)
            # if vision[0][0] == obstacles.NONE or vision[0][0] == obstacles.PENGUIN:
            #     print ('There is an obstacle ahead - turning left')
            #     return actions.LEFT
            # elif vision[0][2] == obstacles.NONE or vision[0][2] == obstacles.PENGUIN:
            #     print('There is an obstacle ahead - turning left')
            #     return actions.RIGHT
        return findTheHighScoreWay(vision, pos)
        # if (vision[0][0] != obstacles.NONE and vision[0][0] != obstacles.PENGUIN) and (
        #         vision[0][2] != obstacles.NONE and vision[0][2] != obstacles.PENGUIN):
        #     return actions.NONE
        """"
        best = -1
        obst = None
        found = False
        for i in range(3):
            for cur in GoodList:
                if vision[1][i + 1] == cur and (
                        vision[0][i] == obstacles.NONE or vision[0][i] == obstacles.PENGUIN):
                    found = True
                    best = i
                    obst = cur
                    if cur == GoodList[0]:
                        return ActionList[i]
                    break
            if found:
                break
        st = 0
        fin = 4
        act = [actions.LEFT, actions.NONE, actions.RIGHT]
        if (vision[0][0] != obstacles.PENGUIN and vision[0][0] != obstacles.NONE):
            st = 1
            act.remove(actions.LEFT)
        elif (vision[0][2] != obstacles.PENGUIN and vision[0][2] != obstacles.NONE):
            fin = 3
            act.remove(actions.RIGHT)
        for i in range(st, fin):
            for cur in GoodList:
                if obst != None:
                    if GoodList.index(obst) <= GoodList.index(cur):
                        break
                if vision[2][2 + i] == cur and (
                        vision[1][i + 1] == obstacles.NONE or vision[1][i + 1] == obstacles.PENGUIN):
                    if i <= (fin + st / 2):
                        return act[0]
                    else:
                        return act[-1]
        if best != -1:
            return ActionList[best]
        # what he does if there is an obstacle in front of him.
        if vision[0][1] != obstacles.NONE:
            if vision[0][0] == obstacles.NONE:
                return actions.LEFT
            elif vision[0][2] == obstacles.NONE:
                return actions.RIGHT
        # else.
        if pos[0] < home[0] and vision[0][2] == obstacles.NONE:
            return actions.RIGHT
        if pos[0] > home[0] and vision[0][0] == obstacles.NONE:
            return actions.LEFT
        """
    return actions.NONE


def sumScore(line):
    penguin = 10
    crack = 5
    water = 4
    sumTotal = 0

    for spot in line:
        if spot == obstacles.PENGUIN and (line.index(spot) != 0 or line[3] == 'front'):
            sumTotal += penguin
            print('pinguin - spot = ', spot, 'lines', line)
        elif spot == obstacles.CRACK and (line.index(spot) != 0 or line[3] == 'front'):
            sumTotal += crack
            print('crack - spot = ', spot, 'lines', line)
        elif spot == obstacles.WATER and (line.index(spot) != 0 or line[3] == 'front'):
            sumTotal += water
            print('water - spot = ', spot, 'lines', line)
        elif spot == obstacles.TRASH or spot == obstacles.CRACK or spot == obstacles.BARRIER or spot == obstacles.BIKE or spot == obstacles.WATER:  # other obstacles
            #add more condition if pinguin and than obs
            print('why drop 10? is there obstacle - spot = ', spot, 'lines=', line)
            sumTotal -= 10
        goodList = [obstacles.PENGUIN, obstacles.CRACK, obstacles.WATER]
    for item in goodList:
        if item in line :
            itemIndex = line.index(item)
            if line[itemIndex+1] == obstacles.TRASH or line[itemIndex+1] == obstacles.BARRIER or line[itemIndex+1] == obstacles.BIKE:
                sumTotal += 10
                print('get up with 10')
    return sumTotal

def findTheHighScoreWay(vision, pos):
    actionToMove = actions.NONE
    scoreLeftLine = 0
    scoreFrontLine = 0
    scoreRightLine = 0

    scoreLeftLine = sumScore([vision[0][0], vision[1][0], vision[2][0], 'left'])
    scoreFrontLine = sumScore([vision[0][1], vision[1][1], vision[2][1], 'front'])
    scoreRightLine = sumScore([vision[0][2], vision[1][2], vision[2][2], 'right'])
    print('left:', vision[0][0], '-', vision[1][0], '-', vision[2][0])
    print('front:', vision[0][1], '-', vision[1][1], '-', vision[2][1])
    print('right:', vision[0][2], '-', vision[1][2], '-', vision[2][2])

    # handle scores when moving between screen sides
    print("Right:", scoreRightLine)
    print("Left:", scoreLeftLine)
    if pos[0] == 2:
        scoreRightLine -= 900
        print("deducted:",scoreRightLine)
    elif pos[0] == 3:
        scoreLeftLine -= 900
        print("deducted:", scoreLeftLine)


    print('score left', scoreLeftLine, ' | score front', scoreFrontLine, ' | score right', scoreRightLine)
    print('---------------------------------------------------------------------------------------')

    if scoreFrontLine == scoreLeftLine:
        if scoreFrontLine == scoreRightLine:
            actionToMove = actions.NONE  # all are equal - don't turn
        else:
            if pos[0] < home[0] and vision[0][2] == obstacles.NONE:
                actionToMove = actions.RIGHT
            if pos[0] > home[0] and vision[0][0] == obstacles.NONE:
                actionToMove = actions.LEFT
        actionToMove = actions.NONE #all are equal - don't turn
    elif scoreLeftLine >= scoreRightLine:
        if scoreLeftLine > scoreFrontLine:
            actionToMove = actions.LEFT
    elif scoreRightLine > scoreFrontLine:
        actionToMove = actions.RIGHT
    print('action to move', actionToMove)
    return actionToMove


