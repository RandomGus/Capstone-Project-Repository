import pygame
import sys

# Initialize Pygame
def Set_Up_Phishing_Lesson_Screen(screen):
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
    background_image = pygame.image.load('Background_Image/phishing_background2.jpeg')
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
    game_state = "title"  # Start at the title screen
    feedback_message = ""  # Message to show feedback on correct answers
    feedback_timer = 0  # Timer to control feedback display duration

    # Lesson Content
    lesson_content = [
        "Lesson 1: Phishing emails often use urgency to trick you. Look out for emails that pressure you to act quickly.",
        "Lesson 2: Suspicious links often resemble real websites but with slight misspellings. Always double-check the URL.",
        "Lesson 3: Fake websites can look real but may have unusual domain names or lack security features.",
        "Lesson 4: Attachments with unexpected extensions like .exe or .bat can be harmful. Avoid opening them.",
        "Lesson 5: Pop-ups claiming you've won a prize are usually fake. Close them without clicking anything inside."
    ]
    current_lesson_index = 0

    # Level Prompts
    level_prompts = [
        ("Level 1: Phishing Detection", "Press 'P' if phishing or 'S' if safe", "Your account is compromised, click here!", 'p', 's', "Phishing emails often use urgency."),
        ("Level 2: Suspicious Link", "Press 'S' for Suspicious or 'C' for Clean", "www.bank-secure-login.com", 's', 'c', "Check for unusual links or extra words."),
        ("Level 3: Fake Website", "Press 'F' for Fake or 'T' for Trusted", "www.amazon-secure-payments.net", 'f', 't', "Look for known websites' correct URLs."),
        ("Level 4: Suspicious Attachment", "Press 'A' to Avoid or 'D' to Download", "invoice.pdf.exe", 'a', 'd', "Double extensions can be suspicious."),
        ("Level 5: Malicious Pop-Up", "Press 'X' to Close or 'C' to Click", "You won a prize! Click here!", 'x', 'c', "Avoid prize prompts; they are often fake.")
    ]

    # Helper Function to Display Text with Line Wrapping
    def display_wrapped_text(text, x, y, width, color=WHITE, font_size=24):
        font = pygame.font.Font(exo_font_path, font_size)
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            test_surface = font.render(test_line, True, color)
            if test_surface.get_width() > width:
                lines.append(current_line)
                current_line = word
            else:
                current_line = test_line
        lines.append(current_line)

        for i, line in enumerate(lines):
            text_surface = font.render(line, True, color)
            text_rect = text_surface.get_rect(center=(x, y + i * font_size))
            screen.blit(text_surface, text_rect)

    # Helper Function to Display Centered Text
    def display_text(text, x, y, color=WHITE, font_size=36):
        font = pygame.font.Font(exo_font_path, font_size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)

    # Function to Display Screens
    def display_screen():
        screen.fill(BLACK)  # Clear screen

        if game_state == "title":
            display_text("Welcome to Cyber Sleuth!", WIDTH // 2, HEIGHT // 2 - 100)
            display_text("Press SPACE to start the lesson", WIDTH // 2, HEIGHT // 2)

        elif game_state == "lesson":
            display_text("Cybersecurity Basics", WIDTH // 2, 50, BLUE, 36)
            display_wrapped_text(lesson_content[current_lesson_index], WIDTH // 2, HEIGHT // 2 - 50, WIDTH - 100)
            display_text("Press RIGHT to continue, SPACE to skip", WIDTH // 2, HEIGHT - 50, BLUE, 20)

        elif game_state == "input":
            display_text("Enter your name:", WIDTH // 2, HEIGHT // 2 - 100)
            input_box = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 20, 300, 40)
            pygame.draw.rect(screen, WHITE, input_box, 2)
            display_text(player_name, WIDTH // 2, HEIGHT // 2 + 5)

        elif game_state == "level":
            screen.blit(background_image, (0, 0))  # Draw background
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
                    game_state = "lesson"

            elif game_state == "lesson":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:  # Move to the next lesson slide
                        current_lesson_index += 1
                        if current_lesson_index >= len(lesson_content):  # End of lesson
                            game_state = "input"  # Move to name input
                    elif event.key == pygame.K_SPACE:  # Skip lesson
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
                title, instructions, prompt, correct_key, incorrect_key, feedback_text = level_prompts[current_level - 1]
                
                if not level_completed[current_level - 1]:
                    if event.type == pygame.KEYDOWN:
                        if event.key == getattr(pygame, f"K_{correct_key}"):
                            score += 10
                            level_completed[current_level - 1] = True
                            level_complete_sound.play()
                            feedback_message = "Correct! " + feedback_text
                            feedback_timer = 2000  # 2 seconds
                        elif event.key == getattr(pygame, f"K_{incorrect_key}"):
                            lives -= 1
                            life_lost_sound.play()
                            feedback_message = "Incorrect! " + feedback_text
                            feedback_timer = 2000

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if level_completed[current_level - 1]:
                        current_level += 1
                        if current_level > 5:  # All levels completed
                            game_state = "game_over"

            elif game_state == "game_over":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Restart
                        current_level = 1
                        score = 0
                        lives = 3
                        level_completed = [False] * 5
                        game_state = "title"
                    elif event.key == pygame.K_q:  # Quit
                        running = False

        # Check if the player is out of lives
        if lives <= 0:
            game_state = "game_over"

        # Display the current screen and update the display
        display_screen()
        pygame.display.flip()
        clock.tick(30)
