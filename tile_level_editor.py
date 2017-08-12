from time import sleep
from graphics import *
import tile_terrain
import tile_renderer


def capVelocity(velArr):
    if velArr[0] > 8:
        velArr[0] = 8
    if velArr[0] < -8:
        velArr[0] = -8
    if velArr[1] > 8:
        velArr[1] = 8
    if velArr[1] < -12:
        velArr[1] = -12


def checkBounds(player,terr,size,velArr):
    x = player.getCenter().getX()
    y = player.getCenter().getY()
    counter = 4*[0]

    #Check left and right
    while terr[int(y/size)][int((x+velArr[0]-size/2)/size)] != 0 and counter[0] < 10 and velArr[0] < 0:
        counter[0] +=1
        velArr[0] /= 2
    while terr[int(y/size)][int((x+velArr[0]+size/2)/size)] != 0 and counter[1] < 10 and velArr[0] > 0:
        counter[1] +=1
        velArr[0] /= 2

    #Check up and down
    while terr[int((y+velArr[1]-size/2)/size)][int(x/size)] != 0 and counter[2] < 10 and velArr[1] < 0:
        counter[2] +=1
        velArr[1] /=2
    while terr[int((y+velArr[1]+size/2)/size)][int(x/size)] != 0 and counter[3] < 10 and velArr[1] > 0:
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


def isFalling(fallingObject,terr,size):
    x = fallingObject.getCenter().getX()
    y = fallingObject.getCenter().getY()
    return(terr[int((y-2/5*size)/size + 1)][int(x/size)] == 0)


def loseVel(velArr,key):
    if velArr[0] > 0 and key['d'] != 1:
        velArr[0] *= .9

    elif velArr[0] < 0 and key['a'] != 1:
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
    window=ren.get_window()

    while(True):
        ren.update()
        key_states = ren.get_all_keystates()

        if key_states['q'] == 1:
            return 'q'

        if key_states['enter'] == 1:
            break

        update_last_number_keystate(key_states, d)
        lastNumber = get_last_number_keystate(d)

        mouse_coords = ren.get_mouse_coords()

        if mouse_coords != None:
            terrain.createBlock(mouse_coords, lastNumber)
            ren.render_block(terrain, mouse_coords)
            blockPoint = None
        sleep(.05)


    player = Rectangle(Point(250,250), Point(250+block_size,250+block_size))
    player.setFill('Black')
    player.draw(window)

    lastKey = None
    falling = False

    velocity = 2*[0]
    # print("Vel:", velocity)

    menuOpen = False
    menu = tile_renderer.Menu(window)
    while(True):
        # print(editor.keyState)
        px = player.getCenter().getX()
        py = player.getCenter().getY()
        # print('position:',px,py)
        if menuOpen and key_states['esc'] == 1:
            menu.closeMenu()
            menuOpen = False
            sleep(.1)
        elif not menuOpen and key_states['esc'] == 1:
            menu.openMenu()
            menuOpen = True
            sleep(.1)
        if not menuOpen:

            if isFalling(player,terrain.get_map(),block_size):
                velocity[1] += 1

            if key_states['a'] == 1 and terrain.get_map()[int(py/block_size)][int((px+block_size/4)/block_size)-1] == 0:
                velocity[0] -= .5
            if key_states['w'] == 1 and terrain.get_map()[int((py+block_size/4)/block_size - 1)][int(px/block_size)] == 0 and not isFalling(player,terrain.get_map(),block_size):
                velocity[1] = -10
            if key_states['d'] == 1 and terrain.get_map()[int(py/block_size)][int((px-block_size/2)/block_size)+1] == 0:
                velocity[0] += .5

            capVelocity(velocity)
            checkBounds(player,terrain.get_map(),block_size,velocity)
            updateMove(player,velocity)
            loseVel(velocity,key_states)
            # print('Vel:', velocity)
        if key_states['q'] == 1:
            break
        ren.update()
        sleep(0.02)

    window.close()
    for line in terrain.get_map():
        print(line)
