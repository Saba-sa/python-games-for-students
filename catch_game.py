import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Falling Ball")

WHITE = (255, 255, 255)
DARK_BLUE = (20, 30, 60)
BLUE = (70, 150, 255)
YELLOW = (255, 210, 60)
RED = (240, 80, 90)

basket = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 70, 100, 25)
ball_radius = 15
ball_x = random.randint(ball_radius, WIDTH - ball_radius)
ball_y = -ball_radius
basket_speed = 7
ball_speed = 4
score = 0
misses = 0
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)
clock = pygame.time.Clock()
game_over = False

def reset_ball():
    """Return a new random ball position above the screen."""
    return random.randint(ball_radius, WIDTH - ball_radius), -ball_radius

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            score = 0
            misses = 0
            ball_speed = 4
            basket.x = WIDTH // 2 - 50
            ball_x, ball_y = reset_ball()
            game_over = False

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            basket.x -= basket_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            basket.x += basket_speed

        basket.x = max(0, min(WIDTH - basket.width, basket.x))
        ball_y += ball_speed

        ball_rect = pygame.Rect(
            ball_x - ball_radius, ball_y - ball_radius,
            ball_radius * 2, ball_radius * 2
        )

        if ball_rect.colliderect(basket):
            score += 1
            ball_speed = min(12, 4 + score // 3)
            ball_x, ball_y = reset_ball()
        elif ball_y - ball_radius > HEIGHT:
            misses += 1
            ball_x, ball_y = reset_ball()
            if misses >= 3:
                game_over = True

    screen.fill(DARK_BLUE)
    pygame.draw.circle(screen, YELLOW, (ball_x, int(ball_y)), ball_radius)
    pygame.draw.rect(screen, BLUE, basket, border_radius=10)

    screen.blit(font.render(f"Score: {score}", True, WHITE), (20, 20))
    screen.blit(small_font.render(f"Misses: {misses}/3", True, WHITE), (20, 60))

    if game_over:
        title = font.render("GAME OVER!", True, RED)
        restart = small_font.render(
            "Press R to play again or close the window to quit.", True, WHITE
        )
        screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
        screen.blit(restart, restart.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 25)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
