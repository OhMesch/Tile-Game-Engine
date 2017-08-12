from time import sleep
import tile_terrain


def capVelocity(velArr):
    if velArr[0] > 8:
        velArr[0] = 8
    if velArr[0] < -8:
        velArr[0] = -8
    if velArr[1] > 8:
        velArr[1] = 8
    if velArr[1] < -12:
        velArr[1] = -12


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


def update_last_number_keystate(key_states, d):
    for key in d.keys():
        if key == 'last':
            continue
        if key_states[key] == 1:
            d[d['last']] = 0
            d[key] = 1
            d['last'] = key
            return


def get_last_number_keystate(d):
    for key in d.keys():
        if key == 'last':
            continue
        if d[key] == 1:
            return int(key)


def loop(ren, window_width, window_height, block_size):
    blockPoint = None
    d = {'last': '1', '1': 1, '2': 0, '3': 0, '4': 0}

    width = window_width // block_size
    height = window_height // block_size
    terrain = tile_terrain.Terrain(width, height)
    ren.draw_grid()

    while(True):
        ren.update()
        key_states = ren.get_all_keystates()

        if key_states['q'] == 1:
            return 'q'

        update_last_number_keystate(key_states, d)
        lastNumber = get_last_number_keystate(d)

        mouse_coords = ren.get_mouse_coords()

        if mouse_coords != None:
            terrain.createBlock(mouse_coords, lastNumber)
            ren.render_block(terrain, mouse_coords)
            blockPoint = None
        sleep(.05)


    player = Rectangle(Point(250,250), Point(270,270))
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
