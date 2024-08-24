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
    def __init__(self, pacman):
        super().__init__()
        self.pacman=pacman
        img = pygame.image.load("Pacman\\Pacman_left.png")
        self.image = pygame.transform.rotozoom(img, 0, resize_factor)
        self.rect = self.image.get_rect()

    def update(self):
        pos = self.pacman.get_position()
        self.rect.center = [pos[1]*cell_size+12*resize_factor, pos[0]*cell_size+12*resize_factor]
        match(self.pacman.get_direction()):
            case 0:
                img= pygame.image.load("Pacman\\Pacman_up.png")                
            case 1:\
                img= pygame.image.load("Pacman\\Pacman_right.png")                
            case 2:\
                img= pygame.image.load("Pacman\\Pacman_down.png")                
            case 3:\
                img= pygame.image.load("Pacman\\Pacman_left.png")
        self.image = pygame.transform.rotozoom(img, 0, resize_factor)

class BlinkySprite(pygame.sprite.Sprite):
    def __init__(self, blinky):
        super().__init__()
        self.blinky=blinky
        img = pygame.image.load("Ghosts\\Blinky_left.png")
        self.image = pygame.transform.rotozoom(img, 0, resize_factor)
        self.rect = self.image.get_rect()

    def update(self):
        pos = self.blinky.get_position()

        if self.blinky.get_mode==2:
            img= pygame.image.load("Ghosts\\Frightened.png")  
        else:
            match(self.blinky.direction):
                case 0:
                    img= pygame.image.load("Ghosts\\Blinky_up.png")   
                    self.blinky.set_y_offset(-1)             
                case 1:
                    img= pygame.image.load("Ghosts\\Blinky_right.png")
                    self.blinky.set_x_offset(+1)                  
                case 2:
                    img= pygame.image.load("Ghosts\\Blinky_down.png") 
                    self.blinky.set_y_offset(+1)                 
                case 3:
                    img= pygame.image.load("Ghosts\\Blinky_left.png")
                    self.blinky.set_x_offset(-1)  
        
        # if self.starting<len(self.start_moves):
        #      self.rect.center = [self.col*cell_size-(20*resize_factor),self.row*cell_size-(8*resize_factor)]
        # else:        
        self.rect.center = [pos[1]*cell_size+12*resize_factor+int(self.blinky.get_x_offset()), pos[0]*cell_size+12*resize_factor+int(self.blinky.get_y_offset())]
        self.image = pygame.transform.rotozoom(img, 0, resize_factor)


class PinkySprite(pygame.sprite.Sprite):
    def __init__(self, pinky):
        super().__init__()
        self.pinky=pinky
        img = pygame.image.load("Ghosts\\Pinky_down.png")
        self.image = pygame.transform.rotozoom(img, 0, resize_factor)
        self.rect = self.image.get_rect()

    def update(self):
        pos = self.pinky.get_position()

        if self.pinky.get_mode==2:
            img= pygame.image.load("Ghosts\\Frightened.png")  
        else:
            match(self.pinky.direction):
                case 0:
                    img= pygame.image.load("Ghosts\\Pinky_up.png")   
                    self.pinky.set_y_offset(-1)           
                case 1:
                    img= pygame.image.load("Ghosts\\Pinky_right.png")
                    self.pinky.set_x_offset(+1)                
                case 2:
                    img= pygame.image.load("Ghosts\\Pinky_down.png") 
                    self.pinky.set_y_offset(+1)              
                case 3:
                    img= pygame.image.load("Ghosts\\Pinky_left.png")
                    self.pinky.set_x_offset(-1)  
        
        if self.pinky.get_starting<len(self.pinky.start_moves):
             self.rect.center = [pos[1]*cell_size-(20*resize_factor),self.row*cell_size-(8*resize_factor)]
        else:        
            self.rect.center = [pos[1]*cell_size+12*resize_factor+int(self.pinky.get_x_offset()), pos[0]*cell_size+12*resize_factor+int(self.pinky.get_y_offset())]
        self.image = pygame.transform.rotozoom(img, 0, resize_factor)