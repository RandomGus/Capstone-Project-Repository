# Main Menu
# This file will serve as the main menu that will be used for the PyGame program.

import pygame
from pygame import mixer

pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('Background_Image/Main_Menu_Background.jpeg')

# Scale the background image to fit the screen
background = pygame.transform.scale(background, (800, 600))

pygame.mixer.music.load('Daft Punk - Veridis Quo (Official Audio).wav')
pygame.mixer.music.play(-1)

pygame.display.set_caption("Cyber Defenders: Rise Through the Ranks")
icon = pygame.image.load('Icons_or_Images/Page Icon.png')
pygame.display.set_icon(icon)

display_main_menu = True

# Load and set font styles
main_menu_font = pygame.font.Font("Source_Code_Pro/static/SourceCodePro-Bold.ttf", 50)  # Adjusted size for title
title_text_line1 = main_menu_font.render("CYBER DEFENDERS:", True, (139, 0, 0))  # Deeper red color for title
title_text_line2 = main_menu_font.render("RISE THROUGH THE RANKS", True, (139, 0, 0))  # Deeper red color for title

# Get coordinates for both lines
title_coordinates_line1 = title_text_line1.get_rect(center=(400, 220))  # Adjust y-coordinate
title_coordinates_line2 = title_text_line2.get_rect(center=(400, 280))  # Adjust y-coordinate

# Create an outline effect for the title text
outline_font = pygame.font.Font("Source_Code_Pro/static/SourceCodePro-Bold.ttf", 50)
outline_text_line1 = outline_font.render("CYBER DEFENDERS:", True, (0, 0, 0))  # Black outline
outline_text_line2 = outline_font.render("RISE THROUGH THE RANKS", True, (0, 0, 0))  # Black outline
outline_coordinates_line1 = outline_text_line1.get_rect(center=(400, 220))
outline_coordinates_line2 = outline_text_line2.get_rect(center=(400, 280))

below_title_font = pygame.font.Font("Source_Code_Pro/static/SourceCodePro-Regular.ttf", 30)
below_title_text = below_title_font.render("Press Enter to Continue", True, (255, 255, 255))
below_title_coordinates = below_title_text.get_rect(center=(400, 325))

display_levels = False
level_button_text_font = pygame.font.Font("Source_Code_Pro/static/SourceCodePro-Regular.ttf", 25)

# Define level texts with better font style
level1_text = level_button_text_font.render("Level 01", True, (255, 255, 255))  # Red text for levels
level1_text_coordinates = level1_text.get_rect(center=(200, 200))
level2_text = level_button_text_font.render("Level 02", True, (255, 255, 255))
level2_text_coordinates = level2_text.get_rect(center=(600, 200))
level3_text = level_button_text_font.render("Level 03", True, (255, 255, 255))
level3_text_coordinates = level3_text.get_rect(center=(200, 400))
level4_text = level_button_text_font.render("Level 04", True, (255, 255, 255))
level4_text_coordinates = level4_text.get_rect(center=(600, 400))

settings_button = pygame.image.load("Icons_or_Images/setting.png")

level1_rectangle = pygame.Rect(100, 150, 200, 100)
level2_rectangle = pygame.Rect(500, 150, 200, 100)
level3_rectangle = pygame.Rect(100, 350, 200, 100)
level4_rectangle = pygame.Rect(500, 350, 200, 100)
settings_button_rectangle = pygame.Rect(725, 25, 64, 64)

def draw_rounded_rect(surface, color, rect, radius=20):
    """Draw a rectangle with rounded corners."""
    pygame.draw.rect(surface, color, rect, border_radius=radius)

# Here we will begin to define the necessary code for the settings page.
display_settings = False

settings_background_rectangle = pygame.Rect(0, 100, 800, 400)

exit_settings_button_rectangle = pygame.Rect(725, 25, 64, 64)
exit_settings_button = pygame.image.load("Icons_or_Images/cancel.png")

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))  # Draw the scaled background image

    mouse_position = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            print("A Key has been pressed.")
            if event.key == pygame.K_RETURN:
                display_main_menu = False
                display_levels = True
                print("The Return/Enter Button has been pressed.")

        if event.type == pygame.MOUSEBUTTONDOWN:
            print("The Mouse has been used.")
            if pygame.mouse.get_pressed()[0]:
                if level1_rectangle.collidepoint(mouse_position) and display_levels:
                    print("Level 01 has been selected by the player.")
                if level2_rectangle.collidepoint(mouse_position) and display_levels:
                    print("Level 02 has been selected by the player.")
                if level3_rectangle.collidepoint(mouse_position) and display_levels:
                    print("Level 03 has been selected by the player.")
                if level4_rectangle.collidepoint(mouse_position) and display_levels:
                    print("Level 04 has been selected by the player.")
                if settings_button_rectangle.collidepoint(mouse_position) and display_levels:
                    display_settings = True
                    display_levels = False
                    print("Settings Button has been clicked.")
                if exit_settings_button_rectangle.collidepoint(mouse_position) and display_settings == True:
                    display_settings = False
                    display_levels = True
                    print("Exit Settings Button has been clicked.")
                print("The Left Click of the Mouse has been pressed.")
                print(mouse_position)

    if display_main_menu:
        # Draw a larger semi-transparent rectangle behind the title
        pygame.draw.rect(screen, (0, 0, 0, 200), (58, 180, 700, 170))  # Larger rectangle
        # First draw the outline
        screen.blit(outline_text_line1, outline_coordinates_line1)
        screen.blit(outline_text_line2, outline_coordinates_line2)
        # Then draw the title text on top
        screen.blit(title_text_line1, title_coordinates_line1)
        screen.blit(title_text_line2, title_coordinates_line2)
        screen.blit(below_title_text, below_title_coordinates)

    if display_levels:
        # Draw level boxes with rounded corners and a background color
        draw_rounded_rect(screen, (0, 0, 0), level1_rectangle)  # Black background for boxes
        draw_rounded_rect(screen, (0, 0, 0), level2_rectangle)
        draw_rounded_rect(screen, (0, 0, 0), level3_rectangle)
        draw_rounded_rect(screen, (0, 0, 0), level4_rectangle)

        # Draw a red border around the boxes
        pygame.draw.rect(screen, (139, 0, 0), level1_rectangle, 3)  # Red border
        pygame.draw.rect(screen, (139, 0, 0), level2_rectangle, 3)
        pygame.draw.rect(screen, (139, 0, 0), level3_rectangle, 3)
        pygame.draw.rect(screen, (139, 0, 0), level4_rectangle, 3)

        screen.blit(level1_text, level1_text_coordinates)
        screen.blit(level2_text, level2_text_coordinates)
        screen.blit(level3_text, level3_text_coordinates)
        screen.blit(level4_text, level4_text_coordinates)
        screen.blit(settings_button, (725, 25))

    if display_settings:
        display_levels = False
        pygame.draw.rect(screen, (0, 0, 0), settings_background_rectangle)

        screen.blit(exit_settings_button, (725, 25))
        pass

    pygame.display.update()
