import pygame, sys
screen = pygame.display.set_mode((1000,800))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    


    pygame.draw.rect(screen, "red", (screen.get_width()/2, screen.get_height()/2, 300, 100))
    pygame.display.flip()

