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
level_completed = [False] * 7  # Track completion for 7 levels now
player_name = ""
input_active = False
game_state = "title"
feedback_message = ""  # Message to show feedback on correct answers
feedback_timer = 0  # Timer to control feedback display duration
countdown_timer = 10000  # 10 seconds in milliseconds
start_time = 0  # Track start time for countdown
show_times_up = False  # Flag to show/hide "Time's up!" message
prompt_next_level = False  # Flag to show/hide prompt for pressing space to continue

# Level Prompts Definition
level_prompts = [
    ("Level 1: Phishing Detection", "Press 'P' if phishing or 'S' if safe", "Your account is compromised, click here!", 'p', 's', "Phishing emails often use urgency."),
    ("Level 2: Suspicious Link", "Press 'S' for Suspicious or 'C' for Clean", "www.bank-secure-login.com", 's', 'c', "Check for unusual links or extra words."),
    ("Level 3: Fake Website", "Press 'F' for Fake or 'T' for Trusted", "www.amazon-secure-payments.net", 'f', 't', "Look for known websites' correct URLs."),
    ("Level 4: Suspicious Attachment", "Press 'A' to Avoid or 'D' to Download", "invoice.pdf.exe", 'a', 'd', "Double extensions can be suspicious."),
    ("Level 5: Malicious Pop-Up", "Press 'X' to Close or 'C' to Click", "You won a prize! Click here!", 'x', 'c', "Avoid prize prompts; they are often fake."),
    ("Level 6: Phishing Email Link", "Press 'P' if phishing or 'S' if safe", "Verify PayPal at paypal-login-support.com", 'p', 's', "Check if the URL matches the official website."),
    ("Level 7: Social Engineering", "Press 'R' to Report or 'I' to Ignore", "CEO: Send the report ASAP. Click link.", 'r', 'i', "Verify urgent requests from executives.")
]

# Helper Function to Display Text with Exo 2 Font and Centered
def display_text(text, x, y, color=WHITE, font_size=36):
    font = pygame.font.Font(exo_font_path, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Function to Display Screens with Timer
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

        # Display remaining time as countdown in seconds
        remaining_time = max(0, (countdown_timer - (pygame.time.get_ticks() - start_time)) // 1000)
        display_text(f"Time left: {remaining_time} s", WIDTH - 150, HEIGHT - 30, RED, 24)

        # Show "Time's up!" if the timer ran out
        if show_times_up:
            display_text("Time's up! Press SPACE to continue", WIDTH // 2, HEIGHT // 2 + 150, RED, 36)
        
        if prompt_next_level and not show_times_up:
            display_text("Press SPACE to continue to the next level", WIDTH // 2, HEIGHT // 2 + 150, BLUE, 24)

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
                    start_time = pygame.time.get_ticks()  # Reset timer at start of level
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode

        elif game_state == "level":
            _, _, _, correct_key, incorrect_key, feedback_text = level_prompts[current_level - 1]
            
            if not level_completed[current_level - 1]:
                if event.type == pygame.KEYDOWN:
                    if event.key == getattr(pygame, f"K_{correct_key}"):
                        score += 10
                        level_completed[current_level - 1] = True
                        level_complete_sound.play()
                        feedback_message = "Correct! " + feedback_text
                        feedback_timer = 2000
                        prompt_next_level = True
                    elif event.key == getattr(pygame, f"K_{incorrect_key}"):
                        lives -= 1
                        life_lost_sound.play()
                        feedback_message = "Incorrect! " + feedback_text
                        feedback_timer = 2000
                        prompt_next_level = True

            # Check if time has run out
            if pygame.time.get_ticks() - start_time > countdown_timer and not show_times_up:
                lives -= 1  # Lose a life if time runs out
                feedback_message = "Time's up! Be faster next time."
                feedback_timer = 2000
                show_times_up = True
                level_completed[current_level - 1] = True  # Mark level as completed to advance

            # Move to next level when SPACE is pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if level_completed[current_level - 1]:
                    current_level += 1
                    show_times_up = False  # Reset "Time's up!" message
                    prompt_next_level = False  # Clear prompt
                    if current_level > 7:
                        game_state = "game_over"
                    else:
                        start_time = pygame.time.get_ticks()  # Reset timer for the next level

        elif game_state == "game_over":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    current_level = 1
                    score = 0
                    lives = 3
                    level_completed = [False] * 7
                    game_state = "title"
                elif event.key == pygame.K_q:
                    running = False

    if lives <= 0:
        game_state = "game_over"

    display_screen()
    pygame.display.flip()
    clock.tick(30)


