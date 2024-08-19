import pygame
import random
import time
import ast
import math
from settings import *


class Cell:
    def __init__(self, row: int, col: int, wall: bool, food: bool, intersection: bool) -> None:
        self.row=row
        self.col=col
        self.wall=wall
        self.food=food
        self.intersection=intersection
        self.pacman=False

    def is_wall(self):
        return self.wall
    
    def is_intersection(self):
        return self.intersection

    def draw_cell(self, screen):
        if self.wall:
            color=(0,0,255)
        elif self.pacman:
            color=(255,255,0)
        elif self.intersection:
            color=(0,255,0)
        else:
            color=(0,0,0)

        line_width=1
        x,y,w,h=self.col*cell_size, self.row*cell_size, cell_size,cell_size
        pygame.draw.rect(screen, color, (x,y,w,h))
        pygame.draw.line(screen, GRID_COLOR, (x,y),(x+cell_size,y), line_width)
        pygame.draw.line(screen, GRID_COLOR, (x+cell_size,y),(x+cell_size,y+cell_size), line_width)
        pygame.draw.line(screen, GRID_COLOR, (x,y+cell_size),(x+cell_size,y+cell_size), line_width)
        pygame.draw.line(screen, GRID_COLOR, (x,y),(x,y+cell_size), line_width)

    def set_pacman(self, b):
        self.pacman=b

class Blinky:
    def __init__(self):
        self.row=17
        self.col=12
        #0 -> Scatter, 1 -> Chase, 2 -> Frightened
        self.mode=0
        #0 -> Up, 1 -> Right, 2 -> Down, 3 -> Left
        self.direction=0

    def draw_ghost(self, screen):
        color=(255,0,0)
        line_width=1
        x,y,w,h=self.col*cell_size, self.row*cell_size, cell_size,cell_size
        pygame.draw.rect(screen, color, (x,y,w,h))
        pygame.draw.line(screen, GRID_COLOR, (x,y),(x+cell_size,y), line_width)
        pygame.draw.line(screen, GRID_COLOR, (x+cell_size,y),(x+cell_size,y+cell_size), line_width)
        pygame.draw.line(screen, GRID_COLOR, (x,y+cell_size),(x+cell_size,y+cell_size), line_width)
        pygame.draw.line(screen, GRID_COLOR, (x,y),(x,y+cell_size), line_width)

    def move_ghost(self, grid, screen):
        self.chose_direction(grid)
        match(dir):
            case 0: 
                #UP
                if not grid[self.row-1][self.col].is_wall():
                    self.clear_ghost()
                    self.row=self.row-1
                    self.draw_ghost(screen)
            case 1:
                #RIGHT
                if not grid[self.row][self.col+1].is_wall():
                    self.clear_ghost()
                    self.col=self.col+1
                    self.draw_ghost(screen)
            case 2:
                #DOWN
                if not grid[self.row+1][self.col].is_wall():
                    self.clear_ghost()
                    self.row=self.row+1
                    self.draw_ghost(screen)
            case 3:
                #LEFT
                if not grid[self.row][self.col-1].is_wall():
                    self.clear_ghost()
                    self.col=self.col-1
                    self.draw_ghost(screen)
                
        def chose_direction(grid):
            if grid[self.row][self.col].is_intersection():
                target=[]
                match(self.mode):
                    case 0:
                        #Scatter 0,25
                        target+[0,25]
                        return
                    case 1:
                        #Chase
                        return
                    case 2:
                        #Frightened
                        return
                min=1000
                valids=self.get_valid_dir(grid)
                possible_dir=[[-1,0], [0,+1], [+1,0], [0,-1]]
                selected_dir=-1
                for i in valids:
                    dis = get_distance(target_row=self.row+possible_dir[i][0], target_col=self.col+possible_dir[i][1])
                    if min > dis:
                        min = dis
                        selected_dir=i
            self.direction=selected_dir
            self.move_ghost(self.direction)
                    
        def get_distance(target_row, target_col):
            return math.sqrt((target_row-self.row)**2+(target_col-self.col)**2)
        
        def get_valid_dir(self, grid):
            valids=[]
            possible_dir=[[-1,0], [0,+1], [+1,0], [0,-1]]
            for i in range (len(possible_dir)):
                if not grid[self.row+possible_dir[i][0]][self.col+possible_dir[i][1]].is_wall():
                    valids.append(i)
            if (self.direction in valids):
                valids.remove(self.direction)
            return valids




            
    
    def clear_ghost(self):
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
    f = open("intersection.txt", "r")
    intersections = ast.literal_eval(f.read())
    f.close()

    for row in range (height_in_cell):
        temp=[]
        for col in range (width_in_cell):
            wall=True
            food=False
            intersection=False
            if [row,col] in walkable:
                wall=False
            if [row,col] in intersections:
                intersection=True
            temp.append(Cell(row, col, wall, food, intersection))
        grid.append(temp)
    grid[26][14].set_pacman(True)
                
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

def handle_movements(dir):
    match(dir):
        case 0: 
            #UP
            if pacman_pos[0]-1!=-1 and not grid[pacman_pos[0]-1][pacman_pos[1]].is_wall():
                grid[pacman_pos[0]][pacman_pos[1]].set_pacman(b=False)
                grid[pacman_pos[0]][pacman_pos[1]].draw_cell(screen)
                grid[pacman_pos[0]-1][pacman_pos[1]].set_pacman(b=True)
                grid[pacman_pos[0]-1][pacman_pos[1]].draw_cell(screen)
                pacman_pos[0]=pacman_pos[0]-1
        case 1:
            #RIGHT
            if pacman_pos[1]+1==len(grid[0]) and pacman_pos[0]==17:
                grid[pacman_pos[0]][pacman_pos[1]].set_pacman(b=False)
                grid[pacman_pos[0]][pacman_pos[1]].draw_cell(screen)
                grid[pacman_pos[0]][0].set_pacman(b=True)
                grid[pacman_pos[0]][0].draw_cell(screen)
                pacman_pos[1]=0  
                return             

            if pacman_pos[1]+1!=len(grid[0]) and not grid[pacman_pos[0]][pacman_pos[1]+1].is_wall():
                grid[pacman_pos[0]][pacman_pos[1]].set_pacman(b=False)
                grid[pacman_pos[0]][pacman_pos[1]].draw_cell(screen)
                grid[pacman_pos[0]][pacman_pos[1]+1].set_pacman(b=True)
                grid[pacman_pos[0]][pacman_pos[1]+1].draw_cell(screen)
                pacman_pos[1]=pacman_pos[1]+1
        case 2:
            #DOWN
            if pacman_pos[0]+1!=len(grid[0]) and not grid[pacman_pos[0]+1][pacman_pos[1]].is_wall():
                grid[pacman_pos[0]][pacman_pos[1]].set_pacman(b=False)
                grid[pacman_pos[0]][pacman_pos[1]].draw_cell(screen)
                grid[pacman_pos[0]+1][pacman_pos[1]].set_pacman(b=True)
                grid[pacman_pos[0]+1][pacman_pos[1]].draw_cell(screen)
                pacman_pos[0]=pacman_pos[0]+1
        case 3:
            #LEFT
            if pacman_pos[1]-1==-1 and pacman_pos[0]==17:
                grid[pacman_pos[0]][pacman_pos[1]].set_pacman(b=False)
                grid[pacman_pos[0]][pacman_pos[1]].draw_cell(screen)
                grid[pacman_pos[0]][27].set_pacman(b=True)
                grid[pacman_pos[0]][27].draw_cell(screen)
                pacman_pos[1]=27     
                return
            
            if pacman_pos[1]-1!=-1 and not grid[pacman_pos[0]][pacman_pos[1]-1].is_wall():
                grid[pacman_pos[0]][pacman_pos[1]].set_pacman(b=False)
                grid[pacman_pos[0]][pacman_pos[1]].draw_cell(screen)  
                grid[pacman_pos[0]][pacman_pos[1]-1].set_pacman(b=True)
                grid[pacman_pos[0]][pacman_pos[1]-1].draw_cell(screen)
                pacman_pos[1]=pacman_pos[1]-1
            

        
        


pygame.init()
clock=pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), flags, vsync=1)
pygame.display.set_caption('Tetris♥')
font = pygame.font.SysFont('arial', 20)



grid=[]
pacman_pos=[26,14]
blinky = Blinky()
init_grid()
draw_background()
draw_grid(cell_size)
draw_cells()
write_number()
display_img()


GHOSTEVENT = pygame.USEREVENT+1


pygame.time.set_timer(event=GHOSTEVENT, millis=1000)
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
                    handle_movements(i)
                    break
        if (event.type == GHOSTEVENT):
            blinky.move_ghost(grid, screen)

    pygame.display.flip()
    clock.tick(30)
    

pygame.quit()
