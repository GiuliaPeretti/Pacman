import pygame

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

    def change_pos(self, pos):
        self.rect.center= [pos[1]*cell_size+12*resize_factor, pos[0]*cell_size+12*resize_factor]