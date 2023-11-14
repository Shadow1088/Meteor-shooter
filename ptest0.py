import pygame

xy = (1000,800)
clock = pygame.time.Clock()
oldMousePos = 0,0

pygame.init()
pygame.display.set_caption("My first game")
screen = pygame.display.set_mode(xy)


while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.polygon(screen, "red",((250,250),(500,500),(250,500)))
            oldMousePos = pygame.mouse.get_pos()
    pygame.display.flip()
    clock.tick(60)