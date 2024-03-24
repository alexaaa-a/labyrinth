import matplotlib.pyplot as plt
import random

from dataclasses import dataclass, field

@dataclass
class MazeCell:
    x: int
    y: int
    component: int
    is_open: bool = field(default=False)
    walls: list = field(default_factory=lambda: [True, True, True, True])

N = 30
LINE_WIDTH = 50

def find(x, parent):
    if x != parent[x]:
        parent[x] = find(parent[x], parent)
    return parent[x]

def union(x, y, parent):
    root_x = find(x, parent)
    root_y = find(y, parent)
    if root_x != root_y:
        parent[root_x] = root_y

def generate_maze(n):
    maze = [[MazeCell(x, y, x * n + y, walls=[True, True, True, True]) for y in range(n)] for x in range(n)]
    parent = [i for i in range(n * n)]

    maze[0][1].is_open = True
    maze[n-1][n-2].is_open = True

    def is_valid_cell(x, y):
        return 0 <= x < n and 0 <= y < n

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def make_opening(cell):
        nonlocal maze, parent
        x, y = cell.x, cell.y
        walls_to_remove = []
        for i, (dx, dy) in enumerate(directions):
            nx, ny = x + dx, y + dy
            if is_valid_cell(nx, ny) and not maze[nx][ny].is_open:
                walls_to_remove.append(i)
        if walls_to_remove:
            wall_index = random.choice(walls_to_remove)
            dx, dy = directions[wall_index]
            nx, ny = x + dx, y + dy
            union(x * n + y, nx * n + ny, parent)
            maze[x][y].walls[wall_index] = False
            maze[nx][ny].walls[(wall_index + 2) % 4] = False

    make_opening(maze[0][1])
    make_opening(maze[n-1][n-2])

    while len(set(find(cell.x * n + cell.y, parent) for row in maze for cell in row)) > 1:
        x, y = random.randint(0, n - 1), random.randint(0, n - 1)
        dx, dy = random.choice(directions)
        nx, ny = x + dx, y + dy

        if is_valid_cell(nx, ny) and (x != 0 or y != 1) and (nx != n-1 or ny != n-2):
            if find(x * n + y, parent) != find(nx * n + ny, parent):
                union(x * n + y, nx * n + ny, parent)
                maze[x][y].walls[directions.index((dx, dy))] = False
                maze[nx][ny].walls[directions.index((-dx, -dy))] = False

    return maze

def draw_maze(maze):
    plt.figure(figsize=(10, 10))

    for row in maze:
        for cell in row:
            x, y = cell.x, cell.y

            if cell.walls[0] and x != 0 and y != 1:
                plt.plot([x, x + 1], [y + 1, y + 1], 'k-', lw=2)
            if cell.walls[1]:
                plt.plot([x + 1, x + 1], [y, y + 1], 'k-', lw=2)
            if cell.walls[2] and x != 29 and y != 30:
                plt.plot([x, x + 1], [y, y], 'k-', lw=2)
            if cell.walls[3]:
                plt.plot([x, x], [y, y + 1], 'k-', lw=2)

    plt.show()

maze = generate_maze(N)
draw_maze(maze)
