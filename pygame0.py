import pygame, sys
import time


pygame.init()


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
elif sets.window_size == "Normal":
    screen_width = 1200
    screen_height = 600
elif sets.window_size == "Big":
    screen_width = 1800
    screen_height = 900
elif sets.window_size == "Full":
    print("Full window size is not set yet")


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Meteor shooter - ZZ")

def QUIT():
    pygame.quit()
    sys.exit()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    pygame.display.update()