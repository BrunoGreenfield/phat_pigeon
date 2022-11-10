import pygame
from sys import exit

# Constants
FRAME_RATE = 60
HEIGHT = 600
WIDTH = 1200

# Classes
class Player(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    self.image = pygame.Surface((60, 60))
    self.image.fill((255, 0, 0))
    self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT//2))

    self.gravity = 0


  def player_input(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]: 
      self.gravity = -10
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
      self.gravity = 10

  def apply_gravity(self):
    global game_active
    self.gravity += 0.5
    self.rect.y += self.gravity
    if self.rect.bottom >= HEIGHT:
      self.rect.bottom = HEIGHT
    if self.rect.top <= 0:
      game_active = False

  def update(self):
    self.player_input()
    self.apply_gravity()


class Obstacle(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    self.image = pygame.Surface((60, 60))
    self.image.fill((0, 255, 0))
    self.rect = self.image.get_rect(midbottom=(WIDTH, HEIGHT//2))
  
  def update(self):
    self.rect.x -= 2
    if self.rect.right <= 0:
      self.kill()

# Functions
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle,False):
        obstacle.empty()
        return False
    else: return True

def update_fps():
	fps = str(int(clock.get_fps()))
	fps_text = pixel_font.render(f'FPS: {fps}', False, pygame.Color(64,64,64))
	return fps_text

def display_score():
    current_time = int((pygame.time.get_ticks() - start_time)/1000)
    score_surf = pixel_font.render(f'Score: {current_time}', False, pygame.Color(64,64,64))
    score_rect = score_surf.get_rect(center=(WIDTH/2, 50))
    screen.blit(score_surf, score_rect)
    return current_time


# Initialization and setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FAT PIGEON")

# Variables
clock = pygame.time.Clock()
start_time = 0
pixel_font = pygame.font.Font('font/pixel.ttf', 24)
game_active = True
score = 0

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle = pygame.sprite.Group()


# Game loop
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()
    if game_active:
      score = display_score()
  if game_active:
    display_score()
    
    screen.fill((255,255,255))
    screen.blit(update_fps(), (0,0))
    player.draw(screen)
    player.update()

    obstacle.draw(screen)
    obstacle.update()
    game_active = collision_sprite()
  else:
    screen.fill((255,255,255))
    score_message = pixel_font.render(f'Your scored: {score}', False, (255,0,0))
    score_message_rect = score_message.get_rect(center = (WIDTH/2, HEIGHT/2))
    screen.blit(score_message, score_message_rect)

  pygame.display.update()

  clock.tick(FRAME_RATE)