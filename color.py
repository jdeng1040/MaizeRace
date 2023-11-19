import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 400, 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Option Selector")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
highlight_color = (255, 0, 0)  # Red for highlighting

# Font and text settings
font = pygame.font.Font(None, 36)
text_color = black

# Options
options = ["Option 1", "Option 2", "Option 3", "Option 4"]
selected_option = options[0]

# Function to draw text on the screen
def draw_text(text, x, y, highlight=False):
    text_color = highlight_color if highlight else black
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
    return text_rect  # Return the Rect object

# Main game loop
running = True
while running:
    screen.fill(white)

    # Draw options
    option_rects = []  # List to store Rect objects for each option
    for i, option in enumerate(options):
        y_offset = 50 * i - 50  # Adjusted y_offset
        is_selected = option == selected_option
        rect = draw_text(option, width // 2, height // 2 + y_offset, is_selected)
        option_rects.append(rect)

    # Draw selected option
    draw_text("Selected Option: " + selected_option, width // 2, height - 50)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the click is within the bounds of an option
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for i, rect in enumerate(option_rects):
                if rect.collidepoint(mouse_x, mouse_y):
                    selected_option = options[i]

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
