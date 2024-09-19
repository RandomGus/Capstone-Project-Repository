import pygame
import string

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Encryption-Decryption Game")

# Set up fonts
font = pygame.font.Font(None, 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Caesar cipher encryption function
def encrypt_caesar(plain_text, shift):
    alphabet = string.ascii_lowercase
    encrypted_text = ""
    for char in plain_text:
        if char.isalpha():
            shifted_index = (alphabet.index(char) + shift) % 26
            encrypted_text += alphabet[shifted_index]
        else:
            encrypted_text += char
    return encrypted_text

# Caesar cipher decryption function
def decrypt_caesar(cipher_text, shift):
    alphabet = string.ascii_lowercase
    decrypted_text = ""
    for char in cipher_text:
        if char.isalpha():
            shifted_index = (alphabet.index(char) - shift) % 26
            decrypted_text += alphabet[shifted_index]
        else:
            decrypted_text += char
    return decrypted_text

# Game variables
input_message = ""
encrypted_message = ""
decrypted_message = ""
shift_value = 3  # Shift value for Caesar cipher
stage = "input"  # Stages: input, encrypted, decrypted

# Main game loop
running = True
while running:
    screen.fill(WHITE)
    
    # Display messages based on game stage
    if stage == "input":
        message_text = font.render("Type a message to encrypt:", True, BLACK)
        screen.blit(message_text, (50, 50))
        user_input_text = font.render(input_message, True, BLACK)
        screen.blit(user_input_text, (50, 100))
    elif stage == "encrypted":
        message_text = font.render(f"Encrypted Message: {encrypted_message}", True, BLACK)
        screen.blit(message_text, (50, 50))
        instruction_text = font.render("Press 'd' to decrypt the message", True, BLACK)
        screen.blit(instruction_text, (50, 100))
    elif stage == "decrypted":
        message_text = font.render(f"Decrypted Message: {decrypted_message}", True, BLACK)
        screen.blit(message_text, (50, 50))
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if stage == "input":
                if event.key == pygame.K_RETURN:
                    # Encrypt the input message
                    encrypted_message = encrypt_caesar(input_message.lower(), shift_value)
                    stage = "encrypted"
                elif event.key == pygame.K_BACKSPACE:
                    input_message = input_message[:-1]
                else:
                    input_message += event.unicode
            elif stage == "encrypted" and event.key == pygame.K_d:
                # Decrypt the message
                decrypted_message = decrypt_caesar(encrypted_message, shift_value)
                stage = "decrypted"

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
