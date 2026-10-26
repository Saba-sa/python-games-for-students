import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
CELL = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - Python + Pygame")

BLACK = (18, 22, 30)
GREEN = (70, 220, 120)
DARK_GREEN = (35, 150, 85)
RED = (245, 80, 90)
WHITE = (245, 245, 245)
GRAY = (65, 75, 90)

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 64)

def new_food(snake):
    while True:
        food = (
            random.randrange(0, WIDTH, CELL),
            random.randrange(0, HEIGHT, CELL),
        )
        if food not in snake:
            return food

def reset_game():
    snake = [(WIDTH // 2, HEIGHT // 2),
             (WIDTH // 2 - CELL, HEIGHT // 2),
             (WIDTH // 2 - 2 * CELL, HEIGHT // 2)]
    direction = (CELL, 0)
    food = new_food(snake)
    score = 0
    return snake, direction, food, score, False

snake, direction, food, score, game_over = reset_game()
move_event = pygame.USEREVENT + 1
pygame.time.set_timer(move_event, 120)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if game_over and event.key == pygame.K_r:
                snake, direction, food, score, game_over = reset_game()
            elif not game_over:
                # Prevent the snake from instantly reversing into itself.
                if event.key in (pygame.K_UP, pygame.K_w) and direction != (0, CELL):
                    direction = (0, -CELL)
                elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -CELL):
                    direction = (0, CELL)
                elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (CELL, 0):
                    direction = (-CELL, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-CELL, 0):
                    direction = (CELL, 0)

        if event.type == move_event and not game_over:
            head_x, head_y = snake[0]
            new_head = (head_x + direction[0], head_y + direction[1])
            eating = new_head == food

            # If not eating, the tail moves away, so entering its old cell is allowed.
            body_to_check = snake if eating else snake[:-1]
            hit_wall = (
                new_head[0] < 0 or new_head[0] >= WIDTH
                or new_head[1] < 0 or new_head[1] >= HEIGHT
            )
            hit_self = new_head in body_to_check

            if hit_wall or hit_self:
                game_over = True
            else:
                snake.insert(0, new_head)
                if eating:
                    score += 1
                    food = new_food(snake)
                    pygame.time.set_timer(move_event, max(55, 120 - score * 3))
                else:
                    snake.pop()

    screen.fill(BLACK)

    # Draw a subtle grid.
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y), 1)

    pygame.draw.rect(screen, RED, (*food, CELL, CELL), border_radius=5)
    for index, segment in enumerate(snake):
        color = GREEN if index == 0 else DARK_GREEN
        pygame.draw.rect(screen, color, (*segment, CELL - 2, CELL - 2), border_radius=5)

    screen.blit(font.render(f"Score: {score}", True, WHITE), (15, 12))
    screen.blit(font.render("Move: Arrows / WASD", True, WHITE), (15, 48))

    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 175))
        screen.blit(overlay, (0, 0))
        title = big_font.render("GAME OVER", True, RED)
        result = font.render(f"Final score: {score}", True, WHITE)
        restart = font.render("Press R to restart | Esc to quit", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 55)))
        screen.blit(result, result.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        screen.blit(restart, restart.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 48)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
