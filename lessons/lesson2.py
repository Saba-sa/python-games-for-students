
import pygame

pygame.init()

# Create the game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Lesson 2 - Drawing Shapes")

# Define colors using RGB
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 220, 0)
BLACK = (0, 0, 0)

running = True

while running:

    # Check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Background
    screen.fill(WHITE)

    # 1. Draw a rectangle
    pygame.draw.rect(screen, RED, (50, 50, 150, 100))

    # 2. Draw a circle
    pygame.draw.circle(screen, BLUE, (350, 100), 50)

    # 3. Draw a line
    pygame.draw.line(screen, GREEN, (500, 50), (700, 150), 5)

    # 4. Draw an ellipse
    pygame.draw.ellipse(screen, YELLOW, (50, 250, 180, 100))

    # 5. Draw a polygon (triangle)
    pygame.draw.polygon(
        screen, GREEN,
        [(350, 250), (300, 350), (400, 350)]
    )

    # 6. Draw a rectangle outline
    pygame.draw.rect(screen, BLACK, (500, 250, 150, 100), 5)

    # Update display
    pygame.display.flip()

pygame.quit()
