import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# Fonts
font = pygame.font.SysFont("arial", 20)
large_font = pygame.font.SysFont("arial", 40)

# Snake properties
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
snake_direction = "RIGHT"
change_to = snake_direction
speed = 15

# Food properties
food_pos = [random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10]
food_spawn = True

# Barriers
barriers = [
    [200, 100], [200, 110], [200, 120], [200, 130]
]

# Score
score = 0
high_score = 0

# Clock for controlling game speed
clock = pygame.time.Clock()


def show_score():
    score_surface = font.render(f"Score: {score}  High Score: {high_score}", True, WHITE)
    screen.blit(score_surface, (10, 10))


def draw_snake(snake_body):
    for i, segment in enumerate(snake_body):
        if i == 0:
            pygame.draw.circle(screen, BLUE, (segment[0] + 5, segment[1] + 5), 7)
        else:
            size = max(5, 7 - i // 2)
            pygame.draw.circle(screen, GREEN, (segment[0] + 5, segment[1] + 5), size)


def draw_barriers():
    for barrier in barriers:
        pygame.draw.rect(screen, GRAY, pygame.Rect(barrier[0], barrier[1], 10, 40))


def start_screen():
    while True:
        screen.fill(BLACK)
        title_surface = large_font.render("Snake Game", True, WHITE)
        start_button = font.render("Press ENTER to Start", True, GREEN)
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, HEIGHT // 3))
        screen.blit(start_button, (WIDTH // 2 - start_button.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return


def game_over_screen():
    global score, high_score, snake_pos, snake_body, snake_direction, change_to, speed, barriers, food_pos, food_spawn
    while True:
        screen.fill(BLACK)
        game_over_surface = large_font.render("Game Over", True, RED)
        restart_button = font.render("Press R to Restart", True, GREEN)
        close_button = font.render("Press Q to Quit", True, WHITE)
        screen.blit(game_over_surface, (WIDTH // 2 - game_over_surface.get_width() // 2, HEIGHT // 3))
        screen.blit(restart_button, (WIDTH // 2 - restart_button.get_width() // 2, HEIGHT // 2))
        screen.blit(close_button, (WIDTH // 2 - close_button.get_width() // 2, HEIGHT // 2 + 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Reset game variables
                    score = 0
                    snake_pos = [100, 50]
                    snake_body = [[100, 50], [90, 50], [80, 50]]
                    snake_direction = "RIGHT"
                    change_to = snake_direction
                    speed = 15
                    barriers = [[200, 100], [200, 110], [200, 120], [200, 130]]
                    food_pos = [random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10]
                    food_spawn = True
                    return
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


# Main game loop
def game_loop():
    global score, high_score, snake_pos, snake_body, snake_direction, change_to, speed, barriers, food_pos, food_spawn
    food_eaten = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not snake_direction == "DOWN":
                    change_to = "UP"
                if event.key == pygame.K_DOWN and not snake_direction == "UP":
                    change_to = "DOWN"
                if event.key == pygame.K_LEFT and not snake_direction == "RIGHT":
                    change_to = "LEFT"
                if event.key == pygame.K_RIGHT and not snake_direction == "LEFT":
                    change_to = "RIGHT"

        # Change direction
        snake_direction = change_to

        # Move the snake
        if snake_direction == "UP":
            snake_pos[1] -= 10
        if snake_direction == "DOWN":
            snake_pos[1] += 10
        if snake_direction == "LEFT":
            snake_pos[0] -= 10
        if snake_direction == "RIGHT":
            snake_pos[0] += 10

        # Snake body growing mechanism
        if snake_pos == food_pos:
            food_spawn = False
            score += 10
            food_eaten += 1
            if food_eaten % 2 == 0:  # Add a new barrier after every 2 foods eaten
                while True:
                    new_barrier = [random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10]
                    if new_barrier not in snake_body and new_barrier != food_pos and new_barrier not in barriers:
                        barriers.append(new_barrier)
                        break
                speed += 1
        else:
            snake_body.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10]
        food_spawn = True

        # Add new position of the snake's head
        snake_body.insert(0, list(snake_pos))

        # Check for collisions
        if (snake_pos[0] < 0 or snake_pos[0] >= WIDTH or
                snake_pos[1] < 0 or snake_pos[1] >= HEIGHT):
            running = False
        for block in snake_body[1:]:
            if snake_pos == block:
                running = False
        for barrier in barriers:
            if snake_pos == barrier:
                running = False

        # Update high score
        if score > high_score:
            high_score = score

        # Draw everything
        screen.fill(BLACK)
        draw_snake(snake_body)
        pygame.draw.circle(screen, RED, (food_pos[0] + 5, food_pos[1] + 5), 5)
        draw_barriers()
        show_score()

        # Refresh game screen
        pygame.display.flip()

        # Control the speed of the game
        clock.tick(speed)

    game_over_screen()


# Start the game
start_screen()
while True:
    game_loop()
