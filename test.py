import pygame
import sys
import random
import math

# Function to display the score
def score_display():
    score_surface = game_font.render(f"Score: {score}", True, (255, 165, 0))
    score_rect = score_surface.get_rect(center=(150, 50))
    screen.blit(score_surface, score_rect)

# Function to display the game over screen
def game_over_display():
    game_over_surface = game_font.render("Game Over!", True, (255, 0, 0))
    game_over_rect = game_over_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(game_over_surface, game_over_rect)

    restart_surface = game_font.render("Press 'B' to Restart", True, (255, 165, 0))  
    restart_rect = restart_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(restart_surface, restart_rect)

    last_score_surface = game_font.render(f"Last Score: {score}", True, (0, 0, 0))
    last_score_rect = last_score_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(last_score_surface, last_score_rect)

# Initialize Pygame
pygame.init()

# Game window size
WIDTH, HEIGHT = 1920, 1080
WINDOW_SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
pygame.display.set_caption("Simple 2D Game")

# Background image
image = pygame.image.load('Vector illustration, blue sky with white clouds, as background or banner image, International Day of Clean Air for Blue Skies_.jpg')
image = pygame.transform.scale(image, WINDOW_SIZE)

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Load images
setting_image = pygame.image.load('setting.png')
setting_sound = pygame.image.load('sound.png')
setting_restart =  pygame.image.load('restart.png')
setting_exit =  pygame.image.load('exit.png')
putplay_image = pygame.image.load('putplay.png')

# Get rectangles for interactive images
putplay_rect = putplay_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
setting_rect = setting_image.get_rect(topright=(WIDTH - 50, 50))

# Load player and enemy images
play_bot = pygame.image.load('yellowbird-downflap.png')
play_top = pygame.image.load('yellowbird-upflap.png')
play_mid = pygame.image.load('yellowbird-midflap.png')
bird_list = [play_bot, play_mid, play_top]

bird_index = 0
bird = bird_list[bird_index]

def resize_images():
    global play_bot, play_top, play_mid, bird_list, bird, player_rect, enemy_image, bullet_image
    scale_factor = WIDTH / 1920  # Assuming 1920x1080 is the original resolution
    play_bot = pygame.transform.scale(bird_list[0], (int(50 * scale_factor), int(50 * scale_factor)))
    play_top = pygame.transform.scale(bird_list[1], (int(50 * scale_factor), int(50 * scale_factor)))
    play_mid = pygame.transform.scale(bird_list[2], (int(50 * scale_factor), int(50 * scale_factor)))
    bird_list = [play_bot, play_mid, play_top]
    bird = bird_list[bird_index]
    player_rect = play_bot.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    
    enemy_image = pygame.image.load('yellowbird-upflap.png').convert_alpha()
    enemy_image = pygame.transform.scale(enemy_image, (int(50 * scale_factor), int(50 * scale_factor)))
    
    bullet_image = pygame.Surface((int(10 * scale_factor), int(10 * scale_factor)))
    bullet_image.fill((0, 0, 255))

resize_images()
enemy_rect = enemy_image.get_rect(center=(random.randint(0, WIDTH), random.randint(0, HEIGHT)))

# Load sounds
shoot_sound = pygame.mixer.Sound('sfx_die.wav')
hit_sound = pygame.mixer.Sound('sfx_hit.wav')

# Movement speeds
player_speed = 5
enemy_speed = 3
bullet_speed = 8

# Score
# Font for score
game_font = pygame.font.Font('04B_19.TTF', 40)
score = 0
high_score = 0

# Health
health = 5

# Game over state
game_over = False
game_active = False
first_run = True

# List to store bullets (position and direction)
bullets = []

# List to store enemies
enemies = [enemy_image.get_rect(center=(random.randint(0, WIDTH), random.randint(0, HEIGHT)))]

# Function to shoot bullet
def shoot_bullet(target_pos):
    dx = target_pos[0] - player_rect.centerx
    dy = target_pos[1] - player_rect.centery
    distance = math.sqrt(dx ** 2 + dy ** 2)
    if distance != 0:
        dx /= distance
        dy /= distance

    bullet_rect = bullet_image.get_rect(center=player_rect.center)
    bullet_direction = (dx, dy)
    bullets.append((bullet_rect, bullet_direction))

# Function to draw health bar
def draw_health_bar():
    bar_width = 20
    bar_height = 10
    gap = 2
    total_width = (bar_width + gap) * health - gap
    x = player_rect.centerx - total_width // 2
    y = player_rect.top - 20

    for i in range(health):
        pygame.draw.rect(screen, RED, (x + i * (bar_width + gap), y, bar_width, bar_height))

def reset_game():
    global score, health, player_rect, bullets, moving_to_target, game_over, enemies, game_active
    score = 0
    health = 5
    player_rect.center = (WIDTH // 2, HEIGHT // 2)
    enemies = [enemy_image.get_rect(center=(random.randint(0, WIDTH), random.randint(0, HEIGHT)))]
    bullets = []
    moving_to_target = False
    game_over = False
    game_active = True

def show_settings_menu():
    global WIDTH, HEIGHT, WINDOW_SIZE, screen, image, player_rect,image, enemies,setting_sound,setting_restart,setting_exit

    setting = True

    setting_sound = pygame.transform.scale(setting_sound, (110, 110))
    setting_restart = pygame.transform.scale(setting_restart, (100, 100))
    setting_exit = pygame.transform.scale(setting_exit, (100, 100))

    setting_sound_rect = setting_sound.get_rect(center=(WIDTH // 2, HEIGHT // 2 -10))
    setting_restart_rect = setting_restart.get_rect(center=(WIDTH//2 -300 // 2, HEIGHT // 2 ))
    setting_exit_rect = setting_exit.get_rect(center=(WIDTH // 2 +175, HEIGHT // 2))

    while setting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if setting_sound_rect.collidepoint(mouse_pos):
                    # Handle sound setting
                    pass
                elif setting_restart_rect.collidepoint(mouse_pos):
                    reset_game()
                    setting = False
                elif setting_exit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        screen.blit(image, (0, 0))
        screen.blit(setting_sound, setting_sound_rect)
        screen.blit(setting_restart, setting_restart_rect)
        screen.blit(setting_exit, setting_exit_rect)

        pygame.display.flip()


def main():
    global score, health, game_over,first_run, bullets, player_rect, moving_to_target, target_x, target_y, bird_index, bird, enemies, game_active
    
    clock = pygame.time.Clock()
    moving_to_target = False
    flap_event = pygame.USEREVENT + 1
    pygame.time.set_timer(flap_event, 200)  # Change image every 200ms

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_b:
                    reset_game()
                elif game_active and not game_over:
                    if event.key == pygame.K_e:
                        mouse_pos = pygame.mouse.get_pos()
                        shoot_bullet(mouse_pos)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if putplay_rect.collidepoint(mouse_pos) and first_run:
                    reset_game()
                    first_run = False
                elif setting_rect.collidepoint(mouse_pos):
                    show_settings_menu()
                elif game_active and not game_over:
                    target_x, target_y = mouse_pos
                    moving_to_target = True

            elif event.type == flap_event and game_active:
                bird_index = (bird_index + 1) % len(bird_list)
                bird = bird_list[bird_index]

        if game_active and not game_over:
            # Move player towards target position
            if moving_to_target:
                dx = target_x - player_rect.centerx
                dy = target_y - player_rect.centery
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if distance > player_speed:
                    player_rect.x += player_speed * (dx / distance)
                    player_rect.y += player_speed * (dy / distance)
                else:
                    player_rect.center = (target_x, target_y)
                    moving_to_target = False

            # Move enemies towards player
            for enemy_rect in enemies:
                if enemy_rect.x < player_rect.x:
                    enemy_rect.x += enemy_speed
                elif enemy_rect.x > player_rect.x:
                    enemy_rect.x -= enemy_speed
                if enemy_rect.y < player_rect.y:
                    enemy_rect.y += enemy_speed
                elif enemy_rect.y > player_rect.y:
                    enemy_rect.y -= enemy_speed

                # Check collision between player and enemy
                if player_rect.colliderect(enemy_rect):
                    hit_sound.play()
                    score -= 1
                    health -= 1
                    if health <= 0:
                        game_over = True
                        game_active = False
                    enemy_rect.x = random.randint(0, WIDTH)
                    enemy_rect.y = random.randint(0, HEIGHT)

            # Check collision with window boundaries
            if player_rect.left < 0 or player_rect.right > WIDTH or player_rect.top < 0 or player_rect.bottom > HEIGHT:
                hit_sound.play()
                score -= 1
                health -= 1
                if health <= 0:
                    game_over = True
                    game_active = False
                player_rect.center = (WIDTH // 2, HEIGHT // 2)

            # Move and draw bullets
            for bullet in bullets:
                bullet_rect, bullet_direction = bullet
                bullet_rect.x += bullet_direction[0] * bullet_speed
                bullet_rect.y += bullet_direction[1] * bullet_speed

            # Check collision between bullets and enemies
            new_bullets = []
            for bullet_rect, bullet_direction in bullets:
                hit_any_enemy = False
                for enemy_rect in enemies:
                    if bullet_rect.colliderect(enemy_rect):
                        score += 1
                        shoot_sound.play()
                        enemy_rect.x = random.randint(0, WIDTH)
                        enemy_rect.y = random.randint(0, HEIGHT)
                        hit_any_enemy = True
                        if score % 10 == 0:
                            enemies.append(enemy_image.get_rect(center=(random.randint(0, WIDTH), random.randint(0, HEIGHT))))
                        break
                if not hit_any_enemy:
                    new_bullets.append((bullet_rect, bullet_direction))
            bullets = new_bullets

            # Remove bullets that are off-screen
            bullets = [(bullet_rect, bullet_direction) for bullet_rect, bullet_direction in bullets if 0 <= bullet_rect.x <= WIDTH and 0 <= bullet_rect.y <= HEIGHT]

        # Draw screen
        screen.blit(image, (0, 0))
        if game_active:
            screen.blit(bird, player_rect)
            for enemy_rect in enemies:
                screen.blit(enemy_image, enemy_rect)
            for bullet_rect, _ in bullets:
                screen.blit(bullet_image, bullet_rect)
            draw_health_bar()
            score_display()
        else:
            screen.blit(image, (0, 0))
            if first_run:  # Display "play" button only if it's the first run
                screen.blit(putplay_image, putplay_rect)
            else:
                game_over_display()

        # Always draw the setting image, ensuring it appears on top
        screen.blit(setting_image, setting_rect)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()