import pygame
import sys
from maze import generate_maze
import numpy as np

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Maze Traversal")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Define maze layout (1 represents a wall, 0 represents an open path)
# maze = [
#     [1, 0, 1, 0, 0],
#     [1, 0, 1, 1, 0],
#     [0, 0, 0, 0, 0],
#     [1, 1, 1, 0, 1],
#     [0, 0, 0, 0, 0],
# ]

# Define player position, end position and maze
width, height = 10, 8
gen_maze, start_tuple, end_tuple = generate_maze(width, height)
player_pos = list(start_tuple)
player_pos[0] += 1
player_pos[1] += 1
end_pos = list(end_tuple)
end_pos[0] += 1
end_pos[1] += 1

maze = [['#' for _ in range(width+2)] for _ in range(height+2)]
for row in range(len(gen_maze)):
    for col in range(len(gen_maze[0])):
        maze[row+1][col+1] = gen_maze[row][col]

# Define player size and speed
player_size = 40
player_speed = 1

# Main game loop
running = True
# print("MAZE\n", maze)
print("MAZE\n", np.matrix(maze))
print("end+pos", (end_pos[0], end_pos[1]))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and player_pos[1] > 0 and maze[player_pos[1] - 1][player_pos[0]] == ".":
                player_pos[1] -= 1
            elif event.key == pygame.K_DOWN and player_pos[1] < len(maze) - 1 and maze[player_pos[1] + 1][player_pos[0]] == ".":
                player_pos[1] += 1
            elif event.key == pygame.K_LEFT and player_pos[0] > 0 and maze[player_pos[1]][player_pos[0] - 1] == ".":
                player_pos[0] -= 1
            elif event.key == pygame.K_RIGHT and player_pos[0] < len(maze[0]) - 1 and maze[player_pos[1]][player_pos[0] + 1] == ".":
                player_pos[0] += 1

            if player_pos[0] == end_pos[0] and player_pos[1] == end_pos[1]:
                print("END GAME")
                running = False

    # Draw the maze
    screen.fill(white)
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if col == end_pos[0] and row == end_pos[1]:
                pygame.draw.rect(screen, red, (col * player_size, row * player_size, player_size, player_size))
            elif maze[row][col] == "#":
                pygame.draw.rect(screen, black, (col * player_size, row * player_size, player_size, player_size))
    maze[end_pos[1]][end_pos[0]] = "."
    # Draw the player
    pygame.draw.rect(screen, red, (player_pos[0] * player_size, player_pos[1] * player_size, player_size, player_size))

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
