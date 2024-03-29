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
light_blue_laser = pygame.image.load("graphics/light_blue_laser.png").convert_alpha()
white_laser = pygame.image.load("graphics/white_laser.png").convert_alpha()
yellow_laser = pygame.image.load("graphics/yellow_laser.png").convert_alpha()
purple_laser = pygame.image.load("graphics/purple_laser.png").convert_alpha()
multi_laser = pygame.image.load("graphics/multi_laser.png").convert_alpha()
chest = pygame.image.load("graphics/chest.png").convert_alpha()
chest_scale = pygame.transform.scale(chest, (40*x, 40*y))
alien_meteor_scale = pygame.transform.scale(alien_meteor, (50*x, 50*y))


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
chest_rect = chest.get_rect(center = (screen_width/2, screen_height/2))


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
test0 = 0
highscore = test0
last_point_check = 0
current_stage = "stock"
stage_selected_index = 0
chest_picked_up = 0
last_chest_spawn = 0
blt_speed_activation_time = 0
blt_speed2_activation_time = 0
blt_dmg_activation_time = 0
blt_dmg2_activation_time = 0
immortality_time = 0
add_blt_sp = False
add_blt_sp2 = False
add_blt_dmg01 = False
add_blt_dmg02 = False
immortality = False
imm = False
xx = "nothing"
the_blt_dmg = 1
blit_deact = True
blit_deact = True
blit_deact_time = 0
the_last_points = 0


class Ship:
    def __init__(self, x, y, img, dmg, angle):
        self.x = ship_rect.x
        self.y = ship_rect.y
        self.img = img
        self.dmg = dmg
        self.angle = angle
        self.mask = pygame.mask.from_surface(self.img)

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
        self.mask = pygame.mask.from_surface(self.img)

    def update(self):
        self.y += self.speed

    def draw(self, screen):
        rotated_meteor = pygame.transform.rotate(self.img, angle=self.angle)
        screen.blit(rotated_meteor, (self.x, self.y))

class BasicMeteor(Meteor):
    def __init__(self, x, y, speed, img, hp, angle=None):
        super().__init__(x, y, speed, img, hp, angle=None)
        self.img = METEOR
        self.hp = 1
        self.angle = random.randint(0, 360) if angle is None else angle
        self.mask = pygame.mask.from_surface(self.img)
    def __str__(self):
        return f"BasicMeteor({self.x}, {self.y}, {self.speed}, {self.img}, {self.hp},{self.angle})"
class MidMeteor(Meteor):
    def __init__(self, x, y, speed, img, hp, angle=None):
        super().__init__(x, y, speed, img, hp, angle=None)
        self.img = meteor0
        self.hp = 2
        self.angle = random.randint(0, 360) if angle is None else angle
        self.mask = pygame.mask.from_surface(self.img)
    def __str__(self):
        return f"MidMeteor({self.x}, {self.y}, {self.speed}, {self.img}, {self.hp}, {self.angle})"
class SpeedyMeteor(Meteor):
    def __init__(self, x, y, speed, img, hp, angle=None):
        super().__init__(x, y, speed, img, hp, angle=None)
        self.img = blue_meteor
        self.hp = 1
        self.angle = random.randint(0, 360) if angle is None else angle
        self.mask = pygame.mask.from_surface(self.img)
    def __str__(self):
        return f"SpeedyMeteor({self.x}, {self.y}, {self.speed}, {self.img}, {self.hp}, {self.angle})"
class GoodMeteor(Meteor):
    def __init__(self, x, y, speed, img, hp, angle=None):
        super().__init__(x, y, speed, img, hp, angle=None)
        self.img = meteor1
        self.hp = 3
        self.angle = random.randint(0, 360) if angle is None else angle
        self.mask = pygame.mask.from_surface(self.img)
    def __str__(self):
        return f"GoodMeteor({self.x}, {self.y}, {self.speed}, {self.img}, {self.hp}, {self.angle})"
class EpicMeteor(Meteor):
    def __init__(self, x, y, speed, img, hp, angle=None):
        super().__init__(x, y, speed, img, hp, angle=None)
        self.img = purple_ease
        self.hp = 6
        self.angle = random.randint(0, 360) if angle is None else angle
        self.mask = pygame.mask.from_surface(self.img)
    def __str__(self):
        return f"EpicMeteor({self.x}, {self.y}, {self.speed}, {self.img}, {self.hp}, {self.angle})"
class HugeMeteor(Meteor):
    def __init__(self, x, y, speed, img, hp, angle=None):
        super().__init__(x, y, speed, img, hp, angle=None)
        self.img = huge_meteor
        self.hp = 8
        self.angle = random.randint(0, 360) if angle is None else angle
        self.mask = pygame.mask.from_surface(self.img)
    def __str__(self):
        return f"HugeMeteor({self.x}, {self.y}, {self.speed}, {self.img}, {self.hp}, {self.angle})"
class LegendaryMeteor(Meteor):
    def __init__(self, x, y, speed, img, hp, angle=None):
        super().__init__(x, y, speed, img, hp, angle=None)
        self.img = legendary_meteor
        self.hp = 10
        self.angle = random.randint(0, 360) if angle is None else angle
        self.mask = pygame.mask.from_surface(self.img)
    def __str__(self):
        return f"LegendaryMeteor({self.x}, {self.y}, {self.speed}, {self.img}, {self.hp}, {self.angle})"
class OverpoweredMeteor(Meteor):
    def __init__(self, x, y, speed, img, hp, angle=None):
        super().__init__(x, y, speed, img, hp, angle=None)
        self.img = overpowered_meteor
        self.hp = 30
        self.angle = random.randint(0, 360) if angle is None else angle
        self.mask = pygame.mask.from_surface(self.img)
    def __str__(self):
        return f"OverpoweredMeteor({self.x}, {self.y}, {self.speed}, {self.img}, {self.hp}, {self.angle})"
class AlienMeteor(Meteor):
    def __init__(self, x, y, speed, img, hp, angle=None):
        super().__init__(x, y, speed, alien_meteor, hp, angle=None)
        self.img = alien_meteor_scale
        self.hp = 10000
        self.angle = random.randint(0, 360) if angle is None else angle
        self.mask = pygame.mask.from_surface(self.img)
    def __str__(self):
        return f"AlienMeteor({self.x}, {self.y}, {self.speed}, {self.img}, {self.hp}, {self.angle})"
class bloodyMeteor(Meteor):
    def __init__(self, x, y, speed, img, hp, angle=None):
        super().__init__(x, y, speed, bloody_meteor, hp, angle=None)
        self.img = bloody_meteor
        self.hp = 25
        self.angle = random.randint(0, 360) if angle is None else angle
        self.mask = pygame.mask.from_surface(self.img)
    def __str__(self):
        return f"bloodyMeteor({self.x}, {self.y}, {self.speed}, {self.img}, {self.hp}, {self.angle})"
class the_rockMeteor(Meteor):
    def __init__(self, x, y, speed, img, hp, angle=None):
        super().__init__(x, y, speed, the_rock, hp, angle=None)
        self.img = the_rock
        self.hp = 15
        self.angle = random.randint(0, 360) if angle is None else angle
        self.mask = pygame.mask.from_surface(self.img)
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
    def __init__(self, x, y, direction, speed, img, dmg, angle=0):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.img = img
        self.dmg = dmg
        self.angle = math.radians(angle)

    def lsr_update(self):
        if self.direction == -1:
            self.y -= self.speed
        else:
            self.x += self.speed * math.cos(self.angle)
            self.y += self.speed * math.sin(self.angle)
    def draw(self, screen):
        screen.blit(self.img, (self.x-5, self.y-5))


basic_lsr = (ship_rect.midtop, ship_rect.top+5, -1, 10, LASER)
lasers = []

def add_blt_speed(speed):
    for meteor in meteors:
        meteor.speed += speed
def add_blt_dmg(dmg):
    for laser in lasers:
        laser.dmg += dmg
def modif_blt_dmg(dmg):
    for laser in lasers:
        laser.dmg = dmg

def add_blt_reload(reload):
    global reload_time
    reload_time += reload
def dur_check():
    for laser in lasers:
        if laser.dmg == 2:
            laser.img = yellow_laser
        elif laser.dmg == 3:
            laser.img = white_laser
        elif laser.dmg == 4:
            laser.img = light_blue_laser
        elif laser.dmg == 5:
            laser.img = purple_laser
        elif laser.dmg > 5:
            laser.img = multi_laser


def shoot():
    if current_stage == "stock":
        lasers.append(Laser(ship_rect.centerx, ship_rect.top, -1, 10, LASER, 1))
    elif current_stage == "basic":
        lasers.append(Laser(ship_rect.centerx-30, ship_rect.top-20, -1, 10, LASER, 1))
        lasers.append(Laser(ship_rect.centerx+30, ship_rect.top-20, -1, 10, LASER, 1))
    elif current_stage == "middle":
        lasers.append(Laser(ship_rect.centerx, ship_rect.top-15, -1, 10, LASER, 1))
        lasers.append(Laser(ship_rect.centerx-20, ship_rect.top, -1, 10, LASER, 1))
        lasers.append(Laser(ship_rect.centerx+20, ship_rect.top, -1, 10, LASER, 1))
    elif current_stage == "better":
        lasers.append(Laser(ship_rect.centerx-40, ship_rect.top, -1, 10, LASER, 1))
        lasers.append(Laser(ship_rect.centerx+40, ship_rect.top, -1, 10, LASER, 1))
        lasers.append(Laser(ship_rect.centerx-20, ship_rect.top-20, -1, 10, LASER, 1))
        lasers.append(Laser(ship_rect.centerx+20, ship_rect.top-20, -1, 10, LASER, 1))
    elif current_stage == "way better":
        lasers.append(Laser(ship_rect.centerx-40, ship_rect.top, +3, 10, LASER, 1, -100))
        lasers.append(Laser(ship_rect.centerx+40, ship_rect.top, -3, 10, LASER, 1, -80))
        lasers.append(Laser(ship_rect.centerx-20, ship_rect.top-20, +2, 10, LASER, 1, -95))
        lasers.append(Laser(ship_rect.centerx+20, ship_rect.top-20, -2, 10, LASER, 1, -85))
        lasers.append(Laser(ship_rect.centerx, ship_rect.top-40, -1, 10, LASER, 1))
    elif current_stage == "good":
        lasers.append(Laser(ship_rect.centerx-60, ship_rect.top, +3, 10, LASER, 1, -100))
        lasers.append(Laser(ship_rect.centerx+60, ship_rect.top, -3, 10, LASER, 1, -80))
        lasers.append(Laser(ship_rect.centerx-40, ship_rect.top-20, +2, 10, LASER, 1, -95))
        lasers.append(Laser(ship_rect.centerx+40, ship_rect.top-20, -2, 10, LASER, 1, -85))
        lasers.append(Laser(ship_rect.centerx-20, ship_rect.top-40, +1, 10, LASER, 1, -90))
        lasers.append(Laser(ship_rect.centerx+20, ship_rect.top-40, -1, 10, LASER, 1, -90))
    elif current_stage == "better good":
        lasers.append(Laser(ship_rect.centerx-80, ship_rect.top, +3, 10, LASER, 1, -100))
        lasers.append(Laser(ship_rect.centerx+80, ship_rect.top, -3, 10, LASER, 1, -80))
        lasers.append(Laser(ship_rect.centerx-60, ship_rect.top-20, +2, 10, LASER, 1, -95))
        lasers.append(Laser(ship_rect.centerx+60, ship_rect.top-20, -2, 10, LASER, 1, -85))
        lasers.append(Laser(ship_rect.centerx-40, ship_rect.top-40, +1, 10, LASER, 1, -90))
        lasers.append(Laser(ship_rect.centerx+40, ship_rect.top-40, +1, 10, LASER, 1, -90))
        lasers.append(Laser(ship_rect.centerx-20, ship_rect.top-60, +1, 10, LASER, 1, -90))
        lasers.append(Laser(ship_rect.centerx+20, ship_rect.top-60, -1, 10, LASER, 1, -90))
    elif current_stage == "better better good":
        lasers.append(Laser(ship_rect.centerx-80, ship_rect.top, +3, 10, LASER, 1, -100))
        lasers.append(Laser(ship_rect.centerx+80, ship_rect.top, -3, 10, LASER, 1, -80))
        lasers.append(Laser(ship_rect.centerx-60, ship_rect.top-20, +2, 10, LASER, 1, -95))
        lasers.append(Laser(ship_rect.centerx+60, ship_rect.top-20, -2, 10, LASER, 1, -85))
        lasers.append(Laser(ship_rect.centerx-40, ship_rect.top-40, +1, 10, LASER, 1, -92.5))
        lasers.append(Laser(ship_rect.centerx+40, ship_rect.top-40, +1, 10, LASER, 1, -87.5))
        lasers.append(Laser(ship_rect.centerx-28, ship_rect.top-60, +1, 10, LASER, 1, -90))
        lasers.append(Laser(ship_rect.centerx+28, ship_rect.top-60, -1, 10, LASER, 1, -90))
        lasers.append(Laser(ship_rect.centerx, ship_rect.top-80, -1, 10, LASER, 1))
    elif current_stage == "better better better good":
        lasers.append(Laser(ship_rect.centerx-80, ship_rect.top, +3, 10, LASER, 1, -100))
        lasers.append(Laser(ship_rect.centerx+80, ship_rect.top, -3, 10, LASER, 1, -80))
        lasers.append(Laser(ship_rect.centerx-60, ship_rect.top-20, +2, 10, LASER, 1, -95))
        lasers.append(Laser(ship_rect.centerx+60, ship_rect.top-20, -2, 10, LASER, 1, -85))
        lasers.append(Laser(ship_rect.centerx-40, ship_rect.top-40, +1, 10, LASER, 1, -92.5))
        lasers.append(Laser(ship_rect.centerx+40, ship_rect.top-40, +1, 10, LASER, 1, -87.5))
        lasers.append(Laser(ship_rect.centerx-28, ship_rect.top-60, +1, 10, LASER, 1, -90))
        lasers.append(Laser(ship_rect.centerx+28, ship_rect.top-60, -1, 10, LASER, 1, -90))
        lasers.append(Laser(ship_rect.centerx-14, ship_rect.top-80, +1, 10, LASER, 1, -90))
        lasers.append(Laser(ship_rect.centerx+14, ship_rect.top-80, -1, 10, LASER, 1, -90))
        lasers.append(Laser(ship_rect.centerx, ship_rect.top-100, -1, 10, LASER, 1))
    elif current_stage == "great":
        lasers.append(Laser(ship_rect.centerx-100, ship_rect.top, +3, 10, LASER, 1, -100))
        lasers.append(Laser(ship_rect.centerx+100, ship_rect.top, -3, 10, LASER, 1, -80))
        lasers.append(Laser(ship_rect.centerx-80, ship_rect.top-20, +2, 10, LASER, 1, -95))
        lasers.append(Laser(ship_rect.centerx+80, ship_rect.top-20, -2, 10, LASER, 1, -85))
        lasers.append(Laser(ship_rect.centerx-60, ship_rect.top-40, +1, 10, LASER, 1, -92.5))
        lasers.append(Laser(ship_rect.centerx+60, ship_rect.top-40, +1, 10, LASER, 1, -87.5))
        lasers.append(Laser(ship_rect.centerx-40, ship_rect.top-60, +1, 10, LASER, 1, -90))
        lasers.append(Laser(ship_rect.centerx+40, ship_rect.top-60, -1, 10, LASER, 1, -90))
        lasers.append(Laser(ship_rect.centerx-20, ship_rect.top-80, +1, 10, LASER, 1, -90))
        lasers.append(Laser(ship_rect.centerx+20, ship_rect.top-80, -1, 10, LASER, 1, -90))
        lasers.append(Laser(ship_rect.centerx-14, ship_rect.top-80, +1, 10, LASER, 1, -90))
        lasers.append(Laser(ship_rect.centerx+14, ship_rect.top-80, -1, 10, LASER, 1, -90))
        lasers.append(Laser(ship_rect.centerx, ship_rect.top-100, -1, 10, LASER, 1))
    elif current_stage == "perfect":
        lasers.append(Laser(ship_rect.centerx-100, ship_rect.top, +3, 10, LASER, 1, -100))
        lasers.append(Laser(ship_rect.centerx+100, ship_rect.top, -3, 10, LASER, 1, -80))
        lasers.append(Laser(ship_rect.centerx-80, ship_rect.top-20, +2, 10, LASER, 1, -95))
        lasers.append(Laser(ship_rect.centerx+80, ship_rect.top-20, -2, 10, LASER, 1, -85))
        lasers.append(Laser(ship_rect.centerx-60, ship_rect.top-40, +1, 10, LASER, 1, -92.5))
        lasers.append(Laser(ship_rect.centerx+60, ship_rect.top-40, +1, 10, LASER, 1, -87.5))
        lasers.append(Laser(ship_rect.centerx-40, ship_rect.top-60, +1, 10, LASER, 1, -90))
        lasers.append(Laser(ship_rect.centerx+40, ship_rect.top-60, -1, 10, LASER, 1, -90))
        lasers.append(Laser(ship_rect.centerx-20, ship_rect.top-80, +1, 10, LASER, 1, -90))
        lasers.append(Laser(ship_rect.centerx+20, ship_rect.top-80, -1, 10, LASER, 1, -90))
        lasers.append(Laser(ship_rect.centerx-10, ship_rect.top-100, +1, 10, LASER, 1, -90))
        lasers.append(Laser(ship_rect.centerx+10, ship_rect.top-100, -1, 10, LASER, 1, -90))
        lasers.append(Laser(ship_rect.centerx, ship_rect.top-120, -1, 10, LASER, 1))
        lasers.append(Laser(ship_rect.centerx-120, ship_rect.top, +3, 10, LASER, 1, -100))
        lasers.append(Laser(ship_rect.centerx+120, ship_rect.top, -3, 10, LASER, 1, -80))


upgrade_stages = ["stock", "basic", "middle", "better", "way better", "good", "better good", "better better good", "better better better good", "great", "perfect"]

class Chest:
    def __init__(self, x, y, img=chest_scale):
        self.x = x
        self.y = y
        self.img = img
        
    def update(self):
        self.y += 1

    def create_chest(x, y, img=chest_scale):
        chest0 = Chest(x, y, img)
        chests.append(chest0)


chests = []
chest_effects = ["blt_speed", "blt_speed2", "blt_dmg", "blt_dmg2", "immortality", "stageup"]
point_memory = []


def save():
    save_file_name = "codes/save_file.txt"
    new_content = []
    
    try:
        with open(save_file_name, "r") as save_file:
            lines = save_file.readlines()

            for line in lines:
                global highscore
                if "highscore" in line:
                    if highscore > int(line.split("=")[1]):
                        modified_line = f"highscore={highscore}\n"
                        new_content.append(modified_line)
                        
                    else:
                        if highscore < int(line.split("=")[1]):
                            highscore = int(line.split("=")[1])
                            global test0
                            test0 = int(line.split("=")[1])   
                        new_content.append(line)
                elif "last_points" in line:
                    modified_line = f"last_points={last_points}\n"
                    new_content.append(modified_line)
                    global the_last_points
                    the_last_points = int(line.split("=")[1])
                else:
                    new_content.append(line)
    except FileNotFoundError:
        pass
    
    with open(save_file_name, "w") as save_file:
        save_file.writelines(new_content)



#sizes
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################

point_memory.append(test0)
while True:
    if MENU == False and SETTINGS == False and STOP == False:
        if sets.gameplay == "Mouse/Space" or sets.gameplay == "Mouse":
            pygame.mouse.set_visible(False) 
    else: pygame.mouse.set_visible(True)       
    
    
    # POINT MECHANISM
    
    points = add_points + alive_points
    
    if highscore < test0:
        highscore = test0
    if max(point_memory) > highscore:
        try: highscore = max(point_memory)
        except: pass
    if last_points == 0:
        last_points = the_last_points
    
    
    if MENU == False and SETTINGS == False and STOP == False and start_has_run == False:
        start_time = time.time() # reset start_time when game restarts
        try:last_points = point_memory[-1]
        except: pass                 
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
    if len(point_memory) > 100:
        point_memory.pop(0)
        
    
    # print(start, points, last_points)
    # print(point_memory)

    
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
                sets.difficulty = round(DIFFICULTY, 2)
                DIFFICULTY = round(DIFFICULTY, 2)
                if DIFFICULTY > 1.0 or sets.difficulty > 1.0:
                    DIFFICULTY = 0.05
                    sets.difficulty = 0.05
                difficulty0 = font1.render(f"Difficulty: {sets.difficulty} -> +0.05", True, "grey40")

        
        # MENU KEYBOARD SHORTCUTS

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and MENU == False:
            MENU = True
            SETTINGS = False
            STOP = False
            #print("r")
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s and MENU == True:
            MENU = False
            SETTINGS = False
            #print("s")
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e and MENU == True:
            #print("e")
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
                    sets.difficulty = round(DIFFICULTY, 2)
                    DIFFICULTY = round(DIFFICULTY, 2)
                    if DIFFICULTY < 0.05 or sets.difficulty < 0.05:
                        DIFFICULTY = 1.0
                        sets.difficulty = 1.0
                    difficulty0 = font1.render(f"Difficulty: {sets.difficulty} -> +0.05", True, "grey40")
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
                    sets.difficulty = round(DIFFICULTY, 2)
                    DIFFICULTY = round(DIFFICULTY, 2)
                    if DIFFICULTY > 1.0 or sets.difficulty > 1.0:
                        DIFFICULTY = 0.05
                        sets.difficulty = 0.05
                    difficulty0 = font1.render(f"Difficulty: {sets.difficulty} -> +0.05", True, "grey40")

        
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
    
    # SHIP BOUNDARIES
    if ship_rect.top < 0:
        ship_rect.top = 0
    if ship_rect.bottom > screen_height:
        ship_rect.bottom = screen_height
    if ship_rect.left < 0:
        ship_rect.left = 0
    if ship_rect.right > screen_width:
        ship_rect.right = screen_width
    
    
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

    

    # METEORS
    for meteor in meteors:
        if meteor.y > screen_height:
            meteors.remove(meteor)

    sum_value = sum(meteor_types_rate.values())
    
    # SPAWN METEORS
    try:
        if (time.time() - last_meteor_spawn_time)+DIFFICULTY > meteor_spawn_time and SETTINGS == False and MENU == False:
            
            current_meteor_rate_num = random.choice(range(0, sum_value+1))
            if current_meteor_rate_num in range(0, meteor_types_rate["basic"]):
                current_meteor = Meteor; hp = 1; speed = 5
        
            elif current_meteor_rate_num in range(meteor_types_rate["basic"], meteor_types_rate["mid"]+meteor_types_rate["basic"]):
                current_meteor = MidMeteor; hp = 2; speed = 5

            elif current_meteor_rate_num in range(meteor_types_rate["mid"], meteor_types_rate["speedy"]+meteor_types_rate["mid"]):
                current_meteor = SpeedyMeteor; hp = 1; speed = 10
            
            elif current_meteor_rate_num in range(meteor_types_rate["speedy"], meteor_types_rate["good"]+meteor_types_rate["speedy"]):
                current_meteor = GoodMeteor; hp = 3; speed = 5
            
            elif current_meteor_rate_num in range(meteor_types_rate["good"], meteor_types_rate["epic"]+meteor_types_rate["good"]):
                current_meteor = EpicMeteor; hp = 6; speed = 5
    
            elif current_meteor_rate_num in range(meteor_types_rate["epic"], meteor_types_rate["huge"]+meteor_types_rate["epic"]):
                current_meteor = HugeMeteor; hp = 8; speed = 5
                
            elif current_meteor_rate_num in range(meteor_types_rate["huge"], meteor_types_rate["legendary"]+meteor_types_rate["huge"]):
                current_meteor = LegendaryMeteor; hp = 10; speed = 5
                
            elif current_meteor_rate_num in range(meteor_types_rate["legendary"], meteor_types_rate["overpowered"]+meteor_types_rate["legendary"]):
                current_meteor = OverpoweredMeteor; hp = 30; speed = 5
                
            elif current_meteor_rate_num in range(meteor_types_rate["overpowered"], meteor_types_rate["alien"]+meteor_types_rate["overpowered"]):
                current_meteor = AlienMeteor; hp = 10000; speed = 5
            
            elif current_meteor_rate_num in range(meteor_types_rate["alien"], meteor_types_rate["bloody"]+meteor_types_rate["alien"]):
                current_meteor = bloodyMeteor; hp = 25; speed = 5
            
            elif current_meteor_rate_num in range(meteor_types_rate["bloody"], meteor_types_rate["the_rock"]+1+meteor_types_rate["bloody"]):
                current_meteor = the_rockMeteor; hp = 15; speed = 5
            
            
            meteors.append(current_meteor(random.randint(0, screen_width - meteor_rect.width), y-meteor_rect.height-300, #spawns above screen
                                        speed, rotation_meteor, hp))
            last_meteor_spawn_time = time.time()
    except: pass              

    # UPDATE AND DRAW METEORS
    for meteor in meteors:
        meteor.update()
        meteor.draw(screen)
        
    # DIFFICUTLTY SCALING
    if MENU == False and SETTINGS == False and STOP == False:
        if math.floor(points/100) > last_point_check:
            last_point_check = math.floor(points/100)
            meteor_types_rate["basic"] = meteor_types_rate["basic"] - 100
            meteor_types_rate["mid"] = meteor_types_rate["mid"] - 50
            meteor_types_rate["speedy"] = meteor_types_rate["speedy"] + 10
            meteor_types_rate["good"] = meteor_types_rate["good"] + 20
            meteor_types_rate["epic"] = meteor_types_rate["epic"] + 30
            meteor_types_rate["huge"] = meteor_types_rate["huge"] +40
            meteor_types_rate["legendary"] = meteor_types_rate["legendary"] + 10
            meteor_types_rate["overpowered"] = meteor_types_rate["overpowered"] + 6
            meteor_types_rate["alien"] = meteor_types_rate["alien"] + 7
            meteor_types_rate["bloody"] = meteor_types_rate["bloody"] + 8
            meteor_types_rate["the_rock"] = meteor_types_rate["the_rock"] + 9
        if meteor_types_rate["basic"] < 40:
            meteor_types_rate["basic"] = 120
        if meteor_types_rate["mid"] < 80:
            meteor_types_rate["mid"] = 150
        if meteor_types_rate["huge"] > 900:
            meteor_types_rate["huge"] = 700
        if meteor_types_rate["legendary"] > 1000:
            meteor_types_rate["legendary"] = 800
        if meteor_types_rate["overpowered"] > 1400:
            meteor_types_rate["overpowered"] = 1000
        if meteor_types_rate["alien"] > 1500:
            meteor_types_rate["alien"] = 900
        if meteor_types_rate["bloody"] > 1600:
            meteor_types_rate["bloody"] = 1000
        if meteor_types_rate["the_rock"] > 1700:
            meteor_types_rate["the_rock"] = 1100
        if meteor_types_rate["speedy"] > 2200:
            meteor_types_rate["speedy"] = 1000

        #debugging 
        # p = random.randint(0, 1000)
        # if p == 0:
        #     print(f" meteor_types_rate: {meteor_types_rate}")

    # AFTER GAME OVER METEOR TYPE RATES RESET
    if STOP == True:
        last_point_check = 0
        
        meteor_types_rate["basic"] = 10000
        meteor_types_rate["mid"] = 1000
        meteor_types_rate["speedy"] = 600
        meteor_types_rate["good"] = 100
        meteor_types_rate["epic"] = 50
        meteor_types_rate["huge"] = 10
        meteor_types_rate["legendary"] = 5
        meteor_types_rate["overpowered"] = 3
        meteor_types_rate["alien"] = 2
        meteor_types_rate["bloody"] = 1
        meteor_types_rate["the_rock"] = 1
    #print(meteor_types_rate["alien"])
    
    ### COLLISIONS
    #LASER AND METEOR
    for meteor in meteors:
        meteor_rect = pygame.Rect(meteor.x, meteor.y, meteor.img.get_width(), meteor.img.get_height())
        for lsr in lasers:
            lsr_rect = pygame.Rect(lsr.x, lsr.y, lsr.img.get_width(), lsr.img.get_height())
            if meteor_rect.colliderect(lsr_rect): 
                if meteor.hp >= 1:
                    meteor.hp = meteor.hp - lsr.dmg
                if meteor.hp <= 0:
                    try: meteors.remove(meteor)
                    except: pass
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
        if meteor_rect.colliderect(ship_rect) and imm == False:
            STOP = True
        meteor.angle = meteor.angle + 1
    

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
        lasers = []

    if MENU == False and SETTINGS == False and STOP == False:
        if math.floor(points/1000) > last_chest_spawn:
            Chest.create_chest(random.randint(0, screen_width - 40), -30, chest_scale)         
            last_chest_spawn = math.floor(points/1000)

        for chest in chests:
            chest_rect = pygame.Rect(chest.x, chest.y, 40, 40)
            chest.y += 1
            if chest_rect.colliderect(ship_rect):
                chest_picked_up = True
                chests.remove(chest)
                
                xx = random.choice(chest_effects)
                if xx == "blt_speed":
                    add_blt_speed(10)
                    add_blt_reload(-0.15)
                    add_blt_sp = True
                    imm = True
                    blt_speed_activation_time = time.time()
                    #print("blt_speed")
                    xx = "nothing"
                if xx == "blt_speed2":
                    add_blt_speed(10)
                    add_blt_reload(-0.15)
                    add_blt_sp2 = True
                    imm = True
                    blt_speed2_activation_time = time.time()
                    #print("blt_speed2")
                if xx == "blt_dmg":
                    the_blt_dmg = the_blt_dmg + 1
                    add_blt_dmg01 = True
                    show_blt_01 = time.time()
                    xx = "nothing"
                if xx == "blt_dmg2":
                    # add_blt_dmg(2)
                    add_blt_dmg02 = True
                    blt_dmg2_activation_time = time.time()
                    #print("dmg2")
                    xx = "nothing"
                if xx == "immortality":
                    immortality = True
                    immortality_time = time.time()
                    imm = True
                    #print("immortality")
                    xx = "nothing"
                if xx == "stageup":
                    try:current_stage = upgrade_stages[stage_selected_index+1]
                    except: pass
                    stage_selected_index = stage_selected_index + 1
                    xx = "nothing"

            if chest.y > screen_height:
                chests.remove(chest)
                chest_picked_up = False
            
            screen.blit(chest.img, (chest.x, chest.y))     
        
        #print(chest.x, chest.y)
        #print(f"{xx}")
        if blt_speed_activation_time + 3 < time.time() and add_blt_sp == True:
            imm = False

        if blt_speed2_activation_time + 3 < time.time() and add_blt_sp2 == True:
            imm = False

        if immortality == True and xx != "nothing":
            imm = True

        if blt_speed_activation_time + 10 < time.time() and add_blt_sp == True:
            add_blt_speed(-10)
            add_blt_reload(0.15)
            
        if blt_speed2_activation_time + 25 < time.time() and add_blt_sp2 == True:
            add_blt_speed(-10)
            add_blt_reload(0.15)
            
        if blt_dmg2_activation_time + 15 < time.time() and add_blt_dmg02 == True:
            modif_blt_dmg(the_blt_dmg-2)

        if immortality_time + 7 < time.time() and imm == True:
            pygame.draw.rect(screen, "red", ship_rect, 3)
            

        if chest_picked_up == False:
            if points/1000+200 > last_chest_spawn:
                chests.append(Chest(random.randint(0, screen_width - 40), random.randint(0, screen_height - 40), chest_scale))
                last_chest_spawn = points/1000
                chest_picked_up = None
        
    if add_blt_dmg01 == True:
        modif_blt_dmg(the_blt_dmg)
        if show_blt_01 + 3 > time.time():
            current_effect = font1.render("+1 laser damage (permanent)", True, "grey50")
            screen.blit(current_effect, (round(screen_width/2-current_effect.get_width()/2), 50))

    if add_blt_dmg02 == True:
        modif_blt_dmg(the_blt_dmg+2)
        if blt_dmg2_activation_time + 3 > time.time():
            current_effect = font1.render("+2 laser damage (15 seconds)", True, "grey50")
            screen.blit(current_effect, (round(screen_width/2-current_effect.get_width()/2), 50))
        if blt_dmg2_activation_time + 15 < time.time() < blt_dmg2_activation_time + 18:
            deactivated_effect = font1.render("(+2 laser dmg): Effect ended", True, "grey40")
            #screen.blit(deactivated_effect, (round(screen_width/2-current_effect.get_width()/2), 50))
            add_blt_dmg02 = False
            blit_deact = True
        if blit_deact == False:
            current_effect = None
            deactivated_effect = None
    if add_blt_sp == True:
        if blt_speed_activation_time + 3 > time.time():
            current_effect = font1.render("+5 laser speed (10 seconds)", True, "grey50")
            screen.blit(current_effect, (round(screen_width/2-current_effect.get_width()/2), 50))
        if blt_speed_activation_time + 10 < time.time() < blt_speed_activation_time + 13:
            deactivated_effect = font1.render("(+5 laser speed): Effect ended", True, "grey40")
            # screen.blit(deactivated_effect, (round(screen_width/2-current_effect.get_width()/2), 50))
            add_blt_sp = False
            blit_deact = True
        if blit_deact == False:
            current_effect = None
            deactivated_effect = None
    if add_blt_sp2 == True:
        if blt_speed2_activation_time + 3 > time.time():
            current_effect = font1.render("+5 laser speed<2> (25 seconds)", True, "grey50")
            screen.blit(current_effect, (round(screen_width/2-current_effect.get_width()/2), 50))
        if blt_speed2_activation_time + 25 < time.time() < blt_speed2_activation_time + 28:
            deactivated_effect = font1.render("(+5 laser speed<2>): Effect ended", True, "grey50")
            blit_deact_time = time.time()
            # screen.blit(deactivated_effect, (round(screen_width/2-current_effect.get_width()/2), 50))
            add_blt_sp2 = False
            blit_deact = True
        if blit_deact == False:
            current_effect = None
            deactivated_effect = None
    if imm == True:
        if immortality_time + 3 > time.time():
            current_effect = font1.render("Immortality (10 seconds)", True, "grey50")
            screen.blit(current_effect, (round(screen_width/2-current_effect.get_width()/2), 50))
        if immortality_time + 10 < time.time() < immortality_time + 13:
            deactivated_effect = font1.render("(Immortality):Effect ended", True, "grey50")
            blit_deact_time = time.time()
            # screen.blit(deactivated_effect, (round(screen_width/2-current_effect.get_width()/2), 50))
            imm = False
            blit_deact = True
        if blit_deact == False:
            current_effect = None
            deactivated_effect = None
    

    # EFFECT AND CHEST RESET
    if STOP == True or MENU == True or SETTINGS == True:
        reload_time = 0.2
        stage_selected_index = 0
        current_stage = upgrade_stages[stage_selected_index]
        current_effect = None
        deactivated_effect = None
        add_blt_dmg01 = False
        add_blt_dmg02 = False
        add_blt_sp = False
        add_blt_sp2 = False
        immortality = False
        imm = False
        blt_speed_activation_time = 0
        blt_speed2_activation_time = 0
        blt_dmg2_activation_time = 0
        immortality_time = 0
        last_chest_spawn = 0
        

    if STOP != True and blit_deact == True:
        try: screen.blit(deactivated_effect, (round(screen_width/2-deactivated_effect.get_width()/2), 50))
        except: pass
        
        if blit_deact_time + 3 < time.time():
            blit_deact = False

    # LASERS
    dur_check()
    for lsr in lasers:
        lsr.draw(screen)
        lsr.lsr_update()
        if lsr.y < 0:
            lasers.remove(lsr)

    # POINTS
    points0 = font1.render(f"Points: {points}", True, "grey40")
    last_points0 = font1.render(f"Last points: {last_points}", True, "grey40")
    highscore0 = font1.render(f"Highscore: {highscore}", True, "grey40")
    if MENU == False and SETTINGS == False and STOP == False:
        screen.blit(points0, (13,5))
        screen.blit(last_points0, (13, points0.get_height()+5))
        screen.blit(highscore0, (screen_width-highscore0.get_width()-SETTINGS_butt_scale.get_width()-50, 0))

    
    
#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#x#

    pygame.display.update()
    save()