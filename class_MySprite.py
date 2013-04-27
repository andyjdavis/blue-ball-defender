import pygame

#from lib import *

class MySprite(pygame.sprite.Sprite):
    def __init__(self, settings, pos, vel, radius):
        pygame.sprite.Sprite.__init__(self)
        
        self.settings = settings
        self._pos = pos
        self._vel = vel
        self._radius = radius
        
        self._age = 0
        self._lifespan = float('inf')
    
    def update(self, dt):
        self._age += dt
        
        self._pos[0] += self._vel[0] * dt
        self._pos[1] += self._vel[1] * dt
        
        if self.is_offscreen():
            self.kill()
    
    def is_offscreen(self):
        return self._pos[0] < 0 or self._pos[0] > self.settings.width or self._pos[1] < 0 or self._pos[1] > self.settings.height
    
    def is_old(self):
        return self._age > self._lifespan
