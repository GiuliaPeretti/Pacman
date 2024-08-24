from typing import Any
import pygame

from pygame.sprite import Group
from settings import *

class BackgroundSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Background.png")
        self.image = pygame.transform.rotozoom(self.image, 0, resize_factor)
        self.rect = self.image.get_rect()

class HighScoreSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("High_score.png")
        self.image = pygame.transform.rotozoom(self.image, 0, resize_factor)
        self.rect = self.image.get_rect()
        self.rect.topleft = [9*cell_size,2]

class CellSprite(pygame.sprite.Sprite):
    def __init__(self, cell, row, col):
        super().__init__()
        self.cell = cell
        self.image = pygame.Surface((cell_size,cell_size))
        self.image.fill(BLACK)
        self.image = pygame.transform.rotozoom(self.image, 0, resize_factor)
        self.rect = self.image.get_rect()
        self.rect.center = [col*cell_size+(cell_size/2)*resize_factor,row*cell_size+(cell_size/2)*resize_factor]
        self.cell

    def update(self):
        match(self.cell.get_dot()):
            case 0:
                self.image = pygame.Surface((cell_size,cell_size))
                self.image.fill(BLACK)
            case 1:
                #TODO: fix this
                img = pygame.image.load("Fruits\\Dot.png").convert()
                self.image = pygame.transform.smoothscale(img,(img.get_width()*resize_factor,img.get_height()*resize_factor))
 
            case 2:
                img = pygame.image.load("Fruits\\Power_pill.png").convert()
                self.image = pygame.transform.smoothscale(img,(img.get_width()*resize_factor,img.get_height()*resize_factor))
        if (self.cell.get_fruit()):
            fruits=[
            "Fruits\\Cherry.png",
            "Fruits\\Strawberry.png",
            "Fruits\\Orange.png",
            "Fruits\\Apple.png",
            "Fruits\\Melon.png",
            "Fruits\\Galaxian.png",
            "Fruits\\Bell.png",
            "Fruits\\Key.png",
            ]

            img = pygame.image.load(fruits[0]).convert()
            self.image = pygame.transform.smoothscale(img,(img.get_width()*resize_factor,img.get_height()*resize_factor))


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
                    # self.blinky.set_y_offset(-1)             
                case 1:
                    img= pygame.image.load("Ghosts\\Blinky_right.png")
                    # self.blinky.set_x_offset(+1)                  
                case 2:
                    img= pygame.image.load("Ghosts\\Blinky_down.png") 
                    # self.blinky.set_y_offset(+1)                 
                case 3:
                    img= pygame.image.load("Ghosts\\Blinky_left.png")
                    # self.blinky.set_x_offset(-1)  
        
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
                    # self.pinky.set_y_offset(-1)           
                case 1:
                    img= pygame.image.load("Ghosts\\Pinky_right.png")
                    # self.pinky.set_x_offset(+1)                
                case 2:
                    img= pygame.image.load("Ghosts\\Pinky_down.png") 
                    # self.pinky.set_y_offset(+1)              
                case 3:
                    img= pygame.image.load("Ghosts\\Pinky_left.png")
                    # self.pinky.set_x_offset(-1)  
        
        if self.pinky.get_starting()<len(self.pinky.get_start_moves()):
             self.rect.center = [pos[1]*cell_size,pos[0]*cell_size+12*resize_factor]
        else:        
            self.rect.center = [pos[1]*cell_size+12*resize_factor+int(self.pinky.get_x_offset()), pos[0]*cell_size+12*resize_factor+int(self.pinky.get_y_offset())]
        self.image = pygame.transform.rotozoom(img, 0, resize_factor)



class InkySprite(pygame.sprite.Sprite):
    def __init__(self, inky):
        super().__init__()
        self.inky=inky
        img = pygame.image.load("Ghosts\\Inky_up.png")
        self.image = pygame.transform.rotozoom(img, 0, resize_factor)
        self.rect = self.image.get_rect()

    def update(self):
        pos = self.inky.get_position()

        if self.inky.get_mode==2:
            img= pygame.image.load("Ghosts\\Frightened.png")  
        else:
            match(self.inky.direction):
                case 0:
                    img= pygame.image.load("Ghosts\\Inky_up.png")   
                    # self.inky.set_y_offset(-1)        
                case 1:
                    img= pygame.image.load("Ghosts\\Inky_right.png")
                    # self.inky.set_x_offset(+1)            
                case 2:
                    img= pygame.image.load("Ghosts\\Inky_down.png") 
                    # self.inky.set_y_offset(+1)          
                case 3:
                    img= pygame.image.load("Ghosts\\Inky_left.png")
                    # self.inky.set_x_offset(-1)  
        
        if self.inky.get_starting()<len(self.inky.get_start_moves()):
             self.rect.center = [pos[1]*cell_size,pos[0]*cell_size+12*resize_factor]
        else:        
            self.rect.center = [pos[1]*cell_size+12*resize_factor+int(self.inky.get_x_offset()), pos[0]*cell_size+12*resize_factor+int(self.inky.get_y_offset())]
        self.image = pygame.transform.rotozoom(img, 0, resize_factor)


    
class ClydeSprite(pygame.sprite.Sprite):
    def __init__(self, clyde):
        super().__init__()
        self.clyde=clyde
        img = pygame.image.load("Ghosts\\Clyde_up.png")
        self.image = pygame.transform.rotozoom(img, 0, resize_factor)
        self.rect = self.image.get_rect()

    def update(self):
        pos = self.clyde.get_position()

        if self.clyde.get_mode==2:
            img= pygame.image.load("Ghosts\\Frightened.png")  
        else:
            match(self.clyde.direction):
                case 0:
                    img= pygame.image.load("Ghosts\\Clyde_up.png")   
                    # self.clyde.set_y_offset(-1)        
                case 1:
                    img= pygame.image.load("Ghosts\\Clyde_right.png")
                    # self.clyde.set_x_offset(+1)            
                case 2:
                    img= pygame.image.load("Ghosts\\Clyde_down.png") 
                    # self.clyde.set_y_offset(+1)          
                case 3:
                    img= pygame.image.load("Ghosts\\Clyde_left.png")
                    # self.clyde.set_x_offset(-1)  
        
        if self.clyde.get_starting()<len(self.clyde.get_start_moves()):
             self.rect.center = [pos[1]*cell_size,pos[0]*cell_size+12*resize_factor]
        else:        
            self.rect.center = [pos[1]*cell_size+12*resize_factor+int(self.clyde.get_x_offset()), pos[0]*cell_size+12*resize_factor+int(self.clyde.get_y_offset())]
        self.image = pygame.transform.rotozoom(img, 0, resize_factor)