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
BLACK = (0, 0, 0)

# Load Background Image
try:
    background_image = pygame.image.load("background_image/phishingback.jpg")
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Scale to fit the window
except FileNotFoundError:
    print("Background image not found. Please check the path.")
    sys.exit()

# Load Fonts
exo_font_path = "fonts/exo2.ttf"
try:
    exo_font = pygame.font.Font(exo_font_path, 36)  # Custom font
    small_exo_font = pygame.font.Font(exo_font_path, 24)  # Smaller font for lessons
except FileNotFoundError:
    print("Font file not found. Falling back to default font.")
    # exo_font = pygame.font.Font(None, 36)  # Default font fallback
    # small_exo_font = pygame.font.Font(None, 24)  # Smaller font fallback

# Load Sounds
pygame.mixer.init()
pygame.mixer.music.load('Game_Noises/game_music.wav')
pygame.mixer.music.play(-1)  # Loop background music
level_complete_sound = pygame.mixer.Sound('Game_Noises/level_complete.wav')
life_lost_sound = pygame.mixer.Sound('Game_Noises/life_lost.wav')

# Game Variables
game_state = "menu"
current_level = 1
score = 0
lives = 3

# Button Rectangles
lesson_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 90, 200, 65)  # Moved down
play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 180, 200, 65)  # Moved down

# Lesson Content
lesson_content = [
    "LESSON 1: Phishing emails often create a sense of urgency", "to trick you into clicking malicious links or downloading attachments. ",
    "LESSON 2: Suspicious links may mimic real URLs but have small",  "changes in the domain name or spelling.",
    "LESSON 3: A website designed to trick users into revealing", "personal information or downloading malware.",
    "LESSON 4: A malicious email attachment disguised as a", "legitimate file to infect a user's computer with malware.",
    "LESSON 5: An intrusive online advertisement that redirects", "users to harmful websites or installs malware on their devices."
]


# Level Prompts
level_prompts = [
    ("Level 1: Phishing Detection", "Press 'P' if phishing or 'S' if safe",'Easy', 'p', 's'),
    ("Level 2: Suspicious Link", "Press 'S' for Suspicious or 'C' for Clean", "Easy", 's', 'c'),
    ("Level 3: Fake Website", "Press 'F' for Fake or 'T' for Trusted", "Medium", 'f', 't'),
    ("Level 4: Suspicious Attachment", "Press 'A' to Avoid or 'D' to Download", "Hard", 'a', 'd'),
    ("Level 5: Malicious Pop-Up", "Press 'X' to Close or 'C' to Click", "Hardest", 'x', 'c')
]
#Load Level 1 Image
try:
    level_1_image = pygame.image.load("Icons_or_Images/Level 1 image.png")
    level_1_image = pygame.transform.scale(level_1_image, (400, 300))  # Resize as needed
except FileNotFoundError:
    print("Level 1 image not found. Please check the path.")
    sys.exit()

# Load Level 2 Image
try:
    level_2_image = pygame.image.load("Icons_or_Images/phishingemail.png")
    level_2_image = pygame.transform.scale(level_2_image, (400, 300))  # Resize as needed
except FileNotFoundError:
    print("Level 2 image not found. Please check the path.")
    sys.exit()

def render_screen(screen):
    global game_state, current_level, score, lives

    # Main Game Loop
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_state == "menu":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if lesson_button.collidepoint(event.pos):
                        game_state = "lessons"
                    elif play_button.collidepoint(event.pos):
                        game_state = "level"

            elif game_state == "lessons":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game_state = "menu"

            elif game_state == "level":
                if event.type == pygame.KEYDOWN:
                    title, instructions, prompt, correct_key, incorrect_key = level_prompts[current_level - 1]
                    if event.key == getattr(pygame, f"K_{correct_key}"):
                        score += 10
                        level_complete_sound.play()
                        current_level += 1
                        if current_level > len(level_prompts):
                            game_state = "menu"
                    elif event.key == getattr(pygame, f"K_{incorrect_key}"):
                        lives -= 1
                        life_lost_sound.play()
                    if lives <= 0:
                        game_state = "menu"

        # Rendering
        if game_state == "menu":
            screen.blit(background_image, (0, 0))
            # Add a semi-transparent rectangle for the title background
            title_background = pygame.Surface((WIDTH, 100))
            title_background.set_alpha(180)  # Semi-transparent
            title_background.fill(BLACK)
            screen.blit(title_background, (0, HEIGHT // 2 - 200))

            title_surface = exo_font.render("CYBER SLUETH: THE THREAT WITHIN", True, WHITE)
            title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
            screen.blit(title_surface, title_rect)

            pygame.draw.rect(screen, (139, 0, 0), lesson_button)
            pygame.draw.rect(screen, (139, 0, 0), play_button)
            lesson_text = exo_font.render("Lessons", True, WHITE)
            play_text = exo_font.render("Play Game", True, WHITE)
            screen.blit(lesson_text, lesson_button.move(30, 15))
            screen.blit(play_text, play_button.move(20, 15))

        elif game_state == "lessons":
            screen.fill(BLACK)
            for i, lesson in enumerate(lesson_content):
                lesson_surface = small_exo_font.render(lesson, True, WHITE)  # Smaller font
                screen.blit(lesson_surface, (50, 50 + i * 40))  # Adjust spacing
            return_text = small_exo_font.render("Press ESC to return to menu", True, RED)
            screen.blit(return_text, (50, HEIGHT - 50))

        elif game_state == "level":
            screen.fill(BLACK)
            title, instructions, prompt, correct_key, incorrect_key = level_prompts[current_level - 1]
            title_surface = exo_font.render(title, True, BLUE)
            instructions_surface = exo_font.render(instructions, True, WHITE)
            prompt_surface = exo_font.render(prompt, True, RED)
            screen.blit(title_surface, (50, 50))
            screen.blit(instructions_surface, (50, 100))
            screen.blit(prompt_surface, (50, 150))
            score_surface = exo_font.render(f"Score: {score}", True, GREEN)
            lives_surface = exo_font.render(f"Lives: {lives}", True, RED)
            screen.blit(score_surface, (50, 200))
            screen.blit(lives_surface, (50, 250))
        
        # Display Popup Image for Level 1
            if current_level == 1:
                popup_rect = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 150, 400, 300)
                pygame.draw.rect(screen, WHITE, popup_rect)  # Add a border
                screen.blit(level_1_image, popup_rect.topleft)
        
        # Display Popup Image for Level 2
            if current_level == 2:
                popup_rect = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 150, 400, 300)
                pygame.draw.rect(screen, WHITE, popup_rect)  # Add a border
                screen.blit(level_2_image, popup_rect.topleft)
        
        
         
        pygame.display.flip()
        clock.tick(30)
