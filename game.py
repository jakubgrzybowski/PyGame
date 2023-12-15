import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Grid dimensions
n_cells_x, n_cells_y = 40, 30
cell_width = width // n_cells_x
cell_height = height // n_cells_y

# Game state
game_state = np.random.choice([0, 1], size=(n_cells_x, n_cells_y), p=[0.8, 0.2])

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
green = (0, 255, 0)
orange = (255, 165, 0)
blue = (0, 0, 255)
purple = (128, 0, 128)

# Button dimensions
button_width, button_height = 150, 40
button_x = width // 2 - button_width * 2 - 30
pause_button_x = button_x + button_width + 10
save_button_x = pause_button_x + button_width + 10
load_button_x = save_button_x + button_width + 10
button_y = height - button_height - 10

# Timer event
NEXT_GENERATION = pygame.USEREVENT + 1
pygame.time.set_timer(NEXT_GENERATION, 2000)

# Pause state
paused = False

# Saved state
saved_state = None
# Wzorzec projektowy: Single Responsibility Principle
def draw_button(text, x, color):
    pygame.draw.rect(screen, color, (x, button_y, button_width, button_height))
    font = pygame.font.Font(None, 24)
    text = font.render(text, True, black)
    text_rect = text.get_rect(center=(x + button_width // 2, button_y + button_height // 2))
    screen.blit(text, text_rect)

def draw_grid():
    for y in range(0, height, cell_height):
        for x in range(0, width, cell_width):
            cell = pygame.Rect(x, y, cell_width, cell_height)
            pygame.draw.rect(screen, gray, cell, 1)
   # Wzorzec projektowy: Command Pattern
def next_generation():
    global game_state
    new_state = np.copy(game_state)

    for y in range(n_cells_y):
        for x in range(n_cells_x):
            n_neighbors = game_state[(x - 1) % n_cells_x, (y - 1) % n_cells_y] + \
                          game_state[(x)     % n_cells_x, (y - 1) % n_cells_y] + \
                          game_state[(x + 1) % n_cells_x, (y - 1) % n_cells_y] + \
                          game_state[(x - 1) % n_cells_x, (y)     % n_cells_y] + \
                          game_state[(x + 1) % n_cells_x, (y)     % n_cells_y] + \
                          game_state[(x - 1) % n_cells_x, (y + 1) % n_cells_y] + \
                          game_state[(x)     % n_cells_x, (y + 1) % n_cells_y] + \
                          game_state[(x + 1) % n_cells_x, (y + 1) % n_cells_y]

            if game_state[x, y] == 1 and (n_neighbors < 2 or n_neighbors > 3):
                new_state[x, y] = 0
            elif game_state[x, y] == 0 and n_neighbors == 3:
                new_state[x, y] = 1

    game_state = new_state

def draw_cells():
    for y in range(n_cells_y):
        for x in range(n_cells_x):
            cell = pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height)
            if game_state[x, y] == 1:
                pygame.draw.rect(screen, black, cell)

running = True
while running:
    screen.fill(white)
    draw_grid()
    draw_cells()
    draw_button("Next Generation", button_x, green)
    draw_button("Pause" if not paused else "Resume", pause_button_x, purple)
    draw_button("Save", save_button_x, orange)
    draw_button("Load", load_button_x, blue)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_x <= event.pos[0] <= button_x + button_width and button_y <= event.pos[1] <= button_y + button_height:
                next_generation()
            elif pause_button_x <= event.pos[0] <= pause_button_x + button_width and button_y <= event.pos[1] <= button_y + button_height:
                paused = not paused
            elif save_button_x <= event.pos[0] <= save_button_x + button_width and button_y <= event.pos[1] <= button_y + button_height:
                saved_state = np.copy(game_state)
            elif load_button_x <= event.pos[0] <= load_button_x + button_width and button_y <= event.pos[1] <= button_y + button_height:
                if saved_state is not None:
                    game_state = np.copy(saved_state)
            else:
                x, y = event.pos[0] // cell_width, event.pos[1] // cell_height
                game_state[x, y] = not game_state[x, y]
        if event.type == NEXT_GENERATION and not paused:
            next_generation()

pygame.quit()





