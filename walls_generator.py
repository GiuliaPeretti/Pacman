import pygame
import random
import time
from settings import *


def draw_background():
    screen.fill(BACKGROUND_COLOR)

def draw_grid(cell_size):
    line_width=3
    for i in range (0,SCREEN_WIDTH+1,cell_size):
        pygame.draw.line(screen, PINK, (i,0),(i,SCREEN_HEIGHT), line_width)
    for i in range (0,SCREEN_HEIGHT+1,cell_size):
        pygame.draw.line(screen, PINK, (0,i),(SCREEN_WIDTH,i), line_width)


def color_cell(row,col,color):
    x,y,w,h=col*cell_size, row*cell_size, cell_size, cell_size
    pygame.draw.rect(screen, color, (x,y,w,h))
    pygame.draw.line(screen, GRID_COLOR, (x,y),(x+cell_size,y), 3)
    pygame.draw.line(screen, GRID_COLOR, (x+cell_size,y),(x+cell_size,y+cell_size), 3)
    pygame.draw.line(screen, GRID_COLOR, (x,y+cell_size),(x+cell_size,y+cell_size), 3)
    pygame.draw.line(screen, GRID_COLOR, (x,y),(x,y+cell_size), 3)

def select_cell(x,y):
    row=y//cell_size
    col=x//cell_size
    if [row,col] in selected_cell:
        selected_cell.remove([row,col])
        color_cell(row=row,col=col,color=(0,0,0))
    else:
        color_cell(row=row,col=col,color=(0,0,255))
        selected_cell["walls"].append([row,col])

def write_on_file():
    f = open("walls.json", "w")
    f.write(str(selected_cell))
    f.close()



pygame.init()
clock=pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), flags, vsync=1)
pygame.display.set_caption('Tetris♥')
font = pygame.font.SysFont('arial', 20)


draw_background()
draw_grid(cell_size)
selected_cell={"walls":[]}



MOUSEEVENT = pygame.USEREVENT+1


pygame.time.set_timer(event=MOUSEEVENT, millis=50)
run  = True
while run:

    for event in pygame.event.get():
        if (event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE)):
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y=pygame.mouse.get_pos()
            select_cell(x,y)
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y=pygame.mouse.get_pos()
            select_cell(x,y)
        if event.type == MOUSEEVENT:
            if pygame.mouse.get_pressed()[0]:
                x,y=pygame.mouse.get_pos()
                select_cell(x,y)



    pygame.display.flip()
    clock.tick(30)
    

pygame.quit()

write_on_file()