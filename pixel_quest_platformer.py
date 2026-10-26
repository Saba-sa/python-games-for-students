import pygame
import sys

# ------------------------------------------------------------
# PLATFORMER GAME: collect coins, jump over gaps, reach the flag
# Controls: Left/Right or A/D to move, Space/Up/W to jump
# R = restart, Esc = quit
# ------------------------------------------------------------

pygame.init()

WIDTH, HEIGHT = 960, 600
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Quest - Python Platformer")
clock = pygame.time.Clock()

# Colors
SKY = (135, 206, 235)
DARK_SKY = (70, 130, 180)
WHITE = (255, 255, 255)
BLACK = (25, 30, 45)
GREEN = (65, 180, 85)
DARK_GREEN = (35, 125, 60)
BROWN = (125, 80, 45)
GOLD = (255, 205, 50)
RED = (220, 65, 75)
BLUE = (55, 100, 220)
PURPLE = (120, 75, 180)

font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 24)
big_font = pygame.font.Font(None, 68)

# World layout. Platforms are rectangles: (x, y, width, height).
WORLD_WIDTH = 2400
GROUND_Y = 520
platforms = [
    pygame.Rect(0, GROUND_Y, 420, HEIGHT - GROUND_Y),
    pygame.Rect(500, GROUND_Y, 300, HEIGHT - GROUND_Y),
    pygame.Rect(880, GROUND_Y, 360, HEIGHT - GROUND_Y),
    pygame.Rect(1320, GROUND_Y, 300, HEIGHT - GROUND_Y),
    pygame.Rect(1700, GROUND_Y, 340, HEIGHT - GROUND_Y),
    pygame.Rect(2120, GROUND_Y, 280, HEIGHT - GROUND_Y),
    # Raised platforms
    pygame.Rect(250, 420, 120, 20),
    pygame.Rect(590, 410, 120, 20),
    pygame.Rect(960, 420, 130, 20),
    pygame.Rect(1130, 350, 120, 20),
    pygame.Rect(1430, 410, 120, 20),
    pygame.Rect(1800, 400, 130, 20),
    pygame.Rect(1990, 330, 100, 20),
]

coin_positions = [
    (290, 385), (630, 375), (1015, 385), (1185, 315),
    (1480, 375), (1850, 365), (2040, 295), (570, 475),
    (930, 475), (1370, 475), (1760, 475), (2160, 475)
]
GOAL_X = 2300
PLAYER_W, PLAYER_H = 34, 46
GRAVITY = 0.65
JUMP_SPEED = -13.5
MOVE_SPEED = 5


def make_coins():
    """Create coin rectangles from the saved coin positions."""
    return [pygame.Rect(x, y, 20, 20) for x, y in coin_positions]


def reset_game():
    """Reset player, coins, score, camera, and game state."""
    player = pygame.Rect(60, GROUND_Y - PLAYER_H, PLAYER_W, PLAYER_H)
    return player, 0.0, 0.0, make_coins(), 0, False, False


player, velocity_y, camera_x, coins, score, game_over, won = reset_game()
on_ground = False
running = True

while running:
    clock.tick(FPS)

    # ---- 1. Process events (quit, jump, restart) ----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if (game_over or won) and event.key == pygame.K_r:
                player, velocity_y, camera_x, coins, score, game_over, won = reset_game()
                on_ground = False

            if not game_over and not won and event.key in (
                pygame.K_SPACE, pygame.K_UP, pygame.K_w
            ) and on_ground:
                velocity_y = JUMP_SPEED
                on_ground = False

    keys = pygame.key.get_pressed()

    if not game_over and not won:
        # ---- 2. Move horizontally ----
        old_x = player.x
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x -= MOVE_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x += MOVE_SPEED
        player.x = max(0, min(WORLD_WIDTH - PLAYER_W, player.x))

        # ---- 3. Apply gravity and resolve vertical collisions ----
        velocity_y += GRAVITY
        velocity_y = min(velocity_y, 15)
        player.y += int(velocity_y)
        on_ground = False

        for platform in platforms:
            if player.colliderect(platform):
                # Falling onto a platform
                if velocity_y >= 0 and player.bottom - velocity_y <= platform.top + 2:
                    player.bottom = platform.top
                    velocity_y = 0
                    on_ground = True
                # Hitting the underside of a platform while jumping
                elif velocity_y < 0 and player.top - velocity_y >= platform.bottom - 2:
                    player.top = platform.bottom
                    velocity_y = 0

        # ---- 4. Collect coins ----
        for coin in coins[:]:
            if player.colliderect(coin):
                coins.remove(coin)
                score += 1

        # ---- 5. Win or fall off the world ----
        if player.x >= GOAL_X:
            won = True
        if player.top > HEIGHT + 100:
            game_over = True

        # ---- 6. Follow the player with a scrolling camera ----
        camera_x = max(0, min(WORLD_WIDTH - WIDTH, player.centerx - WIDTH // 2))

    # ---- Draw everything ----
    screen.fill(SKY)

    # Clouds (drawn in world coordinates, so they scroll)
    for cx, cy in [(100, 100), (390, 150), (760, 90), (1100, 130),
                   (1460, 85), (1820, 140), (2200, 90)]:
        sx = int(cx - camera_x * 0.35)
        pygame.draw.circle(screen, WHITE, (sx, cy), 22)
        pygame.draw.circle(screen, WHITE, (sx + 24, cy - 8), 28)
        pygame.draw.circle(screen, WHITE, (sx + 48, cy), 21)

    # Platforms and grass
    for platform in platforms:
        screen_rect = pygame.Rect(
            int(platform.x - camera_x), platform.y, platform.width, platform.height
        )
        pygame.draw.rect(screen, BROWN, screen_rect)
        pygame.draw.rect(screen, GREEN, (screen_rect.x, screen_rect.y,
                                         screen_rect.width, 7))

    # Coins
    for coin in coins:
        pygame.draw.circle(
            screen, GOLD,
            (int(coin.centerx - camera_x), coin.centery),
            coin.width // 2
        )
        pygame.draw.circle(
            screen, WHITE,
            (int(coin.centerx - camera_x - 3), coin.centery - 3), 3
        )

    # Goal flag
    flag_x = int(GOAL_X - camera_x)
    pygame.draw.line(screen, BLACK, (flag_x, GROUND_Y - 90), (flag_x, GROUND_Y), 5)
    pygame.draw.polygon(
        screen, RED,
        [(flag_x + 2, GROUND_Y - 88),
         (flag_x + 65, GROUND_Y - 70),
         (flag_x + 2, GROUND_Y - 52)]
    )

    # Player character and simple face
    player_screen = pygame.Rect(
        int(player.x - camera_x), player.y, player.width, player.height
    )
    pygame.draw.rect(screen, BLUE, player_screen, border_radius=7)
    pygame.draw.circle(screen, WHITE, (player_screen.x + 23, player_screen.y + 13), 5)
    pygame.draw.circle(screen, BLACK, (player_screen.x + 24, player_screen.y + 13), 2)

    # HUD
    screen.blit(font.render(f"Coins: {score}/{len(coin_positions)}", True, BLACK), (20, 18))
    screen.blit(small_font.render("Move: A/D or arrows   Jump: Space/W/Up", True, BLACK), (20, 54))
    screen.blit(small_font.render("Reach the red flag!   Restart: R   Quit: Esc", True, BLACK), (20, 80))

    if game_over or won:
        shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        shade.fill((15, 20, 35, 185))
        screen.blit(shade, (0, 0))
        if won:
            title = big_font.render("YOU WIN!", True, GOLD)
            message = font.render(f"You collected {score} coins!", True, WHITE)
        else:
            title = big_font.render("GAME OVER", True, RED)
            message = font.render("You fell! Try again.", True, WHITE)
        restart = font.render("Press R to play again or Esc to quit", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
        screen.blit(message, message.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 5)))
        screen.blit(restart, restart.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 55)))

    pygame.display.flip()

pygame.quit()
sys.exit()
