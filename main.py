import pygame
import random
import time
import ast
import math
from settings import *
from characterClasses import *
from Spriets import *

#TODO: implementa livelli
#TODO:  cambia velocita dei fantasmi
#TODO: Allinizio pacman e un cerchio al centro



class Cell:
    def __init__(self, row: int, col: int, wall: bool, dot: int, intersection: bool) -> None:
        self.row=row
        self.col=col
        self.wall=wall
        self.intersection=intersection
        #0 -> no dot, 1 -> dot, 2 -> power pill
        self.dot=dot
        self.fruit=False
        #0 -> no ghost, 1 -> blinky, 2 -> pinky, 3 -> inky, 4 -> clyde
        self.ghost=0

    def is_wall(self):
        return self.wall
    
    def is_intersection(self):
        return self.intersection
    
    def set_dot(self, n):
        self.dot=n

    def set_fruit(self, b):
        self.fruit=b
    
    def set_ghost(self, n):
        self.ghost=n

    def get_ghost(self):
        return self.ghost

    def get_dot(self):
        return self.dot
    
    def get_wall(self):
        return self.wall
    
    def get_fruit(self):
        return self.fruit
    
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
                img = pygame.image.load("Fruits\\Power_pill.png").convert()
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








def draw_background():
    screen.fill(BACKGROUND_COLOR)

def draw_grid(cell_size):
    line_width=1
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
    global grid
    f = open("Cells\\not_walls.txt", "r")
    walkable = ast.literal_eval(f.read())
    f.close()
    f = open("Cells\\intersection.txt", "r")
    intersections = ast.literal_eval(f.read())
    f.close()
    f = open("Cells\\power_pill.txt", "r")
    power_pill = ast.literal_eval(f.read())
    f.close()
    f = open("Cells\\dots.txt", "r")
    dots = ast.literal_eval(f.read())
    f.close()



    for row in range (height_in_cell):
        temp=[]
        for col in range (width_in_cell):
            wall=True
            dot=0
            intersection=False
            if [row,col] in walkable:
                wall=False
            if [row,col] in intersections:
                intersection=True
            if [row,col] in dots:
                dot=1
            if [row,col] in power_pill:
                dot=2

            temp.append(Cell(row, col, wall, dot, intersection))
        grid.append(temp)

                
# def draw_cells():
#     global grid
#     for row in range (len(grid)):
#         for col in range (len(grid[0])):
#             grid[row][col].draw_cell(screen)

def display_background():
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

    img = pygame.image.load("Background.png").convert()
    img = pygame.transform.smoothscale(img,(SCREEN_WIDTH,SCREEN_HEIGHT))
    screen.blit(img, (0,0))
    img = pygame.image.load("High_score.png").convert()
    img = pygame.transform.smoothscale(img,(img.get_width()*resize_factor,img.get_height()*resize_factor))
    screen.blit(img, (9*cell_size,2))

def display_numbers():
    images=[
        "Numbers\\0.png",
        "Numbers\\1.png",
        "Numbers\\2.png",
        "Numbers\\3.png",
        "Numbers\\4.png",
        "Numbers\\5.png",
        "Numbers\\6.png",
        "Numbers\\7.png",
        "Numbers\\8.png",
        "Numbers\\9.png",
    ]

    for i in range(len(images)):
        img = pygame.image.load(images[i]).convert()
        img = pygame.transform.smoothscale(img,(img.get_width()*resize_factor,img.get_height()*resize_factor))
        screen.blit(img, (i*cell_size,2*cell_size))

def display_score():
    numbers=[
        "Numbers\\0.png",
        "Numbers\\1.png",
        "Numbers\\2.png",
        "Numbers\\3.png",
        "Numbers\\4.png",
        "Numbers\\5.png",
        "Numbers\\6.png",
        "Numbers\\7.png",
        "Numbers\\8.png",
        "Numbers\\9.png",
    ]

    s=str(score)
    for i in range(0, len(s)):
        img = pygame.image.load(numbers[int(s[len(s)-1-i])]).convert()
        img = pygame.transform.smoothscale(img,(img.get_width()*resize_factor,img.get_height()*resize_factor))
        screen.blit(img, ((6-i)*cell_size,1*cell_size))

def draw_ghost():
    ghosts=[
        "Ghosts\\Blinky_up.png",
        "Ghosts\\Blinky_down.png",
        "Ghosts\\Blinky_right.png",
        "Ghosts\\Blinky_left.png",

        "Ghosts\\Pinky_up.png",
        "Ghosts\\Pinky_down.png",
        "Ghosts\\Pinky_right.png",
        "Ghosts\\Pinky_left.png",

        "Ghosts\\Inky_up.png",
        "Ghosts\\Inky_down.png",
        "Ghosts\\Inky_right.png",
        "Ghosts\\Inky_left.png",

        "Ghosts\\Clyde_up.png",
        "Ghosts\\Clyde_down.png",
        "Ghosts\\Clyde_right.png",
        "Ghosts\\Clyde_left.png",        
    ]
    count=0
    count1=16
    for i in range (0,len(ghosts)):
        count+=2
        if (i==8):
            count1+=2
            count=2
        img = pygame.image.load(ghosts[i]).convert()
        img = pygame.transform.smoothscale(img,(img.get_width()*resize_factor,img.get_height()*resize_factor))
        screen.blit(img, (count*cell_size-10,count1*cell_size-10))

def draw_dots():
    for row in grid:
        for cell in row:
            cell.draw_dot(screen, level)

def ghost_mode_manager():
    global time_passed
    if time_passed[2] is not None and pygame.time.get_ticks()-time_passed[2]>=6000:
        blinky.set_mode(1)
        pinky.set_mode(1)
        inky.set_mode(1)
        clyde.set_mode(1)
        time_passed[2]=None
        if time_passed[0] is not None:
            time_passed[0]=pygame.time.get_ticks()-time_passed[0]
        else:
            time_passed[1]=pygame.time.get_ticks()-time_passed[1]

    if len(mode_length)!=0:
        if time_passed[0] is not None and pygame.time.get_ticks()-time_passed[0]>=mode_length[0]*1000:
            blinky.set_mode(1)
            pinky.set_mode(1)
            inky.set_mode(1)
            clyde.set_mode(1)
            time_passed[0]=None
            time_passed[1]=pygame.time.get_ticks()
            mode_length.pop(0)

        elif time_passed[1] is not None and pygame.time.get_ticks()-time_passed[1]>=mode_length[0]*1000:
            blinky.set_mode(0)
            pinky.set_mode(0)
            inky.set_mode(0)
            clyde.set_mode(0)
            time_passed[1]=None
            time_passed[0]=pygame.time.get_ticks()
            mode_length.pop(0)

def check_collision():
    global pacman 
    global game_over
    global blinky
    global pinky
    global inky
    global clyde
    global lives
    global game_over
    global gameOverSprite

    ghosts_pos=[blinky.get_position(), pinky.get_position(), inky.get_position(), clyde.get_position()]
    if pacman.get_position() in ghosts_pos:
        if time_passed[2] is not None:
            #TODO: testa che ci sono un bel po di problemi
            ghosts=[blinky,pinky,inky,clyde]
            ghosts[ghosts_pos.index(pacman.get_position())].set_starting_pos()
            ghosts[ghosts_pos.index(pacman.get_position())].set_starting(0)
        else:
            pacman.set_position(26,14)
            lives-=1
            display_lives()
            if lives==0:
                game_over=True
                gameOverSprite.set_game_over(True)
                blinkySprite.set_show(False)
                pinkySprite.set_show(False)
                inkySprite.set_show(False)
                clydeSprite.set_show(False)
                pacmanSprite.set_show(False)
                if grid[20][13].get_fruit():
                    grid[20][13].draw_dot(screen, level)

def display_lives():
    count=0
    pygame.draw.rect(screen,BLACK,(0,34*cell_size+(8*resize_factor),250*resize_factor,50*resize_factor))
    for i in range(0, lives):
        img = pygame.image.load("Pacman\\Pacman_left.png").convert()
        img = pygame.transform.smoothscale(img,(img.get_width()*(resize_factor-0.10),img.get_height()*(resize_factor-0.10)))
        screen.blit(img, ((8-count)*cell_size,34*cell_size+(8*resize_factor)))
        count+=2

def display_bottom_fruit():
    #TODO:The fruit appears after 70 dots are eaten and again after 170 
    # dots are eaten unless the first fruit is still there. They will disappear 
    # if they are not eaten after 9-10 seconds.


    #13, 20
    
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
    count=0
    for i in range (0, level):
        img = pygame.image.load(fruits[i]).convert()
        img = pygame.transform.smoothscale(img,(img.get_width()*resize_factor,img.get_height()*resize_factor))
        screen.blit(img, ((25-count)*cell_size,34*cell_size+(8*resize_factor)))
        count+=2
    
def fruit_manager():
    global fruit_time
    if fruit_time is not None:
        if pygame.time.get_ticks()-fruit_time>=9000:
            grid[20][13].set_fruit(False)
            pygame.draw.rect(screen, BLACK, (13*cell_size+(4*resize_factor),20*cell_size-(8*resize_factor),40*resize_factor,40*resize_factor))
            grid[20][13].draw_dot(screen, level)

            fruit_time=None
    if (dots_eaten==70 and fruit_time is None) or (dots_eaten==140 and fruit_time is None):
        
        grid[20][13].set_fruit(True)
        grid[20][13].draw_dot(screen, level)
        fruit_time=pygame.time.get_ticks()

def draw_fruit():
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

def check_dots_eaten():
    global pacman
    global dots_eaten
    global score
    global level
    global blinky
    global pinky
    global inky
    global clyde
    global animation
    pacman_pos=pacman.get_position()
    match (grid[pacman_pos[0]][pacman_pos[1]].get_dot()):
        case 0:
            return
        case 1:
            score+=10
            dots_eaten+=1
            grid[pacman_pos[0]][pacman_pos[1]].set_dot(0)
        case 2:
            grid[pacman_pos[0]][pacman_pos[1]].set_dot(0)
            if time_passed[0] is not None:
                time_passed[0]=pygame.time.get_ticks()-time_passed[0]
            else:
                time_passed[1]=pygame.time.get_ticks()-time_passed[1]

            score+=50
            time_passed[2]=pygame.time.get_ticks()
            blinky.set_mode(2)
            pinky.set_mode(2)
            inky.set_mode(2)
            clyde.set_mode(2)
    if (dots_eaten>=30 and level==1) or level>1:
        inky.dot_limit_passed()
    elif (dots_eaten>=60 and level==1) or (dots_eaten>=50 and level==2) or level>2:
        clyde.dot_limit_passed()
    if dots_eaten==240:
        animation=0

def display_game_over():
    img = pygame.image.load("Background\\Game_over.png").convert()
    img = pygame.transform.smoothscale(img,(img.get_width()*resize_factor,img.get_height()*resize_factor))
    screen.blit(img, (9*cell_size,20*cell_size))


def level_cleared():
    global blinky
    global pinky
    global inky
    global clyde
    global level
    global ready
    global readySprite
    #TODO: animation
    level+=1
    pacman.set_starting_pos()
    blinky.set_starting_pos()
    pinky.set_starting_pos()
    inky.set_starting_pos()
    clyde.set_starting_pos()
    ready=True
    readySprite.set_ready(True)
    reset_grid()

def reset_grid():
    global grid
    f = open("dots.txt", "r")
    dots = ast.literal_eval(f.read())
    f.close()
    f = open("power_pill.txt", "r")
    power_pill = ast.literal_eval(f.read())
    f.close()
    for pos in dots:
        grid[pos[0]][pos[1]].set_dot(1)
    for pos in power_pill:
        grid[pos[0]][pos[1]].set_dot(2)


pygame.init()
clock=pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), flags, vsync=1)
pygame.display.set_caption('Pacman♥')
font = pygame.font.SysFont('arial', 20)



grid=[]
dots_eaten=0
score=0
level=1
mode_length=[7,20,7,20,5,20,5]
#pos: 0 -> Scatter, 1 -> Chase, 2 -> Frightened
time_passed=[None,None,None]
lives=4
fruit_time=None
animation=-1
game_over=False
ready=True
pacman = Pacman()
blinky = Blinky(pacman)
pinky = Pinky(pacman)
inky = Inky(pacman, blinky)
clyde = Clyde(pacman)

init_grid()
# draw_background()
# write_number()
# display_background()
# draw_dots()
# display_score()
# display_lives()
# display_bottom_fruit()
# display_game_over()
 
# pacman.display_pacman(screen=screen)
# blinky.display_ghost(screen=screen)
# pinky.start_procedure(grid, screen, level)
# inky.start_procedure(grid, screen, level)
# clyde.start_procedure(grid, screen, level)


background = BackgroundSprite()
high_score = HighScoreSprite()
readySprite = ReadySprite()
gameOverSprite = GameOverSprite()
gameOverSprite.set_game_over(False)
pacmanSprite = PacmanSprite(pacman)
blinkySprite = BlinkySprite(blinky)
pinkySprite = PinkySprite(pinky)
inkySprite = InkySprite(inky)
clydeSprite = ClydeSprite(clyde)
game_group = pygame.sprite.Group()
game_group.add(background)
game_group.add(high_score)
for row in range (len(grid)):
    for col in range (len(grid[0])):
        if not grid[row][col].get_wall():
            cellSprite = CellSprite(grid[row][col], row, col)
            game_group.add(cellSprite)
game_group.add(readySprite)
game_group.add(gameOverSprite)
game_group.add(pacmanSprite)
game_group.add(blinkySprite)
game_group.add(pinkySprite)
game_group.add(inkySprite)
game_group.add(clydeSprite)


level_cleared_animation = pygame.sprite.Group()
animationSprite = AnimationSprite()
level_cleared_animation.add(animationSprite)





GHOSTEVENT = pygame.USEREVENT+1
TIMEEVENT = pygame.USEREVENT+2
PACMANEVENT = pygame.USEREVENT+3
AnimationEvent = pygame.USEREVENT+4

pygame.time.set_timer(event=GHOSTEVENT, millis=500)
pygame.time.set_timer(event=TIMEEVENT, millis=1000)
# pygame.time.set_timer(event=PACMANEVENT, millis=500)
pygame.time.set_timer(event=AnimationEvent, millis=200)
time_passed[0]=pygame.time.get_ticks()

run  = True
while run:

    for event in pygame.event.get():
        if (event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE)):
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y=pygame.mouse.get_pos()
            print(y//cell_size, x//cell_size)             
        if (event.type == pygame.KEYDOWN and not game_over):
            for i in range(len(INPUTS)):
                if (event.key==INPUTS[i]):
                    if ready:
                        ready = False
                        readySprite.set_ready(False)


                    pacman.move_pacman(i, grid, screen)
                    check_collision()
                    display_score()
                    fruit_manager()
                    check_dots_eaten()
                    break
        if (event.type == GHOSTEVENT and not game_over and not ready):
            blinky.move_ghost(grid, screen, level)
            pinky.move_ghost(grid, screen, level)
            inky.move_ghost(grid, screen, level)
            clyde.move_ghost(grid, screen, level)
            check_collision()
            fruit_manager()
            
        if (event.type == TIMEEVENT and not game_over and not ready):
            ghost_mode_manager()

        if (event.type == PACMANEVENT and not game_over and not ready):
            pacman.move_pacman(pacman.get_direction(), grid, screen)
            check_collision()
            display_score()
            fruit_manager()
            check_dots_eaten()
        
        if (event.type == AnimationEvent and animation!=-1):
            animation+=1
            if animation==9:
                animation=-1
                level_cleared()
        


    if animation==-1:
        draw_background()
        game_group.update()
        game_group.draw(screen)
        display_bottom_fruit()
        display_score()
        display_lives()
    else:
        draw_background()
        level_cleared_animation.update(animation)
        level_cleared_animation.draw(screen)
    #draw_grid(cell_size)

    pygame.display.flip()
    clock.tick(30)
    

pygame.quit()
