import pygame
import sys
import network
import helper

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Input Menu")

white = (255, 255, 255)
black = (0, 0, 0)
font = pygame.font.Font(None, 36)

players = []

client = None

class Menu:
    # Page identifiers
    PAGE_MAIN = "main"
    PAGE_RESULT = "result"

    def __init__(self):
        self.label1_rect = pygame.Rect(width // 4, height // 8 + 40, width // 2, 40)
        self.input_rect1 = pygame.Rect(width // 4, height // 4, width // 2, 40)
        self.label2_rect = pygame.Rect(width // 4, height // 2 - 50, width // 2, 40)
        self.input_rect2 = pygame.Rect(width // 4, height // 2 - 10, width // 2, 40)
        self.button_rect = pygame.Rect(width // 4, height * 3 // 4, width // 2, 40)

        self.name = ""
        self.ip = ""
        self.current_page = Menu.PAGE_MAIN
    
    def handleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if self.input_rect1.collidepoint(pygame.mouse.get_pos()):
                    if event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]
                    else:
                        self.name += event.unicode
                elif self.input_rect2.collidepoint(pygame.mouse.get_pos()):
                    if event.key == pygame.K_BACKSPACE:
                        self.ip = self.ip[:-1]
                    else:
                        self.ip += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.button_rect.collidepoint(pygame.mouse.get_pos()):
                    print(f"Transitioning to another page with inputs: {self.name}, {self.ip}")

                    # Button clicked, transition to another page
                    if self.current_page == Menu.PAGE_MAIN:
                        global client
                        client = network.Client(self.name, self.ip)
                        self.current_page = Menu.PAGE_RESULT
    
    def draw(self, screen):
        screen.fill(white)
        if self.current_page == Menu.PAGE_MAIN:
            label1_text = font.render("Enter your name:", True, black)
            screen.blit(label1_text, (self.label1_rect.x + 5, self.label1_rect.y + 5))

            pygame.draw.rect(screen, black, self.input_rect1, 2)
            text_surface = font.render(self.name, True, black)
            screen.blit(text_surface, (self.input_rect1.x + 5, self.input_rect1.y + 5))

            label2_text = font.render("Enter server IP:", True, black)
            screen.blit(label2_text, (self.label2_rect.x + 5, self.label2_rect.y + 5))

            pygame.draw.rect(screen, black, self.input_rect2, 2)
            text_surface = font.render(self.ip, True, black)
            screen.blit(text_surface, (self.input_rect2.x + 5, self.input_rect2.y + 5))

            pygame.draw.rect(screen, black, self.button_rect, 2)
            button_text = font.render("JOIN GAME", True, black)
            button_rect_center = self.button_rect.center
            button_rect_center = (button_rect_center[0] - button_text.get_width() // 2, button_rect_center[1] - button_text.get_height() // 2)
            screen.blit(button_text, button_rect_center)
        elif self.current_page == Menu.PAGE_RESULT:
            title_surface = font.render("Waiting for players...", True, black)
            screen.blit(title_surface, (width // 2 - title_surface.get_width() // 2, height // 8))
            for i, item in enumerate(players):
                text_surface = font.render(str(i + 1) + ". " + item, True, black)
                screen.blit(text_surface, (width // 2 - text_surface.get_width() // 2, height // 4 + i * 40))


# States
MENU_STATE = "menu"
PLAY_STATE = "play"
FINISH_STATE = "finish"
state = MENU_STATE

menu = Menu()

while True:
    if state == MENU_STATE:
        menu.handleEvent()
        
        if client is not None:
            response = client.sendConnect()
            if response['type'] == helper.PLAYERS:
                players = response['players']
            elif response['type'] == helper.BEGIN:
                print("moving to play state")
                state = PLAY_STATE
            else:
                print("unknown type", response)
                sys.exit(1)
        menu.draw(screen)
    elif state == PLAY_STATE:
        print("Play state")
        pass
    elif state == FINISH_STATE:
        pass
    else:
        print("unknown state")
        sys.exit(1)
    
    pygame.display.flip()
