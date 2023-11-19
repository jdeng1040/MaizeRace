import random
from collections import deque

random.seed(100)

def _generate_maze(width, height):
    # Initialize the maze with walls
    maze = [['#' for _ in range(width)] for _ in range(height)]

    def carve_path(x, y):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + 2 * dx, y + 2 * dy

            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == '#':
                maze[y + dy][x + dx] = '.'
                maze[ny][nx] = '.'
                carve_path(nx, ny)

    # Start carving paths from a random point
    start_x, start_y = 0, random.randint(0, height - 1)
    carve_path(start_x, start_y)

    # Set the start and end points
    end_x, end_y = width - 1, random.randint(0, height - 1)

    return maze, (start_x, start_y), (end_x, end_y)


def generate_maze(width, height):
    while True:
        maze, start, end = _generate_maze(width, height)
        solution = solve_maze(maze, start, end)
        if solution is not None:
            print_maze(maze, solution)
            return maze, start, end, solution


def print_maze(maze, solution):
    for r, row in enumerate(maze):
        print(' '.join(['+' if (r, c) in solution else cell for c, cell in enumerate(row)]))

def solve_maze(maze, start, end):
    def is_valid_move(maze, position):
        row, col = position
        rows, cols = len(maze), len(maze[0])
        return 0 <= row < rows and 0 <= col < cols and maze[row][col] == "."

    def get_neighbors(position):
        row, col = position
        return [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]

    # Initialize the visited set to keep track of visited cells
    visited = set()

    # Use BFS to find the optimal path
    queue = deque([(start, [])])  # Each element is a tuple (current_position, current_path)

    while queue:
        current_position, current_path = queue.popleft()

        if current_position == end:
            return current_path

        if current_position in visited:
            continue

        visited.add(current_position)

        for neighbor in get_neighbors(current_position):
            if is_valid_move(maze, neighbor):
                queue.append((neighbor, current_path + [current_position]))

    # If no path is found
    return None


SEPARATOR = "|"


def serialize_maze(maze):
    output = []
    for row in maze:
        output.append("".join(row))
    return SEPARATOR.join(output)


def deserialize_maze(maze_string):
    parts = maze_string.split(SEPARATOR)
    output = [list(s) for s in parts]
    return output
