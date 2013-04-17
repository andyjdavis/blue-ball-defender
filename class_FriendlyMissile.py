import pygame
import random

from lib import *
from class_Missile import *

class FriendlyMissile(Missile):
    def __init__(self, settings, destination):
        self.center = (settings.width/2, settings.height/2)
        self.targetrange = distance(self.center, destination)
        
        # use center as pos so we can figure out vel
        vel = calc_vel(self.center, destination, settings.missilevelocity*2)
        
        vector = normalize_vector(vel[0], vel[1])
        h = settings.planetradius + settings.missileradius + 1
        x = settings.width/2 + (vector[0] * h)
        y = settings.height/2 + (vector[1] * h)
        pos = [int(x),int(y)]
    
        Missile.__init__(self, settings, pos, vel, (255,255,255), settings.blastspeed)
        
        sound = load_sound('resources', 'sfx_fly.ogg')
        sound.play()

    def update(self, dt):
        Missile.update(self, dt)
        
        if self.targetrange < distance(self._pos, self.center):
            self.explode()
