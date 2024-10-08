import pygame

# Initialize Pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Introduction to Asymmetrical Encryption")

# Font and colors
font = pygame.font.Font(None, 36)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TRANSLUCENT_BG = (255, 255, 255, 180)  # White with slight transparency for the background

# Load background image
background = pygame.image.load('Background_image/encryption_background.jpeg')
background = pygame.transform.scale(background, (800, 600))  # Scale to fit the window

# Text rendering function with word wrapping and rounded rectangle background
def render_text(text, position):
    # Split text into multiple lines if it exceeds the width of the screen
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        # Check if adding the next word would exceed the screen width
        test_line = f"{current_line} {word}".strip()  # Create test line
        text_surface = font.render(test_line, True, BLACK)
        if text_surface.get_width() <= 700:  # Adjusted for smaller margins (700px instead of 750)
            current_line = test_line
        else:
            lines.append(current_line)  # Add the current line to the list
            current_line = word  # Start a new line with the current word

    lines.append(current_line)  # Add the last line

    # Draw a translucent rounded rectangle behind the text for readability
    text_height = len(lines) * 40
    rect_x = position[0] - 45  # Move the rectangle a bit to the left (-20)
    rect_y = position[1] - 10
    rect_width = 760
    rect_height = text_height + 20
    pygame.draw.rect(screen, TRANSLUCENT_BG, (rect_x, rect_y, rect_width, rect_height), border_radius=15)

    # Render each line of text
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, BLACK)
        screen.blit(text_surface, (position[0], position[1] + i * 40))  # Adjust y-position for each line

# Game state
game_state = "intro"

# Messages and dialogue
ai_intro_message = "AI: Great, you now understand symmetrical encryption!"
ai_problem_message = ("AI: Did you notice a problem? If someone intercepts the key while "
                      "Alice sends it to Bob, they can decrypt all messages exchanged.")
player_response_message = "Player: Right, the key isn’t fully secure."
ai_solution_message = ("AI: Exactly! This is where asymmetrical encryption comes in. "
                       "Bob will have two keys: a public key for encryption and a private key for decryption.")

# Game loop
running = True
while running:
    screen.blit(background, (0, 0))  # Blit the background image
    
    if game_state == "intro":
        render_text(ai_intro_message, (70, 50))  # Shift text slightly to the right
        render_text("Press any key to continue...", (70, 500))
    
    elif game_state == "problem":
        render_text(ai_problem_message, (70, 50))
        render_text("Press any key to continue...", (70, 500))
    
    elif game_state == "response":
        render_text(player_response_message, (70, 50))
        render_text("Press any key to continue...", (70, 500))
    
    elif game_state == "solution":
        render_text(ai_solution_message, (70, 50))
        render_text("Press any key to finish the scene...", (70, 500))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_state == "intro":
                game_state = "problem"
            elif game_state == "problem":
                game_state = "response"
            elif game_state == "response":
                game_state = "solution"
            elif game_state == "solution":
                running = False  # End the scene after the solution

    pygame.display.flip()

# Quit Pygame
pygame.quit()
