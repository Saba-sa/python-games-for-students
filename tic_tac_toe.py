import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 650
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Colors
BG = (20, 25, 45)
WHITE = (255, 255, 255)
BLUE = (50, 180, 255)
RED = (255, 90, 110)
GRAY = (100, 110, 140)

# Fonts
FONT = pygame.font.SysFont("arial", 100, bold=True)
TITLE_FONT = pygame.font.SysFont("arial", 45, bold=True)
SMALL_FONT = pygame.font.SysFont("arial", 28)

# Game variables
board = [""] * 9
current_player = "X"
game_over = False
winner = None

# Winning combinations
WINNING_COMBINATIONS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]


def check_winner():
    for a, b, c in WINNING_COMBINATIONS:
        if board[a] == board[b] == board[c] != "":
            return board[a]

    if "" not in board:
        return "Draw"

    return None


def draw_game():
    SCREEN.fill(BG)

    title = TITLE_FONT.render("TIC-TAC-TOE", True, WHITE)
    SCREEN.blit(title, title.get_rect(center=(WIDTH // 2, 55)))

    # Display game status
    if game_over:
        if winner == "Draw":
            message = "It's a Draw!"
        else:
            message = f"Player {winner} Wins!"
    else:
        message = f"Player {current_player}'s Turn"

    status = SMALL_FONT.render(message, True, BLUE)
    SCREEN.blit(status, status.get_rect(center=(WIDTH // 2, 115)))

    # Draw board lines
    for i in range(1, 3):
        pygame.draw.line(
            SCREEN, GRAY, (100 + i * 133, 180),
            (100 + i * 133, 579), 5
        )
        pygame.draw.line(
            SCREEN, GRAY, (100, 180 + i * 133),
            (499, 180 + i * 133), 5
        )

    # Draw X and O
    for i, mark in enumerate(board):
        if mark:
            row = i // 3
            col = i % 3

            x = 100 + col * 133 + 66
            y = 180 + row * 133 + 66

            color = BLUE if mark == "X" else RED
            text = FONT.render(mark, True, color)
            SCREEN.blit(text, text.get_rect(center=(x, y)))

    # Restart instruction
    restart = SMALL_FONT.render(
        "Press R to Restart | ESC to Quit", True, WHITE
    )
    SCREEN.blit(restart, restart.get_rect(center=(WIDTH // 2, 620)))

    pygame.display.flip()


def restart_game():
    global board, current_player, game_over, winner

    board = [""] * 9
    current_player = "X"
    game_over = False
    winner = None


# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_r:
                restart_game()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not game_over:
                mouse_x, mouse_y = event.pos

                if 100 <= mouse_x < 499 and 180 <= mouse_y < 579:
                    col = (mouse_x - 100) // 133
                    row = (mouse_y - 180) // 133
                    index = row * 3 + col

                    if board[index] == "":
                        board[index] = current_player

                        winner = check_winner()

                        if winner:
                            game_over = True
                        else:
                            current_player = (
                                "O" if current_player == "X" else "X"
                            )

    draw_game()

pygame.quit()
sys.exit()