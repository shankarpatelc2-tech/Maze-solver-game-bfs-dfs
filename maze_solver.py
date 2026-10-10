import pygame
import random
import time
from collections import deque

# Initialize Pygame
pygame.init()

# Game settings
ROWS = 20
COLS = 25
CELL = 28
TOP = 80

WIDTH = COLS * CELL
HEIGHT = ROWS * CELL + TOP

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver - BFS and DFS")

# Colors
WHITE = (255, 255, 255)
BLACK = (25, 25, 35)
GRAY = (190, 190, 200)
GREEN = (40, 190, 90)
RED = (230, 65, 65)
BLUE = (50, 130, 240)
YELLOW = (255, 210, 60)
PURPLE = (160, 100, 220)
DARK = (35, 40, 55)

font = pygame.font.SysFont("arial", 19)
small_font = pygame.font.SysFont("arial", 15)

# Start and goal
start = (0, 0)
goal = (ROWS - 1, COLS - 1)

walls = set()
visited = set()
path = []
message = "Draw walls, then select BFS or DFS"
stats = ""
running = True
mode = "draw"


def neighbors(node):
    r, c = node
    result = []

    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nr, nc = r + dr, c + dc
        nxt = (nr, nc)

        if (0 <= nr < ROWS and 0 <= nc < COLS
                and nxt not in walls):
            result.append(nxt)

    return result


def solve(algorithm):
    global visited, path, message, stats

    visited = set()
    path = []
    parent = {}
    nodes_explored = 0

    start_time = time.perf_counter()

    if algorithm == "BFS":
        frontier = deque([start])
        visited.add(start)

        while frontier:
            current = frontier.popleft()
            nodes_explored += 1

            if current == goal:
                break

            for nxt in neighbors(current):
                if nxt not in visited:
                    visited.add(nxt)
                    parent[nxt] = current
                    frontier.append(nxt)

    else:  # DFS
        frontier = [start]
        visited.add(start)

        while frontier:
            current = frontier.pop()
            nodes_explored += 1

            if current == goal:
                break

            for nxt in neighbors(current):
                if nxt not in visited:
                    visited.add(nxt)
                    parent[nxt] = current
                    frontier.append(nxt)

    elapsed = (time.perf_counter() - start_time) * 1000

    if goal in visited:
        current = goal

        while current != start:
            path.append(current)
            current = parent[current]

        path.append(start)
        path.reverse()

        message = f"{algorithm}: Path found!"
        stats = (
            f"Path: {len(path) - 1} steps | "
            f"Nodes: {nodes_explored} | "
            f"Time: {elapsed:.3f} ms"
        )
    else:
        message = f"{algorithm}: No path found!"
        stats = (
            f"Nodes: {nodes_explored} | "
            f"Time: {elapsed:.3f} ms"
        )


def generate_maze():
    global walls, visited, path, message, stats

    walls = set()
    visited = set()
    path = []

    for r in range(ROWS):
        for c in range(COLS):
            if random.random() < 0.27:
                node = (r, c)
                if node != start and node != goal:
                    walls.add(node)

    message = "New maze generated"
    stats = ""


def draw_text(text, x, y, color=WHITE, f=font):
    image = f.render(text, True, color)
    screen.blit(image, (x, y))


def draw_button(text, x, y, width, color):
    rect = pygame.Rect(x, y, width, 30)
    pygame.draw.rect(screen, color, rect, border_radius=5)
    label = small_font.render(text, True, WHITE)
    screen.blit(label, label.get_rect(center=rect.center))
    return rect


def draw_game():
    screen.fill(DARK)

    draw_text("MAZE SOLVER: BFS vs DFS", 10, 8)
    draw_text("BFS", 10, 43, GREEN, small_font)
    draw_text("DFS", 55, 43, BLUE, small_font)
    draw_text("Reset", 100, 43, WHITE, small_font)
    draw_text("New Maze", 155, 43, YELLOW, small_font)

    draw_text(message, 280, 8, YELLOW, small_font)
    draw_text(stats, 280, 35, WHITE, small_font)

    for r in range(ROWS):
        for c in range(COLS):
            node = (r, c)
            rect = pygame.Rect(
                c * CELL, TOP + r * CELL, CELL, CELL
            )

            color = WHITE

            if node in walls:
                color = BLACK
            if node in visited:
                color = PURPLE
            if node in path:
                color = YELLOW
            if node == start:
                color = GREEN
            if node == goal:
                color = RED

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)

    pygame.display.flip()


bfs_button = pygame.Rect(5, 42, 42, 30)
dfs_button = pygame.Rect(50, 42, 42, 30)
reset_button = pygame.Rect(98, 42, 48, 30)
maze_button = pygame.Rect(151, 42, 80, 30)

generate_maze()

while running:
    draw_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if bfs_button.collidepoint(x, y):
                solve("BFS")

            elif dfs_button.collidepoint(x, y):
                solve("DFS")

            elif reset_button.collidepoint(x, y):
                walls.clear()
                visited.clear()
                path.clear()
                message = "Board reset"
                stats = ""

            elif maze_button.collidepoint(x, y):
                generate_maze()

            elif y >= TOP:
                c = x // CELL
                r = (y - TOP) // CELL
                node = (r, c)

                if node != start and node != goal:
                    if node in walls:
                        walls.remove(node)
                    else:
                        walls.add(node)

                    visited.clear()
                    path.clear()
                    stats = ""

pygame.quit()
