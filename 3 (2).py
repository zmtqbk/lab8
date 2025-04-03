import pygame
import random
from pygame.locals import*
import time
import sys

pygame.init()

FSP = 60
FramePerSec = pygame.time.Clock()

backgroundSound = pygame.mixer.music.load(r"C:\Users\Aidar\Desktop\python\Lecture_G2_Week10_racer_resources_background.wav")
backgroundSound = pygame.mixer.music.play(-1)

background = pygame.image.load(r"C:\Users\Aidar\Desktop\python\fon2.jpg")
screen = pygame.display.set_mode((400,600))

speed = 5
coin_speed = 5
score = 0
coins_collected = 0


#Setting up Fonts
font = pygame.font.SysFont("Times New Roman", 60)
font_small = pygame.font.SysFont("Times New Roman", 20)
game_over = font.render("Game Over", True, (255,255,255))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"C:\Users\Aidar\Desktop\python\smile.png")
        self.rect = self.image.get_rect()
        self.rect.center = (190, 546)

    def move(self):
        pressed_key = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_key[K_LEFT]:
                self.rect.move_ip(-10, 0)
        if self.rect.right < 400:
            if pressed_key[K_RIGHT]:
                self.rect.move_ip(10, 0)

    def collect_coins(self, coins_group):
        global score, coins_collected, speed
        collected_coins = pygame.sprite.spritecollide(self, coins_group, True)
        for coin in collected_coins:
            if coin.value == 5:
                score += 5
            elif coin.value == 10:
                score += 10
            elif coin.value == 25:
                score += 25
            
            if coins_collected % N == 0:
                speed += 0.5

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"C:\Users\Aidar\Desktop\python\sadsmile.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, 360), 0)

    def move(self):
        self.rect.move_ip(0, speed)
        if self.rect.bottom > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(40, 360), 0)

class Coins(pygame.sprite.Sprite):
    def __init__(self, value, enemies, coin_speed):
        super().__init__()
        print("Creating coin with value:", value)
        self.value = value
        if self.value == 5:
            self.image = pygame.image.load(r"C:\Users\Aidar\Desktop\python\5coin.png").convert_alpha()
        elif self.value == 10:
            self.image = pygame.image.load(r"C:\Users\Aidar\Desktop\python\10coin.png").convert_alpha()
        elif self.value == 25:
            self.image = pygame.image.load(r"C:\Users\Aidar\Desktop\python\25coin.png").convert_alpha()
        else:
            raise ValueError("Invalid coin value")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, 360), 0)
        self.enemies = enemies

        while pygame.sprite.spritecollideany(self, self.enemies):
            self.rect.center = (random.randint(40, 360), 0)


    def move(self): 
        self.rect.move_ip(0, coin_speed)
        if self.rect.bottom > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(40, 360), 0)

            while pygame.sprite.spritecollideany(self, self.enemies):
                self.rect.center = (random.randint(40, 360), 0)

        

p1 = Player()
e1 = Enemy()

enemies = pygame.sprite.Group()
enemies.add(e1)


coins = pygame.sprite.Group()
c1 = Coins(5, enemies, coin_speed)
coins.add(c1)

all_sprites = pygame.sprite.Group()
all_sprites.add(p1)
all_sprites.add(e1)
all_sprites.add(c1)

inc_speed = pygame.USEREVENT + 1
pygame.time.set_timer(inc_speed, 1000)

N = 10

done = False
while not done:
    for event in pygame.event.get():
        
        if event.type == inc_speed:
          new_coin = Coins(random.choice([5, 10, 25]), enemies, coin_speed=3)
          coins.add(new_coin)
          all_sprites.add(new_coin)

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    
    screen.blit(background, (0,0))
    scores = font_small.render(str(score), True, (0, 0, 0))
    screen.blit(scores, (10,10))


    for entity in all_sprites:
        entity.move()
        screen.blit(entity.image, entity.rect)

    p1.collect_coins(coins)


    if pygame.sprite.spritecollideany(p1, enemies):
        backgroundSound = pygame.mixer.music.stop()
        crash = pygame.mixer.Sound(r"C:\Users\Aidar\Desktop\python\bonk.mp3")
        crash.play(1)

        screen.fill((255,0,0))

        scores = font.render("Score: " + str(score), True, (255, 255, 255))
        screen.blit(scores, (70,350))
        screen.blit(game_over, (50, 250))
        pygame.display.update()
        time.sleep(1)
        done = True
        


    pygame.display.update()
    FramePerSec.tick(FSP)