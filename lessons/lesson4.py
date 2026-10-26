
import pygame
import random

pygame.init()

# Window settings
WIDTH = 600
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Car Racing")

clock = pygame.time.Clock()

# Colors
GREEN = (30, 130, 50)
GRAY = (55, 55, 60)
WHITE = (255, 255, 255)
BLUE = (40, 140, 255)
RED = (240, 50, 60)
YELLOW = (255, 220, 50)
BLACK = (15, 15, 15)

font = pygame.font.SysFont("arial", 30, bold=True)
big_font = pygame.font.SysFont("arial", 50, bold=True)

# Road
ROAD_LEFT = 100
ROAD_WIDTH = 400

# Player car
CAR_WIDTH = 50
CAR_HEIGHT = 85

player_x = WIDTH // 2 - CAR_WIDTH // 2
player_y = HEIGHT - 120
player_speed = 7

# Enemy cars
enemies = []
enemy_speed = 5
spawn_timer = 0

# Game variables
score = 0
game_over = False
road_offset = 0


def draw_car(x, y, color):
    # Body
    pygame.draw.rect(
        screen, color,
        (x, y, CAR_WIDTH, CAR_HEIGHT),
        border_radius=8
    )

    # Windows
    pygame.draw.rect(
        screen, (180, 220, 245),
        (x + 9, y + 12, 32, 20),
        border_radius=4
    )

    pygame.draw.rect(
        screen, BLACK,
        (x + 9, y + 45, 32, 22),
        border_radius=4
    )

    # Wheels
    pygame.draw.rect(screen, BLACK, (x - 4, y + 12, 6, 20))
    pygame.draw.rect(screen, BLACK, (x + 48, y + 12, 6, 20))
    pygame.draw.rect(screen, BLACK, (x - 4, y + 55, 6, 20))
    pygame.draw.rect(screen, BLACK, (x + 48, y + 55, 6, 20))


def reset_game():
    global player_x, enemies, enemy_speed
    global spawn_timer, score, game_over, road_offset

    player_x = WIDTH // 2 - CAR_WIDTH // 2
    enemies = []
    enemy_speed = 5
    spawn_timer = 0
    score = 0
    game_over = False
    road_offset = 0


running = True

while running:
    clock.tick(60)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if game_over and event.key == pygame.K_r:
                reset_game()

    keys = pygame.key.get_pressed()

    if not game_over:

        # Move player
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= player_speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += player_speed

        # Keep car on road
        player_x = max(
            ROAD_LEFT + 10,
            min(ROAD_LEFT + ROAD_WIDTH - CAR_WIDTH - 10, player_x)
        )

        # Draw moving road effect
        road_offset = (road_offset + enemy_speed) % 80

        # Spawn enemy cars
        spawn_timer += 1

        if spawn_timer >= 50:
            lane = random.randint(0, 2)
            enemy_x = ROAD_LEFT + 35 + lane * 130

            enemies.append({
                "x": enemy_x,
                "y": -CAR_HEIGHT,
                "color": random.choice([RED, YELLOW, (180, 80, 230)])
            })

            spawn_timer = 0

        # Move enemy cars
        for enemy in enemies:
            enemy["y"] += enemy_speed

        # Remove passed cars and increase score
        remaining = []

        for enemy in enemies:
            if enemy["y"] > HEIGHT:
                score += 1
            else:
                remaining.append(enemy)

        enemies = remaining

        # Increase difficulty gradually
        enemy_speed = min(12, 5 + score // 5)

        # Collision detection
        player_rect = pygame.Rect(
            player_x + 5, player_y + 5,
            CAR_WIDTH - 10, CAR_HEIGHT - 10
        )

        for enemy in enemies:
            enemy_rect = pygame.Rect(
                enemy["x"] + 5, enemy["y"] + 5,
                CAR_WIDTH - 10, CAR_HEIGHT - 10
            )

            if player_rect.colliderect(enemy_rect):
                game_over = True

    # Draw background
    screen.fill(GREEN)

    # Draw road
    pygame.draw.rect(
        screen, GRAY,
        (ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT)
    )

    # Road borders
    pygame.draw.line(
        screen, WHITE,
        (ROAD_LEFT, 0), (ROAD_LEFT, HEIGHT), 5
    )

    pygame.draw.line(
        screen, WHITE,
        (ROAD_LEFT + ROAD_WIDTH, 0),
        (ROAD_LEFT + ROAD_WIDTH, HEIGHT), 5
    )

    # Lane markings
    for y in range(-80, HEIGHT, 80):
        line_y = y + road_offset

        pygame.draw.rect(
            screen, WHITE,
            (ROAD_LEFT + 130, line_y, 5, 40)
        )

        pygame.draw.rect(
            screen, WHITE,
            (ROAD_LEFT + 265, line_y, 5, 40)
        )

    # Draw cars
    draw_car(player_x, player_y, BLUE)

    for enemy in enemies:
        draw_car(enemy["x"], enemy["y"], enemy["color"])

    # Score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (15, 15))

    # Game over screen
    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        title = big_font.render("GAME OVER", True, RED)
        screen.blit(
            title,
            title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
        )

        final_score = font.render(
            f"Final Score: {score}", True, WHITE
        )
        screen.blit(
            final_score,
            final_score.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        )

        restart = font.render(
            "Press R to Restart", True, YELLOW
        )
        screen.blit(
            restart,
            restart.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 55))
        )

    pygame.display.flip()

pygame.quit()
