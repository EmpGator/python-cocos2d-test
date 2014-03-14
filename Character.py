__author__ = 'henri'
import pygame
import os
from game_pygame import imageSequence


class Character:
    """
    Base class for each actor in game
    """
    def __init__(self, movAmount=128):
        self.name = "Name"
        self.age = 20
        self.gender = "Male"  # Male or Female or why not hermaphrodite
        self.race = "Human"  # These should hold bonuses and drawbacks
        self.job = "Slave"  # And these too
        self.atributes = {}
        self.tags = []

        self.x = 0
        self.y = 0
        self.angle = 0
        self.movAmount = movAmount

    def up(self):
        self.y -= self.movAmount

    def down(self):
        self.y += self.movAmount

    def left(self):
        self.x -= self.movAmount

    def right(self):
        self.x += self.movAmount

    def update(self, dt, surface):
        surface.blit(self.image, (self.x, self.y))


class Humanoid(Character):
    """
    Base class for humanoid characters
    Including player
    """
    def __init__(self, movAmount=128):
        Character.__init__(self, movAmount)


class Player(Humanoid):
    image = pygame.image.load(os.path.join('Data', 'Images', 'player-move.png'))

    def __init__(self,movAmount=128):
        Humanoid.__init__(self, movAmount)
        self.images = imageSequence(64, 64, Player.image)
        self.image = self.images[0]
        pixlArray = pygame.PixelArray(self.image)
        pixlArray.replace((255, 255, 255), (0, 0, 0, 0), 0.25)
        #pixlArray.replace((10, 60, 205), (250, 250, 250, 128), 0.25)
        self.image = pixlArray.make_surface()
