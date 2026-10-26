
import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter 🚀")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 32)
big_font = pygame.font.Font(None, 64)

BLACK = (10, 12, 35)
WHITE = (255, 255, 255)
CYAN = (50, 220, 255)
RED = (255, 75, 90)
YELLOW = (255, 220, 60)

player = pygame.Rect(375, 520, 50, 35)
bullets = []
enemies = []
stars = [
    (random.randrange(WIDTH), random.randrange(HEIGHT))
    for _ in range(80)
]

score = 0
lives = 3
spawn_timer = 0
shoot_delay = 0
game_over = False


def reset_game():
    global player, bullets, enemies
    global score, lives, spawn_timer, shoot_delay, game_over

    player = pygame.Rect(375, 520, 50, 35)
    bullets = []
    enemies = []
    score = 0
    lives = 3
    spawn_timer = 0
    shoot_delay = 0
    game_over = False


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

            if (
                not game_over
                and event.key == pygame.K_SPACE
                and shoot_delay == 0
            ):
                bullets.append(
                    pygame.Rect(
                        player.centerx - 4,
                        player.top - 15,
                        8,
                        20
                    )
                )
                shoot_delay = 12

    keys = pygame.key.get_pressed()

    if not game_over:
        # Move the spaceship
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x -= 6

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x += 6

        player.x = max(0, min(WIDTH - player.width, player.x))

        shoot_delay = max(0, shoot_delay - 1)

        # Create enemies
        spawn_timer += 1

        if spawn_timer >= 35:
            enemy_width = random.randint(30, 45)

            enemies.append(
                pygame.Rect(
                    random.randint(0, WIDTH - enemy_width),
                    -40,
                    enemy_width,
                    30
                )
            )

            spawn_timer = 0

        # Move bullets
        for bullet in bullets[:]:
            bullet.y -= 9

            if bullet.bottom < 0:
                bullets.remove(bullet)

        # Move enemies
        for enemy in enemies[:]:
            enemy.y += 3

            if enemy.top > HEIGHT:
                enemies.remove(enemy)
                lives -= 1

            elif enemy.colliderect(player):
                enemies.remove(enemy)
                lives -= 1

            if lives <= 0:
                game_over = True

        # Check bullet-enemy collisions
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if bullet.colliderect(enemy):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1
                    break

    # Draw the background
    screen.fill(BLACK)

    for star_x, star_y in stars:
        pygame.draw.circle(
            screen, WHITE, (star_x, star_y), 2
        )

    # Draw the spaceship
    pygame.draw.polygon(
        screen,
        CYAN,
        [
            (player.centerx, player.top - 12),
            (player.left, player.bottom),
            (player.centerx, player.bottom - 10),
            (player.right, player.bottom),
        ]
    )

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, YELLOW, bullet)

    # Draw enemy ships
    for enemy in enemies:
        pygame.draw.rect(
            screen, RED, enemy, border_radius=8
        )

    # Display score and lives
    screen.blit(
        font.render(f"Score: {score}", True, WHITE),
        (20, 20)
    )

    screen.blit(
        font.render(f"Lives: {lives}", True, WHITE),
        (20, 55)
    )

    screen.blit(
        font.render("Move: Arrows / A-D | Shoot: SPACE", True, WHITE),
        (20, HEIGHT - 35)
    )

    # Game-over screen
    if game_over:
        overlay = pygame.Surface(
            (WIDTH, HEIGHT), pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 190))
        screen.blit(overlay, (0, 0))

        title = big_font.render(
            "GAME OVER", True, RED
        )
        result = font.render(
            f"Final score: {score}", True, WHITE
        )
        restart = font.render(
            "Press R to restart | ESC to quit",
            True, WHITE
        )

        screen.blit(
            title,
            title.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 - 50)
            )
        )

        screen.blit(
            result,
            result.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 + 5)
            )
        )

        screen.blit(
            restart,
            restart.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 + 50)
            )
        )

    pygame.display.flip()

pygame.quit()
sys.exit()
