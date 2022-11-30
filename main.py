# phat pigeon :D

import pygame, math
from sys import exit
from random import randint

# Constants
FRAME_RATE = 60
HEIGHT = 600
WIDTH = 1200
PHATNESS_INCREASE = 0.5


# ********************************************************************************************#

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_dive_1 = player_dive_1
        self.player_mid_1 = player_mid_1
        self.player_jump_1 = player_jump_1

        self.image = self.player_mid_1
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT // 2))
        self.gravity = 0

    def player_input(self):
        global mid_timer
        mid_timer = pygame.USEREVENT + 3
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.image = self.player_jump_1
            self.gravity = -jump_height
            pygame.time.set_timer(mid_timer, 400)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.image = self.player_dive_1
            self.gravity = fall_speed
            pygame.time.set_timer(mid_timer, 200)
        if event.type == mid_timer:
            self.image = self.player_mid_1

    def apply_gravity(self):
        global game_active

        self.gravity += 0.5
        self.rect.y += self.gravity
        if self.rect.bottom >= HEIGHT - 31:
            self.rect.bottom = HEIGHT - 31
        if self.rect.top <= 0:
            game_active = False

    def update(self):
        self.player_input()
        self.apply_gravity()


# ********************************************************************************************#

# Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((60, 60))
        self.image.fill((0, 255, 0))
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
        self.image = pygame.Surface((60, 60))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(midbottom=(WIDTH, HEIGHT - randint(31, HEIGHT - 60)))

    def destroy(self):
        global food_collision
        if self.rect.x <= -60:
            self.kill()
        if pygame.sprite.spritecollide(self, obstacle, False):
            self.kill()

    def update(self):
        self.rect.x -= 4
        self.destroy()


# ********************************************************************************************#

# Collisions
def collision_obstacle():
    if pygame.sprite.spritecollide(player.sprite, obstacle, False):
        obstacle.empty()
        return False  # This needs to be false to stop the game
    else:
        return True


def collision_food():
    global jump_height
    global fall_speed
    global PHATNESS_INCREASE

    if pygame.sprite.spritecollide(player.sprite, food, True):
        jump_height -= PHATNESS_INCREASE
        fall_speed += PHATNESS_INCREASE
        return True

    else:
        return False


# ********************************************************************************************#

# Functions
def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = pixel_font.render(f'FPS: {fps}', False, pygame.Color(64, 64, 64))
    return fps_text


def display_score():
    current_time = int((pygame.time.get_ticks() - start_time) / 1000)
    return current_time


def display_score_text():
    score_text = pixel_font.render(f'Score: {display_score()}', False, pygame.Color(64, 64, 64))
    return score_text


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
player_mid_1 = pygame.image.load("graphics/pigeon/finished/pigeon_mid1_fixed.png").convert_alpha()
player_jump_1 = pygame.image.load("graphics/pigeon/finished/pigeon_jump1_fixed.png").convert_alpha()
player_dive_1 = pygame.image.load("graphics/pigeon/finished/pigeon_dive1_fixed.png").convert_alpha()
start_time = 0
game_active = False
score = 0
scroll = 0
k = 0
spawn_speed = 1400
jump_height = 10
fall_speed = 10
original_player_y = 245

# ********************************************************************************************#

# Other stuff goes here
score_text_rect = display_score_text().get_rect(center=(WIDTH - 120, 30))

tiles = math.ceil(WIDTH / background_surf.get_width()) + 1

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
            # if event.type == mid_timer:
            #     player.sprite.image = player_mid_1

        else:
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_UP) or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_w):
                game_active = True
                player.empty()
                player.add(Player())
                obstacle.empty()
                food.empty()
                start_time = pygame.time.get_ticks()
                score = 0

    if game_active:
        screen.fill((0, 0, 0))
        display_score()
        collision_food()
        i = 0
        while i < tiles:
            screen.blit(background_surf, (i * background_surf.get_width() + scroll, 0))
            screen.blit(ground_surf, (i * ground_surf.get_width() + scroll, HEIGHT - ground_surf.get_height()))
            i += 1

        scroll -= 3

        if abs(scroll) > ground_surf.get_width():
            scroll = 0

            # screen.fill((255,255,255))
        screen.blit(update_fps(), (0, 0))

        food.draw(screen)
        food.update()
        obstacle.draw(screen)
        obstacle.update()

        game_active = collision_obstacle()

        player.draw(screen)
        player.update()

        screen.blit(display_score_text(), score_text_rect)
    else:
        jump_height = 10
        fall_speed = 10

        if score == 0:
            screen.fill((255, 255, 255))
            score_surf = pixel_font.render(f'Press UP or w to start', False, pygame.Color(64, 64, 64))
            score_surf_rect = score_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            screen.blit(score_surf, score_surf_rect)
        else:
            screen.fill((255, 255, 255))
            score_message = pixel_font.render(f'Your scored: {score}', False, (64, 64, 64))
            score_message_rect = score_message.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            screen.blit(score_message, score_message_rect)

    pygame.display.update()

    clock.tick(FRAME_RATE)
