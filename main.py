# phat pigeon :D

import pygame, math
import random
from sys import exit
from random import randint

# Constants
FRAME_RATE = 60
HEIGHT = 600
WIDTH = 1200
PHATNESS_INCREASE = 1.25


# ********************************************************************************************#

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_dive_list = player_dive_list
        self.player_mid_list = player_mid_list
        self.player_jump_list = player_jump_list
        self.phatness_level = phatness_level
        self.player_dive = player_dive_list[phatness_level]
        self.player_mid = player_mid_list[phatness_level]
        self.player_jump = player_jump_list[phatness_level]
        self.jump_height = jump_height
        self.fall_speed = fall_speed
        self.phatness_level = phatness_level
        self.jump_sound = pygame.mixer.Sound("audio/jump1.wav")
        self.jump_sound.set_volume(0.3)

        self.image = self.player_mid
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT // 2))
        self.gravity = 0

    def player_input(self):
        global mid_timer
        mid_timer = pygame.USEREVENT + 3
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.image = self.player_jump
            self.jump_sound.play()
            self.gravity = -self.jump_height
            pygame.time.set_timer(mid_timer, 300)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.image = self.player_dive
            self.gravity = self.fall_speed
            pygame.time.set_timer(mid_timer, 200)
        if event.type == mid_timer:
            self.image = self.player_mid

    def collision_food(self):
        if pygame.sprite.spritecollide(self, food, True):
            pigeon_death(self.rect.x, self.rect.y)
            self.jump_height -= PHATNESS_INCREASE
            self.fall_speed += PHATNESS_INCREASE
            state = 0
            if state == 0:
                self.phatness_level += 1
                state += 1
            else:
                state -=1
            if self.phatness_level > 4:
                self.phatness_level = 4
            self.player_dive = self.player_dive_list[self.phatness_level]
            self.player_mid = self.player_mid_list[self.phatness_level]
            self.player_jump = self.player_jump_list[self.phatness_level]
            self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
            return True

        else:
            return False

    def collision_obstacle(self):
        global game_active
        if pygame.sprite.spritecollide(self, obstacle, False):
            pigeon_death(self.rect.x, self.rect.y)
            self.kill()
        else:
            move_background()
    
    def apply_gravity(self):
        global game_active

        self.gravity += 0.5
        self.rect.y += self.gravity
        if self.rect.bottom >= HEIGHT - 31:
            self.rect.bottom = HEIGHT - 31
        if self.rect.top <= 0:
            game_active = False

    def update(self):
        self.collision_obstacle()
        self.player_input()
        self.collision_food()
        self.apply_gravity()


# ********************************************************************************************#

# Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice([pygame.image.load("graphics/obstacles/finished/landscape_props.png"),
                                    pygame.image.load("graphics/obstacles/finished/portrait.png")])
        self.rect = self.image.get_rect(midbottom=(WIDTH, HEIGHT - randint(31, HEIGHT - 60)))

    def destroy(self):
        if self.rect.x <= -60:
            self.kill()

    def update(self):
        self.rect.x -= 4
        self.destroy()


# ********************************************************************************************#

# Food class
class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice([pygame.image.load("graphics/food/finished/burger.png"),
                                    pygame.image.load("graphics/food/finished/chips.png")])
        self.rect = self.image.get_rect(midbottom=(WIDTH, HEIGHT - randint(31, HEIGHT - 60)))

    def destroy(self):
        if self.rect.x <= -60:
            self.kill()
        if pygame.sprite.spritecollide(self, obstacle, False):
            self.kill()

    def update(self):
        self.rect.x -= 4
        self.destroy()

# ********************************************************************************************#

# Functions

# def collision_obstacle():
#     if pygame.sprite.spritecollide(player.sprite,obstacle, True):
#         pigeon_death(player.sprite.rect.x, player.sprite.rect.y)
#         return True
#     else:
#         return False

def move_background():
    global scroll
    global scroll_num

    scroll_num = 0
    while scroll_num < tiles:
        screen.blit(background_surf, (scroll_num * background_surf.get_width() + scroll, 0))
        screen.blit(ground_surf, (scroll_num * ground_surf.get_width() + scroll, HEIGHT - ground_surf.get_height()))
        scroll_num += 1

    scroll -= 3

    if abs(scroll) > ground_surf.get_width():
        scroll = 0

def pigeon_death(locationX, locationY):
    for i in range(30):
        square_size = random.randint(5, 30)
        particles.append([[locationX, locationY, square_size, square_size], 
                        random.randint(4,6), 
                        [random.randint(-10, 10), random.randint(-10,10)], 
                        random.choice([(255,136,0),(255,94,0),(255,68,0),(255,0,0),(255,162,0),(255,200,0),(255,234,0)])])

def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = pixel_font.render('FPS: {}'.format(fps), False, pygame.Color(64, 64, 64))
    return fps_text


def display_score():
    current_time = int((pygame.time.get_ticks() - start_time) / 1000)
    return current_time


def display_score_text():
    score_text = pixel_font.render('Score: {}'.format(display_score()), False, pygame.Color(64, 64, 64))
    return score_text

def particle_update():
    for particle in particles:
        particle[0][0] += particle[2][0]
        particle[0][1] += particle[2][1]
        
        if particle[2][0] > 0:
            particle[2][0] -= 0.1
        elif particle[2][0] < 0:
            particle[2][0] += 0.1
        
        if particle[2][1] > 0:
            particle[2][1] -= 0.1
        if particle[2][1] < 0:
            particle[2][1] += 0.15

        #particle[0][0] -= scroll
        particle[2][1] += 0.2

        pygame.draw.rect(screen, particle[3], particle[0], False)

        particle[1] -= 0.01

        if particle[1] <= 0:
            particles.remove(particle)

# ********************************************************************************************#

# Initialization and setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PHAT PIGEON")

# ********************************************************************************************#

# Variables
clock = pygame.time.Clock()
pixel_font = pygame.font.Font('font/pixel.ttf', 24)
ground_surf = pygame.image.load('graphics/Scenes/default_scene/floor_fixed2.png').convert_alpha()
background_surf = pygame.image.load('graphics/Scenes/default_scene/backgroundL_fixed.png').convert_alpha()
player_dive_1 = pygame.image.load("graphics/pigeon/finished/pigeon_dive1_fixed.png").convert_alpha()
player_dive_2 = pygame.image.load("graphics/pigeon/finished/pigeon_dive2_fixed.png").convert_alpha()
player_dive_3 = pygame.image.load("graphics/pigeon/finished/pigeon_dive3_fixed.png").convert_alpha()
player_dive_4 = pygame.image.load("graphics/pigeon/finished/pigeon_dive4_fixed.png").convert_alpha()
player_dive_5 = pygame.image.load("graphics/pigeon/finished/pigeon_dive5_fixed.png").convert_alpha()
player_mid_1 = pygame.image.load("graphics/pigeon/finished/pigeon_mid1_fixed.png").convert_alpha()
player_mid_2 = pygame.image.load("graphics/pigeon/finished/pigeon_mid2_fixed.png").convert_alpha()
player_mid_3 = pygame.image.load("graphics/pigeon/finished/pigeon_mid3_fixed.png").convert_alpha()
player_mid_4 = pygame.image.load("graphics/pigeon/finished/pigeon_mid4_fixed.png").convert_alpha()
player_mid_5 = pygame.image.load("graphics/pigeon/finished/pigeon_mid5_fixed.png").convert_alpha()
player_jump_1 = pygame.image.load("graphics/pigeon/finished/pigeon_jump1_fixed.png").convert_alpha()
player_jump_2 = pygame.image.load("graphics/pigeon/finished/pigeon_jump2_fixed.png").convert_alpha()
player_jump_3 = pygame.image.load("graphics/pigeon/finished/pigeon_jump3_fixed.png").convert_alpha()
player_jump_4 = pygame.image.load("graphics/pigeon/finished/pigeon_jump4_fixed.png").convert_alpha()
player_jump_5 = pygame.image.load("graphics/pigeon/finished/pigeon_jump5_fixed.png").convert_alpha()

player_dive_list = [player_dive_1, player_dive_2, player_dive_3, player_dive_4, player_dive_5]
player_mid_list = [player_mid_1, player_mid_2, player_mid_3, player_mid_4, player_mid_5]
player_jump_list = [player_jump_1, player_jump_2, player_jump_3, player_jump_4, player_jump_5]

phatness_level = 0

start_time = 0
game_active = False
score = 0
scroll = 0
scroll_num = 0
k = 0
spawn_speed = 1400
jump_height = 10
fall_speed = 10
original_player_y = 245
pigeon_deadness= False

# ********************************************************************************************#

# Other stuff goes here
score_text_rect = display_score_text().get_rect(center=(WIDTH - 120, 30))

tiles = math.ceil(WIDTH / background_surf.get_width()) + 1

# [location, velocity, timer, idek anymore]
particles = []

# ********************************************************************************************#

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle = pygame.sprite.Group()

food = pygame.sprite.Group()

# ********************************************************************************************#

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, spawn_speed)

food_timer = pygame.USEREVENT + 2
pygame.time.set_timer(food_timer, 1500)

# ********************************************************************************************#

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            score = display_score()
            if event.type == obstacle_timer:
                obstacle.add(Obstacle())
            if event.type == food_timer:
                food.add(Food())

        else:
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_UP) or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_w):
                game_active = True
                phatness_level = 0
                player.empty()
                player.add(Player())
                obstacle.empty()
                food.empty()
                start_time = pygame.time.get_ticks()
                score = 0

    if game_active:
        screen.fill((0, 0, 0))
        player.update()
        player.draw(screen)

        display_score()
        #collision_obstacle()


            # screen.fill((255,255,255))
        screen.blit(update_fps(), (0, 0))

        food.draw(screen)
        food.update()
        obstacle.draw(screen)
        obstacle.update()


        num = random.randint(0, 100)            

        particle_update()

        screen.blit(display_score_text(), score_text_rect)
    else:
        jump_height = 10
        fall_speed = 10

        if score == 0:
            screen.fill((255, 255, 255))
            score_surf = pixel_font.render('Press UP or w to start', False, pygame.Color(64, 64, 64))
            score_surf_rect = score_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            screen.blit(score_surf, score_surf_rect)
        else:
            screen.fill((255, 255, 255))
            score_message = pixel_font.render('Your scored: {}'.format(score), False, (64, 64, 64))
            score_message_rect = score_message.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            screen.blit(score_message, score_message_rect)

    pygame.display.update()

    clock.tick(FRAME_RATE)
