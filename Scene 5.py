#This is scene 5 of the module

import pygame

pygame.init()

# Screen setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Key to the Message")

# Font and colors
font = pygame.font.Font(None, 36)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Text rendering function
def render_text(text, position):
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, position)

# Game state
game_state = "intro"

# Game loop
running = True
while running:
    screen.fill(WHITE)
    
    if game_state == "intro":
        render_text("AI: Now, let’s try encrypting a message with Bob’s public key.", (50, 50))
        render_text("Plaintext: MEET ME AT 8PM", (50, 100))
        render_text("Public Key: (Encryption details)", (50, 150))
        render_text("1. I'll encrypt the message with the public key.", (50, 250))
        render_text("2. Can you explain more about how public keys work?", (50, 300))
        
    elif game_state == "encrypt":
        render_text("AI: Well done! The message is securely encrypted.", (50, 50))
        
    elif game_state == "explain":
        render_text("AI: A public key is part of an asymmetric encryption system.", (50, 50))
        render_text("AI: Only Bob's private key can decrypt the message.", (50, 100))
        render_text("Would you like to try encrypting now?", (50, 200))
        render_text("1. Yes, let's encrypt.", (50, 300))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_state == "intro":
                if event.key == pygame.K_1:
                    game_state = "encrypt"
                elif event.key == pygame.K_2:
                    game_state = "explain"
            elif game_state == "explain":
                if event.key == pygame.K_1:
                    game_state = "encrypt"

    pygame.display.flip()

pygame.quit()