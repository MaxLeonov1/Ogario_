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

class Player(pygame.sprite.Sprite):
    def __init__(self,image,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        #self.key = pygame.key.get_pressed()
        self.speed = 5
        self.timer_spawn = 0
        self.amount = 0
        self.food_pos = [0,0]
        self.timer_spawn_civil = 0
        self.amount_civil = 0
        self.civil_pos = [0, 0]
        self.timer_spawn_enemy = 0
        self.amount_enemy = 0
        self.enemy_pos = [0, 0]

    def move(self):
        if self.key[pygame.K_a]:
            self.rect.x -= self.speed
        elif self.key[pygame.K_d]:
            self.rect.x += self.speed
        elif self.key[pygame.K_s]:
            self.rect.y += self.speed
        elif self.key[pygame.K_w]:
            self.rect.y -= self.speed

    def spawn_food(self):
        if self.amount <= 10:
            self.timer_spawn+=1
            if self.timer_spawn/FPS>1:
                self.amount+=1
                self.timer_spawn=0
                self.food_pos[0] = random.randint(0,1200)
                self.food_pos[1] = random.randint(0, 800)
                food = Food(food_image,self.food_pos)
                food_group.add(food)

    def spawn_civil(self):
        if self.amount_civil <= 5:
            self.timer_spawn_civil+=1
            if self.timer_spawn_civil/FPS>1:
                self.amount_civil+=1
                self.timer_spawn_civil=0
                self.civil_pos[0] = random.randint(0,1200)
                self.civil_pos[1] = random.randint(0, 800)
                civil = Civil(civil_image,self.civil_pos)
                civil_group.add(civil)

    def spawn_enemy(self):
        if self.amount_enemy <= 3:
            self.timer_spawn_enemy+=1
            if self.timer_spawn_enemy/FPS>1:
                self.amount_enemy+=1
                self.timer_spawn_enemy=0
                self.enemy_pos[0] = random.randint(0,1200)
                self.enemy_pos[1] = random.randint(0, 800)
                enemy = Enemy(enemy_image,self.enemy_pos)
                enemy_group.add(enemy)

    def grow(self):
        if pygame.sprite.spritecollide(self,food_group,1):
            self.image = pygame.transform.rotozoom(self.image,0,1.05)
            self.pos = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
        elif pygame.sprite.spritecollide(self,civil_group,0):
            enemy = pygame.sprite.spritecollide(self,civil_group,0)[0]
            if enemy.image.get_height() <= self.image.get_height():
                enemy.kill()
                self.image = pygame.transform.rotozoom(self.image, 0, 1.05)
                self.pos = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = self.pos
        elif pygame.sprite.spritecollide(self,enemy_group,0):
            enemy = pygame.sprite.spritecollide(self,enemy_group,0)[0]
            if enemy.image.get_height() <= self.image.get_height():
                enemy.kill()
                self.image = pygame.transform.rotozoom(self.image, 0, 1.05)
                self.pos = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = self.pos
    def update(self):
        self.key = pygame.key.get_pressed()
        self.move()
        self.spawn_food()
        self.grow()
        self.spawn_civil()
        self.spawn_enemy()

class Food(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


    def update(self):
        pass

class Civil(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def grow(self):
        if pygame.sprite.spritecollide(self,food_group,1):
            self.image = pygame.transform.rotozoom(self.image,0,1.05)
            self.pos = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
    def update(self):
        self.grow()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def grow(self):
        if pygame.sprite.spritecollide(self,civil_group,1):
            self.image = pygame.transform.rotozoom(self.image,0,1.05)
            self.pos = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
    def update(self):
        self.grow()



def restart():
    global player_group, civil_group, enemy_group, food_group,player
    player_group = pygame.sprite.Group()
    civil_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    food_group = pygame.sprite.Group()
    player = Player(player_image, (500, 500))
    player_group.add(player)





def game_lvl():
    sc.fill('white')

    player_group.update()
    player_group.draw(sc)
    civil_group.draw(sc)
    civil_group.update()
    enemy_group.draw(sc)
    enemy_group.update()
    food_group.draw(sc)
    food_group.update()
    pygame.display.update()






restart()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    game_lvl()
    clock.tick(FPS)