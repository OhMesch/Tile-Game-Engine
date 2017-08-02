from graphics import *
from time import sleep
print("Import Success")

def capVelocity(velArr):
    for i in range(len(velArr)):
        if velArr[i] > 8:
            velArr[i] = 8
        elif velArr[i] < -8:
            velArr[i] = -8

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

def loseVel(velArr):
    for i in range(len(velArr)):
        if velArr[i] > 0:
            velArr[i] -= .1
        if velArr[i] < 0:
            velArr [i] += .1

def checkBounds(x,y,terr,velArr):
    if terr[int(y/20)][int((x+5)/20)-1] != 0:
        velArr[0] = 0
    if terr[int((y+5)/20 - 1)][int(x/20)] != 0:
        velArr[1] = 0
    if terr[int(y/20)][int((x-10)/20)+1] != 0:
        velArr[2] = 0
    if terr[int((y-10)/20 + 1)][int(x/20)] != 0:
        velArr[3] = 0

def main():
    terrain = [[0 for x in range(25)] for y in range(25)]
    print(terrain)

    editor = generateLevelEditor()

    blockPoint = None
    prevStateOne = None
    prevStateTwo = None
    prevStateThree = None
    prevStateFour = None
    lastKey = None
    
    while(not editor.keyState[5]):
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
            newX = blockPoint.getX() - (blockPoint.getX()%20)
            newY = blockPoint.getY() - (blockPoint.getY()%20)
            p1 = Point(newX,newY)
            p2 = Point(newX+20,newY+20)
            print('point',newX,newY)
            newBlock = Rectangle(p1,p2)
            if lastKey == 1:
                terrain[int(newY/20)][int(newX/20)] = 1
                newBlock.setFill('red')
            elif lastKey == 2:
                terrain[int(newY/20)][int(newX/20)] = 2
                newBlock.setFill('blue')
            elif lastKey == 3:
                terrain[int(newY/20)][int(newX/20)] = 3
                newBlock.setFill('yellow')
            else:
                terrain[int(newY/20)][int(newX/20)] = 4
                newBlock.setFill('green')
            newBlock.draw(editor)
            blockPoint = None
        sleep(.02)

    player = Rectangle(Point(250,250),Point(270,270))
    player.setFill('Black')
    player.draw(editor)

    lastKey = None
    falling = False
    editor.keyState[5] = 0

    velocity = 4*[0]
    print("Vel:", velocity)

    while(not editor.keyState[5]):
        lastKey = editor.checkKey()
        # print(editor.keyState)
        px = player.getCenter().getX()
        py = player.getCenter().getY()

        velocity[1] -= 1

        capVelocity(velocity)
        checkBounds(px,py,terrain,velocity)

        if editor.keyState[0] and terrain[int(py/20)][int((px+5)/20)-1] == 0:
            velocity[0] += .5
            player.move(-velocity[0],0)
        if editor.keyState[1] and terrain[int((py+5)/20 - 1)][int(px/20)] == 0:
            velocity[1] += .5
            player.move(0,-velocity[1])
        if editor.keyState[2] and terrain[int(py/20)][int((px-10)/20)+1] == 0:
            velocity[2] += .5
            player.move(velocity[2],0)
        if editor.keyState[3] and terrain[int((py-10)/20 + 1)][int(px/20)] == 0:
            velocity[3] +=.5
            player.move(0,velocity[3])
        
        loseVel(velocity)

        print(velocity)
        sleep(0.02) #make this a float, beware bugs
    editor.close()
    for line in terrain:
        print(line)
main()
