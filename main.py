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
#TODO: controlla durata di Frightened

class Ghost:
    def __init__(self):
        #0 -> Scatter, 1 -> Chase, 2 -> Frightened
        self.mode=0
        #0 -> Up, 1 -> Right, 2 -> Down, 3 -> Left
        self.direction=0
        self.starting=0
        self.target=[None,None]
        self.special_intersection= [ [14, 12], [14, 15], [26, 12], [26, 15] ]

    def get_position(self):
        return [self.row,self.col]

    def set_starting(self, n):
        self.starting=n

    def set_mode(self, n):
        self.mode=n

    def set_position(self, row, col):
        self.row=row
        self.col=col

    def move_ghost(self, grid, screen):
        if self.starting<=len(self.start_moves):
            self.start_procedure()
            return

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


        if self.mode==2:
            valids=self.get_valid_dir(grid)
            return random.choice(valids)

        
        # if grid[self.row][self.col].is_intersection() or self.starting==4:
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
        if [self.row,self.col] in self.special_intersection:
            if 0 in valids:
                valids.remove(0)
        return valids

    def clear_ghost(self):
        color=(0,0,0)
        line_width=1
        x,y,w,h=self.col*cell_size-(8*resize_factor), self.row*cell_size-(8*resize_factor), 42*resize_factor,42*resize_factor
        pygame.draw.rect(screen, BLACK, (x,y,w,h))
        grid[self.row][self.col].draw_dot(screen)
        # pygame.draw.line(screen, BLACK, (x,y),(x+cell_size,y), line_width)
        # pygame.draw.line(screen, BLACK, (x+cell_size,y),(x+cell_size,y+cell_size), line_width)
        # pygame.draw.line(screen, BLACK, (x,y+cell_size),(x+cell_size,y+cell_size), line_width)
        # pygame.draw.line(screen, BLACK, (x,y),(x,y+cell_size), line_width)

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
    
    def draw_dot(self, scren):
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

class Pacman:
    def __init__(self):
        self.row=26
        self.col=14
        self.direction=3

    def get_position(self):
        return [self.row, self.col]
    
    def get_direction(self):
        return self.direction
    
    def set_position(self, row, col):
        self.row=row
        self.col=col
    
    def display_pacman(self, screen):
        match(self.direction):
            case 0:
                img="Pacman\Pacman_up.png"                
            case 1:
                img="Pacman\Pacman_right.png"                
            case 2:
                img="Pacman\Pacman_down.png"                
            case 3:
                img="Pacman\Pacman_left.png"                

        img = pygame.image.load(img).convert()
        img = pygame.transform.smoothscale(img,(img.get_width()*resize_factor,img.get_height()*resize_factor))
        screen.blit(img, (self.col*cell_size-(8*resize_factor),self.row*cell_size-(8*resize_factor)))

    def clear_pacman(self, screen):
        color=(0,0,0)
        line_width=1
        x,y,w,h=self.col*cell_size-(8*resize_factor), self.row*cell_size-(8*resize_factor), 42*resize_factor,42*resize_factor
        pygame.draw.rect(screen, color, (x,y,w,h))

    def move_pacman(self, dir):
        match(dir):
            case 0: 
                #UP
                if self.row-1!=-1 and not grid[self.row-1][self.col].is_wall():
                    self.clear_pacman(screen)
                    self.row=self.row-1
                    self.direction=0
                    self.display_pacman(screen)
                    self.check_dot()
                    
                    
            case 1:
                #RIGHT
                if self.col+1==len(grid[0]) and self.row==17:
                    self.clear_pacman(screen)
                    self.col=0
                    self.direction=1
                    self.display_pacman(screen)
                    self.check_dot()
                      
                    return             

                if self.col+1!=len(grid[0]) and not grid[self.row][self.col+1].is_wall():
                    self.clear_pacman(screen)
                    self.col=self.col+1
                    self.direction=1
                    self.display_pacman(screen)
                    self.check_dot()
                    
            case 2:
                #DOWN
                if self.row+1!=len(grid) and not grid[self.row+1][self.col].is_wall():
                    self.clear_pacman(screen)
                    self.row=self.row+1
                    self.direction=2
                    self.display_pacman(screen)
                    self.check_dot()
            case 3:
                #LEFT
                if self.col-1==-1 and self.row==17:
                    self.clear_pacman(screen)
                    self.col=27   
                    self.direction=3  
                    self.display_pacman(screen)
                    self.check_dot()
                    return
                
                if self.col-1!=-1 and not grid[self.row][self.col-1].is_wall():
                    self.clear_pacman(screen)
                    self.col=self.col-1
                    self.direction=3
                    self.display_pacman(screen)
                    self.check_dot()

    def check_dot(self):
        global dots_eaten
        global score
        global blinky
        global pinky
        global inky
        global clyde
        global time_passed

        match(grid[self.row][self.col].get_dot()):
            case 0:
                return
            case 1:
                grid[self.row][self.col].set_dot(0)
                dots_eaten+=1
                score+=10
            case 2:
                if time_passed[0] is not None:
                    time_passed[0]=pygame.time.get_ticks()-time_passed[0]
                else:
                    time_passed[1]=pygame.time.get_ticks()-time_passed[1]

                grid[self.row][self.col].set_dot(0)
                score+=50
                time_passed[2]=pygame.time.get_ticks()
                blinky.set_mode(2)
                pinky.set_mode(2)
                inky.set_mode(2)
                clyde.set_mode(2)

class Blinky(Ghost):
    def __init__(self):
        super().__init__()
        self.direction=3
        self.row=14
        self.col=13
        self.start_moves=[3]
    
    def set_starting_pos(self):
        self.row=14
        self.col=13

    def display_ghost(self, screen):
        # color=(255,0,0)
        # line_width=1
        # x,y,w,h=self.col*cell_size, self.row*cell_size, cell_size,cell_size
        # pygame.draw.rect(screen, color, (x,y,w,h))
        # pygame.drawdisplay_ghost.line(screen, GRID_COLOR, (x,y),(x+cell_size,y), line_width)
        # pygame.draw.line(screen, GRID_COLOR, (x+cell_size,y),(x+cell_size,y+cell_size), line_width)
        # pygame.draw.line(screen, GRID_COLOR, (x,y+cell_size),(x+cell_size,y+cell_size), line_width)
        # pygame.draw.line(screen, GRID_COLOR, (x,y),(x,y+cell_size), line_width)
        
        if (self.mode==2):
            img="Ghosts\Frightened.png"
        else:
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
        img = pygame.transform.smoothscale(img,(img.get_width()*resize_factor,img.get_height()*resize_factor))
        screen.blit(img, (self.col*cell_size-(8*resize_factor),self.row*cell_size-(8*resize_factor)))


    def start_pinky(self):
        global pinky
        pinky.set_starting(0)
        

    def set_target(self):
        global pacman
        match(self.mode):
            case 0:
                #Scatter 0,25
                self.target=[0,25]
            case 1:
                #Chase
                #TODO: quando cambi da qualcosa a chase metti target nella posizione in cui e in quel momento
                self.target=pacman.get_position()
            case 2:
                #Frightened
                return

    def start_procedure(self):
        if self.starting==len(self.start_moves):
            self.start_pinky()
            self.starting+=1
            dir = self.chose_direction(grid)

        else:
            dir=self.start_moves[0]
            self.starting+=1
        
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

class Pinky(Ghost):
    def __init__(self):
        super().__init__()
        self.row=17
        self.col=14
        self.starting=-1
        self.direction=2
        self.start_moves=[0,0,0,3]

    def set_starting_pos(self):
        self.row=17
        self.col=14


    def display_ghost(self, screen):
        if (self.mode==2):
            img="Ghosts\Frightened.png"
        else:
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
        img = pygame.transform.smoothscale(img,(img.get_width()*resize_factor,img.get_height()*resize_factor))
        screen.blit(img, (self.col*cell_size-(8*resize_factor),self.row*cell_size-(8*resize_factor)))

    def set_target(self):
        global pacman
        match(self.mode):
            case 0:
                #Scatter 0,25
                self.target=[0,3]
            case 1:
                #Chase
                # if self.target==[self.row,self.col] or self.target==[None,None]:
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
       
    def start_procedure(self):
        if self.starting==-1:
            if (self.mode==2):
                    img="Ghosts\Frightened.png"
            else: 
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
            img = pygame.transform.smoothscale(img,(img.get_width()*resize_factor,img.get_height()*resize_factor))
            screen.blit(img, (self.col*cell_size-(20*resize_factor),self.row*cell_size-(8*resize_factor)))
            return

        if self.starting==len(self.start_moves):
            self.start_inky()
            self.starting+=1
            x,y,w,h=self.col*cell_size-(20*resize_factor), self.row*cell_size-(8*resize_factor), 42*resize_factor,42*resize_factor
            pygame.draw.rect(screen, BLACK, (x,y,w,h))
            self.move_ghost(grid, screen)
            return
        else:
            self.direction=self.start_moves[self.starting]
        x,y,w,h=self.col*cell_size-(20*resize_factor), self.row*cell_size-(8*resize_factor), 42*resize_factor,42*resize_factor
        pygame.draw.rect(screen, BLACK, (x,y,w,h))
        grid[self.row][self.col].draw_dot(screen)

        match(self.direction):
            case 0:
                if (self.mode==2):
                    img="Ghosts\Frightened.png"
                else: 
                    img="Ghosts\Pinky_up.png"
                self.row-=1
            case 1:
                if (self.mode==2):
                    img="Ghosts\Frightened.png"
                else: 
                    img="Ghosts\Pinky_right.png"
                self.col+=1
            case 2:
                if (self.mode==2):
                    img="Ghosts\Frightened.png"
                else: 
                    img="Ghosts\Pinky_down.png"
                self.row+=1
            case 3:
                if (self.mode==2):
                    img="Ghosts\Frightened.png"
                else: 
                    img="Ghosts\Pinky_left.png"   
                self.col-=1             

        img = pygame.image.load(img).convert()
        img = pygame.transform.smoothscale(img,(img.get_width()*resize_factor,img.get_height()*resize_factor))
        screen.blit(img, (self.col*cell_size-(20*resize_factor),self.row*cell_size-(8*resize_factor)))
        self.starting+=1

    def start_inky(self):
        global inky
        inky.set_starting(0)

class Inky(Ghost):
    def __init__(self):
        super().__init__()
        self.row=17
        self.col=12
        self.starting=-1
        self.direction=0
        self.start_moves=[1,1,0,0,0,3]

    def set_starting_pos(self):
        self.row=17
        self.col=12

    def display_ghost(self, screen):
        if (self.mode==2):
            img="Ghosts\Frightened.png"
        else:        
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
        img = pygame.transform.smoothscale(img,(img.get_width()*resize_factor,img.get_height()*resize_factor))
        screen.blit(img, (self.col*cell_size-(8*resize_factor),self.row*cell_size-(8*resize_factor)))

    def set_target(self):
        global pacman
        global blinky
        match(self.mode):
            case 0:
                #Scatter 0,25
                self.target=[35,27]
            case 1:
                #Chase
                pacman_pos=pacman.get_position()
                match(pacman.get_direction()):
                    case 0:
                        target=[pacman_pos[0]-2,pacman_pos[1]]
                    case 1:
                        target=[pacman_pos[0],pacman_pos[1]+2]
                    case 2:
                        target=[pacman_pos[0]+2,pacman_pos[1]]
                    case 3:
                        target=[pacman_pos[0],pacman_pos[1]-2]



                blinky_pos=blinky.get_position()
                self.target=[target[0]+(target[0]-blinky_pos[0]),target[1]+(target[1]-blinky_pos[1])]
            case 2:
                #Frightened
                return

    def start_procedure(self):
        if self.starting==-1:
            if (self.mode==2):
                img="Ghosts\Frightened.png"
            else:      
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
            img = pygame.transform.smoothscale(img,(img.get_width()*resize_factor,img.get_height()*resize_factor))
            screen.blit(img, (self.col*cell_size-(20*resize_factor),self.row*cell_size-(8*resize_factor)))
            return

        if self.starting==len(self.start_moves):
            self.starting+=1
            self.start_clyde()
            x,y,w,h=self.col*cell_size-(20*resize_factor), self.row*cell_size-(8*resize_factor), 42*resize_factor,42*resize_factor
            pygame.draw.rect(screen, BLACK, (x,y,w,h))
            self.move_ghost(grid, screen)
            return
        else:
            self.direction=self.start_moves[self.starting]
        x,y,w,h=self.col*cell_size-(20*resize_factor), self.row*cell_size-(8*resize_factor), 42*resize_factor,42*resize_factor
        pygame.draw.rect(screen, BLACK, (x,y,w,h))
        grid[self.row][self.col].draw_dot(screen)

        match(self.direction):
            case 0:
                if (self.mode==2):
                    img="Ghosts\Frightened.png"
                else:      
                    img="Ghosts\Inky_up.png"
                self.row-=1
            case 1:
                if (self.mode==2):
                    img="Ghosts\Frightened.png"
                else: 
                    img="Ghosts\Inky_right.png"
                self.col+=1
            case 2:
                if (self.mode==2):
                    img="Ghosts\Frightened.png"
                else: 
                    img="Ghosts\Inky_down.png"
                self.row+=1
            case 3:
                if (self.mode==2):
                    img="Ghosts\Frightened.png"
                else: 
                    img="Ghosts\Inky_left.png"   
                self.col-=1             

        img = pygame.image.load(img).convert()
        img = pygame.transform.smoothscale(img,(img.get_width()*resize_factor,img.get_height()*resize_factor))
        screen.blit(img, (self.col*cell_size-(20*resize_factor),self.row*cell_size-(8*resize_factor)))
        self.starting+=1

    def start_clyde(self):
        global clyde
        clyde.set_starting(0)

class Clyde(Ghost):
    def __init__(self):
        super().__init__()
        self.row=17
        self.col=16
        self.starting=-1
        self.direction=0
        self.start_moves=[3,3,0,0,0,3]

    def set_starting_pos(self):
        self.row=17
        self.col=16

    def display_ghost(self, screen):
        if (self.mode==2):
            img="Ghosts\Frightened.png"
        else:        
            match(self.direction):
                case 0:
                    img="Ghosts\Clyde_up.png"
                case 1:
                    img="Ghosts\Clyde_right.png"
                case 2:
                    img="Ghosts\Clyde_down.png"
                case 3:
                    img="Ghosts\Clyde_left.png"                

        img = pygame.image.load(img).convert()
        img = pygame.transform.smoothscale(img,(img.get_width()*resize_factor,img.get_height()*resize_factor))
        screen.blit(img, (self.col*cell_size-(8*resize_factor),self.row*cell_size-(8*resize_factor)))  

    def set_target(self):
        global pacman
        match(self.mode):
            case 0:
                #Scatter 0,25
                self.target=[35,0]
            case 1:
                #Chase
                pacman_pos=pacman.get_position()

                point_x= self.col
                point_y = self.row
                target_x=pacman_pos[1]
                target_y=pacman_pos[0]

                dis = math.sqrt(((target_x-point_x)**2)+((target_y-point_y)**2))
                if dis>8:
                    self.target=pacman_pos
                else:
                    self.target=[35,0]

            case 2:
                #Frightened
                return

    def start_procedure(self):
        if self.starting==-1:
            if (self.mode==2):
                img="Ghosts\Frightened.png"
            else:        
                match(self.direction):
                    case 0:
                        img="Ghosts\Clyde_up.png"
                    case 1:
                        img="Ghosts\Clyde_right.png"
                    case 2:
                        img="Ghosts\Clyde_down.png"
                    case 3:
                        img="Ghosts\Clyde_left.png"   
            img = pygame.image.load(img).convert()
            img = pygame.transform.smoothscale(img,(img.get_width()*resize_factor,img.get_height()*resize_factor))
            screen.blit(img, (self.col*cell_size-(20*resize_factor),self.row*cell_size-(8*resize_factor)))
            return

        if self.starting==len(self.start_moves):
            self.starting+=1
            x,y,w,h=self.col*cell_size-(20*resize_factor), self.row*cell_size-(8*resize_factor), 42*resize_factor,42*resize_factor
            pygame.draw.rect(screen, BLACK, (x,y,w,h))
            self.move_ghost(grid, screen)
            return
        else:
            self.direction=self.start_moves[self.starting]
        x,y,w,h=self.col*cell_size-(20*resize_factor), self.row*cell_size-(8*resize_factor), 42*resize_factor,42*resize_factor
        pygame.draw.rect(screen, BLACK, (x,y,w,h))
        grid[self.row][self.col].draw_dot(screen)

        match(self.direction):
            case 0:
                if (self.mode==2):
                    img="Ghosts\Frightened.png"
                else:        
                    img="Ghosts\Clyde_up.png"
                self.row-=1
            case 1:
                if (self.mode==2):
                    img="Ghosts\Frightened.png"
                else:    
                    img="Ghosts\Clyde_right.png"
                self.col+=1
            case 2:
                if (self.mode==2):
                    img="Ghosts\Frightened.png"
                else:    
                    img="Ghosts\Clyde_down.png"
                self.row+=1
            case 3:
                if (self.mode==2):
                    img="Ghosts\Frightened.png"
                else:    
                    img="Ghosts\Clyde_left.png"   
                self.col-=1             

        img = pygame.image.load(img).convert()
        img = pygame.transform.smoothscale(img,(img.get_width()*resize_factor,img.get_height()*resize_factor))
        screen.blit(img, (self.col*cell_size-(20*resize_factor),self.row*cell_size-(8*resize_factor)))
        self.starting+=1




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
    f = open("not_walls.txt", "r")
    walkable = ast.literal_eval(f.read())
    f.close()
    f = open("intersection.txt", "r")
    intersections = ast.literal_eval(f.read())
    f.close()
    f = open("dots.txt", "r")
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
                dot=1
            if [row,col] in intersections:
                intersection=True
            if [row,col] in dots:
                dot=2
            temp.append(Cell(row, col, wall, dot, intersection))
        grid.append(temp)
                
# def draw_cells():
#     global grid
#     for row in range (len(grid)):
#         for col in range (len(grid[0])):
#             grid[row][col].draw_cell(screen)

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
            cell.draw_dot(screen)

def ghost_mode_manager():
    #TODO: quando inizia firghtened metti in pausa dove era prima
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
    global blinky
    global pinky
    global inky
    global clyde
    global lives

    ghosts_pos=[blinky.get_position(), pinky.get_position(), inky.get_position(), clyde.get_position()]
    if pacman.get_position() in ghosts_pos:
        if time_passed[2] is not None:
            #TODO: testa che ci sono un bel po di problemi
            ghosts=[blinky,pinky,inky,clyde]
            ghosts[ghosts_pos.index(pacman.get_position())].set_starting_pos()
            ghosts[ghosts_pos.index(pacman.get_position())].set_starting(0)
        else:
            pacman.set_position(26,14)
            pacman.display_pacman(screen)
            lives-=1
            display_lives()

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
            grid[20][13].draw_dot(screen)
            grid[20][14].draw_dot(screen)

            fruit_time=None
    if (dots_eaten==7 and fruit_time is None) or (dots_eaten==14 and fruit_time is None):
        draw_fruit()
        grid[20][13].set_fruit(True)
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
    


pygame.init()
clock=pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), flags, vsync=1)
pygame.display.set_caption('Tetris♥')
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
pacman = Pacman()
blinky = Blinky()
pinky = Pinky()
inky = Inky()
clyde = Clyde()

init_grid()
draw_background()
write_number()
display_img()
draw_dots()
display_score()
display_lives()
display_bottom_fruit()
 
pacman.display_pacman(screen=screen)
blinky.display_ghost(screen=screen)
pinky.start_procedure()
inky.start_procedure()
clyde.start_procedure()

# grid[23][4].set_dot(1)
# grid[23][4].draw_dot(screen)
# inky.display_ghost(screen=screen)
# clyde.display_ghost(screen=screen)

# draw_grid(cell_size)

GHOSTEVENT = pygame.USEREVENT+1
TIMEEVENT = pygame.USEREVENT+1
pygame.time.set_timer(event=GHOSTEVENT, millis=500)
pygame.time.set_timer(event=TIMEEVENT, millis=1000)
time_passed[0]=pygame.time.get_ticks()

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
                    check_collision()
                    display_score()
                    fruit_manager()
                    break
        if (event.type == GHOSTEVENT):
            blinky.move_ghost(grid, screen)
            pinky.move_ghost(grid, screen)
            inky.move_ghost(grid, screen)
            clyde.move_ghost(grid, screen)
            check_collision()
            fruit_manager()
            
        if (event.type == TIMEEVENT):
            ghost_mode_manager()


    pygame.display.flip()
    clock.tick(30)
    

pygame.quit()
