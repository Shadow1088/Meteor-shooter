import pygame, sys
import math
import time

pygame.init()

###########################################################################
###########################################################################

class Settings:
    resolutions = ["Low", "Normal", "High"]
    resolution = "Normal"

    window_sizes = ["Small", "Normal", "Big"]
    window_size = "Big"

    gameplay_options = ["Arrows/Space", "Mouse", "Mouse/Space", "WASD/Space", "WASD/Mouse"]
    gameplay = "Mouse"
sets = Settings()

###xxx###

if sets.window_size not in sets.window_sizes:
    print("Invalid window size.")
elif sets.window_size == "Small":
    screen_width = 800
    screen_height = 400
    x = 1
    y = 1
    index1 = 0
elif sets.window_size == "Normal":
    screen_width = 1200
    screen_height = 600
    x = 1.5	
    y = 1.5
    index1 = 1
elif sets.window_size == "Big":
    screen_width = 1800
    screen_height = 900
    x = 2.25
    y = 2.25
    index1 = 2

screenxy = (screen_width, screen_height)

###########################################################################
###########################################################################

#GAME SETTINGS
screen = pygame.display.set_mode(screenxy)
pygame.display.set_caption("Meteor shooter - ZZ")


#IMAGES
ship = pygame.image.load("graphics/ship.png").convert_alpha()
background = pygame.image.load("graphics/background.png").convert()
START_butt = pygame.image.load("graphics/START.png").convert_alpha()
EXIT_butt = pygame.image.load("graphics/EXIT.png").convert_alpha()
SETTINGS_butt = pygame.image.load("graphics/SETTINGS.png").convert_alpha()
SETTINGS_butt_scale = pygame.transform.scale(SETTINGS_butt, (37*x,37*y))
LASER = pygame.image.load("graphics/laser.png").convert_alpha()


#TEXT
font_size = 50
font0 = pygame.font.Font("graphics/subatomic.ttf", font_size)
font1 = pygame.font.Font("graphics/Oswald-Medium.ttf", font_size)
text0 = font0.render("Meteor shooter", True, "grey50")
gameplay_text0 = font1.render(f"Gameplay:  <-   {sets.gameplay}   -> ", True, "grey40")
window_size_text0 = font1.render(f"Window size:  <-   {sets.window_size}   -> ", True, "grey40")

#OBJECT SETTINGS
ship_rect = ship.get_rect(center = (screen_width/2, math.floor(screen_height/4*3.1)))
start_rect = START_butt.get_rect(center = (screen_width/2 - 200*x, screen_height/2 + 30*y))
exit_rect = EXIT_butt.get_rect(center = (screen_width/2 + 200*x, screen_height/2 + 30*y))
settings_rect = SETTINGS_butt.get_rect(center = (screen_width - 50*x, 10*y))
laser_rect = LASER.get_rect(midbottom = (ship_rect.centerx, ship_rect.top))


#OTHER
i = 1
MENU_BOUNCE = False
clock = pygame.time.Clock()
MENU = True
SETTINGS = False
move_up = False
move_down = False
move_left = False
move_right = False
index0 = -1

max_index0 = len(sets.gameplay_options) - 1
max_index1 = len(sets.window_sizes) - 1
settings_selected_any = False
settings_selected_index = 0

win_changed = False
menu_was_true = False
shoots = False
last_reload = 0
reload_time = 0.2



class Laser:
    def __init__(self, x, y, direction, speed, img):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.img = img

    def lsr_update(self):
        if self.direction == "up":
            self.y -= self.speed

    def draw(self, screen):
        screen.blit(self.img, (self.x-5, self.y-5))


basic_lsr = Laser(ship_rect.midtop, ship_rect.top+5, "up", 10, LASER)
lasers = []
def shoot():
    lasers.append(Laser(ship_rect.centerx, ship_rect.top, "up", 10, LASER))

#sizes
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################


while True:
    time.time()
    
    #SCREEN SIZE CHANGING
    if index1 == 0:
        if win_changed:
            #screenxy = (800, 400)
            #screen = pygame.display.set_mode(screenxy)
            win_changed = False
    if index1 == 1:
        if win_changed:
            screenxy = (1200, 600)
            x = 1.5
            y = 1.5
            screen = pygame.display.set_mode(screenxy)
            win_changed = False
    if index1 == -1:
        if win_changed:
            screenxy = (1800, 900)
            x = 2.25
            y = 2.25
            screen = pygame.display.set_mode(screenxy)
            win_changed = False
    if win_changed:
        print(index1)

    # INDEX RESETING - so the index doesnt go out of range
    if index1 == 2:
        index1 = 1
    if index1 == -2:
        index1 = 1

    #### EVENTS
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            
            # BUTTONS
            
            if start_rect.x <= mouse[0] <= start_rect.x + start_rect.width and start_rect.y <= mouse[1] <= start_rect.y + start_rect.height and MENU == True:
                MENU = False
            if exit_rect.x <= mouse[0] <= exit_rect.x + exit_rect.width and exit_rect.y <= mouse[1] <= exit_rect.y + exit_rect.height and MENU == True:
                pygame.quit()
                sys.exit()
            if settings_rect.x <= mouse[0] <= settings_rect.x + settings_rect.width and settings_rect.y <= mouse[1] <= settings_rect.y + settings_rect.height and SETTINGS == False:
                if MENU == True: #if activated SETTINGS from MENU, after DEactivation go back to MENU
                    menu_was_true = True
                SETTINGS = True
                MENU = False
                
            elif SETTINGS == True and settings_rect.x <= mouse[0] <= settings_rect.x + settings_rect.width and settings_rect.y <= mouse[1] <= settings_rect.y + settings_rect.height:
                SETTINGS = False
                if menu_was_true: #same comment as above (line 155)
                    MENU = True
                    menu_was_true = False
                
            # SETTING CHANGING

            if SETTINGS == True and screen_width/2-gameplay_text0.get_width() <= mouse[0] <= screen_width/2+gameplay_text0.get_width() and screen_height/4 <= mouse[1] <= screen_height/4+gameplay_text0.get_height():
                index0 = index0 +1
                sets.gameplay = sets.gameplay_options[index0]
                gameplay_text0 = font1.render(f"Gameplay:  <-   {sets.gameplay}   -> ", True, "grey40")
            if SETTINGS == True and screen_width/2-window_size_text0.get_width() <= mouse[0] <= screen_width/2+window_size_text0.get_width() and screen_height/4*2 <= mouse[1] <= screen_height/4*2+window_size_text0.get_height():
                win_changed = True
                index1 = index1 +1
                sets.window_size = sets.window_sizes[index1]
                if sets.window_size != "Big":
                    window_size_text0 = font1.render(f"Window size:  <-   {sets.window_size}   -> (unfinished)", True, "grey40")
                else:
                    window_size_text0 = font1.render(f"Window size:  <-   {sets.window_size}   ->      (default)", True, "grey40")
        
        # MENU KEYBOARD SHORTCUTS

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and MENU == False:
            MENU = True
            SETTINGS = False
            print("r")
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s and MENU == True:
            MENU = False
            SETTINGS = False
            print("s")
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e and MENU == True:
            print("e")
            pygame.quit()
            sys.exit()
        
        # RECTANGLE AROUND CHOSEN OPTION ON ENTER KEY IN SETTINGS

        if event.type == pygame.KEYDOWN and SETTINGS == True:
            if event.key == pygame.K_RETURN:
                if settings_selected_any == False:
                    settings_selected_any = True
                    settings_selected_index = settings_selected_index + 1
                    
                elif settings_selected_any == True:
                    settings_selected_any = False
                    settings_selected_index = 0

        # REMOVE RECTANGLE IF NOT IN SETTINGS
        if SETTINGS == False and settings_selected_any == True:
            settings_selected_any = False
            settings_selected_index = 0
        
        # SETTINGS KEYBOARD SHORTCUTS - Arrow keys
        if event.type == pygame.KEYDOWN and SETTINGS == True and settings_selected_any == True:
            if event.key == pygame.K_DOWN:
                settings_selected_index = settings_selected_index + 1
            if event.key == pygame.K_UP:
                settings_selected_index = settings_selected_index - 1
            if settings_selected_index > 1:
                settings_selected_index = 1
            if settings_selected_index < 0:
                settings_selected_index = 0
            if event.key == pygame.K_LEFT:
                if settings_selected_index == 0:
                    index0 = index0 - 1
                    sets.gameplay = sets.gameplay_options[index0]
                    gameplay_text0 = font1.render(f"Gameplay:  <-   {sets.gameplay}   -> ", True, "grey40")
                if settings_selected_index == 1:
                    index1 = index1 - 1
                    sets.window_size = sets.window_sizes[index1]
                    if sets.window_size != "Big":
                        window_size_text0 = font1.render(f"Window size:  <-   {sets.window_size}   -> (unfinished)", True, "grey40")
                    else:
                        window_size_text0 = font1.render(f"Window size:  <-   {sets.window_size}   ->  (default)", True, "grey40")        
            if event.key == pygame.K_RIGHT:
                if settings_selected_index == 0:
                    index0 = index0 + 1
                    sets.gameplay = sets.gameplay_options[index0]
                    gameplay_text0 = font1.render(f"Gameplay:  <-   {sets.gameplay}   -> ", True, "grey40")
                if settings_selected_index == 1:
                    index1 = index1 + 1
                    sets.window_size = sets.window_sizes[index1]
                    if sets.window_size != "Big":
                        window_size_text0 = font1.render(f"Window size:  <-   {sets.window_size}   -> (unfinished)", True, "grey40")
                    else:
                        window_size_text0 = font1.render(f"Window size:  <-   {sets.window_size}   ->  (default)", True, "grey40")

    
        # IF GAMEPLAY IS MOUSE, SHIP MOVES AS MOUSE MOVES
        if event.type == pygame.MOUSEMOTION and MENU == False and SETTINGS == False and sets.gameplay == "Mouse":
            ship_rect.center = event.pos
        
        # ESCAPE FOR SETTINGS
        # made this so when you enter settings from menu, you will go back to menu after pressing it again
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if SETTINGS == True:
                    SETTINGS = False
                    if menu_was_true:
                        MENU = True
                        menu_was_true = False
                elif MENU == True:
                    menu_was_true = True
                    SETTINGS = True
                    MENU = False
                else:        
                    SETTINGS = True
                    MENU = False
                

        # MOVEMENT CONTINUOS IF ARROW KEY PRESSED DOWN
        if MENU == False and SETTINGS == False:
            keys = pygame.key.get_pressed()
            if sets.gameplay == "Arrows/Space":
                move_up = keys[pygame.K_UP]
                move_down = keys[pygame.K_DOWN]
                move_left = keys[pygame.K_LEFT]
                move_right = keys[pygame.K_RIGHT]
            
                if move_up:
                    print("yes")

                if keys[pygame.K_SPACE] and time.time() - last_reload > reload_time:
                    shoot()
                    last_reload = time.time()

        
            
            

        if event.type == pygame.KEYUP:
            if sets.gameplay == "Arrows/Space":
                if event.key == pygame.K_UP:
                    move_up = False
                if event.key == pygame.K_DOWN:
                    move_down = False
                if event.key == pygame.K_LEFT:
                    move_left = False
                if event.key == pygame.K_RIGHT:
                    move_right = False
        

    # INDEX RESETING - so the index doesnt go out of range
    if index0 == max_index0:
        index0 = -1
    if index1 == max_index1:
        index1 = -1

    # MOVEMENT SPEED
    if move_up:
        ship_rect.y = ship_rect.y - 10 
    if move_down:
        ship_rect.y = ship_rect.y + 10
    if move_left:
        ship_rect.x = ship_rect.x - 10        
    if move_right:
        ship_rect.x = ship_rect.x + 10
        
    # GAMEPLAY OPTIONS (ignore this)
    if sets.gameplay not in sets.gameplay_options:
        print("Invalid gameplay option.")
    elif sets.gameplay == "Arrows/Space":
        pass
    elif sets.gameplay == "Mouse":
        pass

    # screen filled with colour and topped fps
    screen.fill("grey13")
    clock.tick(80)
    
    mouse = pygame.mouse.get_pos()

    # surfaces(blit and location)
    screen.blit(background, (0, 0))
    screen.blit(SETTINGS_butt_scale, (screen_width - SETTINGS_butt.get_width()+30*x, 20))
    
    # MAIN SCREEN SHIP MOVEMENT
    if MENU == True:
        screen.blit(ship, (i, ship_rect.y + ship.get_height()/2))
        if i >= screen.get_width() - ship.get_width():
            MENU_BOUNCE = True
        elif i <= 0:
            MENU_BOUNCE = False
            
        if MENU_BOUNCE == True:
            i = i - 3*x
        else: i = i + 3*x

        #MAIN SCREEN TEXT
        screen.blit(text0, (screen_width/2 - text0.get_width()/2, screen_height/2-(30*y) - text0.get_height()/2))
        #MAIN SCREEN BUTTONS
        screen.blit(START_butt, (start_rect.x, start_rect.y))
        screen.blit(EXIT_butt, (exit_rect.x, exit_rect.y))
    # INGAME SHIP MOVEMENT
    if MENU == False and SETTINGS == False:
        screen.blit(ship, (ship_rect.x, ship_rect.y))
    # SETTINGS
    if SETTINGS == True:
        screen.blit(gameplay_text0, (screen_width/3, screen_height/4))
        if settings_selected_index == 0 and settings_selected_any == True:
            pygame.draw.rect(screen, "grey", gameplay_text0.get_rect(topleft = (screen_width/3-5*x, screen_height/4)), 3)
        screen.blit(window_size_text0, (screen_width/3, screen_height/4*2))
        if settings_selected_index == 1 and settings_selected_any == True:
            pygame.draw.rect(screen, "grey", window_size_text0.get_rect(topleft = (screen_width/3-5*x, screen_height/4*2)), 3)
        
    if ship_rect.top < 0:
        ship_rect.top = 0
    if ship_rect.bottom > screen_height:
        ship_rect.bottom = screen_height
    if ship_rect.left < 0:
        ship_rect.left = 0
    if ship_rect.right > screen_width:
        ship_rect.right = screen_width

    # LASERS
    for lsr in lasers:
        lsr.draw(screen)
        lsr.lsr_update()
        if lsr.y < 0:
            lasers.remove(lsr)
        


#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#
        

    pygame.display.update()