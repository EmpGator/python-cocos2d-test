__author__ = 'henri'

import pygame

class ImageHelper:

    def __init__(self):
        pass

    def scale(self, surface, factor):
        x, y = surface.get_size()
        x *= factor
        y *= factor
        return pygame.transform.smoothscale(surface,(x,y))