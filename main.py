# -*- coding: utf-8 -*-

import pyglet
from pyglet.window import key

import xmlmap_maker


import cocos
from cocos import tiles, actions, layer, sprite

UP = (0, 1)
DOWN = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class AnimationHandler():
    """
    This class should handle animations.

    It uses image sequences to animate instances.
    """

    # Constants
    STOPPED = 0
    ONGOING = 1

    def __init__(self, owner, sequence, animationLength=1.0, loop=False):
        self.owner = owner
        self.sequence = sequence
        self.animationTimeFull = animationLength
        self.animationTime = 0.0
        self.imageId = 0
        self.loop = loop  # TODO Implement looping
        self.status = AnimationHandler.STOPPED

    def imageUpdate(self, dt):
        if self.status:
            self.animationTime += dt

            if self.animationTime >= self.animationTimeFull:
                self.animationTime = 0.0
                self.imageId = 0
                self.owner.image = Car.carImageSequence[self.imageId]

            changeTime = self.animationTimeFull/len(Car.carImageSequence)*(self.imageId+1)

            if changeTime <= self.animationTime:
                self.imageId += 1
                self.owner.image = Car.carImageSequence[self.imageId]

    def start(self):
        self.status = AnimationHandler.ONGOING

    def stop(self):
        self.status = AnimationHandler.STOPPED

    def toggle(self):
        if self.status == AnimationHandler.ONGOING:
            self.status = AnimationHandler.STOPPED
        else:
            self.status = AnimationHandler.ONGOING


class World(cocos.layer.Layer):
    """
    Responsibilities:
        Generation: random generates a level
        Initial State: Set initial play state
        Play: updates level state, by time and user input. Detection of
        end-of-level conditions.
        Level progression.
    """
    is_event_handler = True

    def __init__(self):
        # TODO method for new game

        super(World, self).__init__()
        self.player = Car(self)
        self.newMap(30, 100)
        self.map = tiles.load('tilemap.xml')['map0']
        self.checkSpawnPoint()
        self.blockKeys = 0.0
        self.blockKeysFull = 0.3
        self.bindings = {
            key.LEFT: 'left',
            key.RIGHT: 'right',
            key.UP: 'up',
            key.DOWN: 'down',
            key.W: 'up2',
            key.Z: 'scale',
                        }
        buttons = {}
        for k in self.bindings:
            buttons[self.bindings[k]] = 0
        self.buttons = buttons

        self.carLayer = layer.ScrollableLayer()
        self.carLayer.add(self.player)
        self.manager = layer.ScrollingManager()
        self.manager.add(self.map)
        self.manager.add(self.carLayer)
        self.add(self.manager)
        self.schedule(self.update)




    def newMap(self, x=30, y=30):
        xmlmap_maker.newMap(x, y, roomsMin=10, roomsMax=40)

    def on_key_press(self, k, m):
        binds = self.bindings
        if k in binds:
            self.buttons[binds[k]] = 1
            return True
        return False

    def on_key_release(self, k, m):
        binds = self.bindings
        if k in binds:
            self.buttons[binds[k]] = 0
            return True
        return False

    def checkSpawnPoint(self):
        #Find spawntile
        cells = self.map.find_cells(pl_spawn=True)
        x, y = cells[0].x, cells[0].y
        self.player.x = x+self.player.movAmount/2
        self.player.y = y+self.player.movAmount/2


    def update(self, dt):
        self.player.walkAnim.imageUpdate(dt)

        self.manager.set_focus(self.player.x, self.player.y)

        if self.blockKeys > 0:
            self.blockKeys -= dt
        if self.blockKeys <= 0:
            cell = self.map.get_at_pixel(self.player.x, self.player.y)
            x2, y2 = cell.x, cell.y
            self.player.x = x2+self.player.movAmount/2
            self.player.y = y2+self.player.movAmount/2

        buttons = self.buttons
        if buttons['up'] and self.blockKeys <= 0:
            self.blockKeys = self.blockKeysFull
            self.player.up()
        elif buttons['up2'] and self.blockKeys <= 0:
            self.blockKeys = self.blockKeysFull
            self.player.up(False)
        elif buttons['left'] and self.blockKeys <= 0:
            self.blockKeys = self.blockKeysFull
            self.player.left()
        elif buttons['right'] and self.blockKeys <= 0:
            self.blockKeys = self.blockKeysFull
            self.player.right()
        elif buttons['down'] and self.blockKeys <= 0:
            self.blockKeys = self.blockKeysFull
            self.player.down()
        elif buttons['scale'] and self.blockKeys <= 0:
            if self.manager.scale == .25:
                self.manager.do(actions.ScaleTo(1, 2))
            else:
                self.manager.do(actions.ScaleTo(.25, 2))


class Car(cocos.sprite.Sprite):
    """
    Car sprite class

    """
    #carImage = pyglet.resource.image('car.png')
    carImage = pyglet.image.load('car.png')
    carImageSequence = pyglet.image.ImageGrid(carImage, 2, 2)
    carImage = carImageSequence[0]


    def __init__(self, owner):

        super(Car, self).__init__(Car.carImage)
        self.owner = owner
        self.x = 64*7
        self.y = 64*7
        self.animTime = 0.3
        self.rotTime = 0.3
        self.orientation = UP
        self.movAmount = 128
        self.walkAnim = AnimationHandler(self, Car.carImageSequence, self.animTime)

    def checkOrientation(self):
        if self.rotation == 0:
            self.orientation = UP
        elif self.rotation == 90:
            self.orientation = RIGHT
        elif self.rotation == 180:
            self.orientation = DOWN
        elif self.rotation == 270:
            self.orientation = LEFT
        else:
            print "bad rotation", str(self.rotation)

    def right(self):
        if self.rotation == 90:
            self.move()
        self.do(actions.RotateTo(90, self.rotTime))

    def left(self):
        if self.rotation == 270:
            self.move()
        self.do(actions.RotateTo(-90, self.rotTime))

    def down(self):
        if self.rotation == 180:
            self.move()
        self.do(actions.RotateTo(-180, self.rotTime))

    def up(self, check=True):
        if self.rotation == 0:
            self.move(check)
        self.do(actions.RotateTo(0, self.rotTime))

    def move(self, check=True):
        cell = self.owner.map.get_at_pixel(self.x, self.y)
        self.checkOrientation()
        x, y = self.orientation
        cell = self.owner.map.get_neighbor(cell, self.orientation)

        try:
            if not "wall" in cell.tile.id or not check:
                newX = self.x + self.movAmount*x
                newY = self.y + self.movAmount*y
                self.do(actions.MoveTo((newX, newY), self.animTime))
        except AttributeError:
            print "You are trying to exceed map limits"


def main():
    """
    Game runs inside this function
    """
    from cocos.director import director

    director.init(width=600, height=600, do_not_scale=True, resizable=True)

    world = World()
    car_layer = layer.ScrollableLayer()
    car_layer.add(world.player)

    scene = cocos.scene.Scene()

    scene.add(world)
    director.run(scene)


if __name__ == '__main__':
    main()
