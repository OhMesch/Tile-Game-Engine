class Terrain():
    def __init__(self, width = 25, height = 25):
        self.map = [[0 for x in range(width)] for y in range(height)]


    def get_map(self):
        return self.map


    def createBlock(self, coords, blockType):
        x = coords[0]
        y = coords[1]
        self.map[y][x] = blockType