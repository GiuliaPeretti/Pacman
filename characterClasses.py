import pygame
import random
import math
from settings import *

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

    def move_pacman(self, dir, grid, screen):
        match(dir):
            case 0: 
                #UP
                if self.row-1!=-1 and not grid[self.row-1][self.col].is_wall():
                    self.clear_pacman(screen)
                    self.row=self.row-1
                    self.direction=0
                    self.display_pacman(screen)
                    
                    
            case 1:
                #RIGHT
                if self.col+1==len(grid[0]) and self.row==17:
                    self.clear_pacman(screen)
                    self.col=0
                    self.direction=1
                    self.display_pacman(screen)
                      
                    return             

                if self.col+1!=len(grid[0]) and not grid[self.row][self.col+1].is_wall():
                    self.clear_pacman(screen)
                    self.col=self.col+1
                    self.direction=1
                    self.display_pacman(screen)
                    
            case 2:
                #DOWN
                if self.row+1!=len(grid) and not grid[self.row+1][self.col].is_wall():
                    self.clear_pacman(screen)
                    self.row=self.row+1
                    self.direction=2
                    self.display_pacman(screen)
            case 3:
                #LEFT
                if self.col-1==-1 and self.row==17:
                    self.clear_pacman(screen)
                    self.col=27   
                    self.direction=3  
                    self.display_pacman(screen)
                    return
                
                if self.col-1!=-1 and not grid[self.row][self.col-1].is_wall():
                    self.clear_pacman(screen)
                    self.col=self.col-1
                    self.direction=3
                    self.display_pacman(screen)







class Ghost:
    def __init__(self):
        #0 -> Scatter, 1 -> Chase, 2 -> Frightened
        self.mode=0
        #0 -> Up, 1 -> Right, 2 -> Down, 3 -> Left
        self.direction=0
        self.starting=0
        self.target=[None,None]
        self.special_intersection= [ [14, 12], [14, 15], [26, 12], [26, 15] ]

    def get_mode(self):
        return self.mode

    def get_position(self):
        return [self.row, self.col]

    def set_starting(self, n):
        self.starting=n

    def set_mode(self, n):
        self.mode=n

    def set_position(self, row, col):
        self.row=row
        self.col=col

    def move_ghost(self, grid, screen, level):
        if self.starting<len(self.start_moves):
            self.start_procedure(grid, screen, level)
            return

        dir = self.chose_direction(grid)
        self.direction=dir
        match(dir):
            case 0: 
                #UP
                # if not grid[self.row-1][self.col].is_wall():
                self.clear_ghost(screen, grid, level)
                self.row=self.row-1
                self.display_ghost(screen)
                    
            case 1:
                #RIGHT
                # if not grid[self.row][self.col+1].is_wall():
                self.clear_ghost(screen, grid, level)
                self.col=self.col+1
                self.display_ghost(screen)
            case 2:
                #DOWN
                # if not grid[self.row+1][self.col].is_wall():
                self.clear_ghost(screen, grid, level)
                self.row=self.row+1
                self.display_ghost(screen)
            case 3:
                #LEFT
                # if not grid[self.row][self.col-1].is_wall():
                self.clear_ghost(screen, grid, level)
                self.col=self.col-1
                self.display_ghost(screen)
        grid[self.row][self.col].set_ghost(self.ghost_id)

    def chose_direction(self, grid):


        if self.mode==2:
            valids=self.get_valid_dir(grid)
            return random.choice(valids)

        
        # if grid[self.row][self.col].is_intersection() or self.starting==4:
        self.set_target(grid)

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

    def clear_ghost(self, screen, grid, level):
        color=(0,0,0)
        line_width=1
        if (self.starting<len(self.start_moves)):
            x,y,w,h=self.col*cell_size-(20*resize_factor), self.row*cell_size-(8*resize_factor), 42*resize_factor,42*resize_factor
        else:
            x,y,w,h=self.col*cell_size-(8*resize_factor), self.row*cell_size-(8*resize_factor), 42*resize_factor,42*resize_factor
        pygame.draw.rect(screen, BLACK, (x,y,w,h))
        grid[self.row][self.col].draw_dot(screen, level)
        grid[self.row][self.col].set_ghost(0)
        # pygame.draw.line(screen, BLACK, (x,y),(x+cell_size,y), line_width)
        # pygame.draw.line(screen, BLACK, (x+cell_size,y),(x+cell_size,y+cell_size), line_width)
        # pygame.draw.line(screen, BLACK, (x,y+cell_size),(x+cell_size,y+cell_size), line_width)
        # pygame.draw.line(screen, BLACK, (x,y),(x,y+cell_size), line_width)




    

class Blinky(Ghost):
    def __init__(self, pacman):
        super().__init__()
        self.direction=3
        self.row=14
        self.col=13
        self.start_moves=[3]
        self.pacman=pacman
        self.ghost_id=1
    
    def set_starting_pos(self):
        self.starting=0
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



        

    def set_target(self, grid):
        match(self.mode):
            case 0:
                #Scatter 0,25
                self.target=[0,25]
            case 1:
                #Chase
                #TODO: quando cambi da qualcosa a chase metti target nella posizione in cui e in quel momento
                self.target=self.pacman.get_position()
            case 2:
                #Frightened
                return

    def start_procedure(self, grid, screen, level):

        dir=self.start_moves[0]
        self.starting+=1
        
        self.direction=dir
        match(dir):
            case 0: 
                #UP
                # if not grid[self.row-1][self.col].is_wall():
                self.clear_ghost(screen, grid, level)
                self.row=self.row-1
                self.display_ghost(screen)
                    
            case 1:
                #RIGHT
                # if not grid[self.row][self.col+1].is_wall():
                self.clear_ghost(screen, grid, level)
                self.col=self.col+1
                self.display_ghost(screen)
            case 2:
                #DOWN
                # if not grid[self.row+1][self.col].is_wall():
                self.clear_ghost(screen, grid, level)
                self.row=self.row+1
                self.display_ghost(screen)
            case 3:
                #LEFT
                # if not grid[self.row][self.col-1].is_wall():
                self.clear_ghost(screen, grid, level)
                self.col=self.col-1
                self.display_ghost(screen)
        grid[self.row][self.col].set_ghost(self.ghost_id)

class Pinky(Ghost):
    def __init__(self, pacman):
        super().__init__()
        self.row=17
        self.col=14
        self.starting=-1
        self.direction=2
        self.start_moves=[0,0,0,3]
        self.pacman=pacman
        self.ghost_id=2

    def set_starting_pos(self):
        self.starting=0
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

    def set_target(self, grid):
        global pacman
        match(self.mode):
            case 0:
                #Scatter 0,25
                self.target=[0,3]
            case 1:
                #Chase
                # if self.target==[self.row,self.col] or self.target==[None,None]:
                pacman_pos=self.pacman.get_position()
                pacman_dir=self.pacman.get_direction()
                match(pacman_dir):
                    case 0:
                        self.target=[pacman_pos[0]-4,pacman_pos[1]]

                    case 1:
                        self.target=[pacman_pos[0],pacman_pos[1]+4]

                    case 2:
                        self.target=[pacman_pos[0]+4, pacman_pos[1]]
                    case 3:
                        self.target=[pacman_pos[0], pacman_pos[1]-4]


            case 2:
                #Frightened
                return
       
    def start_procedure(self, grid, screen, level):
        if self.starting==-1:
            if grid[14][13].get_ghost()!=1:
                self.starting=0
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
            grid[self.row][self.col].set_ghost(self.ghost_id)
            return


        self.direction=self.start_moves[self.starting]
        x,y,w,h=self.col*cell_size-(20*resize_factor), self.row*cell_size-(8*resize_factor), 42*resize_factor,42*resize_factor
        pygame.draw.rect(screen, BLACK, (x,y,w,h))
        grid[self.row][self.col].set_ghost(0)
        grid[self.row][self.col].draw_dot(screen, level)

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
        grid[self.row][self.col].set_ghost(self.ghost_id)
        self.starting+=1


class Inky(Ghost):
    def __init__(self,pacman,blinky):
        super().__init__()
        self.row=17
        self.col=12
        self.starting=-2
        self.direction=0
        self.start_moves=[1,1,0,0,0,3]
        self.pacman=pacman
        self.ghost_id=3
        self.blinky=blinky

    def set_starting_pos(self):
        self.starting=0
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

    def set_target(self, grid):
        match(self.mode):
            case 0:
                #Scatter 0,25
                self.target=[35,27]
            case 1:
                #Chase
                pacman_pos=self.pacman.get_position()
                match(self.pacman.get_direction()):
                    case 0:
                        target=[pacman_pos[0]-2,pacman_pos[1]]
                    case 1:
                        target=[pacman_pos[0],pacman_pos[1]+2]
                    case 2:
                        target=[pacman_pos[0]+2,pacman_pos[1]]
                    case 3:
                        target=[pacman_pos[0],pacman_pos[1]-2]



                blinky_pos=self.blinky.get_position()
                self.target=[target[0]+(target[0]-blinky_pos[0]),target[1]+(target[1]-blinky_pos[1])]
            case 2:
                #Frightened
                return

    def start_procedure(self, grid, screen,level):
        if level>1 and self.starting==-2:
            self.starting=-1
        if self.starting<=-1:
            if self.starting==-1:
                pink_starts=[[17,14],[16,14],[15,14],[14,14],[14,13]]
                check=False
                for p in pink_starts:
                    if grid[p[0]][p[1]].get_ghost()==2:
                        check=True
                if not check:
                    self.starting=0
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
            grid[self.row][self.col].set_ghost(self.ghost_id)
            return


        self.direction=self.start_moves[self.starting]
        x,y,w,h=self.col*cell_size-(20*resize_factor), self.row*cell_size-(8*resize_factor), 42*resize_factor,42*resize_factor
        pygame.draw.rect(screen, BLACK, (x,y,w,h))
        grid[self.row][self.col].set_ghost(0)
        grid[self.row][self.col].draw_dot(screen, level)

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
        grid[self.row][self.col].set_ghost(self.ghost_id)
        self.starting+=1

    def dot_limit_passed(self):
        if self.starting==-2:
            self.starting=-1


class Clyde(Ghost):
    def __init__(self, pacman):
        super().__init__()
        self.row=17
        self.col=16
        self.starting=-2
        self.direction=0
        self.start_moves=[3,3,0,0,0,3]
        self.pacman=pacman
        self.ghost_id=4

    def set_starting_pos(self):
        self.starting=0
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

    def set_target(self, grid):
        global pacman
        match(self.mode):
            case 0:
                #Scatter 0,25
                self.target=[35,0]
            case 1:
                #Chase
                pacman_pos=self.pacman.get_position()

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

    def start_procedure(self, grid, screen, level):

        if level>2 and self.starting==-2:
            self.starting=-1
        if self.starting<=-1:
            if self.starting==-1:
                [1,1,0,0, 0,3]
                inky_starts=[[17,12],[17,13],[17,14],[16,14],[15,14],[14,14],[14,13]]
                check=False
                for p in inky_starts:
                    if grid[p[0]][p[1]].get_ghost()==3:
                        check=True
                if not check:
                    self.starting=0
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
            grid[self.row][self.col].set_ghost(self.ghost_id)
            return


        self.direction=self.start_moves[self.starting]
        x,y,w,h=self.col*cell_size-(20*resize_factor), self.row*cell_size-(8*resize_factor), 42*resize_factor,42*resize_factor
        pygame.draw.rect(screen, BLACK, (x,y,w,h))
        grid[self.row][self.col].set_ghost(0)
        grid[self.row][self.col].draw_dot(screen, level)

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
        grid[self.row][self.col].set_ghost(self.ghost_id)
        self.starting+=1

    def dot_limit_passed(self):
        if self.starting==-2:
            self.starting=-1
