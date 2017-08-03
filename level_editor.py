from graphics import *
from time import sleep
print("Import Success")

def capVelocity(velArr):
    for i in range(len(velArr)):
        if velArr[i] > 8:
            velArr[i] = 8
        elif velArr[i] < -8:
            velArr[i] = -8

def checkBounds(player,terr,velArr):
    x = player.getCenter().getX()
    y = player.getCenter().getY()

    #Determine if touching a block, if it is set its position and velocity appropriately 
    if terr[int(y/20)][int((x+10)/20)-1] != 0:
        velArr[0] = 0
        player.move(10-(x%20),0)

    if terr[int((y+10)/20 - 1)][int(x/20)] != 0:
        velArr[1] = 0
        player.move(0,10-(y%20))

    if terr[int(y/20)][int((x-10)/20)+1] != 0:
        velArr[0] = 0
        player.move(-((x-10)%20),0)

    if terr[int((y+10)/20)][int(x/20)] != 0:
        velArr[1] = 0
        player.move(0,-((y+10)%20))

def createBlock(blockCenter,blockType,window,terr):
    newX = blockCenter.getX() - (blockCenter.getX()%20)
    newY = blockCenter.getY() - (blockCenter.getY()%20)
    p1 = Point(newX,newY)
    p2 = Point(newX+20,newY+20)
    print('Clicked',blockCenter.getX(),blockCenter.getY())
    print('point',newX,newY)
    newBlock = Rectangle(p1,p2)
    if blockType == 1:
        terr[int(newY/20)][int(newX/20)] = 1
        newBlock.setFill('red')
    elif blockType == 2:
        terr[int(newY/20)][int(newX/20)] = 2
        newBlock.setFill('blue')
    elif blockType == 3:
        terr[int(newY/20)][int(newX/20)] = 3
        newBlock.setFill('yellow')
    else:
        terr[int(newY/20)][int(newX/20)] = 4
        newBlock.setFill('green')
    newBlock.draw(window)

def generateLevelEditor():
    window = GraphWin("Level Editor",500,500)
    for i in range(0,500,20): #Determines size of terrain
        horLines = Line(Point(0,i),Point(500,i))
        horLines.setOutline('grey')
        horLines.draw(window)
        verLines = Line(Point(i,0),Point(i,500))
        verLines.setOutline('grey')
        verLines.draw(window)
    return(window)

def isFalling(x,y,terr):
    return(terr[int((y-10)/20 + 1)][int(x/20)] == 0)

def loseVel(velArr):
    for i in range(len(velArr)):
        if velArr[i] > 0:
            velArr[i] -= .1
        if velArr[i] < 0:
            velArr [i] += .1
        if abs(velArr[i]) < .1:
            velArr[i] = 0

def updateMove(moveObj,vel):
    moveObj.move(vel[0],0)
    moveObj.move(0,vel[1])

def main():
    terrain = [[0 for x in range(25)] for y in range(25)]
    # print(terrain)

    editor = generateLevelEditor()

    blockPoint = None
    prevStateOne = None
    prevStateTwo = None
    prevStateThree = None
    prevStateFour = None
    lastKey = None
    
    while(not editor.keyState[5]):
        #Records what block type to place next
        if editor.keyState[6] == 1 and prevStateOne ==0:
            lastKey = 1
        if editor.keyState[7] == 1 and prevStateTwo ==0:
            lastKey = 2
        if editor.keyState[8] == 1 and prevStateThree ==0:
            lastKey = 3
        if editor.keyState[9] == 1 and prevStateFour ==0:
            lastKey = 4

        prevStateOne = editor.keyState[6]
        prevStateTwo = editor.keyState[7]
        prevStateThree = editor.keyState[8]
        prevStateFour = editor.keyState[9]

        # print(editor.keyState)
        if not blockPoint:
            blockPoint = editor.checkMouse()
            # print('PlaceBlock')
        else:
            createBlock(blockPoint,lastKey,editor,terrain)
            blockPoint = None

        sleep(.02)

    player = Rectangle(Point(250,250),Point(270,270))
    player.setFill('Black')
    player.draw(editor)

    lastKey = None
    falling = False
    editor.keyState[5] = 0

    velocity = 2*[0]
    # print("Vel:", velocity)

    while(not editor.keyState[5]):
        lastKey = editor.checkKey()
        # print(editor.keyState)
        px = player.getCenter().getX()
        py = player.getCenter().getY()
        print('position:',px,py)

        if isFalling(px,py,terrain):
            velocity[1] += 1

        capVelocity(velocity)
        checkBounds(player,terrain,velocity)

        if editor.keyState[0] and terrain[int(py/20)][int((px+5)/20)-1] == 0:
            velocity[0] -= .5
            # player.move(-velocity[0],0)
        if editor.keyState[1] and terrain[int((py+5)/20 - 1)][int(px/20)] == 0 and not isFalling(px,py,terrain):
            velocity[1] = -8
            # player.move(0,-velocity[1])
        if editor.keyState[2] and terrain[int(py/20)][int((px-10)/20)+1] == 0:
            velocity[0] += .5
            # player.move(velocity[0],0)
        
        updateMove(player,velocity)
        loseVel(velocity)
        # print('Vel:', velocity)
        editor.update()
        sleep(0.02) #make this a float, beware bugs
    editor.close()
    for line in terrain:
        print(line)
main()
