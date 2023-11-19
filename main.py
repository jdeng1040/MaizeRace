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
red = (255, 0, 0)
gray = (211, 211, 211)
blue = (0, 0, 255)
green = (0, 255, 0)
orange = (255, 165, 0)

stringToColor = {
    "white": white,
    "black": black,
    "red": red,
    "gray": gray,
    "blue": blue,
    "green": green,
    "orange": orange,
}

font = pygame.font.Font(None, 36)

players = []

client = None
name = ""

class Menu:
    # Page identifiers
    PAGE_MAIN = "main"
    PAGE_RESULT = "result"

    def __init__(self):
        color_option_width = 200
        color_option_spacing = 10

        # Calculate the total width of the color options row
        total_color_options_width = (
            4 * color_option_width + 3 * color_option_spacing
        )
        start_x = (width - total_color_options_width) // 2

        self.label1_rect = pygame.Rect(width // 4, height // 8, width // 2, 40)
        self.input_rect1 = pygame.Rect(width // 4, height // 4 - 40, width // 2, 40)
        self.label2_rect = pygame.Rect(width // 4, height // 2 - 120, width // 2, 40)
        self.input_rect2 = pygame.Rect(width // 4, height // 2 - 90, width // 2, 40)
        self.color1 = pygame.Rect(start_x, height // 2 + 50, color_option_width, 40)
        self.color2 = pygame.Rect(start_x + color_option_width + color_option_spacing, height // 2 + 50, color_option_width, 40)
        self.color3 = pygame.Rect(start_x + 2 * (color_option_width + color_option_spacing), height // 2 + 50, color_option_width, 40)
        self.color4 = pygame.Rect(start_x + 3 * (color_option_width + color_option_spacing), height // 2 + 50, color_option_width, 40)
        self.button_rect = pygame.Rect(width // 4, height * 3 // 4, width // 2, 40)
        self.ip = ""
        self.selected_option = "RED"
        self.current_page = Menu.PAGE_MAIN

    def handleEvent(self):
       
        global name
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if self.input_rect1.collidepoint(pygame.mouse.get_pos()):
                    global name
                    if event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode
                elif self.input_rect2.collidepoint(pygame.mouse.get_pos()):
                    if event.key == pygame.K_BACKSPACE:
                        self.ip = self.ip[:-1]
                    else:
                        self.ip += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.button_rect.collidepoint(pygame.mouse.get_pos()):
                    print(f"Transitioning to another page with inputs: {name}, {self.ip}")
                    # Button clicked, transition to another page
                    if self.current_page == Menu.PAGE_MAIN:
                        global client
                        client = network.Client(self.ip, name, self.selected_option)
                        self.current_page = Menu.PAGE_RESULT
                elif self.color1.collidepoint(pygame.mouse.get_pos()):
                    self.selected_option = "RED"
                elif self.color2.collidepoint(pygame.mouse.get_pos()):
                    self.selected_option = "BLUE"
                elif self.color3.collidepoint(pygame.mouse.get_pos()):
                    self.selected_option = "GREEN"
                elif self.color4.collidepoint(pygame.mouse.get_pos()):
                    self.selected_option = "ORANGE"
    def draw(self, screen):
        global name
        screen.fill(white)
        if self.current_page == Menu.PAGE_MAIN:
            label1_text = font.render("Enter your name:", True, black)
            screen.blit(label1_text, (self.label1_rect.x + 5, self.label1_rect.y + 5))

            pygame.draw.rect(screen, black, self.input_rect1, 2)
            text_surface = font.render(name, True, black)
            screen.blit(text_surface, (self.input_rect1.x + 5, self.input_rect1.y + 5))

            label2_text = font.render("Enter server IP:", True, black)
            screen.blit(label2_text, (self.label2_rect.x + 5, self.label2_rect.y + 5))

            pygame.draw.rect(screen, black, self.input_rect2, 2)
            text_surface = font.render(self.ip, True, black)
            screen.blit(text_surface, (self.input_rect2.x + 5, self.input_rect2.y + 5))

            text_surface = font.render("Choose your color", True, black)
            screen.blit(text_surface, (width // 4 + 80, height // 2))

            if self.selected_option == "RED":
                text_surface = font.render("RED", True, red)
            else: 
                text_surface = font.render("RED", True, black)
            text_rect = text_surface.get_rect(center=(self.color1.x + self.color1.width // 2, self.color1.y + self.color1.height // 2))
            screen.blit(text_surface, text_rect.topleft)

            if self.selected_option == "BLUE":
                text_surface = font.render("BLUE", True, blue)
            else :
                text_surface = font.render("BLUE", True, black)
            text_rect = text_surface.get_rect(center=(self.color2.x + self.color2.width // 2, self.color2.y + self.color2.height // 2))
            screen.blit(text_surface, text_rect.topleft)

            if self.selected_option == "GREEN":
                text_surface = font.render("GREEN", True, green)
            else:
                text_surface = font.render("GREEN", True, black)
            text_rect = text_surface.get_rect(center=(self.color3.x + self.color3.width // 2, self.color3.y + self.color3.height // 2))
            screen.blit(text_surface, text_rect.topleft)

            if self.selected_option == "ORANGE":
                text_surface = font.render("ORANGE", True, orange)
            else:
                text_surface = font.render("ORANGE", True, black)
            text_rect = text_surface.get_rect(center=(self.color4.x + self.color4.width // 2, self.color4.y + self.color4.height // 2))
            screen.blit(text_surface, text_rect.topleft)

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


class Playing:
    def __init__(self, maze, start, end, barrier_positions):
        self.width = len(maze[0])
        self.height = len(maze)
        self.player_pos = [start[1] + 1, start[0] + 1]
        self.end = [end[1] + 1, end[0] + 1]
        self.locations = {}
        self.colors = {}
        self.barrier_positions = barrier_positions
        print("barriers: ", self.barrier_positions)

        self.maze = [['#' for _ in range(self.width+2)] for _ in range(self.height+2)]
        for row in range(len(maze)):
            for col in range(len(maze[0])):
                self.maze[row+1][col+1] = maze[row][col]
        
        self.player_size = 20
        self.player_speed = 1
    
    def handleEvent(self):
        """
        Returns if the player won or not
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.player_pos[1] > 0 and self.maze[self.player_pos[1] - 1][self.player_pos[0]] == ".":
                    self.player_pos[1] -= 1
                elif event.key == pygame.K_DOWN and self.player_pos[1] < len(self.maze) - 1 and self.maze[self.player_pos[1] + 1][self.player_pos[0]] == ".":
                    self.player_pos[1] += 1
                elif event.key == pygame.K_LEFT and self.player_pos[0] > 0 and self.maze[self.player_pos[1]][self.player_pos[0] - 1] == ".":
                    self.player_pos[0] -= 1
                elif event.key == pygame.K_RIGHT and self.player_pos[0] < len(self.maze[0]) - 1 and self.maze[self.player_pos[1]][self.player_pos[0] + 1] == ".":
                    self.player_pos[0] += 1
        
        return self.player_pos[0] == self.end[0] and self.player_pos[1] == self.end[1]
    
    def draw(self, screen):
        global name
        screen.fill(white)
        for row in range(len(self.maze)):
            for col in range(len(self.maze[0])):
                if col == self.end[0] and row == self.end[1]:
                    pygame.draw.rect(screen, red, (col * self.player_size, row * self.player_size, self.player_size, self.player_size))
                elif self.maze[row][col] == "#":
                    pygame.draw.rect(screen, black, (col * self.player_size, row * self.player_size, self.player_size, self.player_size))
                elif [row-1, col-1] in self.barrier_positions:
                    pygame.draw.rect(screen, gray, (col * self.player_size, row * self.player_size, self.player_size, self.player_size))
        self.maze[self.end[1]][self.end[0]] = "."
        
        # Draw the player
        global client
        pygame.draw.rect(screen, client.color, (self.player_pos[0] * self.player_size, self.player_pos[1] * self.player_size, self.player_size, self.player_size))

        # Draw the other players
        # players is just a list of names of players
        for player in players:
            if player != name:
                ppos = self.locations[player]
                pygame.draw.rect(screen, stringToColor[self.colors[player].lower()], (ppos[0] * self.player_size, ppos[1] * self.player_size, self.player_size, self.player_size))

    def update_locations(self, all_locations, all_colors):
        self.locations = all_locations
        self.colors = all_colors


class Quiz:
    PAGE_MAIN = "main"
    PAGE_FAIL = "fail"

    input_color_inactive = pygame.Color('lightskyblue3')
    input_color_active = pygame.Color('dodgerblue2')
    input_color = input_color_inactive
    input_text = ''
    input_active = False

    def __init__(self):
        self.font_title = pygame.font.Font(None, 48)
        self.font_input = pygame.font.Font(None, 36)
        self.current_page = Quiz.PAGE_MAIN
        self.input_rect = pygame.Rect(width // 4, height // 2, width // 2, 40)

    def handleEvent(self):
        pass


    def draw(self, screen):
        pass


# States
MENU_STATE = "menu"
PLAY_STATE = "play"
FINISH_STATE = "finish"
QUIZ_STATE = "quiz"
state = MENU_STATE

menu = Menu()
playing = None
quiz = None

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
                maze = response['maze']
                start = response['start']
                end = response['end']
                players = response['players']
                playing = Playing(maze, start, end, response['barriers'])
            else:
                print("unknown type", response)
                sys.exit(1)
        menu.draw(screen)
    elif state == PLAY_STATE:
        if playing.handleEvent():
            # won,
            print("won")
            # exit
            pygame.quit()
        
        response = client.sendPosition(playing.player_pos, name)
        if response["type"] == helper.ALL_POSITIONS:
            all_locations = response["locations"]
            print("ALL LOCATIONS:\n-----------", all_locations)
            print("PLAYERS :\n-----------", players)
            playing.update_locations(all_locations, response["colors"])
        else:
            print("unknown return")
            sys.exit(1)

        if [playing.player_pos[0]-1, playing.player_pos[1]-1] in playing.barrier_positions:
            state = QUIZ_STATE
            quiz = Quiz()

        playing.draw(screen)
    elif state == QUIZ_STATE:
        if quiz.handleEvent():
            state = PLAY_STATE
        quiz.draw(screen)

    elif state == FINISH_STATE:
        pass
    else:
        print("unknown state")
        sys.exit(1)
    
    pygame.display.flip()
