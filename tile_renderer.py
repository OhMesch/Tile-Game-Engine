import graphics 
from graphics import *

class Renderer():
    def __init__(self, width=500, height=500, block_size = 20):
        self.width = width
        self.height = height
        self.win = GraphWin("Level Editor", width, height)
        self.block_size = block_size
        self.states = {
        'w': 0,
        'a': 0,
        's': 0,
        'd': 0,
        'esc': 0,
        'space': 0,
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0,
        '5': 0,
        'q': 0,
        'enter': 0
        }


    def update(self):
        self.win.update()
        self.update_keystates()


    def get_window(self):
        return(self.win)


    def draw_grid(self):
        for i in range(0, 500, self.block_size): #Determines size of terrain
            horLines = Line(Point(0, i),Point(self.width, i))
            horLines.setOutline('grey')
            horLines.draw(self.win)

            verLines = Line(Point(i, 0),Point(i, self.height))
            verLines.setOutline('grey')
            verLines.draw(self.win)


    def update_keystates(self):
        self.states['a'] = self.win.keyState[0]
        self.states['w'] = self.win.keyState[1]
        self.states['d'] = self.win.keyState[2]
        self.states['s'] = self.win.keyState[3]
        self.states['space'] = self.win.keyState[4]
        self.states['esc'] = self.win.keyState[5]
        self.states['1'] = self.win.keyState[6]
        self.states['2'] = self.win.keyState[7]
        self.states['3'] = self.win.keyState[8]
        self.states['4'] = self.win.keyState[9]
        self.states['5'] = self.win.keyState[10]
        self.states['q'] = self.win.keyState[11]
        self.states['enter'] = self.win.keyState[12]


    def get_all_keystates(self):
        return self.states


    def get_mouse_position(self):
        return self.win.checkMouse()


    def get_mouse_coords(self):
        pos = self.get_mouse_position()
        if pos == None:
            return None
        x = pos.getX() - (pos.getX()%self.block_size)
        y = pos.getY() - (pos.getY()%self.block_size)
        x = int(x/self.block_size)
        y = int(y/self.block_size)
        return (x, y)


    def render_block(self, terrain, coords):
        x = coords[0]
        y = coords[1]
        p1 = Point(x*self.block_size, y*self.block_size)
        p2 = Point((x*self.block_size)+self.block_size, (y*self.block_size)+self.block_size)
        newBlock = Rectangle(p1, p2)

        blockType = terrain.get_map()[y][x]

        if blockType == 1:
            newBlock.setFill('green')
        elif blockType == 2:
            newBlock.setFill('blue')
        elif blockType == 3:
            newBlock.setFill('yellow')
        else:
            newBlock.setFill('red')
        newBlock.draw(self.win)




class Menu(): #CHANGE TO SELF. WIDTH AND HIEGHT
    def __init__(self,window):
        self.window = window

        skyBlue = color_rgb(135,206,250)
        royalBlue = color_rgb(65,105,225)

        self.menu = Rectangle(Point(.2*500,.15*500),Point(.8*500,.8*500))
        self.menu.setFill(skyBlue)
        self.menu.setOutline(skyBlue)

        self.save = Rectangle(Point(.25*500,.2*500),Point(.75*500,.35*500))
        self.save.setOutline(royalBlue)
        self.save.setFill(royalBlue)

        self.saveTxt = Text(Point(.50*500,.275*500), "SAVE")
        self.saveTxt.setSize(30)
        self.saveTxt.setFace("helvetica")
        self.saveTxt.setStyle("bold")

        self.saveAs = Rectangle(Point(.25*500,.4*500),Point(.75*500,.55*500))
        self.saveAs.setOutline(royalBlue)
        self.saveAs.setFill(royalBlue)

        self.saveAsTxt = Text(Point(.50*500,.475*500), "SAVE AS")
        self.saveAsTxt.setSize(30)
        self.saveAsTxt.setFace("helvetica")
        self.saveAsTxt.setStyle("bold")

        self.back = Rectangle(Point(.25*500,.6*500),Point(.75*500,.75*500))
        self.back.setOutline(royalBlue)
        self.back.setFill(royalBlue)

        self.backTxt = Text(Point(.50*500,.675*500), "BACK")
        self.backTxt.setSize(30)
        self.backTxt.setFace("helvetica")
        self.backTxt.setStyle("bold")

        self.load = Rectangle(Point(.25*500,.4*500),Point(.75*500,.55*500))
        self.load.setOutline(royalBlue)
        self.load.setFill(royalBlue)

        self.loadTxt = Text(Point(.50*500,.475*500), "LOAD")
        self.loadTxt.setSize(30)
        self.loadTxt.setFace("helvetica")
        self.loadTxt.setStyle("bold")

        self.quit = Rectangle(Point(.25*500,.6*500),Point(.75*500,.75*500))
        self.quit.setOutline(royalBlue)
        self.quit.setFill(royalBlue)

        self.quitTxt = Text(Point(.50*500,.675*500), "QUIT")
        self.quitTxt.setSize(30)
        self.quitTxt.setFace("helvetica")
        self.quitTxt.setStyle("bold")

    def openMenu(self):
        self.menu.draw(self.window)
        self.save.draw(self.window)
        self.saveTxt.draw(self.window)
        self.load.draw(self.window)
        self.loadTxt.draw(self.window)
        self.quit.draw(self.window)
        self.quitTxt.draw(self.window)

    def saveMenu(self):
        self.closeMenu()
        self.menu.draw(self.window)
        self.saveAs.draw(self.window)
        self.saveAsTxt.draw(self.window)
        self.back.draw(self.window)
        self.backTxt.draw(self.window)

    def closeMenu(self):
        self.menu.undraw()
        self.save.undraw()
        self.saveTxt.undraw()
        self.load.undraw()
        self.loadTxt.undraw()
        self.quit.undraw()
        self.quitTxt.undraw()

    def closeSave(self):
        self.menu.undraw()
        self.saveAs.undraw()
        self.saveAsTxt.undraw()
        self.back.undraw()
        self.backTxt.undraw()
        self.openMenu()