import pygame

pygame.init()

# Screen setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Key to the Message")

# Font and colors
font = pygame.font.Font(None, 36)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TRANSLUCENT_BG = (255, 255, 255, 180)  # A white translucent color for text background

# Load background image
background = pygame.image.load('Background_image/encryption_background.jpeg')
background = pygame.transform.scale(background, (800, 600))  # Scale to fit the window

# Function to draw rounded rectangle
def draw_rounded_rect(surface, color, rect, corner_radius):
    """ Draws a rectangle with rounded corners on the specified surface. """
    pygame.draw.rect(surface, color, (rect[0] + corner_radius, rect[1], rect[2] - corner_radius * 2, rect[3]))  # Top
    pygame.draw.rect(surface, color, (rect[0], rect[1] + corner_radius, rect[2], rect[3] - corner_radius * 2))  # Middle
    pygame.draw.rect(surface, color, (rect[0] + corner_radius, rect[1] + rect[3] - corner_radius, rect[2] - corner_radius * 2, corner_radius))  # Bottom
    
    pygame.draw.circle(surface, color, (rect[0] + corner_radius, rect[1] + corner_radius), corner_radius)  # Top-left corner
    pygame.draw.circle(surface, color, (rect[0] + rect[2] - corner_radius, rect[1] + corner_radius), corner_radius)  # Top-right corner
    pygame.draw.circle(surface, color, (rect[0] + corner_radius, rect[1] + rect[3] - corner_radius), corner_radius)  # Bottom-left corner
    pygame.draw.circle(surface, color, (rect[0] + rect[2] - corner_radius, rect[1] + rect[3] - corner_radius), corner_radius)  # Bottom-right corner

# Text rendering function with background
def render_text_with_bg(text, position, box_width):
    # Split text into multiple lines if it exceeds the width of the screen
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        # Check if adding the next word would exceed the screen width
        test_line = f"{current_line} {word}".strip()  # Create test line
        text_surface = font.render(test_line, True, BLACK)
        if text_surface.get_width() <= box_width - 20:  # Adjust for margins
            current_line = test_line
        else:
            lines.append(current_line)  # Add the current line to the list
            current_line = word  # Start a new line with the current word

    lines.append(current_line)  # Add the last line

    # Draw a translucent, rounded background behind text for readability
    text_height = len(lines) * 40
    rect_x = position[0] - 20  # Shift the box slightly to the left
    rect_y = position[1] - 10
    draw_rounded_rect(screen, TRANSLUCENT_BG, (rect_x, rect_y, box_width, text_height + 20), 20)  # Rounded rectangle

    # Render each line of text
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, BLACK)
        screen.blit(text_surface, (position[0], position[1] + i * 40))  # Adjust y-position for each line

# Function to evenly space textboxes vertically
def render_evenly_spaced_text(text_list, box_width, y_margin=50):
    available_height = 600 - 2 * y_margin  # Screen height minus top/bottom margins
    spacing = available_height // len(text_list)  # Calculate spacing between each textbox

    for index, text in enumerate(text_list):
        y_position = y_margin + index * spacing
        render_text_with_bg(text, (60, y_position), box_width)

# Game state
game_state = "intro"

# Game loop
running = True
while running:
    screen.blit(background, (0, 0))  # Blit the background image

    if game_state == "intro":
        # List of text to display in the intro
        intro_texts = [
            "AI: Now, let’s try encrypting a message with Bob’s public key.",
            "Plaintext: MEET ME AT 8PM",
            "Public Key: (Encryption details)",
            "1. I'll encrypt the message with the public key.",
            "2. Can you explain more about how public keys work?",
            "Press 1 or 2 to continue"
        ]
        render_evenly_spaced_text(intro_texts, 700)

    elif game_state == "encrypt":
        render_text_with_bg("AI: Well done! The message is securely encrypted.", (60, 50), 700)

    elif game_state == "explain":
        # List of text to display in the explanation
        explain_texts = [
            "AI: A public key is part of an asymmetric encryption system.",
            "AI: Only Bob's private key can decrypt the message.",
            "Would you like to try encrypting now?",
            "1. Yes, let's encrypt.",
            "Press 1 to encrypt the message"
        ]
        render_evenly_spaced_text(explain_texts, 700)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_state == "intro":
                if event.key == pygame.K_1:
                    game_state = "encrypt"
                elif event.key == pygame.K_2:
                    game_state = "explain"
            elif game_state == "explain":
                if event.key == pygame.K_1:
                    game_state = "encrypt"

    pygame.display.flip()

pygame.quit()
