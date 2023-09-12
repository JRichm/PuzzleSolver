from pygame import *

class Solver:
    def __init__(self):
        self.menu_surface = Surface((1280, 720))
        self.menu_surface.fill('white')    

    def show(self, window): 
        window.blit(self.menu_surface, (0, 0))