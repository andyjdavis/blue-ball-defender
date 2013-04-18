import os, pygame
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

import math
import random

from lib import *
from class_EnemyMissile import EnemyMissile
from class_FriendlyMissile import FriendlyMissile
from class_TheWorld import TheWorld

class Settings:
    def __init__(self):
        #CONSTANTS
        self.width = 900
        self.height = 600
        self.resourcepath = 'resources'
        self.background_color = (0,0,0)
        
        self.splash_size = (500, 300)
        self.splash_background_color = (10, 10, 10)
        self.text_antialias = 1
        self.text_color = (136,206,250)
        
        self.planetradius = 16
        self.missileradius = 2
        self.missilevelocity = 25
        self.blastradius = 70
        self.blastspeed = 12
settings = Settings()

class State:
    PREGAME = 1
    INGAME = 2
    ENDGAME = 3
state = None

pregame_splash = None
endgame_splash = None

pygame.init()
screen = pygame.display.set_mode((settings.width, settings.height))
pygame.display.set_caption('Blue Ball Defender')
#pygame.mouse.set_visible(0)

all_sprites = pygame.sprite.RenderPlain()
missile_group = pygame.sprite.RenderPlain()
enemy_missile_group = pygame.sprite.RenderPlain()
theworld = None
starttime = 0
currenttime = 0

def change_state(newstate):
    global state
    
    state = newstate
    
    soundtrack_path = None
    if state == State.PREGAME:
        soundtrack_path = os.path.join('resources/music', 'DST-2ndBallad.mp3')
    if state == State.INGAME:
        soundtrack_path = os.path.join('resources/music', 'DST-AngryRobotIII.mp3')
    if state == State.ENDGAME:
        soundtrack_path = os.path.join('resources/music', 'DST-GangsterCredit.mp3')
    
    pygame.mixer.music.load(soundtrack_path)
    #pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play()

def new_game():
    global theworld, state, starttime
    
    all_sprites.empty()
    missile_group.empty()
    enemy_missile_group.empty()
    
    theworld = TheWorld(settings)
    all_sprites.add(theworld)
    
    change_state(State.INGAME)
    starttime = pygame.time.get_ticks()
    
    add_dirty_rect(screen.get_rect())

def click(pos):
    if state == State.PREGAME or state == State.ENDGAME:
        new_game()
    elif state == State.INGAME:
        m = FriendlyMissile(settings, pos)
        missile_group.add(m)
        all_sprites.add(m)

def one_second_update():
    if state == State.INGAME:
        spawn_enemy_missile()

def spawn_enemy_missile():
    # Raise max number of missiles by 1 every 10 seconds
    if len(enemy_missile_group) < ((currenttime - starttime) // 10000) + 1:
        m = EnemyMissile(settings)
        enemy_missile_group.add(m)
        missile_group.add(m)
        all_sprites.add(m)

def display_pregame_splash(screen):
    global pregame_splash
    
    if not pregame_splash:
        pregame_splash = pygame.Surface(settings.splash_size).convert()
        pregame_splash.fill(settings.splash_background_color)

        font_big = pygame.font.SysFont("arial",24)
        font_small = pygame.font.SysFont("arial", 18)
        
        text = font_big.render("Our fragile blue planet is under attack", settings.text_antialias, settings.text_color, settings.splash_background_color)
        pregame_splash.blit(text, (10, 20))
                
        text = font_small.render("Use the mouse to target missiles and destroy attackers", settings.text_antialias, settings.text_color, settings.splash_background_color)
        pregame_splash.blit(text, (10, 150))
    
    splash_dest_rect = pygame.Rect((settings.width/2) - (settings.splash_size[0]/2), (settings.height/2) - (settings.splash_size[1]/2), settings.splash_size[0], settings.splash_size[1])
    screen.blit(pregame_splash, splash_dest_rect)
    add_dirty_rect(splash_dest_rect)

def display_endgame_splash(screen):
    global endgame_splash
    
    if not endgame_splash:
        endgame_splash = pygame.Surface(settings.splash_size).convert()
    
    endgame_splash.fill(settings.splash_background_color)

    font_big = pygame.font.SysFont("arial",24)
    font_small = pygame.font.SysFont("arial", 18)
    
    text = font_big.render("You lasted " + str(calc_time()) + " seconds", settings.text_antialias, settings.text_color, settings.splash_background_color)
    endgame_splash.blit(text, (10, 20))
    
    text = font_small.render("Click anywhere to try and do better", settings.text_antialias, settings.text_color, settings.splash_background_color)
    endgame_splash.blit(text, (10, 150))
    
    splash_dest_rect = pygame.Rect((settings.width/2) - (settings.splash_size[0]/2), (settings.height/2) - (settings.splash_size[1]/2), settings.splash_size[0], settings.splash_size[1])
    screen.blit(endgame_splash, splash_dest_rect)
    add_dirty_rect(splash_dest_rect)

def calc_time():
    return (currenttime - starttime) // 1000

#def draw_score(screen):
#    message = "You lasted " + calc_time() + " seconds"
#    text = settings.font.render(message, settings.text_antialias, settings.text_color, settings.background_color)
#    screen.blit(text, (settings.width - 200, 80))

def main():
    global state, currenttime
    
    bg = pygame.Surface(screen.get_size()).convert()
    # draw stars
    for i in range(0,100):
        x = rand(0, settings.width)
        y = rand(0, settings.height)
        bg.set_at((int(x), int(y)), (255,255,255))
    
    change_state(State.PREGAME)
    add_dirty_rect(screen.get_rect())
    
    clock = pygame.time.Clock()
    
    pygame.time.set_timer(USEREVENT + 1, 1000)
    
    while 1:
        dt = clock.tick()/1000.00
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                pass
            elif event.type == KEYUP:
                pass
            elif event.type == MOUSEBUTTONDOWN:
                click(event.pos)
            elif event.type == USEREVENT + 1:
                one_second_update()
        
        screen.blit(bg, (0, 0))
        
        if state == State.PREGAME:
            display_pregame_splash(screen)
        else:
            # keep updating in ENDGAME so animation continues in the background
            all_sprites.update(dt)
            
            for m1 in missile_group:
                for m2 in missile_group:
                    if m1 != m2 and distance(m1._pos, m2._pos) < m1.currentradius + m2.currentradius:
                        m1.explode()
                        m2.explode()
            
            #for s in all_sprites:
            #    if s.is_old():
            #        s.kill()
            
            for m1 in missile_group:
                if distance(m1._pos, theworld._pos) < (m1.currentradius + theworld._radius):
                    m1.explode()
                    if state == State.INGAME:
                        change_state(State.ENDGAME)

            all_sprites.draw(screen)
            
            if state == State.INGAME:
                currenttime = pygame.time.get_ticks()
            elif state == State.ENDGAME:
                display_endgame_splash(screen)
        
        pygame.display.update(get_dirty_rects())
        clear_dirty_rects()

if __name__ == '__main__': main()

