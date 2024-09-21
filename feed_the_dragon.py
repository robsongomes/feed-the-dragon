import pygame, random

pygame.init()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 400
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

VELOCITY = 5
FPS = 60
clock = pygame.time.Clock()

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Feed the Dragon")

# set fps and clock
FPS = 60
clock = pygame.time.Clock()

# set game values
PLAYER_STARTING_LIVES = 5
PLAYER_VELOCITY = 5
COIN_STARTING_VELOCITY = 5
COIN_ACCELERATION = .5
BUFFER_DISTANCE = 100

score = 0
player_lives = PLAYER_STARTING_LIVES
coin_velocity = COIN_STARTING_VELOCITY

# set colors
BACKGROUND_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 255, 0)
TEXT_BACKGROUND_COLOR = (10, 50, 10)

# set fonts
font = pygame.font.Font("attack_graffit.ttf", 32)

# set texts
score_text = font.render("Score: " + str(score), True, TEXT_COLOR)
score_rect = score_text.get_rect()
score_rect.topleft = (10, 10)

title_text = font.render("Feed the Dragon", True, TEXT_COLOR)
title_rect = title_text.get_rect()
title_rect.centerx = WINDOW_WIDTH // 2
title_rect.y = 10

lives_text = font.render("Lives: " + str(player_lives), True, TEXT_COLOR)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH - 10, 10)

game_over_text = font.render("GAME OVER", True, TEXT_COLOR)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

continue_text = font.render("Press any key to keep playing", True, TEXT_COLOR)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 32)

# set sound and music
back_music = pygame.mixer.Sound("music.wav")
coin_sound = pygame.mixer.Sound("coin.mp3")
miss_sound = pygame.mixer.Sound("miss.mp3")

pygame.mixer.music.load("music.wav")
pygame.mixer.music.play(-1)

# set images
player_image = pygame.image.load("dragon_right.png")
player_rect = player_image.get_rect()
player_rect.left = 32
player_rect.centery = WINDOW_HEIGHT // 2

coin_image = pygame.image.load("coin.png")
coin_rect = coin_image.get_rect()
coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
coin_rect.centery = random.randint(64, WINDOW_HEIGHT - 36)

running = True

def respawn_coin():
    coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
    coin_rect.centery = random.randint(64, WINDOW_HEIGHT - 36)

while running:
    for event in pygame.event.get():        
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP] and player_rect.top > 64:
        player_rect.top -= PLAYER_VELOCITY
    if keys[pygame.K_DOWN] and player_rect.bottom < WINDOW_HEIGHT:
        player_rect.bottom += PLAYER_VELOCITY

    coin_rect.x -= coin_velocity

    if coin_rect.x < 0:
        miss_sound.play()
        player_lives -= 1
        respawn_coin()
    
    if player_rect.colliderect(coin_rect):
        coin_sound.play()
        score += 1
        coin_velocity += COIN_ACCELERATION
        respawn_coin()

    lives_text = font.render("Lives: " + str(player_lives), True, TEXT_COLOR)
    score_text = font.render("Score: " + str(score), True, TEXT_COLOR)
    
    if player_lives == 0:
        is_game_over = True
        pygame.mixer.music.stop()
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()
        while is_game_over:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    is_game_over = False
                    score = 0
                    player_lives = PLAYER_STARTING_LIVES
                    coin_velocity = COIN_STARTING_VELOCITY
                    pygame.mixer.music.play(-1, 0.0)
                if event.type == pygame.QUIT:
                    is_game_over = False
                    running = False
            

    display_surface.fill(BACKGROUND_COLOR)

    display_surface.blit(score_text, score_rect)
    display_surface.blit(title_text, title_rect)
    display_surface.blit(lives_text, lives_rect)

    pygame.draw.line(display_surface, TEXT_COLOR, (0, 64), (WINDOW_WIDTH, 64), 2)

    display_surface.blit(player_image, player_rect)
    display_surface.blit(coin_image, coin_rect)

    pygame.display.update()
    clock.tick(FPS)


pygame.quit()