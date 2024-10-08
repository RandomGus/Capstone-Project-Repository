import pygame
import time

# Initialize Pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Introduction to Asymmetrical Encryption")

# Font and colors
font = pygame.font.Font(None, 36)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SCREEN_WIDTH = 800  # Screen width to manage text wrapping

# Function to split text into lines
def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        # Check width of current line plus the new word
        if font.size(current_line + word)[0] <= max_width:
            current_line += word + " "
        else:
            lines.append(current_line.strip())  # Add current line and start a new one
            current_line = word + " "
    lines.append(current_line.strip())  # Add the last line
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

# Messages and dialogue in an array
messages = [
    "AI: Great, you now understand symmetrical encryption!",
    ("AI: Did you notice a problem? If someone intercepts the key while "
     "Alice sends it to Bob, they can decrypt all messages exchanged."),
    "Player: Right, the key isn’t fully secure.",
    ("AI: Exactly! This is where asymmetrical encryption comes in. "
     "Bob will have two keys: a public key for encryption and a private key for decryption.")
]

# Typing speed (in seconds per letter)
typing_speed = 0.025

# Game state variables
nextState = False
typed_message = False
current_message_index = 0

# Game loop
running = True
while running:
    screen.fill(BLACK)

    # If we haven't finished typing the current message
    if not typed_message:
        current_message = draw_typing_effect(messages[current_message_index], (50, 50), typing_speed, SCREEN_WIDTH - 100)
        typed_message = True

    # Once the message has finished typing, draw it once
    if typed_message:
        screen.fill(BLACK)  # Clear screen to avoid text stacking
        lines = wrap_text(current_message, font, SCREEN_WIDTH - 100)
        for index, line in enumerate(lines):
            screen.blit(font.render(line, True, WHITE), (50, 50 + index * font.get_height()))
        screen.blit(font.render("Press any key to continue...", True, WHITE), (50, 500))

    # Handle user input for progressing through messages
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and typed_message:  # Only allow key press when typing is done
            nextState = True

    # When the user presses a key, go to the next message
    if nextState:
        nextState = False
        current_message_index += 1
        typed_message = False  # Reset typing state for next message

        # If we've gone through all the messages, exit the loop
        if current_message_index >= len(messages):
            running = False

    pygame.display.flip()

# Quit Pygame
pygame.quit()
