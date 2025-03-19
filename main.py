import pygame
import time
import random

pygame.init()

# Define colors
WHITE = (7, 241, 84)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 0, 255)

WIDTH, HEIGHT = 600, 400

# Initialize the game window
game_display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# Snake settings
SNAKE_SIZE = 10
SNAKE_SPEED = 8

# Fonts
message_font = pygame.font.SysFont('ubuntu', 30)
score_font = pygame.font.SysFont('ubuntu', 30)

# Function to display score
def print_score(score):
    text = score_font.render("Score: " + str(score), True, ORANGE)
    game_display.blit(text, [10, 10])

# Function to draw the snake
def draw_snake(snake_size, snake_pixels):
    for pixel in snake_pixels:
        pygame.draw.rect(game_display, WHITE, [pixel[0], pixel[1], snake_size, snake_size])

# Function to spawn food without overlap
def generate_food(snake_pixels):
    while True:
        target_x = round(random.randrange(0, WIDTH - SNAKE_SIZE) / 10.0) * 10.0
        target_y = round(random.randrange(0, HEIGHT - SNAKE_SIZE) / 10.0) * 10.0
        if [target_x, target_y] not in snake_pixels:
            return target_x, target_y

# Main game loop
def run_game():
    game_over = False
    game_close = False

    # Initial position of the snake
    x, y = WIDTH / 2, HEIGHT / 2
    x_speed, y_speed = 0, 0

    snake_pixels = []
    snake_length = 1

    # Generate initial food position
    target_x, target_y = generate_food(snake_pixels)

    while not game_over:
        while game_close:
            game_display.fill(BLACK)
            game_over_message = message_font.render("Game Over!", True, RED)
            restart_message = message_font.render("Press 1 to Quit, 2 to Restart", True, ORANGE)
            game_display.blit(game_over_message, [WIDTH / 3, HEIGHT / 3])
            game_display.blit(restart_message, [WIDTH / 5, HEIGHT / 2])
            print_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_2:
                        run_game()
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_speed == 0:
                    x_speed = -SNAKE_SIZE
                    y_speed = 0
                if event.key == pygame.K_RIGHT and x_speed == 0:
                    x_speed = SNAKE_SIZE
                    y_speed = 0
                if event.key == pygame.K_UP and y_speed == 0:
                    x_speed = 0
                    y_speed = -SNAKE_SIZE
                if event.key == pygame.K_DOWN and y_speed == 0:
                    x_speed = 0
                    y_speed = SNAKE_SIZE

        # Check if snake hits the wall
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True

        x += x_speed
        y += y_speed

        game_display.fill(BLACK)
        pygame.draw.rect(game_display, ORANGE, [target_x, target_y, SNAKE_SIZE, SNAKE_SIZE])

        snake_pixels.append([x, y])
        if len(snake_pixels) > snake_length:
            del snake_pixels[0]

        # Check if snake collides with itself
        for pixel in snake_pixels[:-1]:
            if pixel == [x, y]:
                game_close = True

        draw_snake(SNAKE_SIZE, snake_pixels)
        print_score(snake_length - 1)

        pygame.display.update()

        # Check if the snake eats food
        if x == target_x and y == target_y:
            target_x, target_y = generate_food(snake_pixels)
            snake_length += 1

        clock.tick(SNAKE_SPEED)

    pygame.quit()
    quit()

run_game()
