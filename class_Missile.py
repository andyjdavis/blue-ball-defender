import pygame
import random

from lib import *
from class_MySprite import *

class MissileState:
    FLYING = 1
    EXPLODING = 2
    COLLAPSING = 3

class Missile(MySprite):
    def __init__(self, settings, pos, vel, color, blastspeed):
        self.state = MissileState.FLYING
        self.currentradius = settings.missileradius
        self.color = color
        self.blastspeed = blastspeed
        self.background_color = settings.background_color
        self.explosionsound = load_sound('resources', 'DeathFlash.ogg')
        
        MySprite.__init__(self, settings, pos, vel, settings.blastradius)
        self.rect = pos_to_rect(self._pos, self._radius)
        
        self.image = pygame.Surface((self._radius*2, self._radius*2)).convert()
        set_top_left_transparent(self.image)
    
    def update(self, dt):
        MySprite.update(self, dt)
        
        if self.state == MissileState.EXPLODING:
            self.radius_float += (self.blastspeed * dt)
            self.currentradius = int(self.radius_float)
            if self.currentradius > self._radius:
                self.state = MissileState.COLLAPSING
        elif self.state == MissileState.COLLAPSING:
            self.radius_float -= (self.blastspeed * dt)
            self.currentradius = int(self.radius_float)
            if self.currentradius < 0:
                self.kill()
                return
        
        self.rect = pos_to_rect(self._pos, self._radius)
        
        self.image.fill(self.background_color)
        pygame.draw.circle(self.image, self.color, (self._radius, self._radius), self.currentradius)
        
        #DEBUG
        #pygame.draw.circle(self.image, (0,255,0), (0, 0), 1)
        #pygame.draw.circle(self.image, (0,255,0), (self._radius*2, self._radius*2), 1)
        
    def explode(self):
        if self.state == MissileState.FLYING:
            self.state = MissileState.EXPLODING
            self.radius_float = self.currentradius
            self._vel = (0,0)
            self.explosionsound.play()

