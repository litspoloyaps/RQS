import pygame
import sys
import random

# Initialize pygame
pygame.init()

# --- Game Constants ---
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
FPS = 12

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)

# --- Setup ---
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game 🐍")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 24)

# --- Functions ---
def get_random_food():
    while True:
        pos = (random.randrange(0, WIDTH, CELL_SIZE),
               random.randrange(0, HEIGHT, CELL_SIZE))
        if pos not in snake:
            return pos

def draw_snake():
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, DARK_GREEN, (*segment, CELL_SIZE, CELL_SIZE), 1)

def draw_food():
    pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

def show_score():
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

def game_over():
    over_text = font.render("GAME OVER", True, RED)
    restart_text = font.render("Press R to Restart | ESC to Quit", True, WHITE)

    screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 40))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2))

# --- Snake and Food ---
snake = [(100, 100), (80, 100), (60, 100)]
direction = "RIGHT"
food = get_random_food()
score = 0

# --- Main Loop ---
running = True
game_active = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and direction != "DOWN":
                direction = "UP"
            elif event.key == pygame.K_s and direction != "UP":
                direction = "DOWN"
            elif event.key == pygame.K_a and direction != "RIGHT":
                direction = "LEFT"
            elif event.key == pygame.K_d and direction != "LEFT":
                direction = "RIGHT"

            elif event.key == pygame.K_r and not game_active:
                snake = [(100, 100), (80, 100), (60, 100)]
                direction = "RIGHT"
                food = get_random_food()
                score = 0
                game_active = True

            elif event.key == pygame.K_ESCAPE:
                running = False

    if game_active:
        # Move snake
        head_x, head_y = snake[0]
        if direction == "UP":
            head_y -= CELL_SIZE
        elif direction == "DOWN":
            head_y += CELL_SIZE
        elif direction == "LEFT":
            head_x -= CELL_SIZE
        elif direction == "RIGHT":
            head_x += CELL_SIZE

        new_head = (head_x, head_y)
        snake.insert(0, new_head)

        # Wall & self collision
        if (
            head_x < 0 or head_x >= WIDTH or
            head_y < 0 or head_y >= HEIGHT or
            new_head in snake[1:]
        ):
            game_active = False

        # Food collision
        if new_head == food:
            score += 10
            food = get_random_food()
        else:
            snake.pop()

    # Draw everything
    screen.fill(BLACK)
    draw_grid()
    draw_snake()
    draw_food()
    show_score()

    if not game_active:
        game_over()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
