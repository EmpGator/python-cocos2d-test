import pygame
import os
from Character import *
from map_maker import dungeonGenerator
#from PAdLib.shadow import Shadow
#from PAdLib.occluder import Occluder

# Constants

#Tile Id
WHITE_TILE = 0
BLACKWALL = 1
RED_TILE = 2
NEONGREEN_TILE = 3
YELLOW_TILE = 4
CONCRETE_WALL = 6
ORANGE_WALL = 15
FLOOR = 19
PATH = 11
DOOR = 18
SPAWN = 3
EXIT = 2
#...
idList = {
            '#': BLACKWALL,
            '.': CONCRETE_WALL,
            'R': ORANGE_WALL,
            'F': FLOOR,
            'P': PATH,
            'D': DOOR,
            'S': SPAWN,
            'E': EXIT,
        }


class Game:
    """
    Should handle game logic and loop
    and also screen updates
    """

    def __init__(self, w=1006, h=600, flags=0):
        pygame.init()
        # Setting up a screen
        self.width = w
        self.height = h
        self.flags = flags
        self.screen = pygame.display.set_mode([self.width, self.height], self.flags)

        # Setting up a map and tiles
        self.map = dungeonGenerator(100, 100, 80, 120)
        self.map_tiles = pygame.image.load(os.path.join('Data', 'Images', 'tileSet.png'))
        self.tile_width = 128
        self.tile_height = 128
        self.tiles = imageSequence(self.tile_width, self.tile_height, self.map_tiles)
        self.scale = 1.0

        #Testing
        self.drawMinX = 0
        self.drawMaxX = self.width/self.tile_width+1
        self.drawMinY = 0
        self.drawMaxY = self.height/self.tile_height+1

        self.player = Player(0*self.scale)
        self.setCharacterStart()
        self.loop()

    def loop(self):
        while True:
            #self.drawTiles()
            self.drawTilesCentered()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                    elif event.key in self.player.keys:
                        self.player.keys[event.key]()
                    else:
                        print event.key

            self.player.update(0, self.screen)
            pygame.display.flip()

    def drawTiles(self):
        width = 0
        height = 0
        for row in self.map:
            for tile in row:
                if width < self.width:
                    self.screen.blit(self.tiles[idList[tile]], (width, height))
                    width += self.tile_width*self.scale
                else:
                    break
            if height >= self.height:
                break
            height += self.tile_height*self.scale
            width = 0

    def drawTilesCentered(self):
        width = 0
        height = 0

        self.drawMinX = self.player.mapX - (self.drawMinX - self.drawMaxX)/2
        self.drawMinY = self.player.mapY - (self.drawMinY - self.drawMaxY)/2

        print self.drawMinX, self.drawMinY, self.player.mapX, self.player.mapY
        if self.drawMinX < 0:
            self.drawMinX = 0
        if self.drawMinY < 0:
            self.drawMinY = 0


        for y in range(self.drawMaxY):
            for x in range(self.drawMaxX):
                tile = self.map[y+self.drawMinY][x+self.drawMinX]
                #print "X:", x, "Y:", y, "W:", width, "H:", height, "Tile:", tile
                self.screen.blit(self.tiles[idList[tile]], (width, height))
                width += self.tile_width*self.scale
                print self.tile_width*self.scale
            height += self.tile_height*self.scale
            width = 0

    def setCharacterStart(self):
        for yId in range(len(self.map)):
            for xId in range(len((self.map[yId]))):
                if self.map[yId][xId] == "S":
                    self.player.mapX = xId
                    self.player.mapY = yId

def imageSequence(w, h, image):
    """
    Specs :
    Master can be any height.
    sprites frames width must be the same width
    Master width must be len(frames)*frame.width
    Assuming you resources directory is named "resources"
    """

    images = []
    master_image = image.convert_alpha()

    master_width, master_height = master_image.get_size()
    for y in xrange(int(master_height/h)):
        for x in xrange(int(master_width/w)):
            images.append(master_image.subsurface((x*w, y*h, w, h)).convert_alpha())
    return images


if __name__ == '__main__':
    Game()