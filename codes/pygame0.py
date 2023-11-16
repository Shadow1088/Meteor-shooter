import pygame, sys
import math
import time
import random
from time import sleep as wait
pygame.init()

###########################################################################
###########################################################################

start_time = time.time()
DIFFICULTY = 0.95 # 0%, 100% = 1.0 (1.0 = 1 second, so the meteors would spawn instantly..
#                              honestly its insane, but the ship is too weak for it now)
#                              CHANGE THIS HOW MUCH YOU WANT, BUT KEEP IN MIND IT MIGHT BE UNPLAYABLE

class Settings:
    resolutions = ["Low", "Normal", "High"]
    resolution = "Normal"

    window_sizes = ["Small", "Normal", "Big"]
    window_size = "Big"

    gameplay_options = ["Arrows/Space", "Mouse", "Mouse/Space", "WASD/Space", "WASD/Mouse"]
    gameplay = "Mouse/Space"

    difficulty = DIFFICULTY
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
METEOR = pygame.image.load("graphics/meteor.png").convert_alpha()
GAME_OVER = pygame.image.load("graphics/game_over.png").convert_alpha()
GAME_OVER_scale = pygame.transform.scale(GAME_OVER, screenxy)
huge_meteor = pygame.image.load("graphics/huge_meteor.png").convert_alpha()
legendary_meteor = pygame.image.load("graphics/legendary_meteor.png").convert_alpha()
overpowered_meteor = pygame.image.load("graphics/overpowered.png").convert_alpha()
alien_meteor = pygame.image.load("graphics/ufo.png").convert_alpha()
bloody_meteor = pygame.image.load("graphics/bloody.png").convert_alpha()
meteor0 = pygame.image.load("graphics/meteor0.png").convert_alpha()
meteor1 = pygame.image.load("graphics/meteor1.png").convert_alpha()
the_rock = pygame.image.load("graphics/the_rock.png").convert_alpha()
purple_ease = pygame.image.load("graphics/purple_ease.png").convert_alpha()
blue_meteor = pygame.image.load("graphics/blue_meteor.png").convert_alpha()
red_meteor = pygame.image.load("graphics/red_meteor.png").convert_alpha()


#TEXT
font_size = 50
font0 = pygame.font.Font("graphics/subatomic.ttf", font_size)
font1 = pygame.font.Font("graphics/Oswald-Medium.ttf", font_size)
text0 = font0.render("Meteor shooter", True, "grey50")
gameplay_text0 = font1.render(f"Gameplay:  <-   {sets.gameplay}   -> ", True, "grey40")
window_size_text0 = font1.render(f"Window size:  <-   {sets.window_size}   -> ", True, "grey40")
YOU_LOST = font0.render("!!! YOU LOST !!!  (r) to enter Menu", True, "red")
YOU_LOST2 = font0.render("!!! YOU LOST !!!  (r) to enter Menu", True, "red3")
difficulty0 = font1.render(f"Difficulty: {sets.difficulty} -> +5", True, "grey40")


#OBJECT SETTINGS
ship_rect = ship.get_rect(center = (screen_width/2, math.floor(screen_height/4*3.1)))
start_rect = START_butt.get_rect(center = (screen_width/2 - 200*x, screen_height/2 + 30*y))
exit_rect = EXIT_butt.get_rect(center = (screen_width/2 + 200*x, screen_height/2 + 30*y))
settings_rect = SETTINGS_butt.get_rect(center = (screen_width - 50*x, 10*y))
laser_rect = LASER.get_rect(midbottom = (ship_rect.centerx, ship_rect.top))
meteor_rect = METEOR.get_rect(center = (screen_width/2, screen_height/2))
huge_meteor = pygame.transform.scale(huge_meteor, (math.floor(huge_meteor.get_width()*x), math.floor(huge_meteor.get_height()*y)))
huge_meteor_rect = huge_meteor.get_rect(center = (screen_width/2, screen_height/2))


#OTHER
i = 1
MENU_BOUNCE = False
clock = pygame.time.Clock()
MENU = True
SETTINGS = False
STOP = False
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
redindex = 0
game = False
start = 0
start_has_run = False
points = 0
alive_points = 0
add_points = 0
last_points = 0
highscore = 0
#hp = 1

class Ship:
    def __init__(self, x, y, img, dmg, angle):
        self.x = ship_rect.x
        self.y = ship_rect.y
        self.img = img
        self.dmg = dmg
        self.angle = angle

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

basic_ship = Ship(ship_rect.x, ship_rect.y, ship, 1, 0)


rotation_meteor = random.randint(0, 360)
class Meteor:
    def __init__(self, x, y, speed, img, hp, angle=None):
        self.x = x
        self.y = y
        self.speed = speed
        self.img = METEOR
        self.hp = hp
        self.angle = random.randint(0, 360) if angle is None else angle

    def update(self):
        self.y += self.speed

    def draw(self, screen):
        rotated_meteor = pygame.transform.rotate(self.img, rotation_meteor)
        screen.blit(rotated_meteor, (self.x, self.y))
#basic_meteor = Meteor(random.randint(0, screen_width - meteor_rect.width), y-meteor_rect.height, 5, METEOR, rotation_meteor)
class BasicMeteor(Meteor):
    def __init__(self, x, y, speed, img, hp, angle=None):
        super().__init__(x, y, speed, img, hp, angle=None)
        self.img = METEOR
        self.hp = 1
        self.angle = random.randint(0, 360) if angle is None else angle
    def __str__(self):
        return f"BasicMeteor({self.x}, {self.y}, {self.speed}, {self.img}, {self.hp}, {self.angle})"
class MidMeteor(Meteor):
    def __init__(self, x, y, speed, img, hp, angle=None):
        super().__init__(x, y, speed, img, hp, angle=None)
        self.img = meteor0
        self.hp = 2
        self.angle = random.randint(0, 360) if angle is None else angle
    def __str__(self):
        return f"MidMeteor({self.x}, {self.y}, {self.speed}, {self.img}, {self.hp}, {self.angle})"
class SpeedyMeteor(Meteor):
    def __init__(self, x, y, speed, img, hp, angle=None):
        super().__init__(x, y, speed, img, hp, angle=None)
        self.img = meteor1
        self.hp = 1
        self.angle = random.randint(0, 360) if angle is None else angle
    def __str__(self):
        return f"SpeedyMeteor({self.x}, {self.y}, {self.speed}, {self.img}, {self.hp}, {self.angle})"
class GoodMeteor(Meteor):
    def __init__(self, x, y, speed, img, hp, angle=None):
        super().__init__(x, y, speed, img, hp, angle=None)
        self.img = blue_meteor
        self.hp = 3
        self.angle = random.randint(0, 360) if angle is None else angle
    def __str__(self):
        return f"GoodMeteor({self.x}, {self.y}, {self.speed}, {self.img}, {self.hp}, {self.angle})"
class EpicMeteor(Meteor):
    def __init__(self, x, y, speed, img, hp, angle=None):
        super().__init__(x, y, speed, img, hp, angle=None)
        self.img = purple_ease
        self.hp = 6
        self.angle = random.randint(0, 360) if angle is None else angle
    def __str__(self):
        return f"EpicMeteor({self.x}, {self.y}, {self.speed}, {self.img}, {self.hp}, {self.angle})"
class HugeMeteor(Meteor):
    def __init__(self, x, y, speed, img, hp, angle=None):
        super().__init__(x, y, speed, img, hp, angle=None)
        self.img = huge_meteor
        self.hp = 8
        self.angle = random.randint(0, 360) if angle is None else angle
    def __str__(self):
        return f"HugeMeteor({self.x}, {self.y}, {self.speed}, {self.img}, {self.hp}, {self.angle})"
class LegendaryMeteor(Meteor):
    def __init__(self, x, y, speed, img, hp, angle=None):
        super().__init__(x, y, speed, img, hp, angle=None)
        self.img = legendary_meteor
        self.hp = 10
        self.angle = random.randint(0, 360) if angle is None else angle
    def __str__(self):
        return f"LegendaryMeteor({self.x}, {self.y}, {self.speed}, {self.img}, {self.hp}, {self.angle})"
class OverpoweredMeteor(Meteor):
    def __init__(self, x, y, speed, img, hp, angle=None):
        super().__init__(x, y, speed, img, hp, angle=None)
        self.img = overpowered_meteor
        self.hp = 30
        self.angle = random.randint(0, 360) if angle is None else angle
    def __str__(self):
        return f"OverpoweredMeteor({self.x}, {self.y}, {self.speed}, {self.img}, {self.hp}, {self.angle})"
class AlienMeteor(Meteor):
    def __init__(self, x, y, speed, img, hp, angle=None):
        super().__init__(x, y, speed, alien_meteor, hp, angle=None)
        self.img = alien_meteor
        self.hp = 10000
        self.angle = random.randint(0, 360) if angle is None else angle
    def __str__(self):
        return f"AlienMeteor({self.x}, {self.y}, {self.speed}, {self.img}, {self.hp}, {self.angle})"
class bloodyMeteor(Meteor):
    def __init__(self, x, y, speed, img, hp, angle=None):
        super().__init__(x, y, speed, bloody_meteor, hp, angle=None)
        self.img = bloody_meteor
        self.hp = 25
        self.angle = random.randint(0, 360) if angle is None else angle
    def __str__(self):
        return f"bloodyMeteor({self.x}, {self.y}, {self.speed}, {self.img}, {self.hp}, {self.angle})"
class the_rockMeteor(Meteor):
    def __init__(self, x, y, speed, img, hp, angle=None):
        super().__init__(x, y, speed, the_rock, hp, angle=None)
        self.img = the_rock
        self.hp = 15
        self.angle = random.randint(0, 360) if angle is None else angle
    def __str__(self):
        return f"the_rockMeteor({self.x}, {self.y}, {self.speed}, {self.img}, {self.hp}, {self.angle})"


meteor_types_rate = {
    "basic": 10000,
    "mid": 1000,
    "speedy": 200,
    "good": 100,
    "epic": 50,
    "huge": 10,
    "legendary": 5,
    "the_rock": 3,
    "bloody": 2,
    "overpowered": 1,
    "alien": 1,
}

meteors = []
meteor_spawn_time = 1.0
last_meteor_spawn_time = 0.0
meteor_types = [BasicMeteor, MidMeteor, SpeedyMeteor, GoodMeteor, EpicMeteor, HugeMeteor, LegendaryMeteor, OverpoweredMeteor, AlienMeteor, bloodyMeteor, the_rockMeteor]

class Laser:
    def __init__(self, x, y, direction, speed, img):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.img = img

    def lsr_update(self):
        if self.direction == -1:
            self.y -= self.speed

    def draw(self, screen):
        screen.blit(self.img, (self.x-5, self.y-5))


basic_lsr = Laser(ship_rect.midtop, ship_rect.top+5, -1, 10, LASER)
lasers = []
def shoot():
    lasers.append(Laser(ship_rect.centerx, ship_rect.top, -1, 10, LASER))


point_memory = []

#sizes
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################


while True:
    
    

    # POINT MECHANISM
    try: highscore = max(point_memory)
    except: pass
    points = add_points + alive_points
    if MENU == False and SETTINGS == False and STOP == False and start_has_run == False:
        start_time = time.time() # reset start_time when game restarts
        last_points = points
        start = 0
        alive_points = 0
        add_points = 0
        start_has_run = True
    elif MENU == False and SETTINGS == False and STOP == False and start_has_run == True:
        start = time.time() - start_time
        alive_points = int(round(start, 1) * 10) # calculate points based on time

    else:
        if start_has_run == True:
            point_memory.append(points)
            points = add_points + alive_points
        start_has_run = False
        
    
    # print(start, points, last_points)
    # print(point_memory)

    rotation_meteor = random.randint(0, 360)
    time.time()
    if MENU == True:
        STOP = False
    
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
            if settings_rect.x <= mouse[0] <= settings_rect.x + settings_rect.width and settings_rect.y <= mouse[1] <= settings_rect.y + settings_rect.height and SETTINGS == False and STOP == False:
                if MENU == True: #if activated SETTINGS from MENU, after DEactivation go back to MENU
                    menu_was_true = True
                SETTINGS = True
                MENU = False
                
            elif SETTINGS == True and settings_rect.x <= mouse[0] <= settings_rect.x + settings_rect.width and settings_rect.y <= mouse[1] <= settings_rect.y + settings_rect.height and STOP == False:
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
            if SETTINGS == True and screen_width/2-difficulty0.get_width() <= mouse[0] <= screen_width/2+difficulty0.get_width() and screen_height/4*3 <= mouse[1] <= screen_height/4*3+difficulty0.get_height():
                DIFFICULTY = DIFFICULTY + 0.05
                difficulty0 = font1.render(f"Difficulty: {sets.difficulty} -> +5", True, "grey40")
                sets.difficulty = round(DIFFICULTY, 2)
                DIFFICULTY = round(DIFFICULTY, 2)
                if DIFFICULTY > 1.0 or sets.difficulty > 1.0:
                    DIFFICULTY = 0.05
                    sets.difficulty = 0.05

        
        # MENU KEYBOARD SHORTCUTS

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and MENU == False:
            MENU = True
            SETTINGS = False
            STOP = False
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
            if settings_selected_index < -1:
                settings_selected_index = -1
            if event.key == pygame.K_LEFT:
                if settings_selected_index == -1:
                    index0 = index0 - 1
                    sets.gameplay = sets.gameplay_options[index0]
                    gameplay_text0 = font1.render(f"Gameplay:  <-   {sets.gameplay}   -> ", True, "grey40")
                if settings_selected_index == 0:
                    index1 = index1 - 1
                    sets.window_size = sets.window_sizes[index1]
                    if sets.window_size != "Big":
                        window_size_text0 = font1.render(f"Window size:  <-   {sets.window_size}   -> (unfinished)", True, "grey40")
                    else:
                        window_size_text0 = font1.render(f"Window size:  <-   {sets.window_size}   ->  (default)", True, "grey40")
                if settings_selected_index == 1:
                    DIFFICULTY = DIFFICULTY - 0.05
                    difficulty0 = font1.render(f"Difficulty: {sets.difficulty} -> +0.05", True, "grey40")
                    sets.difficulty = round(DIFFICULTY, 2)
                    DIFFICULTY = round(DIFFICULTY, 2)
                    if DIFFICULTY < 0.05 or sets.difficulty < 0.05:
                        DIFFICULTY = 1.0
                        sets.difficulty = 1.0
            if event.key == pygame.K_RIGHT:
                if settings_selected_index == -1:
                    index0 = index0 + 1
                    sets.gameplay = sets.gameplay_options[index0]
                    gameplay_text0 = font1.render(f"Gameplay:  <-   {sets.gameplay}   -> ", True, "grey40")
                if settings_selected_index == 0:
                    index1 = index1 + 1
                    sets.window_size = sets.window_sizes[index1]
                    if sets.window_size != "Big":
                        window_size_text0 = font1.render(f"Window size:  <-   {sets.window_size}   -> (unfinished)", True, "grey40")
                    else:
                        window_size_text0 = font1.render(f"Window size:  <-   {sets.window_size}   ->  (default)", True, "grey40")
                if settings_selected_index == 1:
                    DIFFICULTY = DIFFICULTY + 0.05
                    difficulty0 = font1.render(f"Difficulty: {sets.difficulty} -> +0.05", True, "grey40")
                    sets.difficulty = round(DIFFICULTY, 2)
                    DIFFICULTY = round(DIFFICULTY, 2)
                    if DIFFICULTY > 1.0 or sets.difficulty > 1.0:
                        DIFFICULTY = 0.05
                        sets.difficulty = 0.05

    
        # IF GAMEPLAY IS MOUSE, SHIP MOVES AS MOUSE MOVES
        if event.type == pygame.MOUSEMOTION and MENU == False and SETTINGS == False and sets.gameplay == "Mouse" and STOP == False:
            ship_rect.center = event.pos
        
        # ESCAPE FOR SETTINGS
        # made this so when you enter settings from menu, you will go back to menu after pressing it again
        if event.type == pygame.KEYDOWN and STOP == False:
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
                

        # MOVEMENT AND SHOOTING
        if MENU == False and SETTINGS == False and STOP == False:
            keys = pygame.key.get_pressed()
            
            if sets.gameplay == "Arrows/Space" or sets.gameplay == "WASD/Space" or sets.gameplay == "WASD/Mouse":
                move_up = keys[pygame.K_UP] or keys[pygame.K_w]
                move_down = keys[pygame.K_DOWN] or keys[pygame.K_s]
                move_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
                move_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
            
                if keys[pygame.K_SPACE] and time.time() - last_reload > reload_time and sets.gameplay != "WASD/Mouse":
                    shoot()
                    last_reload = time.time()
            
            if sets.gameplay == "Mouse" or sets.gameplay == "WASD/Mouse":
                if pygame.mouse.get_pressed()[0] and time.time() - last_reload > reload_time:
                    shoot()
                    last_reload = time.time()
            
            if sets.gameplay == "Mouse/Space":
                ship_rect.center = pygame.mouse.get_pos()
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
        

    # INDEX RESETING - so the settings choosing index doesnt go out of range
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
    if MENU == False and SETTINGS == False and STOP == False:
        screen.blit(ship, (ship_rect.x, ship_rect.y))
    # SETTINGS
    if SETTINGS == True:
        screen.blit(gameplay_text0, (screen_width/3, screen_height/4))
        if settings_selected_index == -1 and settings_selected_any == True:
            pygame.draw.rect(screen, "grey", gameplay_text0.get_rect(topleft = (screen_width/3-5*x, screen_height/4)), 3)
        screen.blit(window_size_text0, (screen_width/3, screen_height/4*2))
        if settings_selected_index == 0 and settings_selected_any == True:
            pygame.draw.rect(screen, "grey", window_size_text0.get_rect(topleft = (screen_width/3-5*x, screen_height/4*2)), 3)
        screen.blit(difficulty0, (screen_width/3, screen_height/4*3))
        if settings_selected_index == 1 and settings_selected_any == True:
            pygame.draw.rect(screen, "grey", difficulty0.get_rect(topleft = (screen_width/3-5*x, screen_height/4*3)), 3)
    
    # SHIP BOUNDARIES
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

    # METEORS
    for meteor in meteors:
        if meteor.y > screen_height:
            meteors.remove(meteor)

    sum_value = sum(meteor_types_rate.values())
    
    # SPAWN METEORS
    if (time.time() - last_meteor_spawn_time)+DIFFICULTY > meteor_spawn_time and SETTINGS == False and MENU == False:
        current_meteor_rate_num = random.choice(range(0, sum_value+1))
        if current_meteor_rate_num in range(0, meteor_types_rate["basic"]):
            current_meteor = Meteor
            hp = 1
        elif current_meteor_rate_num in range(meteor_types_rate["basic"], meteor_types_rate["mid"]+meteor_types_rate["basic"]):
            current_meteor = MidMeteor
            hp = 2
        elif current_meteor_rate_num in range(meteor_types_rate["mid"], meteor_types_rate["speedy"]+meteor_types_rate["mid"]):
            current_meteor = SpeedyMeteor
            hp = 1
        elif current_meteor_rate_num in range(meteor_types_rate["speedy"], meteor_types_rate["good"]+meteor_types_rate["speedy"]):
            current_meteor = GoodMeteor
            hp = 3
        elif current_meteor_rate_num in range(meteor_types_rate["good"], meteor_types_rate["epic"]+meteor_types_rate["good"]):
            current_meteor = EpicMeteor
            hp = 6
        elif current_meteor_rate_num in range(meteor_types_rate["epic"], meteor_types_rate["huge"]+meteor_types_rate["epic"]):
            current_meteor = HugeMeteor
            hp = 8
        elif current_meteor_rate_num in range(meteor_types_rate["huge"], meteor_types_rate["legendary"]+meteor_types_rate["huge"]):
            current_meteor = LegendaryMeteor
            hp = 10
        elif current_meteor_rate_num in range(meteor_types_rate["legendary"], meteor_types_rate["overpowered"]+meteor_types_rate["legendary"]):
            current_meteor = OverpoweredMeteor
            hp = 30
        elif current_meteor_rate_num in range(meteor_types_rate["overpowered"], meteor_types_rate["alien"]+meteor_types_rate["overpowered"]):
            current_meteor = AlienMeteor
            hp = 10000
        elif current_meteor_rate_num in range(meteor_types_rate["alien"], meteor_types_rate["bloody"]+meteor_types_rate["alien"]):
            current_meteor = bloodyMeteor
            hp = 25
        elif current_meteor_rate_num in range(meteor_types_rate["bloody"], meteor_types_rate["the_rock"]+1+meteor_types_rate["bloody"]):
            current_meteor = the_rockMeteor
            hp = 15
        
        meteors.append(current_meteor(random.randint(0, screen_width - meteor_rect.width), y-meteor_rect.height, 5, rotation_meteor, hp))
        last_meteor_spawn_time = time.time()

    # UPDATE AND DRAW METEORS
    for meteor in meteors:
        meteor.update()
        meteor.draw(screen)
    

    # METEOR DESTROYING REWARDS
    


    ## COLLISIONS
    #LASER AND METEOR
    for meteor in meteors:
        meteor_rect = pygame.Rect(meteor.x, meteor.y, meteor.img.get_width(), meteor.img.get_height())
        for lsr in lasers:
            lsr_rect = pygame.Rect(lsr.x, lsr.y, lsr.img.get_width(), lsr.img.get_height())
            if meteor_rect.colliderect(lsr_rect): 
                if meteor.hp == 1:
                    meteor.hp = meteor.hp - basic_ship.dmg
                if meteor.hp <= 0:
                    meteors.remove(meteor)
                    lasers.remove(lsr)
                    if meteor.img == METEOR:
                        add_points = add_points + 5
                    if meteor.img == meteor0:
                        add_points = add_points + 10
                    if meteor.img == meteor1:
                        add_points = add_points + 15
                    if meteor.img == blue_meteor:
                        add_points = add_points + 20
                    if meteor.img == purple_ease:
                        add_points = add_points + 25
                    if meteor.img == huge_meteor:
                        add_points = add_points + 30
                    if meteor.img == legendary_meteor:
                        add_points = add_points + 35
                    if meteor.img == overpowered_meteor:
                        add_points = add_points + 50
                    if meteor.img == alien_meteor:
                        add_points = add_points + 5000
                    if meteor.img == bloody_meteor:
                        add_points = add_points + 45
                    if meteor.img == the_rock:
                        add_points = add_points + 50
                else:
                    meteor.hp = meteor.hp - basic_ship.dmg
                    lasers.remove(lsr)
                    
    
    #SHIP AND METEOR
    for meteor in meteors:
        meteor_rect = pygame.Rect(meteor.x, meteor.y, meteor.img.get_width(), meteor.img.get_height())
        if meteor_rect.colliderect(ship_rect):
            STOP = True

    # GAME OVER
    if STOP == True:
        screen.blit(GAME_OVER_scale, (0, 0))
        
        # GAME OVER TEXT
        redindex = redindex + 1
        if redindex >= 20:
            screen.blit(YOU_LOST, (screen_width/2 - YOU_LOST.get_width()/2, screen_height/2 - YOU_LOST.get_height()/2))
        else:
            screen.blit(YOU_LOST2, (screen_width/2 - YOU_LOST.get_width()/2, screen_height/2 - YOU_LOST.get_height()/2))
        if redindex == 40:
            redindex = 0
        
    # METEORS RESET
    if MENU == True:
        meteors = []

    # POINTS
    points0 = font1.render(f"Points: {points}", True, "grey40")
    last_points0 = font1.render(f"Last points: {last_points}", True, "grey40")
    highscore0 = font1.render(f"Highscore: {highscore}", True, "grey40")
    if MENU == False and SETTINGS == False and STOP == False:
        screen.blit(points0, (13,5))
        screen.blit(last_points0, (13, points0.get_height()+5))
        screen.blit(highscore0, (screen_width-highscore0.get_width()-SETTINGS_butt_scale.get_width()-50, 0))
#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#
        

    pygame.display.update()