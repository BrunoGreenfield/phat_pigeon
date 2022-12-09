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
        self.dedstate = 0
        self.phatness_level = phatness_level
        self.jump_sound = pygame.mixer.Sound("audio/jump2.wav")
        self.jump_sound.set_volume(0.2)
        self.dive_sound = pygame.mixer.Sound("audio/dive1.wav")
        self.dive_sound.set_volume(0.2)
        self.eat_sound = pygame.mixer.Sound("audio/eat1.wav")
        self.eat_sound.set_volume(0.3)
        self.death_sound = pygame.mixer.Sound("audio/death.wav")
        self.death_sound.set_volume(0.4)

        self.image = self.player_mid
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT // 2))
        self.gravity = 0

    def player_input(self):
        global mid_timer
        global soundstate

        mid_timer = pygame.USEREVENT + 3
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.image = self.player_jump
            if soundstate == 0:
                self.jump_sound.play()
            self.gravity = -self.jump_height
            pygame.time.set_timer(mid_timer, 300)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.image = self.player_dive
            if soundstate == 0:
                self.dive_sound.play()
            self.gravity = self.fall_speed
            pygame.time.set_timer(mid_timer, 200)
        if event.type == mid_timer:
            self.image = self.player_mid

    def collision_food(self):
        global game_active
        global soundstate
        global state
        global phatnesslevtxt

        if pygame.sprite.spritecollide(self, food, True):
            pigeon_eat(self.rect.x, self.rect.y)
            if soundstate == 0:
                self.eat_sound.play()
            self.jump_height -= PHATNESS_INCREASE
            self.fall_speed += PHATNESS_INCREASE
            phatnesslevtxt += 1
            self.dedstate +=1
            if state == 0:
                self.phatness_level += 1
                state += 1
            else:
                state -=1
            if self.phatness_level > 4:
                self.phatness_level = 4
            if self.dedstate == 8:
                pigeon_death(self.rect.x, self.rect.y)
                game_active = False
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
            if soundstate == 0:
                self.death_sound.play()
            self.kill()
            game_active = False
        else:
            move_background()
    
    def apply_gravity(self):
        global game_active
        global soundstate

        self.gravity += 0.5
        self.rect.y += self.gravity
        if self.rect.bottom >= HEIGHT - 31:
            if soundstate == 0:
                self.death_sound.play()
            pigeon_death(self.rect.x, self.rect.y)
            game_active = False
        if self.rect.top <= 0:
            pigeon_death(self.rect.x, self.rect.y)
            if soundstate == 0:
                self.death_sound.play()
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
        self.image = random.choice([pygame.image.load("graphics/obstacles/finished/landscape_boarder.png"),
                                    pygame.image.load("graphics/obstacles/finished/portrait_boarder.png")])
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

def move_background():
    global background_surf_rect
    global scroll
    scroll_num = 0
    while scroll_num < tiles:
        background_surf_rect = background_surf.get_rect(topleft = (scroll_num * background_surf.get_width() + scroll, 0))
        ground_surf_rect = ground_surf.get_rect(topleft = (scroll_num * ground_surf.get_width() + scroll, HEIGHT - ground_surf.get_height()))
        screen.blit(background_surf, background_surf_rect)
        screen.blit(ground_surf, ground_surf_rect)
        scroll_num += 1

    scroll -= 3

    if abs(scroll) > ground_surf.get_width():
        scroll = 0

def pigeon_eat(locationX, locationY):
    for i in range(30):
        square_size = random.randint(3,20)
        particles.append([[locationX, locationY, square_size, square_size],
                        5,
                        [(random.randint(-80, 80)/4), (random.randint(-80,80)/4)],
                        random.choice(['#408245', '#0bde1d', '#f2ff00'])])

def pigeon_death(locationX, locationY):
    for i in range(500):
        square_size = random.randint(5, 70)
        particles.append([[locationX, locationY, square_size, square_size], 
                        random.randint(4,6), 
                        [(random.randint(-80, 80)/6), (random.randint(-80,80)/6)], 
                        random.choice(['#ff8800','#ff5e00','#ff4400','#ff0000','#ffa200','#ffc800','#ffea00','#000000','#383636','#a3a3a3'])])


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

        particle[1] -= 0.03

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
pixel_font_small = pygame.font.Font('font/pixel.ttf', 16)
pixel_font_tiny = pygame.font.Font('font/pixel.ttf', 12)
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
player_mid_3_mainscreen = pygame.image.load("graphics/pigeon/finished/pigeon_mid3_fixed_mainscreen.png").convert_alpha()
music = pygame.image.load("graphics/music.png").convert_alpha()
music_rect = music.get_rect(center=(WIDTH - 75, 200))
no_music = pygame.image.load("graphics/no_music.png").convert_alpha()
no_music_rect = no_music.get_rect(center=(WIDTH - 75, 200))
state = 0

sound = [music, no_music]
sound_rect = [music_rect, no_music_rect]
soundstate = 0

soundtrack = pygame.mixer.Sound('audio/phat_pigeon_soundtrack1.wav')
soundtrack.set_volume(1)
soundtrack.play(-1)

leaderboardtxt = open("leaderboard.txt")
topscore = [68, 66, 64, 62, 60, 58, 56, 54, 52, 50, 48, 46, 44, 42, 40, 38, 36, 34, 32, 30, 28, 26, 24, 22, 20, 18, 16, 14, 12, 10, 8, 6, 4, 2, 0]

score_surf = pixel_font.render(f'Welcome to Phat pigeon... Python Edition!', False, pygame.Color('#d18100'))
score_surf_rect = score_surf.get_rect(center=(WIDTH / 2, 75))
instructions_surf = pixel_font_small.render('Press (up) or (W) to start and jump', False, pygame.Color('#b8b8b8'))
start_height = 125
instructions_surf_instu = pixel_font.render('How to play:', False, pygame.Color('#b8b8b8'))
instructions_surf_instu_rect = instructions_surf_instu.get_rect(center=(WIDTH / 2, HEIGHT-start_height-50))
instructions_surf_rect = instructions_surf.get_rect(center=(WIDTH / 2, HEIGHT-start_height))
instructions_surf_2 = pixel_font_small.render('Press (down) or (S) to dive down', False, pygame.Color('#b8b8b8'))
instructions_surf_2_rect = instructions_surf_2.get_rect(center=(WIDTH / 2, HEIGHT-start_height+25))
instructions_surf_3 = pixel_font_small.render('Avoid obstacles as they kill you instantly', False, pygame.Color('#b8b8b8'))
instructions_surf_3_rect = instructions_surf_3.get_rect(center=(WIDTH/2, HEIGHT-start_height+50))
instructions_surf_4 = pixel_font_small.render('Try to avoid food when possible as it increases your weight and decreases your jump ability', False, pygame.Color('#b8b8b8'))
instructions_surf_4_rect = instructions_surf_4.get_rect(center=(WIDTH/2, HEIGHT-start_height+75))
have_fun_surf = pixel_font_small.render('Have fun!', False, pygame.Color('#b8b8b8'))
have_fun_surf_rect  = have_fun_surf.get_rect(center=(WIDTH/2, HEIGHT-start_height+100))
art_credit = pixel_font_tiny.render('Art credit: @lg_purearts', False, pygame.Color('#b8b8b8'))
art_credit_rect = art_credit.get_rect(bottomleft=(3, HEIGHT-3))
me_plug = pixel_font_tiny.render('Programmed with blood, sweat and tears by me! (Bruno Greenfield (age: 15 years))', False, pygame.Color('#8cc9ff'))
me_plug_rect = me_plug.get_rect(center=(WIDTH/2, 385))
leaderboard = pixel_font_small.render('Top scores', False, pygame.Color('black'))
leaderboard_rect = leaderboard.get_rect(center=(75, 25))
leaderboard_1 = pixel_font_small.render(f'1. {topscore[0]}', False, pygame.Color('black'))
leaderboard_1_rect = leaderboard_1.get_rect(midleft=(25, 75))
leaderboard_2 = pixel_font_small.render(f'2. {topscore[1]}', False, pygame.Color('black'))
leaderboard_2_rect = leaderboard_2.get_rect(midleft=(25, 100))
leaderboard_3 = pixel_font_small.render(f'3. {topscore[2]}', False, pygame.Color('black'))
leaderboard_3_rect = leaderboard_3.get_rect(midleft=(25, 125))
leaderboard_4 = pixel_font_small.render(f'4: {topscore[3]}', False, pygame.Color('black'))
leaderboard_4_rect = leaderboard_4.get_rect(midleft=(25, 150))
leaderboard_5 = pixel_font_small.render(f'5: {topscore[4]}', False, pygame.Color('black'))
leaderboard_5_rect = leaderboard_4.get_rect(midleft=(25, 175))
leaderboard_6 = pixel_font_small.render(f'6: {topscore[5]}', False, pygame.Color('black'))
leaderboard_6_rect = leaderboard_4.get_rect(midleft=(25, 200))
leaderboard_7 = pixel_font_small.render(f'7: {topscore[6]}', False, pygame.Color('black'))
leaderboard_7_rect = leaderboard_4.get_rect(midleft=(25, 225))
leaderboard_8 = pixel_font_small.render(f'8: {topscore[7]}', False, pygame.Color('black'))
leaderboard_8_rect = leaderboard_4.get_rect(midleft=(25, 250))
leaderboard_9 = pixel_font_small.render(f'9: {topscore[8]}', False, pygame.Color('black'))
leaderboard_9_rect = leaderboard_4.get_rect(midleft=(25, 275))
leaderboard_10 = pixel_font_small.render(f'10: {topscore[9]}', False, pygame.Color('black'))
leaderboard_10_rect = leaderboard_4.get_rect(midleft=(25, 300))
leaderboard_11 = pixel_font_small.render(f'11: {topscore[10]}', False, pygame.Color('black'))
leaderboard_11_rect = leaderboard_4.get_rect(midleft=(25, 325))
leaderboard_12 = pixel_font_small.render(f'12: {topscore[11]}', False, pygame.Color('black'))
leaderboard_12_rect = leaderboard_4.get_rect(midleft=(25, 350))

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
phatnesslevtxt = 0

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sound_rect[soundstate].collidepoint(event.pos):
                    if soundstate == 0:
                        soundstate = 1
                        soundtrack.stop()
                    else:
                        soundstate = 0
                        soundtrack.play(-1)

    if game_active:
        player.update()
        player.draw(screen)

        display_score()
    
        screen.blit(update_fps(), (0, 0))

        food.draw(screen)
        food.update()
        obstacle.draw(screen)
        obstacle.update()       

        particle_update()

        screen.blit(display_score_text(), score_text_rect)
        if phatnesslevtxt == 0:
            phatness_display = 'None'
        elif phatnesslevtxt == 1:
            phatness_display = 'Tiny bit'
        elif phatnesslevtxt == 2:
            phatness_display = 'Not enough to worry about'
        elif phatnesslevtxt == 3:
            phatness_display = 'Maybe start worrying'
        elif phatnesslevtxt == 4:
            phatness_display = "Okay you've got some gurthe"
        elif phatnesslevtxt == 5:
            phatness_display = "You can denie it at this point"
        elif phatnesslevtxt == 6:
            phatness_display = 'Oh god...'
        elif phatnesslevtxt == 7:
            phatness_display = 'Eat one more, and pigeon go boom boom'
        else:
            phatness_display = 'should not be displayed'
        phatness_text = pixel_font.render(f'Phatness: {phatness_display}', False, pygame.Color('black'))
        phatness_text_rect = phatness_text.get_rect(center= (WIDTH/2, 25))
        screen.blit(phatness_text, phatness_text_rect)
    else:
        jump_height = 10
        fall_speed = 10

        screen.fill((64, 64, 64))
        pygame.draw.rect(screen, ('#387038'), (0, HEIGHT-200, WIDTH, HEIGHT))
        pygame.draw.rect(screen, ('#4685eb'), (0, 0, 150, 400))
        pygame.draw.rect(screen, ('#4685eb'), (WIDTH-150, 0, WIDTH-150, 400))
        screen.blit(sound[soundstate], sound_rect[soundstate])
        screen.blit(instructions_surf_instu, instructions_surf_instu_rect)
        screen.blit(instructions_surf, instructions_surf_rect)
        screen.blit(instructions_surf_2, instructions_surf_2_rect)
        screen.blit(instructions_surf_3, instructions_surf_3_rect)
        screen.blit(instructions_surf_4, instructions_surf_4_rect)
        screen.blit(have_fun_surf, have_fun_surf_rect)
        screen.blit(leaderboard, leaderboard_rect)
        screen.blit(leaderboard_1, leaderboard_1_rect)
        screen.blit(leaderboard_2, leaderboard_2_rect)
        screen.blit(leaderboard_3, leaderboard_3_rect)
        screen.blit(leaderboard_4, leaderboard_4_rect)
        screen.blit(leaderboard_5, leaderboard_5_rect)
        screen.blit(leaderboard_6, leaderboard_6_rect)
        screen.blit(leaderboard_7, leaderboard_7_rect)
        screen.blit(leaderboard_8, leaderboard_8_rect)
        screen.blit(leaderboard_9, leaderboard_9_rect)
        screen.blit(leaderboard_10, leaderboard_10_rect)
        screen.blit(leaderboard_11, leaderboard_11_rect)
        screen.blit(leaderboard_12, leaderboard_12_rect)

        if score == 0:
            screen.blit(player_mid_3_mainscreen, player_mid_3_mainscreen.get_rect(center = (WIDTH / 2, HEIGHT/2.4)))
            screen.blit(score_surf, score_surf_rect)
            screen.blit(art_credit, art_credit_rect)
            screen.blit(me_plug, me_plug_rect)

        else:
            screen.blit(player_mid_3_mainscreen, player_mid_3_mainscreen.get_rect(center = (WIDTH / 2, 175)))
            score_message = pixel_font.render(f'Your score: {score}', False, ('#b8b8b8'))
            score_message_rect = score_message.get_rect(center=(WIDTH / 2, 350))
            screen.blit(score_message, score_message_rect)
        
        particle_update()

    pygame.display.update()

    clock.tick(FRAME_RATE)
