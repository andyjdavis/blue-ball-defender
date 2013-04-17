import math, os, pygame
from pygame.locals import *

import random

def distance(p1, p2):
    xdiff = p1[0] - p2[0]
    ydiff = p1[1] - p2[1]
    return math.sqrt(xdiff**2 + ydiff**2)

def rand(minimum, maximum):
    return random.random() * (maximum - minimum) + minimum

def normalize_vector(xlength, ylength):
    '''Scale the vector down to 0-1'''
    hypotenuse = math.sqrt(xlength**2 + ylength**2)
    return [xlength/hypotenuse, ylength/hypotenuse]
    
def calc_vel(pos, destination, totalvel):
    xdiff = destination[0] - pos[0]
    ydiff = destination[1] - pos[1]
    
    vel = normalize_vector(xdiff, ydiff)
    vel[0] *= totalvel
    vel[1] *= totalvel
    
    return vel

def pos_to_top_left(pos, radius):
    return (pos[0] - radius, pos[1] - radius)

def pos_to_rect(pos, radius):
    (x, y) = pos_to_top_left(pos, radius)
    return pygame.Rect(x, y, radius*2, radius*2)

def set_top_left_transparent(image):
    colorkey = image.get_at((0,0))
    image.set_colorkey(colorkey, RLEACCEL)
    
def load_image(resourcepath, name, colorkey=-1, perpixelalpha=False):
    fullname = os.path.join(resourcepath, name)
    
    try:
        image = pygame.image.load(fullname)
        if perpixelalpha:
            image = image.convert_alpha()
        else:
            image = image.convert()
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message

    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(resourcepath, name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(resourcepath, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', fullname
        raise SystemExit, message
    return sound
