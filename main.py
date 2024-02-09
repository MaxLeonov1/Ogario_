import os
import sys
import random
import pygame


pygame.init()
concurrent_path = os.path.dirname(__file__)
os.chdir(concurrent_path)
WIDTH = 1200
HEIGHT = 800
FPS = 60
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
from load import *


#{CLASSES}

class Player():
    def __init__(self,player_image,pos):
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]




def restart():
    global player_group, civil_group, enemy_group
    player_group = pygame.sprite.Group()
    civil_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    food_group = pygame.sprite.Group()




def game_lvl():
    sc.fill('white')
    pygame.display.update()
    player_group.draw(sc)
    player_group.update()
    civil_group.draw(sc)
    civil_group.update()
    enemy_group.draw(sc)
    enemy_group.update()








while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    game_lvl()
    clock.tick(FPS)