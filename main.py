import pygame
import random
import time
import ast
import math
from settings import *

#TODO: A ghost in Frightened mode also turns dark blue, moves much more slowly and can be eaten by Pac-Man
#TODO: implementa livelli
#TODO: ricontrolla meglio lo sfondo che secondo me hai sbagliato qualcosa
#TODO: — ghosts can not choose to turn upwards from these tiles.    

class Ghost:
    def __init__(self):
        #0 -> Scatter, 1 -> Chase, 2 -> Frightened
        self.mode=0
        #0 -> Up, 1 -> Right, 2 -> Down, 3 -> Left
        self.direction=0
        self.starting=0
        self.target=[None,None]

    def move_ghost(self, grid, screen):
        dir = self.chose_direction(grid)
        self.direction=dir
        match(dir):
            case 0: 
                #UP
                # if not grid[self.row-1][self.col].is_wall():
                self.clear_ghost()
                self.row=self.row-1
                self.display_ghost(screen)
                    
            case 1:
                #RIGHT
                # if not grid[self.row][self.col+1].is_wall():
                self.clear_ghost()
                self.col=self.col+1
                self.display_ghost(screen)
            case 2:
                #DOWN
                # if not grid[self.row+1][self.col].is_wall():
                self.clear_ghost()
                self.row=self.row+1
                self.display_ghost(screen)
            case 3:
                #LEFT
                # if not grid[self.row][self.col-1].is_wall():
                self.clear_ghost()
                self.col=self.col-1
                self.display_ghost(screen)

    def chose_direction(self, grid):
        if self.starting<len(self.start_moves):
            self.starting+=1
            return self.start_moves[self.starting-1]

        if self.mode==2:
            valids=self.get_valid_dir(grid)
            return random.choice(valids)

        
        # if grid[self.row][self.col].is_intersection() or self.starting==4:
        self.starting=len(self.start_moves)
        self.set_target()

        min=1000
        valids=self.get_valid_dir(grid)
        possible_dir=[[-1,0], [0,+1], [+1,0], [0,-1]]
        selected_dir=-1
        for i in valids:
            point_x= self.col+possible_dir[i][1]
            point_y = self.row+possible_dir[i][0]
            target_x=self.target[1]
            target_y=self.target[0]

            dis = math.sqrt(((target_x-point_x)**2)+((target_y-point_y)**2))
            # dis = math.sqrt(((target[0]-self.row+possible_dir[i][0])**2)+((target[1]-self.col+possible_dir[i][1])**2))
            
            if min > dis:
                min = dis
                selected_dir=i
        return selected_dir                
        
    def get_valid_dir(self, grid):
        valids=[]
        possible_dir=[[-1,0], [0,+1], [+1,0], [0,-1]]
        print(self.row, self.col)
        for i in range (len(possible_dir)):
            row = self.row+possible_dir[i][0]
            col = self.col+possible_dir[i][1]
            if not grid[self.row+possible_dir[i][0]][self.col+possible_dir[i][1]].is_wall():
                valids.append(i)
        match (self.direction):
            case 0:
                if (2 in valids):
                    valids.remove(2)
            case 1:
                if (3 in valids):
                    valids.remove(3)
            case 2:
                if (0 in valids):
                    valids.remove(0)
            case 3:
                if (1 in valids):
                    valids.remove(1)
        return valids

    def clear_ghost(self):
        color=(0,0,0)
        line_width=1
        x,y,w,h=self.col*cell_size-8, self.row*cell_size-8, 42,42
        pygame.draw.rect(screen, BLACK, (x,y,w,h))
        pygame.draw.line(screen, BLACK, (x,y),(x+cell_size,y), line_width)
        pygame.draw.line(screen, BLACK, (x+cell_size,y),(x+cell_size,y+cell_size), line_width)
        pygame.draw.line(screen, BLACK, (x,y+cell_size),(x+cell_size,y+cell_size), line_width)
        pygame.draw.line(screen, BLACK, (x,y),(x,y+cell_size), line_width)




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

class Pacman:
    def __init__(self):
        self.row=26
        self.col=14
        self.direction=3

    def get_position(self):
        return [self.row, self.col]
    
    def get_direction(self):
        return self.direction
    
    def display_pacman(self):
        color=(255,255,0)
        line_width=1
        x,y,w,h=self.col*cell_size, self.row*cell_size, cell_size,cell_size
        pygame.draw.rect(screen, color, (x,y,w,h))
        pygame.draw.line(screen, GRID_COLOR, (x,y),(x+cell_size,y), line_width)
        pygame.draw.line(screen, GRID_COLOR, (x+cell_size,y),(x+cell_size,y+cell_size), line_width)
        pygame.draw.line(screen, GRID_COLOR, (x,y+cell_size),(x+cell_size,y+cell_size), line_width)
        pygame.draw.line(screen, GRID_COLOR, (x,y),(x,y+cell_size), line_width)

    def clear_pacman(self):
        color=(0,0,0)
        line_width=1
        x,y,w,h=self.col*cell_size, self.row*cell_size, cell_size,cell_size
        pygame.draw.rect(screen, color, (x,y,w,h))
        pygame.draw.line(screen, GRID_COLOR, (x,y),(x+cell_size,y), line_width)
        pygame.draw.line(screen, GRID_COLOR, (x+cell_size,y),(x+cell_size,y+cell_size), line_width)
        pygame.draw.line(screen, GRID_COLOR, (x,y+cell_size),(x+cell_size,y+cell_size), line_width)
        pygame.draw.line(screen, GRID_COLOR, (x,y),(x,y+cell_size), line_width)

    def move_pacman(self, dir):
        match(dir):
            case 0: 
                #UP
                if self.row-1!=-1 and not grid[self.row-1][self.col].is_wall():
                    grid[self.row][self.col].set_pacman(b=False)
                    grid[self.row][self.col].draw_cell(screen)
                    grid[self.row-1][self.col].set_pacman(b=True)
                    grid[self.row-1][self.col].draw_cell(screen)
                    self.row=self.row-1
            case 1:
                #RIGHT
                if self.col+1==len(grid[0]) and self.row==17:
                    grid[self.row][self.col].set_pacman(b=False)
                    grid[self.row][self.col].draw_cell(screen)
                    grid[self.row][0].set_pacman(b=True)
                    grid[self.row][0].draw_cell(screen)
                    self.col=0  
                    return             

                if self.col+1!=len(grid[0]) and not grid[self.row][self.col+1].is_wall():
                    grid[self.row][self.col].set_pacman(b=False)
                    grid[self.row][self.col].draw_cell(screen)
                    grid[self.row][self.col+1].set_pacman(b=True)
                    grid[self.row][self.col+1].draw_cell(screen)
                    self.col=self.col+1
            case 2:
                #DOWN
                if self.row+1!=len(grid) and not grid[self.row+1][self.col].is_wall():
                    grid[self.row][self.col].set_pacman(b=False)
                    grid[self.row][self.col].draw_cell(screen)
                    grid[self.row+1][self.col].set_pacman(b=True)
                    grid[self.row+1][self.col].draw_cell(screen)
                    self.row=self.row+1
            case 3:
                #LEFT
                if self.col-1==-1 and self.row==17:
                    grid[self.row][self.col].set_pacman(b=False)
                    grid[self.row][self.col].draw_cell(screen)
                    grid[self.row][27].set_pacman(b=True)
                    grid[self.row][27].draw_cell(screen)
                    self.col=27     
                    return
                
                if self.col-1!=-1 and not grid[self.row][self.col-1].is_wall():
                    grid[self.row][self.col].set_pacman(b=False)
                    grid[self.row][self.col].draw_cell(screen)  
                    grid[self.row][self.col-1].set_pacman(b=True)
                    grid[self.row][self.col-1].draw_cell(screen)
                    self.col=self.col-1

class Blinky(Ghost):
    def __init__(self):
        super().__init__()
        self.row=17
        self.col=12
        self.start_moves=[0,1,0,0,3]

    def display_ghost(self, screen):
        # color=(255,0,0)
        # line_width=1
        # x,y,w,h=self.col*cell_size, self.row*cell_size, cell_size,cell_size
        # pygame.draw.rect(screen, color, (x,y,w,h))
        # pygame.drawdisplay_ghost.line(screen, GRID_COLOR, (x,y),(x+cell_size,y), line_width)
        # pygame.draw.line(screen, GRID_COLOR, (x+cell_size,y),(x+cell_size,y+cell_size), line_width)
        # pygame.draw.line(screen, GRID_COLOR, (x,y+cell_size),(x+cell_size,y+cell_size), line_width)
        # pygame.draw.line(screen, GRID_COLOR, (x,y),(x,y+cell_size), line_width)
        
        match(self.direction):
            case 0:
                img="Ghosts\Blinky_up.png"
            case 1:
                img="Ghosts\Blinky_right.png"
            case 2:
                img="Ghosts\Blinky_down.png"
            case 3:
                img="Ghosts\Blinky_left.png"                

        img = pygame.image.load(img).convert()
        screen.blit(img, (self.col*cell_size-8,self.row*cell_size-8))


    def start_pinky(self):
        global pinky
        

    def set_target(self):
        global pacman
        match(self.mode):
            case 0:
                #Scatter 0,25
                self.target=[0,25]
            case 1:
                #Chase
                #TODO: quando cambi da qualcosa a chase metti target nella posizione in cui e in quel momento
                if self.target==[self.row,self.col] or self.target==[None,None]:
                    self.target=pacman.get_position()
            case 2:
                #Frightened
                return

class Pinky(Ghost):
    def __init__(self):
        super().__init__()
        self.row=17
        self.col=13
        self.start_moves=[0,0,0,3]

    def display_ghost(self, screen):
        match(self.direction):
            case 0:
                img="Ghosts\Pinky_up.png"
            case 1:
                img="Ghosts\Pinky_right.png"
            case 2:
                img="Ghosts\Pinky_down.png"
            case 3:
                img="Ghosts\Pinky_left.png"                

        img = pygame.image.load(img).convert()
        screen.blit(img, (self.col*cell_size-8,self.row*cell_size-8))

    def set_target(self):
        global pacman
        match(self.mode):
            case 0:
                #Scatter 0,25
                self.target=[0,3]
            case 1:
                #Chase
                if self.target==[self.row,self.col] or self.target==[None,None]:
                    pacman_pos=pacman.get_position()
                    pacman_dir=pacman.get_direction()
                    match(pacman_dir):
                        case 0:
                            self.target=[pacman_pos[0]-4,pacman_pos[1]]
                            while grid[self.target[0]][self.target[1]].is_wall():
                                self.target[0]+=1
                        case 1:
                            self.target=[pacman_pos[0],pacman_pos[1]+4]
                            while grid[self.target[0]][self.target[1]].is_wall():
                                self.target[1]-=1
                        case 2:
                            self.target=[pacman_pos[0]+4, pacman_pos[1]]
                            while grid[self.target[0]][self.target[1]].is_wall():
                                self.target[0]-=1                            
                        case 3:
                            self.target=[pacman_pos[0], pacman_pos[1]-4]
                            while grid[self.target[0]][self.target[1]].is_wall():
                                self.target[1]+=1

            case 2:
                #Frightened
                return

class Inky(Ghost):
    def __init__(self):
        super().__init__()
        self.row=17
        self.col=14
        self.start_moves=[0,0,0,3]

    def display_ghost(self, screen):
        match(self.direction):
            case 0:
                img="Ghosts\Inky_up.png"
            case 1:
                img="Ghosts\Inky_right.png"
            case 2:
                img="Ghosts\Inky_down.png"
            case 3:
                img="Ghosts\Inky_left.png"                

        img = pygame.image.load(img).convert()
        screen.blit(img, (self.col*cell_size-8,self.row*cell_size-8))


    def start_pinky(self):
        global pinky
        

    def set_target(self):
        global pacman
        match(self.mode):
            case 0:
                #Scatter 0,25
                self.target=[35,27]
            case 1:
                #Chase
                #TODO: fai chase
                if self.target==[self.row,self.col] or self.target==[None,None]:
                    self.target=pacman.get_position()
            case 2:
                #Frightened
                return








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
    # images=[
    #     "GamesImages\\bottom_to_right.png",
    #     "GamesImages\\bottom_to_left.png",
    #     "GamesImages\\top_to_right.png",
    #     "GamesImages\\top_to_left.png",
    #     "GamesImages\\vertical_right.png",
    #     "GamesImages\\vertical_left.png",
    #     "GamesImages\\horizontal_top.png",
    #     "GamesImages\\horizontal_bottom.png",
    #     "GamesImages\\vertical_right2.png",
    #     "GamesImages\\vertical_left2.png",
    #     "GamesImages\\horizontal_top2.png",
    #     "GamesImages\\horizontal_bottom2.png",
    #     "GamesImages\\bottom_to_right2.png",
    #     "GamesImages\\bottom_to_left2.png",
    # ]
    images=[
        "pixil-frame-0.png",
    ]
    for i in range (len(images)):
        imp = pygame.image.load(images[i]).convert()
        screen.blit(imp, (i*300,0))

def draw_ghost():
    ghosts=[
        "Ghosts\Blinky_up.png",
        "Ghosts\Blinky_down.png",
        "Ghosts\Blinky_right.png",
        "Ghosts\Blinky_left.png",

        "Ghosts\Pinky_up.png",
        "Ghosts\Pinky_down.png",
        "Ghosts\Pinky_right.png",
        "Ghosts\Pinky_left.png",

        "Ghosts\Inky_up.png",
        "Ghosts\Inky_down.png",
        "Ghosts\Inky_right.png",
        "Ghosts\Inky_left.png",

        "Ghosts\Clyde_up.png",
        "Ghosts\Clyde_down.png",
        "Ghosts\Clyde_right.png",
        "Ghosts\Clyde_left.png",        
    ]
    count=0
    count1=16
    for i in range (0,len(ghosts)):
        count+=2
        if (i==8):
            count1+=2
            count=2
        imp = pygame.image.load(ghosts[i]).convert()
        screen.blit(imp, (count*cell_size-10,count1*cell_size-10))

            

        
        


pygame.init()
clock=pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), flags, vsync=1)
pygame.display.set_caption('Tetris♥')
font = pygame.font.SysFont('arial', 20)



grid=[]
pacman = Pacman()
blinky = Blinky()
pinky = Pinky()
inky = Inky()

init_grid()
draw_background()
draw_grid(cell_size)
draw_cells()
write_number()
display_img()
blinky.display_ghost(screen=screen)
pinky.display_ghost(screen=screen)
inky.display_ghost(screen=screen)

GHOSTEVENT = pygame.USEREVENT+1
pygame.time.set_timer(event=GHOSTEVENT, millis=500)

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
                    pacman.move_pacman(i)
                    break
        if (event.type == GHOSTEVENT):
            pinky.move_ghost(grid, screen)
            blinky.move_ghost(grid, screen)
            inky.move_ghost(grid, screen)

    pygame.display.flip()
    clock.tick(30)
    

pygame.quit()
