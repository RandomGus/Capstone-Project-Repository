# Main Menu
# This file will serve as the main menu that will be used for the PyGame program.

# Here are the necessary modules that will be imported in order to make the menu work correctly.
import pygame
from pygame import mixer

# The following code will serve to initialize the game.
pygame.init()

# Here we will set the screen size that will be used for the program.
screen = pygame.display.set_mode((800, 600))

# This code will be where the background variable will be defined. 
background = pygame.image.load('Background_Image/Main_Menu_Background.jpg')

# This is where the code for the background sound will be placed. 
# The "-1" makes it so that the music loops after it has finished.
# I know that we can't use this music, but I felt that it was a good option for a placeholder.
pygame.mixer.music.load('Daft Punk - Veridis Quo (Official Audio).wav')
pygame.mixer.music.play(-1)

# The code on the bottom of this comment will set the title and image for the window. 
pygame.display.set_caption("Cyber Defenders: Rise Through the Ranks")
icon = pygame.image.load('Icons_or_Images/Page Icon.png')
pygame.display.set_icon(icon)

# Here we will begin to write the code that is related to the displaying of the title.
# This should also showcase the text of "Press Enter to Start".
display_main_menu = True
main_menu_font = pygame.font.Font("freesansbold.ttf", 75)
title_text = main_menu_font.render("Cyber Defenders", True, (255, 255, 255))
title_coordinates = title_text.get_rect(center = (400, 250))
below_title_font = pygame.font.Font("freesansbold.ttf", 25)
below_title_text = below_title_font.render("Press Enter to Continue", True, (255, 255, 255))
below_title_coordinates = below_title_text.get_rect(center = (400, 325))

# Here is where the code for the game loop will be placed. 
running = True
while running:

    # This will be used in order to generate the background image that I have chosen.
    # Moreover, I am making it so that the image begins to generate from the top-left corner.
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        # This will make it so that if the user clicks on the "X" of the window, the program will end.
        if event.type == pygame.QUIT:
            running = False
        
        # The following code should make it so that if the user presses "Enter" the Main Menu text will disappear.
        # The reason that the main menu text will disappear will be because of how the statement will now be false. 
        if event.type == pygame.KEYDOWN:
            # The following print statement will be used to check whether the program is registering if any button is being pressed.
            print("A Key has been pressed.")
            if event.key == pygame.K_RETURN:
                display_main_menu = False
                # The following print statement will be used to check whether or not the program is registering the button being pressed.
                print("The Return/Enter Button has been pressed.")

    # This will make it so that if the flag is True, the text will display. 
    if display_main_menu:
        screen.blit(title_text, title_coordinates)
        screen.blit(below_title_text, below_title_coordinates)

    # This will make sure that the code is constantly being updated so that the image background can always be seen by the user. 
    pygame.display.update()