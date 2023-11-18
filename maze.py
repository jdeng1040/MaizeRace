import random


def generate_maze(width, height):
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


def print_maze(maze, solution):
    for r, row in enumerate(maze):
        print(' '.join(['+' if (r, c) in solution else cell for c, cell in enumerate(row)]))


def solve_maze(maze, start, end):
    height, width = len(maze), len(maze[0])

    def is_valid(x, y):
        return 0 <= x < width and 0 <= y < height and maze[y][x] in {'S', 'E', '#', '.'}

    DIRECTIONS = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
    ]
    visited = set()

    def dfs(x, y, path):
        if not is_valid(x, y):
            return None

        if (y, x) == end:
            return path

        if (maze[y][x] == '.' or maze[y][x] == 'S') and (x, y) not in visited:
            visited.add((x, y))
            for d in DIRECTIONS:
                newY, newX = d[0] + y, d[1] + x
                if is_valid(newX, newY):
                    path.append((x, y))
                    result = dfs(newX, newY, path)
                    if result:
                        return result
                    path.pop()
            return None

    return dfs(start[1], start[0], [start])


if __name__ == "__main__":
    width = 10
    height = 10

    while True:
        maze, start, end = generate_maze(width, height)
        solution = solve_maze(maze, start, end)
        if solution is not None:
            print_maze(maze, solution)
            break

    print(f"Start position: {start}")
    print(f"End position: {end}")
