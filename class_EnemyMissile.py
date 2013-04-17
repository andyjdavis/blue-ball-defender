import pygame
import random

from lib import *
from class_Missile import *

class EnemyMissile(Missile):
    def __init__(self, settings):
        vel = pos = None
        if random.choice((0, 1)) == 0:
            # left or right side
            pos = [random.choice((0, settings.width)), rand(0, settings.height)]
        else:
            # top or bottom edge
            pos = [rand(0, settings.width), random.choice((0, settings.height))]
        vel = calc_vel(pos, (settings.width/2, settings.height/2), settings.missilevelocity)
    
        Missile.__init__(self, settings, pos, vel, (255,0,0), settings.blastspeed)
