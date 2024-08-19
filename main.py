import pygame
import random
import time
import ast
from settings import *


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
    x,y,w,h=col*cell_size+20, row*cell_size+20, cell_size,cell_size
    pygame.draw.rect(screen, color, (x,y,w,h))
    pygame.draw.line(screen, GRID_COLOR, (x,y),(x+cell_size,y), 3)
    pygame.draw.line(screen, GRID_COLOR, (x+cell_size,y),(x+cell_size,y+cell_size), 3)
    pygame.draw.line(screen, GRID_COLOR, (x,y+cell_size),(x+cell_size,y+cell_size), 3)
    pygame.draw.line(screen, GRID_COLOR, (x,y),(x,y+cell_size), 3)

def draw_not_walls():
    f = open("not_walls.txt", "r")
    not_walls = ast.literal_eval(f.read())
    f.close()
    for i in not_walls:
        color_cell(i[0]-1,i[1]-1,color=(0,0,255))


    
    
def manage_buttons(n):
    global game_status
    global start_time
    global ms_passed
    global buttons
    global best_score

    match n:
        case 0:
            if game_status==3:
                stop_the_game()
            game_status=1
            start_time = pygame.time.get_ticks() 
            new_next_pieces()
            gen_piece()
        case 1:


            if game_status==2:
                game_status=1
                start_time = pygame.time.get_ticks() 
                buttons[1]['name']='Pause'
                draw_buttons()

            else:
                game_status=2
                ms_passed = ms_passed + pygame.time.get_ticks() - start_time
                buttons[1]['name']='Restart'
                draw_buttons()

        case 2:
            stop_the_game()

        case 3:
            f = open("best_score.txt", "w")
            f.write('0')
            f.close()
            best_score=0
            display_best_score()






pygame.init()
clock=pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), flags, vsync=1)
pygame.display.set_caption('Tetris♥')
font = pygame.font.SysFont('arial', 20)


draw_background()
draw_grid(cell_size)
draw_not_walls()



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
            # for i in range (len(buttons)):
            #     if(x>=buttons[i]['coordinates'][0] and x<=buttons[i]['coordinates'][0]+buttons[i]['coordinates'][2] and y>=buttons[i]['coordinates'][1] and y<=buttons[i]['coordinates'][1]+buttons[i]['coordinates'][3]):
            #         manage_buttons(i)
            # else:
            #     selected=-1
            # draw_buttons()              
        if (event.type == pygame.KEYDOWN):
            for i in range(len(INPUTS)):
                if (event.key==INPUTS[i] and game_status==1):
                    pass

    pygame.display.flip()
    clock.tick(30)
    

pygame.quit()
