import pygame
import random
import time
import sys


WIDTH, HEIGHT = 1366, 768
GRID_SIZE = 30
MAZE_WIDTH, MAZE_HEIGHT = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
BACKGROUND_COLOR = (0, 0, 0)
WALL_COLOR = (255, 255, 255)
PATH_COLOR = (50, 50, 50)
PLAYER_COLOR = (255, 0, 0)
EXIT_COLOR = (0, 0, 255)
HINT_COLOR = (0, 255, 0)
FPS = 60

TIME_LIMIT = 60
MOVE_TIMEOUT = 10.2


DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]  

def generate_maze():
    maze = [[1] * MAZE_WIDTH for _ in range(MAZE_HEIGHT)]

    def carve(x, y):
        maze[y][x] = 0
        directions = DIRECTIONS.copy()
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and maze[ny][nx] == 1:
                maze[ny][nx] = 0
                maze[y + dy][x + dx] = 0
                carve(nx, ny)

    start_x, start_y = random.randint(0, MAZE_WIDTH - 1), random.randint(0, MAZE_HEIGHT - 1)
    carve(start_x, start_y)

    
    exit_x, exit_y = start_x, start_y
    while exit_x == start_x and exit_y == start_y:
        exit_x, exit_y = random.randint(0, MAZE_WIDTH - 1), random.randint(0, MAZE_HEIGHT - 1)
    
        if maze[exit_y][exit_x] != 0:
            exit_x, exit_y = start_x, start_y

    return maze, (start_x, start_y), (exit_x, exit_y)

def draw_maze(maze, player_pos, exit_pos, screen):
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            color = WALL_COLOR if maze[y][x] == 1 else PATH_COLOR
            pygame.draw.rect(screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    pygame.draw.rect(screen, PLAYER_COLOR, (player_pos[0] * GRID_SIZE, player_pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(screen, EXIT_COLOR, (exit_pos[0] * GRID_SIZE, exit_pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def provide_hint(player_pos, maze, screen):
    possible_moves = []
    for dx, dy in DIRECTIONS:
        nx, ny = player_pos[0] + dx, player_pos[1] + dy
        if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and maze[ny][nx] == 0:
            possible_moves.append((nx, ny))

    if possible_moves:
        next_move = random.choice(possible_moves)
        pygame.draw.rect(screen, HINT_COLOR, (next_move[0] * GRID_SIZE, next_move[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Game with Hints")
    clock = pygame.time.Clock()

    maze, start_pos, exit_pos = generate_maze()
    player_pos = list(start_pos)
    last_move_time = time.time()
    start_time = time.time()

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        draw_maze(maze, player_pos, exit_pos, screen)

        elapsed_time = time.time() - start_time
        if elapsed_time > TIME_LIMIT:
            print("Time's up!")
            running = False

        if time.time() - last_move_time > MOVE_TIMEOUT:
            provide_hint(player_pos, maze, screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    new_pos = (player_pos[0] - 1, player_pos[1])
                elif event.key == pygame.K_RIGHT:
                    new_pos = (player_pos[0] + 1, player_pos[1])
                elif event.key == pygame.K_UP:
                    new_pos = (player_pos[0], player_pos[1] - 1)
                elif event.key == pygame.K_DOWN:
                    new_pos = (player_pos[0], player_pos[1] + 1)
                else:
                    continue

                if 0 <= new_pos[0] < MAZE_WIDTH and 0 <= new_pos[1] < MAZE_HEIGHT and maze[new_pos[1]][new_pos[0]] == 0:
                    player_pos = new_pos
                    last_move_time = time.time()

    
        if player_pos == exit_pos:
            print("You win!")
            running = False

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
