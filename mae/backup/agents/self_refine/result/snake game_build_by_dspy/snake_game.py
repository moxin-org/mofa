import pygame
import random

# Initialize pygame
pygame.init()

# Set up the game screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# Snake
snake_block = 10
snake_speed = 15
snake_list = []

# Food
food_block = 10
food_pos = [random.randrange(1, screen_width // 10) * 10, random.randrange(1, screen_height // 10) * 10]

# Score
score = 0

# Game loop
game_over = False
clock = pygame.time.Clock()

# Function to draw the snake on the screen
def snake(snake_block, snake_list):
    for block in snake_list:
        pygame.draw.rect(screen, green, [block[0], block[1], snake_block, snake_block])

# Function to display the current score on the screen
def show_score(score):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score: " + str(score), True, white)
    screen.blit(text, (10, 10))

# Function to display game over message
def game_over_message():
    font = pygame.font.SysFont(None, 50)
    text = font.render("Game Over", True, white)
    screen.blit(text, (screen_width // 2 - 100, screen_height // 2))

def game():
    global game_over, score
    x = screen_width // 2
    y = screen_height // 2
    x_change = 0
    y_change = 0
    snake_list = []
    snake_length = 1

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -snake_block
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = snake_block
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -snake_block
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = snake_block
                    x_change = 0

        if x >= screen_width or x < 0 or y >= screen_height or y < 0:
            game_over = True

        x += x_change
        y += y_change
        screen.fill(black)
        pygame.draw.rect(screen, red, [food_pos[0], food_pos[1], food_block, food_block])
        snake_head = []
        snake_head.append(x)
        snake_head.append(y)
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        for block in snake_list[:-1]:
            if block == snake_head:
                game_over = True

        snake(snake_block, snake_list)
        show_score(score)

        if x == food_pos[0] and y == food_pos[1]:
            score += 1
            food_pos = [random.randrange(1, screen_width // 10) * 10, random.randrange(1, screen_height // 10) * 10]
            snake_length += 1

        pygame.display.update()
        clock.tick(snake_speed)

    game_over_message()
    pygame.display.update()
    pygame.time.wait(2000)  # Display game over message for 2 seconds
    pygame.quit()

game()