import pygame
import sys
import random

CELL_SIZE = 20
CELL_NUMBER = 30  # 30x30 grid -> window 600x600
WINDOW_SIZE = CELL_SIZE * CELL_NUMBER
INITIAL_SPEED = 10  # frames per second

# Colors (R,G,B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
RED = (200, 0, 0)
GRAY = (40, 40, 40)
YELLOW = (240, 210, 10)

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Zmeyka (Snake) - Python + Pygame")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

def draw_rect(pos, color):
    r = pygame.Rect(pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, r)

def random_food_position(snake):
    while True:
        pos = (random.randint(0, CELL_NUMBER - 1), random.randint(0, CELL_NUMBER - 1))
        if pos not in snake:
            return pos

def show_text_center(text, font_obj, color, y_offset=0):
    surf = font_obj.render(text, True, color)
    rect = surf.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 + y_offset))
    screen.blit(surf, rect)

# --- Game state init ---
def new_game():
    # Snake starts in middle, length 3, moving right
    start_x = CELL_NUMBER // 2
    start_y = CELL_NUMBER // 2
    snake = [(start_x - i, start_y) for i in range(3)]
    direction = (1, 0)  # (dx, dy)
    food = random_food_position(snake)
    score = 0
    speed = INITIAL_SPEED
    return snake, direction, food, score, speed

snake, direction, food, score, speed = new_game()
game_over = False
paused = False

# --- Main loop ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                if direction != (0, 1):  # prevent reverse
                    direction = (0, -1)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                if direction != (0, -1):
                    direction = (0, 1)
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                if direction != (1, 0):
                    direction = (-1, 0)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                if direction != (-1, 0):
                    direction = (1, 0)
            elif event.key == pygame.K_p:
                paused = not paused
            elif event.key == pygame.K_r and game_over:
                snake, direction, food, score, speed = new_game()
                game_over = False
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    if not paused and not game_over:
        # Move snake: add new head based on direction
        head_x, head_y = snake[0]
        dx, dy = direction
        new_head = (head_x + dx, head_y + dy)

        # Wrap-around or collision with wall? (choose one)
        # Here we end the game when hitting walls:
        if (new_head[0] < 0 or new_head[0] >= CELL_NUMBER or
                new_head[1] < 0 or new_head[1] >= CELL_NUMBER):
            game_over = True
        else:
            # Check self collision
            if new_head in snake:
                game_over = True
            else:
                snake.insert(0, new_head)

                # Eat food?
                if new_head == food:
                    score += 1
                    food = random_food_position(snake)
                    # speed up slightly every 3 foods
                    if score % 3 == 0:
                        speed += 1
                else:
                    # remove tail
                    snake.pop()

    # Draw
    screen.fill(BLACK)

# grid (optional subtle)
    for x in range(0, WINDOW_SIZE, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, WINDOW_SIZE))
    for y in range(0, WINDOW_SIZE, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WINDOW_SIZE, y))

    # Draw food
    draw_rect(food, RED)

    # Draw snake (head different color)
    if len(snake) > 0:
        draw_rect(snake[0], YELLOW)
    for s in snake[1:]:
        draw_rect(s, GREEN)

    # Score
    score_surf = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_surf, (8, 8))

    # Pause / Game over overlays
    if paused:
        show_text_center("PAUSED (P to continue)", font, WHITE, y_offset=-30)
        show_text_center("ESC to quit", font, WHITE, y_offset=30)

    if game_over:
        show_text_center("GAME OVER", big_font, RED, y_offset=-40)
        show_text_center(f"Score: {score}", font, WHITE, y_offset=10)
        show_text_center("Press R to restart or ESC to quit", font, WHITE, y_offset=60)

    pygame.display.flip()
    clock.tick(speed)