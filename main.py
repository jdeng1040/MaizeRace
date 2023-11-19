import pygame
import sys
import network
import helper
import random
import time
from datetime import datetime

from pygame.locals import (
    RLEACCEL,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()
width, height = 640, 640
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("The Maize Game")

white = (251,247,245)
black = (0, 0, 0)
red = (255, 0, 0)
gray = (211, 211, 211)
blue = (0, 0, 255)
green = (0, 255, 0)
orange = (255, 165, 0)
light_blue = (249,241,241)
maize = (11, 11, 69)
navy_blue = (11, 11, 69)

stringToColor = {
    "white": white,
    "black": black,
    "red": red,
    "gray": gray,
    "blue": blue,
    "green": green,
    "orange": orange,
}

red_img = pygame.image.load("red.png").convert()
blue_img = pygame.image.load("blue.png").convert()
green_img = pygame.image.load("green.png").convert()
orange_img = pygame.image.load("orange.png").convert()
red_img.set_colorkey((0, 0, 0), RLEACCEL)
blue_img.set_colorkey((0, 0, 0), RLEACCEL)
green_img.set_colorkey((0, 0, 0), RLEACCEL)
orange_img.set_colorkey((0, 0, 0), RLEACCEL)

stringToImage = {
    "red": red_img,
    "blue": blue_img,
    "green": green_img,
    "orange": orange_img
}

font = pygame.font.Font(None, 36)
bigfont = pygame.font.Font(None, 46)

players = []

client = None
name = "jj"
start_time = None

class Menu:
    # Page identifiers
    PAGE_MAIN = "main"
    PAGE_RESULT = "result"

    def __init__(self):
        color_option_width = 150
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
        self.ip = "127.0.0.1"
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
        screen.fill(light_blue)
        if self.current_page == Menu.PAGE_MAIN:
            title_text = bigfont.render("Welcome to The Maize Game!", True, maize)
            screen.blit(title_text, (self.label1_rect.x - 50, self.label1_rect.y - 50))

            label1_text = font.render("Enter your name:", True, black)
            screen.blit(label1_text, (self.label1_rect.x + 5, self.label1_rect.y + 5))

            pygame.draw.rect(screen, black, self.input_rect1, 2)
            text_surface = font.render(name, True, black)
            screen.blit(text_surface, (self.input_rect1.x + 5, self.input_rect1.y + 5))

            label2_text = font.render("Enter server IPv4 address:", True, black)
            screen.blit(label2_text, (self.label2_rect.x + 5, self.label2_rect.y + 5))

            pygame.draw.rect(screen, black, self.input_rect2, 2)
            text_surface = font.render(self.ip, True, black)
            screen.blit(text_surface, (self.input_rect2.x + 5, self.input_rect2.y + 5))

            text_surface = font.render("Choose your character color", True, black)
            screen.blit(text_surface, (width // 4 + 20, height // 2))

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
            global start_time
            if start_time is not None:
                seconds_left = int((start_time-datetime.now()).total_seconds())
                print(seconds_left)
                text = font.render(f"Start in {seconds_left} second{'s' if seconds_left > 1 else ''}", True, black)
                i = len(players)
                screen.blit(text, (width // 2 - text.get_width() // 2, height // 4 + i * 40))
                if seconds_left <= 0:
                    return True
        return False


class Finish:
    def __init__(self):
        self.rankings = []
    
    def handleEvent(self):
        # allow users to close the game
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == K_ESCAPE:
                    pygame.quit()

            # Did the user click the window close button? If so, stop the loop.
            elif event.type == QUIT:
                pygame.quit()

    def draw(self, screen):
        screen.fill(light_blue)
        title_surface = font.render("You finished!", True, black)
        title_surface2 = font.render("Leaderboard", True, black)
        screen.blit(title_surface, (width // 2 + 100, height // 12))
        screen.blit(title_surface2, (width // 2 + 100, height // 4))
        for i, item in enumerate(self.rankings):
            text_surface = font.render(str(i + 1) + ". " + item, True, black)
            screen.blit(text_surface, (width // 2 + 100, height // 3 + i * 40))


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

        self.wall_img = pygame.image.load("bricks.png").convert()
        self.wall_img.set_colorkey((0, 0, 0), RLEACCEL)
        self.barrier_img = pygame.image.load("gemstone.png").convert()
        self.barrier_img.set_colorkey((0, 0, 0), RLEACCEL)
        self.end_img = pygame.image.load("star.png").convert()
        self.end_img.set_colorkey((0, 0, 0), RLEACCEL)
        self.player_img = stringToImage[client.color.lower()]
        self.player_img.set_colorkey((0, 0, 0), RLEACCEL)

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
                    #pygame.draw.rect(screen, red, (col * self.player_size, row * self.player_size, self.player_size, self.player_size))
                    screen.blit(self.end_img, (col * self.player_size, row * self.player_size))
                elif self.maze[row][col] == "#":
                    #pygame.draw.rect(screen, black, (col * self.player_size, row * self.player_size, self.player_size, self.player_size))
                    screen.blit(self.wall_img, (col * self.player_size, row * self.player_size))
                elif [row-1, col-1] in self.barrier_positions:
                    #pygame.draw.rect(screen, gray, (col * self.player_size, row * self.player_size, self.player_size, self.player_size))
                    screen.blit(self.barrier_img, (col * self.player_size, row * self.player_size))

        self.maze[self.end[1]][self.end[0]] = "."
        
        # Draw the player
        global client
        # pygame.draw.rect(screen, client.color, (self.player_pos[0] * self.player_size, self.player_pos[1] * self.player_size, self.player_size, self.player_size))
        screen.blit(self.player_img, (self.player_pos[0] * self.player_size, self.player_pos[1]* self.player_size))

        # Draw the other players
        # players is just a list of names of players
        for player in players:
            if player != name:
                ppos = self.locations[player]
                #ygame.draw.rect(screen, stringToColor[self.colors[player].lower()], (ppos[0] * self.player_size, ppos[1] * self.player_size, self.player_size, self.player_size))
                screen.blit(stringToImage[self.colors[player].lower()], (ppos[0] * self.player_size, ppos[1] * self.player_size))

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
    input_active = True

    # Define button properties
    button_rect = pygame.Rect(width // 4, height // 2 + 60, width // 2, 40)
    button_color = pygame.Color(navy_blue)
    button_text = 'Enter'

    input_rect = pygame.Rect(width // 4, height // 2, width // 2, 40)

    operator = ""

    def __init__(self):
        self.font_title = pygame.font.Font(None, 48)
        self.font_input = pygame.font.Font(None, 36)
        self.current_page = Quiz.PAGE_MAIN
        self.first_num = random.randint(0, 12)
        self.second_num = random.randint(0, self.first_num)
        self.operator = random.choice([" + ", " - ", " * "])
        self.question = str(self.first_num) + self.operator + str(self.second_num) + " = ?"

    def handleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if self.input_rect.collidepoint(event.pos):
                #     self.input_active = not self.input_active
                #     self.input_color = self.input_color_active if self.input_active else self.input_color_inactive
                if self.button_rect.collidepoint(event.pos) and self.input_text and self.input_text.isdigit():
                    if int(self.input_text) == self.first_num * self.second_num:
                        return True
                    else:
                        self.current_page = self.PAGE_FAIL

            elif event.type == pygame.KEYDOWN:
                if self.input_active:
                    if event.key == pygame.K_RETURN and self.input_text and self.input_text.isdigit():
                        if self.operator == " * " and int(self.input_text) == self.first_num * self.second_num:
                            return True
                        elif self.operator == " + " and int(self.input_text) == self.first_num + self.second_num:
                            return True
                        elif self.operator == " - " and int(self.input_text) == self.first_num - self.second_num:
                            return True
                        else:
                            self.current_page = self.PAGE_FAIL
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        self.input_text += event.unicode
        return False

    def draw(self, screen):
        # Draw the page
        screen.fill(white)
        global width
        global height
        if self.current_page == self.PAGE_MAIN:
            # Draw title
            title_surface = self.font_title.render(self.question, True, black)
            title_rect = title_surface.get_rect(center=(width, height // 4))
            screen.blit(title_surface, title_rect)

            # Draw input field
            pygame.draw.rect(screen, self.input_color, self.input_rect, 2)
            input_surface = self.font_input.render(self.input_text, True, black)
            width = max(self.input_rect.w, input_surface.get_width()+10)
            self.input_rect.w = width
            screen.blit(input_surface, (self.input_rect.x+5, self.input_rect.y+5))

            # Draw enter button
            pygame.draw.rect(screen, self.button_color, self.button_rect)
            button_surface = self.font_input.render(self.button_text, True, white)
            self.button_rect_center = self.button_rect.center
            self.button_rect_center = (self.button_rect_center[0] - button_surface.get_width() // 2, self.button_rect_center[1] - button_surface.get_height() // 2)
            screen.blit(button_surface, self.button_rect_center)
        elif self.current_page == self.PAGE_FAIL:
            for i in range(3, 0, -1):
                screen.fill(white)
                title_surface = font.render("Wrong answer! Try again in: ", True, black)
                screen.blit(title_surface, (width // 2, height // 3))

                text = self.font_input.render(str(i), True, black)
                text_rect = text.get_rect(center=(width, height // 2))
                screen.blit(text, text_rect)
                pygame.display.flip()
                time.sleep(1)
            self.current_page = self.PAGE_MAIN


# States
MENU_STATE = "menu"
PLAY_STATE = "play"
FINISH_STATE = "finish"
QUIZ_STATE = "quiz"
state = MENU_STATE

menu = Menu()
finish = Finish()
playing = None

while True:
    if state == MENU_STATE:
        menu.handleEvent()
        
        if client is not None:
            response = client.sendConnect()
            if response['type'] == helper.PLAYERS:
                players = response['players']
            elif response['type'] == helper.BEGIN:
                print("moving to play state")
                maze = response['maze']
                start = response['start']
                end = response['end']
                players = response['players']
                start_time = datetime.fromisoformat(response['start_time'])
                playing = Playing(maze, start, end, response['barriers'])
            else:
                print("unknown type", response)
                sys.exit(1)
        if menu.draw(screen):
            state = PLAY_STATE
    elif state == PLAY_STATE:
        if playing.handleEvent():
            print(f"{name} Finished")
            state = FINISH_STATE

        response = client.sendPosition(playing.player_pos, name)
        if response["type"] == helper.ALL_POSITIONS:
            all_locations = response["locations"]
            playing.update_locations(all_locations, response["colors"])
        else:
            print("unknown return")
            sys.exit(1)

        if [playing.player_pos[1]-1, playing.player_pos[0]-1] in playing.barrier_positions:
            playing.barrier_positions.remove([playing.player_pos[1]-1, playing.player_pos[0]-1])
            state = QUIZ_STATE
            quiz = Quiz()

        playing.draw(screen)
    elif state == QUIZ_STATE:
        if quiz.handleEvent():
            state = PLAY_STATE
        quiz.draw(screen)

    elif state == FINISH_STATE:
        # send message to server
        response = client.sendFinish(name)

        if response["type"] == helper.FINISH:
            finish.rankings = response["rankings"]
        else:
            print("unknown return")
            sys.exit(1)

        # render the ranking screen
        finish.handleEvent()
        finish.draw(screen)

    else:
        print("unknown state")
        sys.exit(1)
    
    pygame.display.flip()
