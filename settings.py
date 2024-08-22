import pygame

# cell_size=24
width_in_cell=28
height_in_cell=36
# SCREEN_HEIGHT=cell_size*height_in_cell
# SCREEN_WIDTH=cell_size*width_in_cell

SCREEN_HEIGHT=648
cell_size=SCREEN_HEIGHT//height_in_cell
SCREEN_WIDTH=cell_size*width_in_cell

resize_factor=cell_size//24




WHITE=(255,255,255)
GRAY=(150,150,150)
BLACK=(0,0,0)
PINK=(255, 179, 217)
GREEN=(0,255,0)
DARK_GREEN=(0,150,0)
RED=(255,0,0)
BACKGROUND_COLOR = BLACK
GRID_COLOR=WHITE
pieces_colors=[RED, (255,130,0), (255,255,0),GREEN, (0,0,255),(255,0,255)]
flags=(pygame.HWSURFACE | pygame.DOUBLEBUF)
INPUTS=[pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT]