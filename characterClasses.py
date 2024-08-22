import pygame
from settings import *

class Cell:
    def __init__(self, row: int, col: int, wall: bool, dot: int, intersection: bool) -> None:
        self.row=row
        self.col=col
        self.wall=wall
        self.intersection=intersection
        #0 -> no dot, 1 -> dot, 2 -> power pill
        self.dot=dot
        self.fruit=False

    def is_wall(self):
        return self.wall
    
    def is_intersection(self):
        return self.intersection
    
    def set_dot(self, n):
        self.dot=n

    def set_fruit(self, b):
        self.fruit=b

    def get_dot(self):
        return self.dot
    
    def draw_dot(self, screen, level):
        match(self.dot):
            case 0:
                return
                # x,y,w,h=self.col*cell_size, self.row*cell_size, cell_size,cell_size
                # pygame.draw.rect(screen, PINK, (x,y,w,h))
            case 1:
                #TODO: fix this
                x,y,w,h=self.col*cell_size+(2*resize_factor), self.row*cell_size+(2*resize_factor), cell_size-(4*resize_factor),cell_size-(4*resize_factor)
                pygame.draw.rect(screen, BLACK, (x,y,w,h))
                x,y,w,h=self.col*cell_size+(9*resize_factor), self.row*cell_size+(9*resize_factor), 6*resize_factor, 6*resize_factor
                pygame.draw.rect(screen, (205, 150, 140), (x,y,w,h))      
            case 2:
                img = pygame.image.load("Fruits\\Food.png").convert()
                img = pygame.transform.smoothscale(img,(img.get_width()*resize_factor,img.get_height()*resize_factor))
                screen.blit(img, ( self.col*cell_size+(cell_size-img.get_width())/2, self.row*cell_size+(cell_size-img.get_height())/2 ))
        if (self.fruit):
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

            img = pygame.image.load(fruits[level-1]).convert()
            img = pygame.transform.smoothscale(img,(img.get_width()*resize_factor,img.get_height()*resize_factor))
            screen.blit(img, (13*cell_size+(4*resize_factor),20*cell_size-(8*resize_factor)))

    # def draw_cell(self, screen):
    #     if self.wall:
    #         color=(0,0,255)
    #     elif self.pacman:
    #         color=(255,255,0)
    #     elif self.intersection:
    #         color=(0,255,0)
    #     else:
    #         color=(0,0,0)

    #     line_width=1
    #     x,y,w,h=self.col*cell_size, self.row*cell_size, cell_size,cell_size
    #     pygame.draw.rect(screen, color, (x,y,w,h))
    #     pygame.draw.line(screen, GRID_COLOR, (x,y),(x+cell_size,y), line_width)
    #     pygame.draw.line(screen, GRID_COLOR, (x+cell_size,y),(x+cell_size,y+cell_size), line_width)
    #     pygame.draw.line(screen, GRID_COLOR, (x,y+cell_size),(x+cell_size,y+cell_size), line_width)
    #     pygame.draw.line(screen, GRID_COLOR, (x,y),(x,y+cell_size), line_width)
