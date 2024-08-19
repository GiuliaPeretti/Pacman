import pygame
from settings import *
from main import grid

class Cell:
    def __init__(self, row: int, col: int, wall: bool, food: bool) -> None:
        self.row=row
        self.col=col
        self.wall=wall
        self.food=food

    def is_wall(self):
        return self.wall

    def draw_cell(self, screen):
        if self.wall:
            color=(0,0,255)
        else:
            color=(0,0,0)

        x,y,w,h=self.col*cell_size+20, self.row*cell_size+20, cell_size,cell_size
        pygame.draw.rect(screen, color, (x,y,w,h))
        pygame.draw.line(screen, GRID_COLOR, (x,y),(x+cell_size,y), 3)
        pygame.draw.line(screen, GRID_COLOR, (x+cell_size,y),(x+cell_size,y+cell_size), 3)
        pygame.draw.line(screen, GRID_COLOR, (x,y+cell_size),(x+cell_size,y+cell_size), 3)
        pygame.draw.line(screen, GRID_COLOR, (x,y),(x,y+cell_size), 3)

    