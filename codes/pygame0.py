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
    window_size = "Normal"
sets = Settings()

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
ship_an = True
i = 1



screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Meteor shooter - ZZ")

ship = pygame.image.load("graphics/ship.png").convert_alpha()
background = pygame.image.load("graphics/background.png").convert()

font_size = 50
font = pygame.font.Font("graphics/subatomic.ttf", font_size)
text0 = font.render("Meteor shooter", True, "grey50")

# sizes







###########################################################################
###########################################################################

while True:
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # updates
    screen.fill("grey13")
    # location of surfaces
    screen.blit(background, (0, 0))
    
    while ship_an == True:
        if i > screen_width:
            i = -1
        elif i == 0:
            i = 1 
        i = i*10
        screen.blit(ship, (i, math.floor(screen_height/3*2)))
    
    screen.blit(text0, (screen_width/2 - text0.get_width()/2, screen_height/2-(30*y) - text0.get_height()/2))


    ##
    pygame.display.update()