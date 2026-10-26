
import pygame

# Start Pygame
pygame.init()

# Create a window
screen = pygame.display.set_mode((800, 600))

# Set window title
pygame.display.set_caption("My First Game")

# Game loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Background color
    screen.fill((30, 30, 60))

    # Update the display
    pygame.display.flip()

# Close Pygame
pygame.quit()
