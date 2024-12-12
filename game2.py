import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Inside the Vault: Exposing Weak Links in Cybersecurity")

# Fonts
title_font = pygame.font.Font(None, 74)
text_font = pygame.font.Font(None, 30)
hint_font = pygame.font.Font(None, 24)  # Smaller font size for the hint text

# Character data pool
name_list = ["Alice", "David", "Roxie", "Miller", "Johnson", "Martin", "Davis"]
last_name_list = ["Jackson", "Jones", "Brown", "Joe", "Wilson", "Anderson", "Smith"]

# Button Class
class Button:
    def __init__(self, text, width, height, pos):
        self.rect = pygame.Rect(pos, (width, height))
        self.text = text
        self.color = GREEN
        self.text_surf = text_font.render(text, True, BLACK)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=12)
        screen.blit(self.text_surf, self.text_rect)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]

# Function to generate a random employee
def generate_character():
    first_name = random.choice(name_list)
    last_name = random.choice(last_name_list)
    dob = f"{random.randint(1970, 2000)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
    return {"first_name": first_name, "last_name": last_name, "dob": dob}

# Display the OSINT introduction
def display_intro_osint():
    intro_text = [
        "Open Source Intelligence (OSINT) allows attackers to gather public data",
        "such as names, birth dates, and other personal information.",
        "This data can be used to guess passwords and access sensitive accounts.",
        "Your mission: Uncover how weak links in cybersecurity can be exploited.",
        "Press Enter to continue...",
    ]
    screen.fill(WHITE)
    for i, line in enumerate(intro_text):
        line_surf = text_font.render(line, True, BLACK)
        line_rect = line_surf.get_rect(center=(SCREEN_WIDTH / 2, 150 + i * 40))
        screen.blit(line_surf, line_rect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

# Level Gameplay
def level_osint(level_number):
    character = generate_character()
    hints = [
        "Think about combining the year of birth with the first name.",
        "Try initials with parts of the date of birth.",
        "Special characters might be used as separators.",
        "Could a reversed name or date be part of the password?",
        "Look for patterns in their name and date combinations.",
        "Mix uppercase, lowercase, and parts of their birth year.",
        "Think about creative substitutions like replacing letters with numbers.",
        "What if the password includes their name and a simple suffix?",
    ]

    password_logic = [
        lambda c: c["first_name"].lower() + c["dob"][:4],
        lambda c: c["first_name"][0].upper() + c["last_name"][0].lower() + c["dob"][-2:],
        lambda c: c["first_name"].capitalize() + "!" + c["dob"].replace("-", ""),
        lambda c: c["last_name"].lower()[::-1] + c["dob"][:4],
        lambda c: c["dob"].replace("-", "")[:6] + c["first_name"].lower(),
        lambda c: c["dob"].replace("-", "")[::-1] + c["last_name"].upper()[:2],
        lambda c: c["first_name"].capitalize() + "#" + c["dob"][2:4],
        lambda c: c["first_name"].lower() + "2024" + c["last_name"].capitalize(),
    ]

    password = password_logic[level_number - 1](character)

    input_password = ""
    timer = 60
    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()

    hint_button = Button("Hint", 100, 40, (SCREEN_WIDTH - 120, SCREEN_HEIGHT - 60))
    hint_box = pygame.Rect(100, SCREEN_HEIGHT - 120, SCREEN_WIDTH - 200, 60)
    hint_text = hints[level_number - 1]
    show_hint = False

    while True:
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        remaining_time = max(timer - seconds, 0)

        if remaining_time <= 0:
            return False, password

        screen.fill(BLACK)

        level_texts = [
            f"OSINT Level {level_number}",
            f"Name: {character['first_name']} {character['last_name']}",
            f"Date of Birth: {character['dob']}",
            "Guess the password:",
        ]
        for i, line in enumerate(level_texts):
            line_surf = text_font.render(line, True, WHITE)
            line_rect = line_surf.get_rect(center=(SCREEN_WIDTH / 2, 150 + i * 40))
            screen.blit(line_surf, line_rect)

        input_surf = text_font.render(input_password, True, GREEN)
        input_rect = input_surf.get_rect(center=(SCREEN_WIDTH / 2, 400))
        screen.blit(input_surf, input_rect)

        timer_surf = text_font.render(f"Time Left: {int(remaining_time)}", True, WHITE)
        timer_rect = timer_surf.get_rect(center=(SCREEN_WIDTH / 2, 500))
        screen.blit(timer_surf, timer_rect)

        if show_hint:
            pygame.draw.rect(screen, WHITE, hint_box)
            hint_surf = hint_font.render(hint_text, True, BLACK)
            screen.blit(hint_surf, (110, SCREEN_HEIGHT - 110))

        hint_button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_password = input_password[:-1]
                elif event.key == pygame.K_RETURN:
                    if input_password == password:
                        return True, password
                    else:
                        return False, password
                else:
                    input_password += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if hint_button.check_click():
                    show_hint = not show_hint

        pygame.display.update()
        clock.tick(60)

# Display success or failure
def display_result(success, correct_password, next_part=False):
    screen.fill(BLACK)
    if success:
        result_text = (
            "Correct! Press Enter to learn about a brute force attack."
            if next_part
            else "Level Complete! Press Enter to continue."
        )
    else:
        result_text = f"Incorrect! Correct password was: {correct_password}. Press Enter to try again."

    result_surf = text_font.render(result_text, True, GREEN if success else RED)
    result_rect = result_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(result_surf, result_rect)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

# Brute force attack lesson
def display_lesson(level_number):
    lessons = [
        "Brute force attacks involve systematically guessing passwords.",
        "Attackers use dictionaries or combinations of characters to guess passwords.",
        "Adding complexity to passwords reduces the success rate of brute force.",
        "Protect against brute force by using account lockouts after failed attempts.",
        "Consider multi-factor authentication to safeguard against brute force attacks.",
        "Keep your passwords unique and unrelated to public information.",
        "Regularly updating passwords reduces the risk of successful brute force.",
        "Monitor login attempts to detect and mitigate brute force attacks early.",
    ]

    screen.fill(WHITE)
    lesson_text = lessons[level_number - 1]
    lesson_surf = text_font.render(lesson_text, True, BLACK)
    lesson_rect = lesson_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(lesson_surf, lesson_rect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

# Main menu
def main_menu(screen):
    while True:
        screen.fill(WHITE)
        title_surf = title_font.render("Inside the Vault", True, BLACK)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH / 2, 100))

        osint_button = Button("Start OSINT Game", 300, 50, (SCREEN_WIDTH / 2 - 150, 250))
        exit_button = Button("Exit", 300, 50, (SCREEN_WIDTH / 2 - 150, 350))

        screen.blit(title_surf, title_rect)
        osint_button.draw()
        exit_button.draw()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if osint_button.check_click():
                    display_intro_osint()

                    for i in range(1, 9):
                        while True:
                            success, correct_password = level_osint(i)
                            display_result(success, correct_password, next_part=(i < 8))
                            if success:
                                display_lesson(i)
                                break
                            else:
                                display_result(False, correct_password)

                elif exit_button.check_click():
                    pygame.quit()
                    sys.exit()

# if __name__ == "__main__":
#     main_menu()
