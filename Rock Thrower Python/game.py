import os
import sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import time
import random
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000,800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Thrower")

current_dir = os.path.dirname(__file__)



BG = pygame.transform.scale(pygame.image.load(os.path.join(current_dir, "BG.jpeg")), (WIDTH, HEIGHT))
PLAYER_IMAGE = pygame.image.load(os.path.join(current_dir, "slingshot.png")).convert_alpha()
ROCK_IMAGE = pygame.image.load(os.path.join(current_dir, "rock.png")).convert_alpha()
BIRD_IMAGE = pygame.image.load(os.path.join(current_dir, "bird.png")).convert_alpha()
pygame.mixer.music.load(os.path.join(current_dir, "background_music.mp3"))
rock_hit_sound = pygame.mixer.Sound(os.path.join(current_dir, "rockhit.wav"))

FONT = pygame.font.SysFont("comicsans", 30)

PLAYER_WIDTH = 60
PLAYER_HEIGHT = 80
PLAYER_VEL = 5

ROCK_HEIGHT = 30
ROCK_WIDTH = 30
ROCK_VEL = 5

BIRD_HEIGHT = 100
BIRD_WIDTH = 100
BIRD_VEL = 3

def draw(player, birds, level, rocks):
  WIN.blit(BG, (0, 0))
  WIN.blit(PLAYER_IMAGE, player)
  level_text = FONT.render(f"Level: {level}",1, "white")
  for bird in birds:
      WIN.blit(BIRD_IMAGE, bird)
  for rock in rocks:
      WIN.blit(ROCK_IMAGE, rock)
  WIN.blit(level_text, (10, 10))
  pygame.display.update()

def main():
  run = True
  player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
  clock = pygame.time.Clock()
  birds = []
  rocks = []
  rockcount = 0
  level = 0
  birdstoadd = 0
  birdsleft = 0
  pygame.mixer.music.play(-1)
  while run:
      clock.tick(60)
      if birdsleft == 0:
        level += 1
        birdstoadd = level+2
        birdsleft = birdstoadd

      for _ in range(birdstoadd):
          bird_x = random.randint(10, WIDTH - BIRD_WIDTH)
          bird = pygame.Rect(bird_x, 140, BIRD_WIDTH, BIRD_HEIGHT)
          birds.append(bird)
          if bird.colliderect(bird):
              random.randint(10, WIDTH - BIRD_WIDTH)
      birdstoadd = 0

      for rock in rocks[:]:
          rock.y -= ROCK_VEL
          if rock.y < 0:
              rocks.remove(rock)
              rockcount -= 1
          else:
              for bird in birds[:]:
                  if rock.colliderect(bird):
                      pygame.mixer.Sound.play(rock_hit_sound)
                      rocks.remove(rock)
                      birds.remove(bird)
                      birdsleft -= 1
                      rockcount -= 1
                      break

      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              run = False
              break

      keys = pygame.key.get_pressed()
      if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
          player.x -= PLAYER_VEL
      if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
          player.x += PLAYER_VEL
      if keys[pygame.K_SPACE] and rockcount == 0:
        rock_y = player.y + player.height - ROCK_HEIGHT + -30
        rock_x = player.x + player.width / 2 - ROCK_WIDTH / 2
        rock = pygame.Rect(rock_x, rock_y, ROCK_WIDTH, ROCK_HEIGHT)
        rocks.append(rock)
        rockcount += 1

      draw(player, birds, level, rocks)

  pygame.quit()

if __name__ == "__main__":
  main()
