import pygame, sys

from pygame.sprite import Group
from settings import *

class BackgroundSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Background.png")
        self.image = pygame.transform.rotozoom(self.image, 0, resize_factor)
        self.rect = self.image.get_rect()

class PacmanSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pygame.image.load("Pacman\\Pacman_left.png")
        self.image = pygame.transform.rotozoom(img, 0, resize_factor)
        self.rect = self.image.get_rect()
        self.rect.center= [14*cell_size+12*resize_factor, 26*cell_size+12*resize_factor]

    def change_pos(self,row, col):
        self.rect.center= [col*cell_size+12*resize_factor, row*cell_size+12*resize_factor]


pygame.init()
clock=pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), flags, vsync=1)
pygame.display.set_caption('Pacman♥')
font = pygame.font.SysFont('arial', 20)

background = BackgroundSprite()
pacmanSprite = PacmanSprite()
game_group = pygame.sprite.Group()
game_group.add(background)
game_group.add(pacmanSprite)

pacmanSprite.change_pos(23,11)


run  = True
while run:

    for event in pygame.event.get():
        if (event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE)):
            run = False

    game_group.draw(screen)
    game_group.update()


    pygame.display.flip()
    clock.tick(30)
    

pygame.quit()
