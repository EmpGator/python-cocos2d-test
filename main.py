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
        super(World, self).__init__()
        self.player = Car(self)
        self.newMap(30, 30)
        self.map = tiles.load('tilemap.xml')['map0']
        self.blockKeys = 0.0
        self.blockKeysFull = 0.21
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
        xmlmap_maker.newMap()

    def on_key_press(self, k, m):
        binds = self.bindings
        if k in binds:
            self.buttons[binds[k]] = 1
            return True
        return False

    def on_key_release(self, k, m ):
        binds = self.bindings
        if k in binds:
            self.buttons[binds[k]] = 0
            return True
        return False

    def update(self, dt):
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
            self.player.forward()
        elif buttons['up2'] and self.blockKeys <= 0:
            self.blockKeys = self.blockKeysFull
            self.player.forward(False)
        elif buttons['left'] and self.blockKeys <= 0:
            self.blockKeys = self.blockKeysFull
            self.player.turnLeft()
        elif buttons['right'] and self.blockKeys <= 0:
            self.blockKeys = self.blockKeysFull
            self.player.turnRight()
        elif buttons['down'] and self.blockKeys <= 0:
            self.blockKeys = self.blockKeysFull
            self.player.turnBack()
        elif buttons['scale'] and self.blockKeys <= 0:
            if self.manager.scale == .25:
                self.manager.do(actions.ScaleTo(1, 2))
            else:
                self.manager.do(actions.ScaleTo(.25, 2))


class Car(cocos.sprite.Sprite):
    """
    Car sprite class

    """
    carImage = pyglet.resource.image('car.png')

    def __init__(self,owner):
        super(Car, self).__init__(Car.carImage)
        self.owner = owner
        self.x = 64*7
        self.y = 64*7
        self.animTime = 0.2
        self.rotTime = 0.2
        self.orientation = UP
        self.movAmount = 128

    def checkOrientation(self):
        print "rotation:", str(self.rotation)
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
        print "Orientation:", str(self.orientation)

    def turnRight(self):
        self.do(actions.RotateBy(90, self.rotTime))

    def turnLeft(self):
        self.do(actions.RotateBy(-90, self.rotTime))

    def turnBack(self):
        self.do(actions.RotateBy(-180, self.rotTime))

    def forward(self,check=True):
        cell = self.owner.map.get_at_pixel(self.x, self.y)
        self.checkOrientation()
        x, y = self.orientation
        cell = self.owner.map.get_neighbor(cell, self.orientation)

        try:
            if not "wall" in cell.tile.id or not check:
                self.do(actions.MoveBy((x*self.movAmount, y*self.movAmount), self.animTime))
        except AttributeError:
            print "You are trying to exceed map limits"



def main():
    """
    Game runs inside thi function
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
