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

# Text rendering function with word wrapping
def render_text(text, position):
    # Split text into multiple lines if it exceeds the width of the screen
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        # Check if adding the next word would exceed the screen width
        test_line = f"{current_line} {word}".strip()  # Create test line
        text_surface = font.render(test_line, True, BLACK)
        if text_surface.get_width() <= 750:  # Adjust for margins
            current_line = test_line
        else:
            lines.append(current_line)  # Add the current line to the list
            current_line = word  # Start a new line with the current word

    lines.append(current_line)  # Add the last line

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
    screen.fill(WHITE)
    
    if game_state == "intro":
        render_text(ai_intro_message, (50, 50))
        render_text("Press any key to continue...", (50, 500))
    
    elif game_state == "problem":
        render_text(ai_problem_message, (50, 50))
        render_text("Press any key to continue...", (50, 500))
    
    elif game_state == "response":
        render_text(player_response_message, (50, 50))
        render_text("Press any key to continue...", (50, 500))
    
    elif game_state == "solution":
        render_text(ai_solution_message, (50, 50))
        render_text("Press any key to finish the scene...", (50, 500))
    
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
