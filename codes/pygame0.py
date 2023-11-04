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

    gameplay_options = ["Arrows/Space", "Mouse", "Mouse/Space", "WASD/Space", "WASD/Mouse"]
    gameplay = "Mouse"
sets = Settings()

###xxx###

# RESOLUTIONS

###xxx###

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
ship_rect = ship.get_rect(center = (screen_width/2, math.floor(screen_height/4*3.1)))
start_rect = START_butt.get_rect(center = (screen_width/2 - 200*x, screen_height/2 + 30*y))
exit_rect = EXIT_butt.get_rect(center = (screen_width/2 + 200*x, screen_height/2 + 30*y))
#OTHER
i = 1
BREAK = False
clock = pygame.time.Clock()
MENU = True
SETTINGS = False
move_up = False
move_down = False
move_left = False
move_right = False





if sets.gameplay not in sets.gameplay_options:
    print("Invalid gameplay option.")
elif sets.gameplay == "Arrows/Space":
    shoot = pygame.K_SPACE
    move_up = pygame.K_UP
    move_down = pygame.K_DOWN
    move_left = pygame.K_LEFT
    move_right = pygame.K_RIGHT
elif sets.gameplay == "Mouse":
    pass

def shoot():
    pass
#sizes
###########################################################################
###########################################################################

print(start_rect.y); print(start_rect.height)

while True:
    #### events
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            if start_rect.x <= mouse[0] <= start_rect.x + start_rect.width and start_rect.y <= mouse[1] <= start_rect.y + start_rect.height:
                MENU = False
            elif exit_rect.x <= mouse[0] <= exit_rect.x + exit_rect.width and exit_rect.y <= mouse[1] <= exit_rect.y + exit_rect.height:
                pygame.quit()
                sys.exit()
        
        if event.type == pygame.MOUSEMOTION and MENU == False and Settings.gameplay == "Mouse":
            ship_rect.center = event.pos
            
        if event.type == pygame.KEYDOWN and MENU == False:
            if event.key == pygame.K_ESCAPE:
                SETTINGS = True
            if SETTINGS == True and event.key == pygame.K_ESCAPE:
                SETTINGS = False
            if event.key == pygame.K_UP:
                move_up = True    
            if event.key == pygame.K_DOWN:
                move_down = True
            if event.key == pygame.K_LEFT:
                move_left = True
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_r:
                MENU = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                move_up = False
            if event.key == pygame.K_DOWN:
                move_down = False
            if event.key == pygame.K_LEFT:
                move_left = False
            if event.key == pygame.K_RIGHT:
                move_right = False
                    
    if move_up == True:
        ship_rect.y -= 10
    if move_down == True:
        ship_rect.y += 10
    if move_left == True:
        ship_rect.x -= 10
    if move_right == True:
        ship_rect.x += 10


    #### 
    screen.fill("grey13")
    clock.tick(80)
    #### 
    # updates
    mouse = pygame.mouse.get_pos()

    # surfaces(blit and location)
    screen.blit(background, (0, 0))
    #/#screen.blit(ship, (i, ship_rect.y + ship.get_height()/2))
    
    # MAIN SCREEN SHIP MOVEMENT
    if MENU == True:
        screen.blit(ship, (i, ship_rect.y + ship.get_height()/2))
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
    else:
        screen.blit(ship, ship_rect)
    
    ### SETTINGS
        

               
#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#
        

    pygame.display.update()