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
                eyes = Eyes(civil.rect.center, civil, 1)
                civil.eyes = eyes
                eyes_group.add(eyes)
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
                eyes = Eyes(enemy.rect.center, enemy, 2)
                enemy.eyes = eyes
                eyes_group.add(eyes)
                enemy_group.add(enemy)

    def grow(self):
        if pygame.sprite.spritecollide(self,food_group,1):
            self.image = pygame.transform.rotozoom(self.image,0,1.05)
            self.pos = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.amount-=1
        elif pygame.sprite.spritecollide(self,civil_group,0):
            enemy = pygame.sprite.spritecollide(self,civil_group,0)[0]
            if enemy.image.get_height() <= self.image.get_height():
                enemy.kill()
                self.image = pygame.transform.rotozoom(self.image, 0, 1.05)
                self.pos = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = self.pos
                self.amount_civil-=1
        elif pygame.sprite.spritecollide(self,enemy_group,0):
            enemy = pygame.sprite.spritecollide(self,enemy_group,0)[0]
            if enemy.image.get_height() <= self.image.get_height():
                enemy.kill()
                self.image = pygame.transform.rotozoom(self.image, 0, 1.05)
                self.pos = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = self.pos
                self.amount_enemy-=1
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
        self.timer_move = 0
        self.speed = 5
        self.randx = 0
        self.randy = 0
        self.food = None
        self.agr = False

    def grow(self):
        if pygame.sprite.spritecollide(self,food_group,1):
            self.agr = False
            self.image = pygame.transform.rotozoom(self.image,0,1.05)
            self.pos = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            player.amount -= 1

            self.eyes.pos = self.rect.center
            self.eyes.image = pygame.transform.rotozoom(self.eyes.image, 0, 1.05)
            self.eyes.rect = self.eyes.image.get_rect()
            self.eyes.rect.center = self.eyes.pos
            self.arg = False
    def random_move(self):
        self.timer_move += 1
        self.rect.x += self.randx
        self.rect.y += self.randy
        if self.rect.x <= 0:
            self.randx = self.speed
        if self.rect.x >= 1200:
            self.randx = -self.speed
        if self.rect.y <= 0:
            self.randy = self.speed
        if self.rect.y >= 800:
            self.randy = -self.speed
        if (self.timer_move/FPS) >1 and self.agr == False:
            self.randx = random.randint(-self.speed,self.speed)
            self.randy = random.randint(-self.speed, self.speed)
            self.timer_move = 0
        if self.agr:
            if self.rect.center[0] > self.food.rect.center[0]:
                self.randx = -1
                if self.rect.center[1] > self.food.rect.center[1]:
                    self.randy = -1
                else:
                    self.randy = 1
            else:
                self.randx = 1
                if self.rect.center[1] > self.food.rect.center[1]:
                    self.randy = -1
                else:
                    self.randy = 1

    def update(self):
        self.grow()
        self.random_move()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.timer_move = 0
        self.speed = 5
        self.randx = 0
        self.randy = 0
        self.food = None
        self.agr = False

    def grow(self):
        if pygame.sprite.spritecollide(self,civil_group,False):
            food = pygame.sprite.spritecollide(self,civil_group, False)[0]
            if self.image.get_height() / food.image.get_height() > 0.5:
                food.eyes.kill()
                food.kill()
                self.agr = False
                self.image = pygame.transform.rotozoom(self.image,0,1.05)
                self.pos = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = self.pos
                player.amount_civil -= 1

                self.eyes.pos = self.rect.center
                self.eyes.image = pygame.transform.rotozoom(self.eyes.image, 0, 1.05)
                self.eyes.rect = self.eyes.image.get_rect()
                self.eyes.rect.center = self.eyes.pos

            else:
                self.agr = False

    def random_move(self):
        self.timer_move += 1
        self.rect.x += self.randx
        self.rect.y += self.randy
        if self.rect.x <= 0:
            self.randx = self.speed
        if self.rect.x >= 1200:
            self.randx = -self.speed
        if self.rect.y <= 0:
            self.randy = self.speed
        if self.rect.y >= 800:
            self.randy = -self.speed
        if (self.timer_move/FPS) >1 and self.agr == False:
            self.randx = random.randint(-self.speed,self.speed)
            self.randy = random.randint(-self.speed, self.speed)
            self.timer_move = 0
        if self.agr:
            if self.rect.center[0] > self.food.rect.center[0]:
                self.randx = -1
                if self.rect.center[1] > self.food.rect.center[1]:
                    self.randy = -1
                else:
                    self.randy = 1
            else:
                self.randx = 1
                if self.rect.center[1] > self.food.rect.center[1]:
                    self.randy = -1
                else:
                    self.randy = 1
    def update(self):
        self.grow()
        self.random_move()

class Eyes(pygame.sprite.Sprite):
    def __init__(self,pos,block,type):
        pygame.sprite.Sprite.__init__(self)
        self.image = eyes_image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.block = block
        self.type = type
        self.pos = pos

    def update(self):
        self.rect.center = self.block.rect.center
        if self.type == 1:
            if (
                pygame.sprite.spritecollide(self, food_group, False)
                and self.block.agr == False
            ):
                food = pygame.sprite.spritecollide(self,food_group,False)[0]
                self.block.agr = True
                self.block.food = food
        if self.type == 2:
            if (
                pygame.sprite.spritecollide(self, civil_group, False)
                and self.block.agr == False
            ):
                food = pygame.sprite.spritecollide(self,civil_group,False)[0]
                self.block.agr = True
                self.block.food = food


def restart():
    global player_group, civil_group, enemy_group, food_group,player, eyes_group
    player_group = pygame.sprite.Group()
    civil_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    food_group = pygame.sprite.Group()
    eyes_group = pygame.sprite.Group()
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
    #eyes_group.draw(sc)
    eyes_group.update()
    pygame.display.update()






restart()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    game_lvl()
    clock.tick(FPS)