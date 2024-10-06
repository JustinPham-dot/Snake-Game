import pygame
import time
import random

# Initialize pygame
pygame.init()

# Set up display
width, height = 800, 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
yellow = (255, 255, 102)

# Snake settings
snake_block = 10
initial_snake_speed = 15

# Clock
clock = pygame.time.Clock()

# Fonts
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)


# Snake Class
class Snake:
    def __init__(self):
        self.head = [300, 300]  # Initial position of the snake's head
        self.body = [self.head[:]]  # The body starts as just the head
        self.direction = "STOP"  # Initial direction is stopped
        self.change_direction = self.direction
        self.length = 1

    # Function to move the snake
    def move(self):
        if self.change_direction == "LEFT":
            self.head[0] -= snake_block
        if self.change_direction == "RIGHT":
            self.head[0] += snake_block
        if self.change_direction == "UP":
            self.head[1] -= snake_block
        if self.change_direction == "DOWN":
            self.head[1] += snake_block

        # Append the new head position to the body
        self.body.append(self.head[:])
        if len(self.body) > self.length:
            del self.body[0]  # Remove the tail if the body is longer than the length

        self.direction = self.change_direction

    # Change the direction of the snake based on user input
    def change_dir(self, direction):
        if direction == "LEFT" and not self.direction == "RIGHT":
            self.change_direction = "LEFT"
        if direction == "RIGHT" and not self.direction == "LEFT":
            self.change_direction = "RIGHT"
        if direction == "UP" and not self.direction == "DOWN":
            self.change_direction = "UP"
        if direction == "DOWN" and not self.direction == "UP":
            self.change_direction = "DOWN"

    # Draw the snake on the screen
    def draw(self):
        for segment in self.body[:-1]:
            pygame.draw.rect(display, black, [segment[0], segment[1], snake_block, snake_block])
        pygame.draw.rect(display, blue, [self.body[-1][0], self.body[-1][1], snake_block, snake_block])

    # Check if the snake collided with itself
    def collision_with_self(self):
        return self.head in self.body[:-1]

    # Check if the snake collided with the boundaries
    def collision_with_boundaries(self):
        return self.head[0] >= width or self.head[0] < 0 or self.head[1] >= height or self.head[1] < 0


# Food Class
class Food:
    def __init__(self):
        self.position = [random.randrange(0, width // snake_block) * snake_block,
                         random.randrange(0, height // snake_block) * snake_block]

    # Spawn new food at a random position
    def spawn(self):
        self.position = [random.randrange(0, width // snake_block) * snake_block,
                         random.randrange(0, height // snake_block) * snake_block]

    # Draw the food on the screen
    def draw(self):
        pygame.draw.rect(display, green, [self.position[0], self.position[1], snake_block, snake_block])


# Function to display score on the screen
def show_score(score):
    value = score_font.render(f"Your Score: {score}", True, black)
    display.blit(value, [0, 0])


# Function to display messages on the screen
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    display.blit(mesg, [width / 6, height / 3])


# Main game loop
def gameLoop():
    game_over = False
    game_close = False

    snake = Snake()
    food = Food()
    background_color = white
    snake_speed = initial_snake_speed

    while not game_over:

        while game_close:
            display.fill(white)
            message("You Lost! Press Q-Quit or C-Play Again", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake.change_dir("LEFT")
                elif event.key == pygame.K_RIGHT:
                    snake.change_dir("RIGHT")
                elif event.key == pygame.K_UP:
                    snake.change_dir("UP")
                elif event.key == pygame.K_DOWN:
                    snake.change_dir("DOWN")

        # Check for collisions
        if snake.collision_with_boundaries() or snake.collision_with_self():
            game_close = True

        snake.move()

        # Draw background, food, and snake
        display.fill(background_color)
        food.draw()
        snake.draw()
        show_score(snake.length - 1)
        pygame.display.update()

        # Check if snake eats food
        if snake.head == food.position:
            food.spawn()
            snake.length += 1
            background_color = yellow  # Change background color
            snake_speed += 5  # Increase snake speed
        else:
            background_color = white  # Reset background color

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Start the game
gameLoop()
