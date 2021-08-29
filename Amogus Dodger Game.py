# Amazing Game made by Antokid555

import os
import pickle
import pygame
import random

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_w,
    K_s,
    K_a,
    K_d,
)


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load('Assets/car.png').convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.move_ip((10, 300))

    def move(self, pressed_key):
        if pressed_key[K_UP] or pressed_key[K_w]:
            self.rect.move_ip(0, -5)
        if pressed_key[K_DOWN] or pressed_key[K_s]:
            self.rect.move_ip(0, 5)
        if pressed_key[K_LEFT] or pressed_key[K_a]:
            self.rect.move_ip(-5, 0)
        if pressed_key[K_RIGHT] or pressed_key[K_d]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screenW:
            self.rect.right = screenW
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screenH:
            self.rect.bottom = screenH


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load('Assets/SUS.png').convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(screenW + 20, screenW + 100),
                random.randint(0, screenH)
            )
        )
        self.speed = random.randint(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
        if CurrentScore < 1:
            self.kill()


pygame.mixer.init()
pygame.init()
pygame.display.set_caption('Epic Amogus Avoider Game')

screenW = 800
screenH = 600
screen = pygame.display.set_mode((screenW, screenH))

filler = 0
running = True

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

ScoreTimer = pygame.USEREVENT + 2
pygame.time.set_timer(ScoreTimer, 1000)

CurrentScore = 0
BestScore = 0


if os.path.exists('Assets/Amogus.sus'):
    try:
        BestScore = pickle.load(open('Assets/Amogus.sus', 'rb'))
    except:
        BestScore = 0
else:
    open('Assets/Amogus.sus', 'x')




font = pygame.font.Font('Assets/freesansbold.ttf', 20)
font2 = pygame.font.Font('Assets/freesansbold.ttf', 70)
text = font.render(str(CurrentScore), True, (255, 255, 255))
textRect = text.get_rect()
textRect.left = 0


player = Player()

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Imagine crediting people LMAO
pygame.mixer.music.load('Assets/music.mp3')
pygame.mixer.music.play(loops=-1)

clock = pygame.time.Clock()

screen.blit(text, (20, 20))
while running:

    for event in pygame.event.get():

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type == ScoreTimer:
            CurrentScore += 1
            if CurrentScore > BestScore:
                BestScore = CurrentScore

    pressed_keys = pygame.key.get_pressed()

    player.move(pressed_keys)

    enemies.update()

    screen.fill((0, 0, 0))

    screen.blit(text, textRect)
    text = font.render('Current Score: ' + str(CurrentScore) + '  ' + 'Best Score: ' + str(BestScore), True,
                       (255, 255, 255))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(player, enemies):
        player.rect.center = (10, screenH / 2)
        CurrentScore = 0

    pygame.display.flip()
    clock.tick(30)

pickle.dump(BestScore, open('Assets/Amogus.sus', 'wb'))
pygame.quit()
