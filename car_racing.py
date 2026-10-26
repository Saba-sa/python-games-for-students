
import pygame
import random
import sys

pygame.init()

# Screen settings
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing Game")

clock = pygame.time.Clock()

# Colors
GREEN = (30, 130, 55)
DARK_GREEN = (20, 100, 40)
GRAY = (55, 55, 60)
WHITE = (255, 255, 255)
RED = (240, 50, 60)
BLUE = (40, 150, 255)
YELLOW = (255, 220, 50)
BLACK = (15, 15, 15)

font = pygame.font.SysFont("arial", 30, bold=True)
big_font = pygame.font.SysFont("arial", 48, bold=True)

# Road settings
ROAD_LEFT = 70
ROAD_RIGHT = 430
LANE_WIDTH = 120

# Player car
car_width = 48
car_height = 85
player_x = WIDTH // 2 - car_width // 2
player_y = HEIGHT - 125
player_speed = 7

# Enemy cars
enemies = []
enemy_speed = 5
spawn_timer = 0

# Game state
score = 0
game_over = False
road_line_y = 0


def draw_car(x, y, color):
    # Car body
    pygame.draw.rect(
        screen, color,
        (x, y, car_width, car_height),
        border_radius=9
    )

    # Windows
    pygame.draw.rect(
        screen, (170, 220, 245),
        (x + 9, y + 12, car_width - 18, 22),
        border_radius=4
    )
    pygame.draw.rect(
        screen, (30, 40, 55),
        (x + 9, y + 43, car_width - 18, 22),
        border_radius=4
    )

    # Wheels
    pygame.draw.rect(screen, BLACK, (x - 5, y + 12, 7, 20))
    pygame.draw.rect(screen, BLACK, (x + car_width - 2, y + 12, 7, 20))
    pygame.draw.rect(screen, BLACK, (x - 5, y + 55, 7, 20))
    pygame.draw.rect(screen, BLACK, (x + car_width - 2, y + 55, 7, 20))

    # Headlights
    pygame.draw.rect(screen, YELLOW, (x + 5, y + 3, 10, 5))
    pygame.draw.rect(
        screen, YELLOW,
        (x + car_width - 15, y + 3, 10, 5)
    )


def reset_game():
    global player_x, enemies, enemy_speed
    global spawn_timer, score, game_over, road_line_y

    player_x = WIDTH // 2 - car_width // 2
    enemies = []
    enemy_speed = 5
    spawn_timer = 0
    score = 0
    game_over = False
    road_line_y = 0


def draw_road():
    global road_line_y

    screen.fill(GREEN)

    # Road
    pygame.draw.rect(
        screen, GRAY,
        (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, HEIGHT)
    )

    # Road edges
    pygame.draw.rect(screen, WHITE, (ROAD_LEFT, 0, 5, HEIGHT))
    pygame.draw.rect(screen, WHITE, (ROAD_RIGHT - 5, 0, 5, HEIGHT))

    # Moving lane markings
    for y in range(-60, HEIGHT, 100):
        pygame.draw.rect(
            screen, WHITE,
            (ROAD_LEFT + 120, y + road_line_y, 5, 55)
        )
        pygame.draw.rect(
            screen, WHITE,
            (ROAD_LEFT + 240, y + road_line_y, 5, 55)
        )

    road_line_y = (road_line_y + enemy_speed) % 100


def draw_text(text, font_obj, color, x, y):
    image = font_obj.render(text, True, color)
    screen.blit(image, image.get_rect(center=(x, y)))


# Main game loop
running = True

while running:
    clock.tick(60)

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
        # Player movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= player_speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += player_speed

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_y -= player_speed

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_y += player_speed

        # Keep player on the road
        player_x = max(
            ROAD_LEFT + 8,
            min(ROAD_RIGHT - car_width - 8, player_x)
        )
        player_y = max(10, min(HEIGHT - car_height - 10, player_y))

        # Spawn enemy cars
        spawn_timer += 1

        if spawn_timer >= max(22, 55 - score // 5):
            enemy_x = random.choice([
                ROAD_LEFT + 35,
                ROAD_LEFT + 155,
                ROAD_LEFT + 275
            ])

            enemies.append({
                "x": enemy_x,
                "y": -car_height,
                "color": random.choice([
                    RED, BLUE, YELLOW, (180, 80, 230)
                ])
            })

            spawn_timer = 0

        # Move enemy cars
        for enemy in enemies:
            enemy["y"] += enemy_speed

        # Remove cars that leave the screen
        remaining = []

        for enemy in enemies:
            if enemy["y"] > HEIGHT:
                score += 1
            else:
                remaining.append(enemy)

        enemies = remaining

        # Increase difficulty
        enemy_speed = min(13, 5 + score // 10)

        # Collision detection
        player_rect = pygame.Rect(
            player_x + 5, player_y + 5,
            car_width - 10, car_height - 10
        )

        for enemy in enemies:
            enemy_rect = pygame.Rect(
                enemy["x"] + 5, enemy["y"] + 5,
                car_width - 10, car_height - 10
            )

            if player_rect.colliderect(enemy_rect):
                game_over = True

    # Draw everything
    draw_road()

    draw_car(player_x, player_y, BLUE)

    for enemy in enemies:
        draw_car(enemy["x"], enemy["y"], enemy["color"])

    # Score display
    pygame.draw.rect(screen, BLACK, (10, 10, 155, 45),
                     border_radius=8)
    draw_text(f"Score: {score}", font, WHITE, 87, 32)

    if game_over:
        # Dark overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        draw_text("GAME OVER", big_font, RED, WIDTH // 2, 270)
        draw_text(f"Final Score: {score}", font, WHITE,
                  WIDTH // 2, 330)
        draw_text("Press R to Restart", font, YELLOW,
                  WIDTH // 2, 390)
        draw_text("Press ESC to Quit", font, WHITE,
                  WIDTH // 2, 435)

    pygame.display.flip()

pygame.quit()
sys.exit()
