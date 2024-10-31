import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up game window dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cyber Sleuth: The Threat Within")

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up fonts
font = pygame.font.Font(None, 36)  # Default font with size 36

# Game Variables
current_level = 1
score = 0
lives = 3
level1_completed = False  # Track Level 1 completion
player_name = ""           # Store player's name
input_active = False       # Track if name input is active
game_state = "title"       # State of the game: title, input, or level

# Helper Function to Display Text
def display_text(text, x, y, color=WHITE, font_size=36):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Function to Handle the Different Screens
def display_screen():
    screen.fill(BLACK)  # Fill the background with black

    # Title Screen
    if game_state == "title":
        display_text("Welcome to Cyber Sleuth!", WIDTH // 2 - 150, HEIGHT // 2 - 100)
        display_text("Press SPACE to start", WIDTH // 2 - 100, HEIGHT // 2)

    # Name Input Screen
    elif game_state == "input":
        display_text("Enter your name:", WIDTH // 2 - 150, HEIGHT // 2 - 100)
        display_text(player_name, WIDTH // 2 - 150, HEIGHT // 2)  # Display the typed name

    # Game Level Screens
    elif game_state == "level":
        if current_level == 1:
            if not level1_completed:
                # Display instructions for Level 1
                display_text("Level 1: Phishing Detection", WIDTH // 2 - 150, HEIGHT // 2 - 100)
                display_text("Press 'P' for Phishing or 'S' for Safe", WIDTH // 2 - 200, HEIGHT // 2)
                display_text("Email: 'Your account is compromised, click here!'", WIDTH // 2 - 250, HEIGHT // 2 + 50)
            else:
                # Display level complete message if Level 1 is done
                display_text("Level 1 Complete! Press SPACE to continue.", WIDTH // 2 - 200, HEIGHT // 2)
        elif current_level == 2:
            display_text("Level 2: Malware Maze", WIDTH // 2 - 150, HEIGHT // 2 - 50)
        
        # Display score and lives with player’s name
        display_text(f"Player: {player_name}", 10, 10, BLUE)
        display_text(f"Score: {score}", 10, 40, GREEN)
        display_text(f"Lives: {lives}", WIDTH - 100, 10, RED)

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Handle title screen input
        if game_state == "title":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = "input"  # Move to name input screen

        # Handle name input screen
        elif game_state == "input":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state = "level"  # Move to level 1 after name is entered
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]  # Remove last character on backspace
                else:
                    player_name += event.unicode  # Add typed character to name

        # Handle level-specific interactions
        elif game_state == "level":
            if current_level == 1 and not level1_completed:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # P for "Phishing"
                        score += 10  # Award points for correct identification
                        level1_completed = True  # Mark level as completed
                    elif event.key == pygame.K_s:  # S for "Safe"
                        lives -= 1  # Deduct a life for incorrect answer
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and level1_completed:
                current_level += 1
                level1_completed = False  # Reset for next level if needed

    # Display the current screen based on the state and level
    display_screen()

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(30)  # 30 frames per second
