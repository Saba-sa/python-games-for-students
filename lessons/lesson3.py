
import pygame

pygame.init()

# Create the game window
WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lesson 3 - Move the Car")

# Colors
WHITE = (255, 255, 255)
BLUE = (30, 100, 255)
BLACK = (0, 0, 0)
GREEN = (40, 160, 60)

# Car position
car_x = 350
car_y = 400

# Car size
car_width = 100
car_height = 60

# Car speed
speed = 5

clock = pygame.time.Clock()
running = True

while running:

    # Check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get keyboard input
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        car_x -= speed

    if keys[pygame.K_RIGHT]:
        car_x += speed

    if keys[pygame.K_UP]:
        car_y -= speed

    if keys[pygame.K_DOWN]:
        car_y += speed

    # Keep the car inside the window
    car_x = max(0, min(WIDTH - car_width, car_x))
    car_y = max(0, min(HEIGHT - car_height, car_y))

    # Draw background
    screen.fill(GREEN)

    # Draw road
    pygame.draw.rect(screen, (55, 55, 60), (100, 0, 600, HEIGHT))

    # Draw road markings
    for y in range(0, HEIGHT, 100):
        pygame.draw.rect(
            screen, WHITE,
            (395, y, 10, 50)
        )

    # Draw car body
    pygame.draw.rect(
        screen, BLUE,
        (car_x, car_y, car_width, car_height),
        border_radius=10
    )

    # Draw windows
    pygame.draw.rect(
        screen, WHITE,
        (car_x + 25, car_y + 10, 50, 20),
        border_radius=4
    )

    # Draw wheels
    pygame.draw.rect(
        screen, BLACK,
        (car_x + 10, car_y + 45, 20, 20)
    )

    pygame.draw.rect(
        screen, BLACK,
        (car_x + 70, car_y + 45, 20, 20)
    )

    # Update screen
    pygame.display.flip()

    # Limit game speed to 60 frames per second
    clock.tick(60)

pygame.quit()
