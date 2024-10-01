import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Binary Toggle Encryption")

# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)

# Message and binary conversion
message = "hi"
binary_message = ''.join(format(ord(char), '08b') for char in message)

# Generate random binary encryption key of the same length as binary_message
key = ''.join(random.choice(['0', '1']) for _ in range(len(binary_message)))

# XOR encryption function
def xor_encrypt(binary_msg, binary_key):
    return ''.join(str(int(b) ^ int(k)) for b, k in zip(binary_msg, binary_key))

# The encrypted message
encrypted_message = xor_encrypt(binary_message, key)

# Create a grid for toggling bits (binary_message length)
grid = [0] * len(binary_message)

# Constants for grid display
GRID_START_Y = 240
CELL_SIZE = 30  # Reduced cell size to fit screen
START_X = 90

def draw_text_row(text, y_pos, color=BLACK):
    """ Helper function to draw the bits of a string in a row. """
    for i, bit in enumerate(text):
        bit_text = small_font.render(bit, True, color)
        screen.blit(bit_text, (START_X + i * CELL_SIZE + 10, y_pos))

def draw_grid():
    """ Draws the clickable grid where the user toggles bits. """
    for i in range(len(grid)):
        rect = pygame.Rect(START_X + i * CELL_SIZE, GRID_START_Y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, WHITE if grid[i] == 1 else BLACK, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)  # Border
        bit_text = small_font.render(str(grid[i]), True, WHITE if grid[i] == 0 else BLACK)
        screen.blit(bit_text, (rect.x + 10, rect.y + 5))

# Check if the player solution matches the encrypted message
def check_solution():
    player_binary = ''.join(map(str, grid))
    return player_binary == encrypted_message

# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Display the binary message, key, and player's grid answer
    draw_text_row(binary_message, 100)  # Display binary message
    draw_text_row(key, 160)             # Display encryption key
    draw_grid()                         # Display player's grid (answer)

    # Labels
    message_label = small_font.render("Message:", True, BLACK)
    key_label = small_font.render("Key:", True, BLACK)
    answer_label = small_font.render("Your Answer:", True, BLACK)

    screen.blit(message_label, (10, 100))
    screen.blit(key_label, (10, 160))
    screen.blit(answer_label, (10, GRID_START_Y - 20))

    # Check if the solution is correct
    if check_solution():
        result_text = font.render("Correct!", True, GREEN)
        screen.blit(result_text, (START_X, 300))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if GRID_START_Y <= mouse_y <= GRID_START_Y + CELL_SIZE:
                index = (mouse_x - START_X) // CELL_SIZE
                if 0 <= index < len(grid):
                    grid[index] = 1 - grid[index]  # Toggle bit

    pygame.display.flip()

# Quit Pygame
pygame.quit()
