import pygame, sys
import time
import math

pygame.init()

###########################################################################
###########################################################################

class Settings:
    resolutions = ["Low", "Normal", "High"]
    resolution = "Normal"

    window_sizes = ["Small", "Normal", "Big", "Full"]
    window_size = "Big"
sets = Settings()

###xxx###

# RESOLUTIONS

###xxx###

if sets.resolution not in sets.resolutions:
    print("Invalid resolution.")

if sets.window_size not in sets.window_sizes:
    print("Invalid window size.")
elif sets.window_size == "Small":
    screen_width = 800
    screen_height = 400
    x = 1
    y = 1
elif sets.window_size == "Normal":
    screen_width = 1200
    screen_height = 600
    x = 1.5	
    y = 1.5
elif sets.window_size == "Big":
    screen_width = 1800
    screen_height = 900
    x = 2.25
    y = 2.25
elif sets.window_size == "Full":
    print("Full window size is not set yet")

###########################################################################
###########################################################################

#GAME SETTINGS
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Meteor shooter - ZZ")

#IMAGES
ship = pygame.image.load("graphics/ship.png").convert_alpha()
background = pygame.image.load("graphics/background.png").convert()
START_butt = pygame.image.load("graphics/START.png").convert_alpha()
EXIT_butt = pygame.image.load("graphics/EXIT.png").convert_alpha()


#TEXT
font_size = 50
font = pygame.font.Font("graphics/subatomic.ttf", font_size)
text0 = font.render("Meteor shooter", True, "grey50")

#OBJECT SETTINGS
ship_rect = ship.get_rect(center = (screen_width/2, screen_height/2))
start_rect = START_butt.get_rect(center = (screen_width/2 - 200*x, screen_height/2 + 30*y))
exit_rect = EXIT_butt.get_rect(center = (screen_width/2 + 200*x, screen_height/2 + 30*y))
#OTHER
i = 1
BREAK = False
clock = pygame.time.Clock()
MENU = True
#sizes
###########################################################################
###########################################################################

while True:
    #### events
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_rect.x <= mouse[0] <= start_rect.x + start_rect.width and start_rect.y <= mouse[1] <= start_rect.y + start_rect.height:
                MENU = False
            elif exit_rect.x <= mouse[0] <= exit_rect.x + exit_rect.width and exit_rect.y <= mouse[1] <= exit_rect.y + exit_rect.height:
                pygame.quit()
                sys.exit()
    
    #### 
    screen.fill("grey13")
    clock.tick(80)
    #### 
    # updates
    mouse = pygame.mouse.get_pos()

    # surfaces(blit and location)
    screen.blit(background, (0, 0))
    
    screen.blit(ship, (i, math.floor(screen_height/4*3.1)))
    
    # MAIN SCREEN SHIP MOVEMENT
    if MENU == True:
        if i >= screen.get_width() - ship.get_width():
            BREAK = True
        elif i <= 0:
            BREAK = False
            
        if BREAK == True:
            i = i - 3*x
        else: i = i + 3*x

        #MAIN SCREEN TEXT
        screen.blit(text0, (screen_width/2 - text0.get_width()/2, screen_height/2-(30*y) - text0.get_height()/2))
        #MAIN SCREEN BUTTONS
        screen.blit(START_butt, start_rect)
        screen.blit(EXIT_butt, exit_rect)
    
        

               
#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#
        

    pygame.display.update()