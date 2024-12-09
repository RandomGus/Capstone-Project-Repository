import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up game window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cyber Sleuth: The Threat Within")

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Load Background Image
try:
    background_image = pygame.image.load("background_image/phishingback.jpg")
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Scale to fit the window
except FileNotFoundError:
    print("Background image not found. Please check the path.")
    sys.exit()

# Load Fonts
exo_font_path = 'fonts/exo2.ttf'
try:
    exo_font = pygame.font.Font(exo_font_path, 36)  # Custom font
except FileNotFoundError:
    print("Font file not found. Falling back to default font.")
    exo_font = pygame.font.Font(None, 36)  # Default font fallback

# Load Sounds
pygame.mixer.init()
pygame.mixer.music.load('Game_Noises/game_music.wav')
pygame.mixer.music.play(-1)  # Loop background music
level_complete_sound = pygame.mixer.Sound('Game_Noises/level_complete.wav')
life_lost_sound = pygame.mixer.Sound('Game_Noises/life_lost.wav')

# Define Game State Class
class GameState:
    def __init__(self):
        self.game_state = "menu"  # Possible states: menu, lessons, level
        self.current_level = 1
        self.score = 0
        self.lives = 3
        self.feedback_message = ""
        self.feedback_timer = 0
        self.level_completed = [False] * 5

# Initialize game state
game_state = GameState()

# Button Rectangles
lesson_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)

# Lesson Content
lesson_content = [
    "Lesson 1: Phishing emails often create urgency to trick you.",
    "Lesson 2: Suspicious links may mimic real URLs but have small changes.",
    "Lesson 3: Fake websites often lack HTTPS or use strange domains.",
    "Lesson 4: Attachments with double extensions like .exe are risky.",
    "Lesson 5: Pop-ups claiming prizes are usually scams."
]

# Level Prompts
level_prompts = [
    ("Level 1: Phishing Detection", "Press 'P' if phishing or 'S' if safe", "Your account is compromised, click here!", 'p', 's', "Phishing emails often use urgency."),
    ("Level 2: Suspicious Link", "Press 'S' for Suspicious or 'C' for Clean", "www.bank-secure-login.com", 's', 'c', "Check for unusual links or extra words."),
    ("Level 3: Fake Website", "Press 'F' for Fake or 'T' for Trusted", "www.amazon-secure-payments.net", 'f', 't', "Look for known websites' correct URLs."),
    ("Level 4: Suspicious Attachment", "Press 'A' to Avoid or 'D' to Download", "invoice.pdf.exe", 'a', 'd', "Double extensions can be suspicious."),
    ("Level 5: Malicious Pop-Up", "Press 'X' to Close or 'C' to Click", "You won a prize! Click here!", 'x', 'c', "Avoid prize prompts; they are often fake.")
]

# Helper Functions
def draw_button(rect, text, color, hover_color):
    """Draws a button with hover effects."""
    mouse_pos = pygame.mouse.get_pos()
    button_color = hover_color if rect.collidepoint(mouse_pos) else color
    pygame.draw.rect(screen, button_color, rect)
    text_surface = exo_font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(rect.x + rect.width // 2, rect.y + rect.height // 2))
    screen.blit(text_surface, text_rect)

def display_text(text, x, y, font_size=36, color=WHITE):
    """Displays centered text on the screen."""
    font = pygame.font.Font(exo_font_path, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def render_screen():
    """Renders the screen based on the current game state."""
    screen.blit(background_image, (0, 0))

    if game_state.game_state == "menu":
        display_text("Cyber Sleuth: The Threat Within", WIDTH // 2, HEIGHT // 2 - 150, 48, BLUE)
        draw_button(lesson_button, "Lessons", GRAY, RED)
        draw_button(play_button, "Play Game", GRAY, RED)

    elif game_state.game_state == "lessons":
        display_text("Cybersecurity Lessons", WIDTH // 2, 50, 48, BLUE)
        for i, lesson in enumerate(lesson_content):
            display_text(lesson, WIDTH // 2, 150 + i * 50, 24, WHITE)
        display_text("Press ESC to return to the main menu", WIDTH // 2, HEIGHT - 50, 24, RED)

    elif game_state.game_state == "level":
        title, instructions, prompt, correct_key, incorrect_key, feedback_text = level_prompts[game_state.current_level - 1]
        display_text(title, WIDTH // 2, 100, BLUE)
        display_text(instructions, WIDTH // 2, 150, WHITE)
        display_text(prompt, WIDTH // 2, 250, RED)
        display_text(f"Score: {game_state.score}", WIDTH // 2, 400, GREEN)
        display_text(f"Lives: {game_state.lives}", WIDTH // 2, 450, RED)
        if game_state.feedback_timer > 0:
            display_text(game_state.feedback_message, WIDTH // 2, 500, GREEN)
            game_state.feedback_timer -= 1

# Main Game Loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_state.game_state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if lesson_button.collidepoint(event.pos):
                    game_state.game_state = "lessons"
                elif play_button.collidepoint(event.pos):
                    game_state.game_state = "level"

        elif game_state.game_state == "lessons":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_state.game_state = "menu"

        elif game_state.game_state == "level":
            title, instructions, prompt, correct_key, incorrect_key, feedback_text = level_prompts[game_state.current_level - 1]
            if event.type == pygame.KEYDOWN:
                if event.key == getattr(pygame, f"K_{correct_key}"):
                    game_state.score += 10
                    level_complete_sound.play()
                    game_state.feedback_message = "Correct! " + feedback_text
                    game_state.feedback_timer = 100
                    game_state.level_completed[game_state.current_level - 1] = True
                    game_state.current_level += 1
                    if game_state.current_level > len(level_prompts):
                        game_state.game_state = "menu"
                elif event.key == getattr(pygame, f"K_{incorrect_key}"):
                    game_state.lives -= 1
                    life_lost_sound.play()
                    game_state.feedback_message = "Incorrect! " + feedback_text
                    game_state.feedback_timer = 100
                if game_state.lives <= 0:
                    game_state.game_state = "menu"

    render_screen()
    pygame.display.flip()
    clock.tick(30)
