from graphics import *
from time import sleep
print("Import Success")

class Menu():
    def __init__(self,window):
        self.window = window
        self.menu = Rectangle(Point(.15*500,.15*500),Point(.85*500,.85*500))
        skyBlue = color_rgb(135,206,250)
        self.menu.setFill(skyBlue)
        self.menu.setOutline(skyBlue)

    def openMenu(self):
        self.menu.draw(self.window)

    def closeMenu(self):
        self.menu.undraw()

def capVelocity(velArr):
    if velArr[0] > 8:
        velArr[0] = 8
    if velArr[0] < -8:
        velArr[0] = -8
    if velArr[1] > 8:
        velArr[1] = 8
    if velArr[1] < -12:
        velArr[1] = -12
    # print(velArr)

def checkBounds(player,terr,velArr):
    x = player.getCenter().getX()
    y = player.getCenter().getY()
    counter = 4*[0]

    #Check left and right
    while terr[int(y/20)][int((x+velArr[0]-10)/20)] != 0 and counter[0] < 10 and velArr[0] < 0:
        counter[0] +=1
        velArr[0] /= 2
    while terr[int(y/20)][int((x+velArr[0]+10)/20)] != 0 and counter[1] < 10 and velArr[0] > 0:
        counter[1] +=1
        velArr[0] /= 2

    #Check up and down
    while terr[int((y+velArr[1]-10)/20)][int(x/20)] != 0 and counter[2] < 10 and velArr[1] < 0:
        counter[2] +=1
        velArr[1] /=2
    while terr[int((y+velArr[1]+10)/20)][int(x/20)] != 0 and counter[3] < 10 and velArr[1] > 0:
        counter[3] +=1
        velArr[1] /=2


# def checkBounds(player,terr,velArr):
#     x = player.getCenter().getX()
#     y = player.getCenter().getY()

#     #Determine if touching a block, if it is set its position and velocity appropriately 
#     #Left Block
#     if terr[int(y/20)][int((x+10)/20)-1] != 0:
#         if velArr[0] < 0:
#             velArr[0] = 0
#         player.move(10-(x%20),0)

#     #Block above
#     if terr[int((y+10)/20 - 1)][int(x/20)] != 0:
#         if velArr[1] < 0:
#             velArr[1] = 0
#         player.move(0,10-(y%20))

#     #Right block
#     if terr[int(y/20)][int((x-10)/20)+1] != 0:
#         if velArr[0] > 0:
#             velArr[0] = 0
#         player.move(-((x-10)%20),0)

#     #Block below
#     if terr[int((y+10)/20)][int(x/20)] != 0:
#         if velArr[1] > 0:
#             velArr[1] = 0
#         player.move(0,-((y+10)%20))

def createBlock(blockCenter,blockType,window,terr):
    newX = blockCenter.getX() - (blockCenter.getX()%20)
    newY = blockCenter.getY() - (blockCenter.getY()%20)
    p1 = Point(newX,newY)
    p2 = Point(newX+20,newY+20)
    # print('Clicked',blockCenter.getX(),blockCenter.getY())
    # print('point',newX,newY)
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

def isFalling(fallingObject,terr):
    x = fallingObject.getCenter().getX()
    y = fallingObject.getCenter().getY()
    return(terr[int((y-8)/20 + 1)][int(x/20)] == 0)

def loseVel(velArr,key):
    if velArr[0] > 0 and key[2] != 1:
        velArr[0] *= .9

    elif velArr[0] < 0 and key[0] != 1:
        velArr[0] *= .9

    if abs(velArr[1]) < 0:
        velArr[1] *= .95

    if abs(velArr[0]) < .05:
        velArr[0] = 0
    if abs(velArr[1]) < .05:
        velArr[1] = 0

def updateMove(moveObj,velArr):
    moveObj.move(velArr[0],0)
    moveObj.move(0,velArr[1])

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

    menuOpen = False
    menu = Menu(editor)
    while(True):
        # print(editor.keyState)
        px = player.getCenter().getX()
        py = player.getCenter().getY()
        # print('position:',px,py)
        if menuOpen and editor.keyState[5]:
            menu.closeMenu()
            menuOpen = False
            sleep(.05)
        elif not menuOpen and editor.keyState[5]:
            menu.openMenu()
            menuOpen = True
            sleep(.05)
        if not menuOpen:
            if isFalling(player,terrain):
                velocity[1] += 1

            if editor.keyState[0] and terrain[int(py/20)][int((px+5)/20)-1] == 0:
                velocity[0] -= .5
            if editor.keyState[1] and terrain[int((py+5)/20 - 1)][int(px/20)] == 0 and not isFalling(player,terrain):
                velocity[1] = -10
            if editor.keyState[2] and terrain[int(py/20)][int((px-10)/20)+1] == 0:
                velocity[0] += .5

            capVelocity(velocity)
            checkBounds(player,terrain,velocity)
            updateMove(player,velocity)
            loseVel(velocity,editor.keyState)
            # print('Vel:', velocity)
        editor.update()
        sleep(0.02)

    editor.close()
    for line in terrain:
        print(line)
main()
