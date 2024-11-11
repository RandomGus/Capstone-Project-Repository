
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

# Load Background Image and Sounds
background_image = pygame.image.load('Background_Image/phishing_background.jpeg')
pygame.mixer.init()
pygame.mixer.music.load('Game_Noises/game_music.wav')
pygame.mixer.music.play(-1)  # Loop background music
level_complete_sound = pygame.mixer.Sound('Game_Noises/level_complete.wav')
life_lost_sound = pygame.mixer.Sound('Game_Noises/life_lost.wav')

# Load the Exo 2 Font
exo_font_path = 'fonts/exo2.ttf'
exo_font = pygame.font.Font(exo_font_path, 36)

# Game Variables
current_level = 1
score = 0
lives = 3
level_completed = [False] * 5  # Track completion for 5 levels
player_name = ""
input_active = False
game_state = "title"
feedback_message = ""  # Message to show feedback on correct answers
feedback_timer = 0  # Timer to control feedback display duration
difficulty_timer = [2000, 1800, 1600, 1400, 1200]  # Progressive difficulty (feedback duration decreases)

# Level Prompts Definition (Moved to a global scope)
level_prompts = [
    ("Level 1: Phishing Detection", "Press 'P' if phishing or 'S' if safe", "Your account is compromised, click here!", 'p', 's', "Phishing emails often use urgency."),
    ("Level 2: Suspicious Link", "Press 'S' for Suspicious or 'C' for Clean", "www.bank-secure-login.com", 's', 'c', "Check for unusual links or extra words."),
    ("Level 3: Fake Website", "Press 'F' for Fake or 'T' for Trusted", "www.amazon-secure-payments.net", 'f', 't', "Look for known websites' correct URLs."),
    ("Level 4: Suspicious Attachment", "Press 'A' to Avoid or 'D' to Download", "invoice.pdf.exe", 'a', 'd', "Double extensions can be suspicious."),
    ("Level 5: Malicious Pop-Up", "Press 'X' to Close or 'C' to Click", "You won a prize! Click here!", 'x', 'c', "Avoid prize prompts; they are often fake.")
]

# Helper Function to Display Text with Exo 2 Font and Centered
def display_text(text, x, y, color=WHITE, font_size=36):
    font = pygame.font.Font(exo_font_path, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Function to Display Screens
def display_screen():
    screen.blit(background_image, (0, 0))  # Draw background

    if game_state == "title":
        display_text("Welcome to Cyber Sleuth!", WIDTH // 2, HEIGHT // 2 - 100)
        display_text("Press SPACE to start", WIDTH // 2, HEIGHT // 2)

    elif game_state == "input":
        display_text("Enter your name:", WIDTH // 2, HEIGHT // 2 - 100)
        input_box = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 20, 300, 40)
        pygame.draw.rect(screen, WHITE, input_box, 2)
        display_text(player_name, WIDTH // 2, HEIGHT // 2 + 5)

    elif game_state == "level":
        title, instructions, prompt, correct_key, incorrect_key, feedback_text = level_prompts[current_level - 1]
        display_text(title, WIDTH // 2, HEIGHT // 2 - 150)
        display_text(instructions, WIDTH // 2, HEIGHT // 2 - 100)
        display_text(prompt, WIDTH // 2, HEIGHT // 2 - 50)

        if feedback_timer > 0:
            display_text(feedback_message, WIDTH // 2, HEIGHT // 2 + 100, GREEN, 24)

        if level_completed[current_level - 1]:
            display_text("Press SPACE to proceed to the next level", WIDTH // 2, HEIGHT // 2 + 150, BLUE, 24)

        display_text(f"Player: {player_name}", 100, 30, BLUE)
        display_text(f"Score: {score}", 100, 60, GREEN)
        display_text(f"Lives: {lives}", WIDTH - 100, 30, RED)

    elif game_state == "game_over":
        screen.fill(BLACK)
        display_text("Game Over", WIDTH // 2, HEIGHT // 2 - 50, RED, 48)
        display_text("Press R to Restart or Q to Quit", WIDTH // 2, HEIGHT // 2 + 50)

# Main Game Loop
clock = pygame.time.Clock()
running = True
while running:
    if feedback_timer > 0:
        feedback_timer -= clock.get_time()  # Decrease timer based on time passed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_state == "title":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = "input"

        elif game_state == "input":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and player_name:
                    game_state = "level"
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode

        elif game_state == "level":
            # Unpack level prompt details
            _, _, _, correct_key, incorrect_key, feedback_text = level_prompts[current_level - 1]
            
            if not level_completed[current_level - 1]:
                if event.type == pygame.KEYDOWN:
                    if event.key == getattr(pygame, f"K_{correct_key}"):
                        score += 10
                        level_completed[current_level - 1] = True
                        level_complete_sound.play()
                        feedback_message = "Correct! " + feedback_text
                        feedback_timer = difficulty_timer[current_level - 1]
                    elif event.key == getattr(pygame, f"K_{incorrect_key}"):
                        lives -= 1
                        life_lost_sound.play()
                        feedback_message = "Incorrect! " + feedback_text
                        feedback_timer = difficulty_timer[current_level - 1]

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if level_completed[current_level - 1]:
                    current_level += 1
                    if current_level > 5:
                        game_state = "game_over"

        elif game_state == "game_over":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    current_level = 1
                    score = 0
                    lives = 3
                    level_completed = [False] * 5
                    game_state = "title"
                elif event.key == pygame.K_q:
                    running = False

    if lives <= 0:
        game_state = "game_over"

    display_screen()
    pygame.display.flip()
    clock.tick(30)
