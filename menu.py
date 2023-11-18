import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Input Menu")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)

# Define fonts
font = pygame.font.Font(None, 36)

# Define input fields and button
# input1_rect = pygame.Rect(width // 4, height // 4, width // 2, 40)
# input2_rect = pygame.Rect(width // 4, height // 2 + 40, width // 2, 40)
label1_rect = pygame.Rect(width // 4, height // 8 + 40, width // 2, 40)
input_rect1 = pygame.Rect(width // 4, height // 4, width // 2, 40)
label2_rect = pygame.Rect(width // 4, height // 2 - 50, width // 2, 40)
input_rect2 = pygame.Rect(width // 4, height // 2 - 10, width // 2, 40)
button_rect = pygame.Rect(width // 4, height * 3 // 4, width // 2, 40)

# Input field values
name = ""
ip = ""

# Page identifiers
PAGE_MAIN = "main"
PAGE_RESULT = "result"
current_page = PAGE_MAIN

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if input_rect1.collidepoint(pygame.mouse.get_pos()):
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode
            elif input_rect2.collidepoint(pygame.mouse.get_pos()):
                if event.key == pygame.K_BACKSPACE:
                    ip = ip[:-1]
                else:
                    ip += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and button_rect.collidepoint(pygame.mouse.get_pos()):
                # Add code to transition to another page with input_text1 and input_text2 values
                print(f"Transitioning to another page with inputs: {name}, {ip}")
                # Button clicked, transition to another page
                if current_page == PAGE_MAIN:
                    current_page = PAGE_RESULT
                elif current_page == PAGE_RESULT:
                    current_page = PAGE_MAIN

    # Draw the input fields and button
    screen.fill(white)
    if current_page == PAGE_MAIN:
        label1_text = font.render("Enter your name:", True, black)
        screen.blit(label1_text, (label1_rect.x + 5, label1_rect.y + 5))

        pygame.draw.rect(screen, black, input_rect1, 2)
        text_surface = font.render(name, True, black)
        screen.blit(text_surface, (input_rect1.x + 5, input_rect1.y + 5))

        label2_text = font.render("Enter server IP:", True, black)
        screen.blit(label2_text, (label2_rect.x + 5, label2_rect.y + 5))

        pygame.draw.rect(screen, black, input_rect2, 2)
        text_surface = font.render(ip, True, black)
        screen.blit(text_surface, (input_rect2.x + 5, input_rect2.y + 5))

        pygame.draw.rect(screen, black, button_rect, 2)
        button_text = font.render("JOIN GAME", True, black)
        button_rect_center = button_rect.center
        button_rect_center = (button_rect_center[0] - button_text.get_width() // 2, button_rect_center[1] - button_text.get_height() // 2)
        screen.blit(button_text, button_rect_center)

    elif current_page == PAGE_RESULT:
        text_surface1 = font.render(name, True, black)
        screen.blit(text_surface1, (width // 2 - text_surface1.get_width() // 2, height // 4))

        # Render and blit the second phrase
        text_surface2 = font.render(ip, True, black)
        screen.blit(text_surface2, (width // 2 - text_surface2.get_width() // 2, height // 2))

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
