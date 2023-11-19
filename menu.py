import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame Page Example")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)

# Define fonts
font_title = pygame.font.Font(None, 48)
font_input = pygame.font.Font(None, 36)

# Page identifiers
PAGE_MAIN = "main"
PAGE_FAIL = "fail"
current_page = PAGE_MAIN

# Define input field properties
input_rect = pygame.Rect(width // 4, height // 2, width // 2, 40)
input_color_inactive = pygame.Color('lightskyblue3')
input_color_active = pygame.Color('dodgerblue2')
input_color = input_color_inactive
input_text = ''
input_active = False

# Define button properties
button_rect = pygame.Rect(width // 4, height // 2 + 60, width // 2, 40)
button_color = pygame.Color('green')
button_text = 'Enter'

# Define the question
# Generate a random integer between 1 and 10 (inclusive)
first_num = random.randint(0, 12)
second_num = random.randint(0, 12)
question = str(first_num) + " * " + str(second_num)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                input_active = not input_active
                input_color = input_color_active if input_active else input_color_inactive
            elif button_rect.collidepoint(event.pos):
                if int(input_text) == first_num * second_num:
                    print("GOOD")
                else:
                    current_page = PAGE_FAIL

        elif event.type == pygame.KEYDOWN:
            if input_active:
                if event.key == pygame.K_RETURN:
                    if int(input_text) == first_num * second_num:
                        print("GOOD")
                    else:
                        current_page = PAGE_FAIL
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

    # Draw the page
    screen.fill(white)
    if current_page == PAGE_MAIN:
        # Draw title
        title_surface = font_title.render(question, True, black)
        title_rect = title_surface.get_rect(center=(width, height // 4))
        screen.blit(title_surface, title_rect)

        # Draw input field
        pygame.draw.rect(screen, input_color, input_rect, 2)
        input_surface = font_input.render(input_text, True, black)
        width = max(input_rect.w, input_surface.get_width()+10)
        input_rect.w = width
        screen.blit(input_surface, (input_rect.x+5, input_rect.y+5))

        # Draw enter button
        pygame.draw.rect(screen, button_color, button_rect)
        button_surface = font_input.render(button_text, True, white)
        button_rect_center = button_rect.center
        button_rect_center = (button_rect_center[0] - button_surface.get_width() // 2, button_rect_center[1] - button_surface.get_height() // 2)
        screen.blit(button_surface, button_rect_center)
    elif current_page == PAGE_FAIL:
        for i in range(5, 0, -1):
            screen.fill(white)
            text = font_input.render(str(i), True, black)
            text_rect = text.get_rect(center=(width, height // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            time.sleep(1)
        current_page = PAGE_MAIN
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
