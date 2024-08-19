import pygame
import random
import time
import ast
from settings import *


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

        line_width=1
        x,y,w,h=self.col*cell_size, self.row*cell_size, cell_size,cell_size
        pygame.draw.rect(screen, color, (x,y,w,h))
        pygame.draw.line(screen, GRID_COLOR, (x,y),(x+cell_size,y), line_width)
        pygame.draw.line(screen, GRID_COLOR, (x+cell_size,y),(x+cell_size,y+cell_size), line_width)
        pygame.draw.line(screen, GRID_COLOR, (x,y+cell_size),(x+cell_size,y+cell_size), line_width)
        pygame.draw.line(screen, GRID_COLOR, (x,y),(x,y+cell_size), line_width)

    

def draw_background():
    screen.fill(BACKGROUND_COLOR)

def draw_grid(cell_size):
    line_width=3
    for i in range (0,SCREEN_WIDTH+1,cell_size):
        pygame.draw.line(screen, PINK, (i,0),(i,SCREEN_HEIGHT), line_width)
    for i in range (0,SCREEN_HEIGHT+1,cell_size):
        pygame.draw.line(screen, PINK, (0,i),(SCREEN_WIDTH,i), line_width)

def draw_wall(row,col,n,wall_color=(00,00,00)):
    line_width=1
    #0->up, 1->right, 2->down, 3->left
    x,y,w,h=col*cell_size+20, row*cell_size+20, cell_size,cell_size
    match n:
        case 0:
            pygame.draw.line(screen, wall_color, (x,y),(x+cell_size,y), line_width)
        case 1:
            pygame.draw.line(screen, wall_color, (x+cell_size,y),(x+cell_size,y+cell_size), line_width)
        case 2:
            pygame.draw.line(screen, wall_color, (x,y+cell_size),(x+cell_size,y+cell_size), line_width)
        case 3:
            pygame.draw.line(screen, wall_color, (x,y),(x,y+cell_size), line_width)
    if(row==0 and col==0):
        pygame.draw.line(screen, RED, (20,20),(20+cell_size,20), line_width)
    elif(row==(560/cell_size)-1 and col==(560/cell_size)-1):
        pygame.draw.line(screen, RED, ( (row*cell_size)+cell_size+20 , (col*cell_size)+20 ) , ((row*cell_size)+cell_size+20 , (col*cell_size)+cell_size+20), line_width)

def color_cell(row,col,color):
    line_width=1
    x,y,w,h=col*cell_size, row*cell_size, cell_size,cell_size
    pygame.draw.rect(screen, color, (x,y,w,h))
    pygame.draw.line(screen, GRID_COLOR, (x,y),(x+cell_size,y), line_width)
    pygame.draw.line(screen, GRID_COLOR, (x+cell_size,y),(x+cell_size,y+cell_size), line_width)
    pygame.draw.line(screen, GRID_COLOR, (x,y+cell_size),(x+cell_size,y+cell_size), line_width)
    pygame.draw.line(screen, GRID_COLOR, (x,y),(x,y+cell_size), line_width)

def draw_not_walls():
    f = open("not_walls.txt", "r")
    walkable = ast.literal_eval(f.read())
    f.close()
    for i in walkable:
        color_cell(i[0],i[1],color=(0,0,255))

def write_number():
    font = pygame.font.SysFont('arial', 15)
    for i in range (0,SCREEN_WIDTH+1,cell_size):
        text=font.render(str(i//cell_size), True, GREEN)
        screen.blit(text, (i,2))
    for i in range (0,SCREEN_HEIGHT+1,cell_size):
        text=font.render(str(i//cell_size), True, GREEN)
        screen.blit(text, (2,i))

def init_grid():
    f = open("not_walls.txt", "r")
    walkable = ast.literal_eval(f.read())
    f.close()
    for row in range (height_in_cell):
        temp=[]
        for col in range (width_in_cell):
            wall=True
            food=False
            if [row,col] in walkable:
                wall=False
            temp.append(Cell(row, col, wall, food))
        grid.append(temp)
                
def draw_cells():
    global grid
    for row in range (len(grid)):
        for col in range (len(grid[0])):
            grid[row][col].draw_cell(screen)

def display_img():
    images=[
        "GamesImages\\bottom_to_right.png",
        "GamesImages\\bottom_to_left.png",
        "GamesImages\\top_to_right.png",
        "GamesImages\\top_to_left.png",
        "GamesImages\\vertical_right.png",
        "GamesImages\\vertical_left.png",
        "GamesImages\\horizontal_top.png",
        "GamesImages\\horizontal_bottom.png",
        "GamesImages\\vertical_right2.png",
        "GamesImages\\vertical_left2.png",
        "GamesImages\\horizontal_top2.png",
        "GamesImages\\horizontal_bottom2.png",
        "GamesImages\\bottom_to_right2.png",
        "GamesImages\\bottom_to_left2.png",
    ]
    for i in range (len(images)):
        imp = pygame.image.load(images[i]).convert()
        screen.blit(imp, (i*cell_size,0))


pygame.init()
clock=pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), flags, vsync=1)
pygame.display.set_caption('Tetris♥')
font = pygame.font.SysFont('arial', 20)



grid=[]
init_grid()
draw_background()
draw_grid(cell_size)
draw_cells()
write_number()
display_img()


MOVEEVENT = pygame.USEREVENT+1
TIMEEVENT = pygame.USEREVENT+2
KEYEVENT = pygame.USEREVENT+3

pygame.time.set_timer(event=MOVEEVENT, millis=500)
pygame.time.set_timer(event=TIMEEVENT, millis=100)
# pygame.time.set_timer(event=KEYEVENT, millis=500)
run  = True
while run:

    for event in pygame.event.get():
        if (event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE)):
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y=pygame.mouse.get_pos()
            print(y//cell_size, x//cell_size)             
        if (event.type == pygame.KEYDOWN):
            for i in range(len(INPUTS)):
                if (event.key==INPUTS[i]):
                    pass

    pygame.display.flip()
    clock.tick(30)
    

pygame.quit()
