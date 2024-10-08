import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Introduction to Asymmetrical Encryption")

# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

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
CELL_SIZE = 30
START_X = 90

def binary_to_text(binary_str):
    # Ensure binary string is valid and of the right length
    if len(binary_str) % 8 != 0 or not all(bit in '01' for bit in binary_str):
        return ""  # Return empty string if invalid

    chars = [binary_str[i:i+8] for i in range(0, len(binary_str), 8)]  # Split binary string into chunks of 8 bits
    return ''.join(chr(int(char, 2)) for char in chars if int(char, 2) > 0)  # Convert each 8-bit chunk to a character

# Function to split text into lines
def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        if font.size(current_line + word)[0] <= max_width:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    lines.append(current_line.strip())
    return lines

# Typing effect function with text wrapping
def draw_typing_effect(text, position, speed, max_width):
    displayed_text = ""
    for i in range(len(text)):
        displayed_text += text[i]  # Add one letter at a time
        lines = wrap_text(displayed_text, font, max_width)  # Handle text wrapping
        screen.fill(BLACK)  # Clear the screen

        # Draw each line
        for index, line in enumerate(lines):
            rendered_text = font.render(line, True, WHITE)
            screen.blit(rendered_text, (position[0], position[1] + index * font.get_height()))

        pygame.display.update()  # Update the display
        time.sleep(speed)  # Pause to create typing effect

    return displayed_text  # Return full text after typing is done

# Draw binary message and key rows
def draw_text_row(text, y_pos, color=WHITE):
    """ Helper function to draw the bits of a string in a row. """
    for i, bit in enumerate(text):
        bit_text = small_font.render(bit, True, color)
        screen.blit(bit_text, (START_X + i * CELL_SIZE + 10, y_pos))

# Draw grid for toggling bits
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

def check_solution2():
    player_binary = ''.join(map(str, grid))
    return player_binary == binary_message

# Messages and dialogue in an array
messages = [
    "",

    "AI: Welcome, Agent, your first assignment has been received. Our client Alice needs to communicate securely with Bob. "
    "To do that, she sends him a key that they will both use to encrypt and decrypt their messages. Let’s see how this works!",

    "AI: In symmetrical encryption, both Alice and Bob use the same key for encryption and decryption. "
    "This means that if you know the key, you can encrypt a message to Alice or decrypt a message she sends.",

    "Your first task is to encrypt a message Alice wants to send to Bob. "
    "Here’s the plaintext message and the binary version, along with the key Alice will use. "
    "Use the XOR function to combine the plaintext and the key to get the ciphertext. "
    "Just apply XOR to the corresponding bits of the binary plaintext and the key, "
    "so that if the bits match the result is 0, and if they don't then the resulting bit is 1.",

    "",

    "Now it’s Bob’s turn. He received the ciphertext from Alice, and he will decrypt it using the same key. "
    "Here’s the ciphertext and key in binary. "
    "Use XOR again on the ciphertext and the key to retrieve the original plaintext.",

    "",

    "AI: Great, you now understand symmetrical encryption!",

    ("AI: Did you notice a problem? If someone intercepts the key while "
     "Alice sends it to Bob, they can decrypt all messages exchanged."),

    "Player: Right, the key isn’t fully secure.",

    ("AI: Exactly! This is where asymmetrical encryption comes in. "
     "Bob will have two keys: a public key for encryption and a private key for decryption.")
]

# Typing speed (in seconds per letter)
typing_speed = 0.01

# Game state variables
nextState = False
typed_message = False
current_message_index = 0
exercise_active = False
exercise_number = 0

# Main loop
running = True
while running:
    screen.fill(BLACK)

    if not exercise_active:  # Normal dialogue part
        # If we haven't finished typing the current message
        if not typed_message:
            current_message = draw_typing_effect(messages[current_message_index], (50, 50), typing_speed, WIDTH - 100)
            typed_message = True

        # Once the message has finished typing, draw it once
        if typed_message:
            screen.fill(BLACK)  # Clear screen to avoid text stacking
            lines = wrap_text(current_message, font, WIDTH - 100)
            for index, line in enumerate(lines):
                screen.blit(font.render(line, True, WHITE), (50, 50 + index * font.get_height()))
            screen.blit(font.render("Press any key to continue...", True, WHITE), (50, 500))

        # Handle user input for progressing through messages
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and typed_message:  # Only allow key press when typing is done
                nextState = True

        # When the user presses a key, go to the next message or start the exercise
        if nextState:
            nextState = False
            current_message_index += 1
            typed_message = False  # Reset typing state for next message

            # If we've reached the third message, go to the XOR exercise
            if current_message_index == 4:
                exercise_active = True
                exercise_number = 1
            if current_message_index == 6:
                exercise_active = True
                exercise_number = 2

            # If we've gone through all the messages, exit the loop
            if current_message_index >= len(messages):
                running = False

    elif exercise_number == 1:  # XOR exercise part
        # Draw the binary message, key, and player's grid
        draw_text_row(binary_message, 100)
        draw_text_row(key, 160)
        draw_grid()

        # Labels
        message_label = small_font.render("Message:", True, WHITE)
        key_label = small_font.render("Key:", True, WHITE)
        answer_label = small_font.render("Your Answer:", True, WHITE)

        screen.blit(message_label, (10, 100))
        screen.blit(key_label, (10, 160))
        screen.blit(answer_label, (10, GRID_START_Y - 20))

        player_answer_label = small_font.render(f"Ciphertext: {binary_to_text(''.join(map(str, grid)))}", True, WHITE)
        screen.blit(player_answer_label, (10, GRID_START_Y + 50))  # Display below the player's grid

        player_answer_label = small_font.render(f"Original Message: {message}", True, WHITE)
        screen.blit(player_answer_label, (10, 50))  # Display below the player's grid

        # Check if the solution is correct
        if check_solution():
            result_text = font.render("Correct! Press any key to continue...", True, GREEN)
            screen.blit(result_text, (START_X, 350))
            # If player hits any key after completing the XOR, return to dialogue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    exercise_active = False
                    current_message_index += 1
                    typed_message = False
                    nextState = False
        else:
            # Handle bit toggling in the grid
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if GRID_START_Y <= mouse_y <= GRID_START_Y + CELL_SIZE:
                        index = (mouse_x - START_X) // CELL_SIZE
                        if 0 <= index < len(grid):
                            grid[index] = 1 - grid[index]  # Toggle bit

    elif exercise_number == 2:  # XOR exercise part
        if not typed_message:  # Only reset once when transitioning into this exercise
            grid = [0] * len(encrypted_message)  # Reset grid to all zeros
            typed_message = True  # Prevents resetting on every frame

        # Draw the binary message, key, and player's grid
        draw_text_row(encrypted_message, 100)
        draw_text_row(key, 160)
        draw_grid()

        # Labels
        cyphertext_label = small_font.render("Ciphertext:", True, WHITE)
        key_label = small_font.render("Key:", True, WHITE)
        answer_label = small_font.render("Your Answer:", True, WHITE)
        screen.blit(message_label, (10, 100))
        screen.blit(key_label, (10, 160))
        screen.blit(answer_label, (10, GRID_START_Y - 20))


        player_answer_label = small_font.render(f"Plaintext: {binary_to_text(''.join(map(str, grid)))}", True, WHITE)
        screen.blit(player_answer_label, (10, GRID_START_Y + 50))  # Display below the player's grid

        player_answer_label = small_font.render(f"Ciphertext: {binary_to_text(encrypted_message)}", True, WHITE)
        screen.blit(player_answer_label, (10, 50))  # Display below the player's grid

        # Check if the solution is correct
        if check_solution2():
            result_text = font.render("Correct! Press any key to continue...", True, GREEN)
            screen.blit(result_text, (START_X, 350))
            # If player hits any key after completing the XOR, return to dialogue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    exercise_active = False
                    current_message_index += 1
                    typed_message = False
                    nextState = False
        else:
            # Handle bit toggling in the grid
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