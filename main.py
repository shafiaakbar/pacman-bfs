import pygame
import random
import queue
import sys
import numpy as np

# Initialize maze
maze = [
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,3,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1],
[1,1,1,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,0,0,0,1,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
[1,0,0,0,0,1,1,1,1,1,0,0,0,0,0,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1],
[1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,1,1,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
[1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,1,1,0,0,1,1,1,0,0,0,0,0,0,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]
h,w = np.shape(maze)

#print(h,w)

# Constants
BLOCK_SIZE = 22
GRID_WIDTH = w
GRID_HEIGHT = h

# Initialize Pygaem
pygame.init()

# Set up the display
screen = pygame.display.set_mode((GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE))
pygame.display.set_caption("bfs")

# Load images
boundary_image = pygame.image.load("bd2.png")
free_space_image = pygame.image.load("grass2.png")
##boundary_image = pygame.image.load("bg1.png")
##free_space_image = pygame.image.load("bg2.png")
food_image = pygame.image.load("food2.png").convert_alpha()
character_image = pygame.image.load("main2.png").convert_alpha()
enemy_image = pygame.image.load("pinky2.png").convert_alpha()

# Initialize game variables

enemies = []
food = None
score = 0
game_over = False

# Set up the clock to control game speed
clock = pygame.time.Clock()

# Initialize character position
character_pos = None
for i in range(GRID_HEIGHT):
    for j in range(GRID_WIDTH):
        if maze[i][j] == 3:
            character_pos = (i, j)
            maze[i][j] = 0
            break

# Set up BFS queue and visited set
bfs_queue = queue.Queue()
visited = set()

# Function to check if a position is within the bounds of the grid
def is_valid(pos):
    i, j = pos
    return i >= 0 and i < GRID_HEIGHT and j >= 0 and j < GRID_WIDTH

# Function to check if a position is a boundary
def is_boundary(pos):
    i, j = pos
    return maze[i][j] == 1

# Function to check if a position is an enemy
def is_enemy(pos):
    i, j = pos
    return maze[i][j] == 5

# Function to add an enemy to the grid
def add_enemy():
    enemy_pos = (random.randint(0, GRID_HEIGHT - 1), random.randint(0, GRID_WIDTH - 1))
    while maze[enemy_pos[0]][enemy_pos[1]] != 0 or enemy_pos == character_pos or enemy_pos in enemies:
        enemy_pos = (random.randint(0, GRID_HEIGHT - 1), random.randint(0, GRID_WIDTH - 1))
    maze[enemy_pos[0]][enemy_pos[1]] = 5
    enemies.append(enemy_pos)

# Function to add food to the grid
def add_food():
    food_pos = (random.randint(0, GRID_HEIGHT - 1), random.randint(0, GRID_WIDTH - 1))
    while maze[food_pos[0]][food_pos[1]] != 0 or food_pos == character_pos or food_pos in enemies:
        food_pos = (random.randint(0, GRID_HEIGHT - 1), random.randint(0, GRID_WIDTH - 1))
    maze[food_pos[0]][food_pos[1]] = 2
    return food_pos

# Function to find the shortest path to food using BFS
def find_path_to_food():
    # Reset the queue and visited set
    bfs_queue = queue.Queue()
    visited.clear()

    # Add the starting position to the queue and visited set
    bfs_queue.put(character_pos)
    visited.add(character_pos)

    # Keep track of the previous position for each position visited
    prev = {}

    # Run BFS
    while not bfs_queue.empty():
        curr_pos = bfs_queue.get()
        i, j = curr_pos

        # Check all four neighbors
        for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_pos = (i + di, j + dj)
            if is_valid(new_pos) and not is_boundary(new_pos) and new_pos not in visited and not is_enemy(new_pos):
                bfs_queue.put(new_pos)
                visited.add(new_pos)
                prev[new_pos] = curr_pos
                if new_pos == food:
                    # We have reached the food, so reconstruct the path and return it
                    path = []
                    while new_pos in prev:
                        path.append(new_pos)
                        new_pos = prev[new_pos]
                    return path[::-1]

    # No path was found, so return an empty path
    return []

# Add two enemies to the grid
add_enemy()
add_enemy()

# Add food to the grid
food = add_food()

# Set up font for displaying score
font = pygame.font.Font(None, 22)





# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and not game_over:
                # Start the game
                game_over = False
                score = 0
                enemies.clear()
                add_enemy()
                add_enemy()
                food = add_food()
                character_pos = None
                for i in range(GRID_HEIGHT):
                    for j in range(GRID_WIDTH):
                        if maze[i][j] == 3:
                            character_pos = (i, j)
                            maze[i][j] = 0
                            break
            elif event.key == pygame.K_SPACE and game_over:
                # Restart the game
                game_over = False
                score = 0
                enemies.clear()
                add_enemy()
                add_enemy()
                food = add_food()
                character_pos = None
                for i in range(GRID_HEIGHT):
                    for j in range(GRID_WIDTH):
                        if maze[i][j] == 3:
                            character_pos = (i, j)
                            maze[i][j] = 0
                            break

    # Find the shortest path to the food
    path = find_path_to_food()

    # Update character position
    if path:
        # Move to the next position on the path
        character_pos = path[0]
        maze[character_pos[0]][character_pos[1]] = 0  # Set the block back to empty (0)
        if len(path) > 1:
            maze[path[1][0]][path[1][1]] = 4  # Highlight the next block to visit
        path.pop(0)
    else:
        # No path was found, so add more food
        food = add_food()

    # Check if character has collided with an enemy
    if character_pos in enemies:
        game_over = True

    # Check if character has reached the food
    if character_pos == food:
        # Remove the food and add more points to the score
        maze[food[0]][food[1]] = 0
        score += 10
        food = add_food()

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the grid
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            if maze[i][j] == 1:
                # Draw boundary
                screen.blit(boundary_image, (j * BLOCK_SIZE, i * BLOCK_SIZE))
            elif maze[i][j] == 0:
                # Draw free space
                screen.blit(free_space_image, (j * BLOCK_SIZE, i * BLOCK_SIZE))
            elif maze[i][j] == 2:
                # Draw food
                screen.blit(food_image, (j * BLOCK_SIZE, i * BLOCK_SIZE))
            elif maze[i][j] == 4:
                # Draw character, but only if the character's current position is not the same as the position of the food
                if (i, j) != food:
                    screen.blit(character_image, (j * BLOCK_SIZE, i * BLOCK_SIZE))
            elif maze[i][j] == 5:
                # Draw enemy
                screen.blit(enemy_image, (j * BLOCK_SIZE, i * BLOCK_SIZE))
                
    # Display score
    score_text = font.render("Score: {}".format(score), True, (0, 0, 0))
    screen.blit(score_text, (2, 2))

    if game_over:
        # Display game over screen
        game_over_text = font.render("Game Over", True, (0, 0, 0))
        screen.blit(game_over_text, (GRID_WIDTH * BLOCK_SIZE // 2 - 50, GRID_HEIGHT * BLOCK_SIZE // 2))
        continue_text = font.render("Press space bar to continue", True, (0, 0, 0))
        screen.blit(continue_text, (GRID_WIDTH * BLOCK_SIZE // 2 - 115, GRID_HEIGHT * BLOCK_SIZE // 2 + 40))

    # Update the display
    pygame.display.flip()

    # Limit the frame rate to x FPS
    # Change this "x" variable to modulate the speed of main character
    rate_flow = 4
    clock.tick(rate_flow)

    

