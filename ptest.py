import pygame

pygame.init()

size = (1000,900)
screen = pygame.display.set_mode(size)

oldMousePos = None
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEMOTION:
            oldMousePos = pygame.mouse.get_pos()
            pygame.draw.circle(screen, "green", oldMousePos, 30, width=4)
    pygame.display.flip()
    clock.tick(60)

