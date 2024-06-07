import os
import sys
import pygame
import time
import random
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
current_dir = os.path.dirname(__file__)
BG = pygame.transform.scale(pygame.image.load(os.path.join(current_dir, "BG.jpeg")), (WIDTH, HEIGHT))
PLAYER_IMAGE = pygame.image.load(os.path.join(current_dir, "slingshot.png")).convert_alpha()
ROCK_IMAGE = pygame.image.load(os.path.join(current_dir, "rock.png")).convert_alpha()
BIRD_IMAGE = pygame.image.load(os.path.join(current_dir, "bird.png")).convert_alpha()
LIGHTNING_IMAGE = pygame.image.load(os.path.join(current_dir, "lightning.png")).convert_alpha()
pygame.mixer.music.load(os.path.join(current_dir, "background_music.mp3"))
rock_hit_sound = pygame.mixer.Sound(os.path.join(current_dir, "rockhit.wav"))
lightning_hit_sound = pygame.mixer.Sound(os.path.join(current_dir, "lightninghit.wav"))
pygame.display.set_caption(f"Rock Thrower")
pygame.display.set_icon(ROCK_IMAGE)


current_dir = os.path.dirname(__file__)


FONT = pygame.font.SysFont("comicsans", 30)
BIGFONT = pygame.font.SysFont("comicsans", 65)
PLAYER_WIDTH = 60
PLAYER_HEIGHT = 80
PLAYER_VEL = 5

ROCK_HEIGHT = 30
ROCK_WIDTH = 30
ROCK_VEL = 5

BIRD_HEIGHT = 100
BIRD_WIDTH = 100
BIRD_VEL = 3

LIGHTNING_HEIGHT = 35
LIGHTNING_WIDTH = 35
LIGHTNING_VEL = 5

ROCK_COOLDOWN = 500

def draw(player, birds, level, rocks, lightnings):
    WIN.blit(BG, (0, 0))
    WIN.blit(PLAYER_IMAGE, player)
    level_text = FONT.render(f"Level: {level}", 1, "white")
    for bird in birds:
        WIN.blit(BIRD_IMAGE, bird[0])
    for rock in rocks:
        WIN.blit(ROCK_IMAGE, rock)
    for lightning in lightnings:
        WIN.blit(LIGHTNING_IMAGE, lightning)
    WIN.blit(level_text, (10, 10))
    pygame.display.update()

def main():
    run = True
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    birds = []
    rocks = []
    lightnings = []
    rockcount = 0
    level = 0
    birdstoadd = 0
    birdsleft = 0
    LAST_ROCK_TIME = 0
    pygame.mixer.music.play(-1)

    while run:
        clock.tick(60)
        if birdsleft == 0:
            level += 1
            birdstoadd = level + 2
            birdsleft = birdstoadd
        if level == 10:
            WIN.blit(BIGFONT.render("You Win! Nice Job!", 1, "red"), (WIDTH/2 - 100, HEIGHT/2))
            pygame.display.update()
            time.sleep(5)
            run = False
            

        for _ in range(birdstoadd):
            bird_x = random.randint(10, WIDTH - BIRD_WIDTH)
            bird = pygame.Rect(bird_x, 140, BIRD_WIDTH, BIRD_HEIGHT)
            birds.append((bird, random.choice([-1, 1])))
            if bird.colliderect(bird):
                bird.x = random.randint(10, WIDTH - BIRD_WIDTH)
        birdstoadd = 0

        for rock in rocks[:]:
            rock.y -= ROCK_VEL
            if rock.y < 0:
                rocks.remove(rock)
                rockcount -= 1
            else:
                for bird in birds[:]:
                    if rock.colliderect(bird[0]):
                        pygame.mixer.Sound.play(rock_hit_sound)
                        rocks.remove(rock)
                        birds.remove(bird)
                        birdsleft -= 1
                        rockcount -= 1
                        break

        current_time = pygame.time.get_ticks()
        for i, bird in enumerate(birds):
            bird_rect, direction = bird
            bird_rect.x += direction * BIRD_VEL
            if bird_rect.left <= 0:
                direction = 1  
                bird_rect.left = 0  
            elif bird_rect.right >= WIDTH:
                direction = -1 
                bird_rect.right = WIDTH

            bird = (bird_rect, direction)
            birds[i] = bird
        if level >= 5:
         for bird in birds[:]:
             if random.randint(1,240) == 60:
                 lightning = pygame.Rect(bird[0].x, bird[0].y, LIGHTNING_WIDTH, LIGHTNING_HEIGHT)
                 lightnings.append(lightning)
        for lightning in lightnings[:]:
            lightning.y += LIGHTNING_VEL
            for rock in rocks[:]:
                if lightning.colliderect(rock):
                    pygame.mixer.Sound.play(lightning_hit_sound)
                    lightnings.remove(lightning)
                    rocks.remove(rock)
                    rockcount -= 1
                    break
            if lightning.colliderect(player):
                game_over_text = BIGFONT.render(f"Game Over! You made it to level {level}", 1, "red")
                pygame.mixer.Sound.play(lightning_hit_sound)
                lightnings.remove(lightning)
                WIN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
                pygame.display.update()
                time.sleep(4)
                run = False
            elif lightning.y > HEIGHT:
                lightnings.remove(lightning)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL
        if keys[pygame.K_SPACE] and rockcount < 3 and current_time - LAST_ROCK_TIME > ROCK_COOLDOWN:
            rock_y = player.y + player.height - ROCK_HEIGHT + -30
            rock_x = player.x + player.width / 2 - ROCK_WIDTH / 2
            rock = pygame.Rect(rock_x, rock_y, ROCK_WIDTH, ROCK_HEIGHT)
            rocks.append(rock)
            rockcount += 1
            LAST_ROCK_TIME = current_time

        draw(player, birds, level, rocks, lightnings)

    pygame.quit()

if __name__ == "__main__":
    main()
