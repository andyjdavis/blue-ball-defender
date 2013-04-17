import pygame
import random

from lib import *
from class_MySprite import *

class TheWorld(MySprite):
    def __init__(self, settings):
        
        #self.image = pygame.Surface((settings.planetradius*2, settings.planetradius*2)).convert()
        #set_top_left_transparent(self.image)
        
        pos = [settings.width/2, settings.height/2]
        MySprite.__init__(self, settings, pos, [0, 0], settings.planetradius)
        self.rect = pos_to_rect(self._pos, self._radius)
        
        #pygame.draw.circle(self.image, (0,0,255), (self._radius, self._radius), self._radius)
        self.image, image_rect = load_image(settings.resourcepath, 'terre.png')
        
        #DEBUG
        #pygame.draw.circle(self.image, (0,255,0), (0, 0), 1)
        #pygame.draw.circle(self.image, (0,255,0), (settings.planetradius*2, settings.planetradius*2), 1)
    
    def update(self, dt):
        MySprite.update(self, dt)
    
    def die(self):
        print 'the world destroyed'
