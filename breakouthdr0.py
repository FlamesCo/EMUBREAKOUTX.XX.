import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Define the screen size
WIDTH = 800
HEIGHT = 600

# Define the paddle and ball classes
class Paddle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

    def move_left(self):
        self.x -= 5
        self.rect.x = self.x

    def move_right(self):
        self.x += 5
        self.rect.x = self.x

class Ball:
    def __init__(self, x, y, radius, speed_x, speed_y):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)

    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)

    def update(self):
        # Update ball position
        self.x += self.speed_x
        self.y += self.speed_y

        # Check for collisions with screen edges
        if self.x + self.radius >= WIDTH or self.x - self.radius <= 0:
            self.speed_x *= -1
        if self.y - self.radius <= 0:
            self.speed_y *= -1

        # Check for game over (ball falls off the screen)
        if self.y + self.radius >= HEIGHT:
            print("Game Over!")
            pygame.quit()
            exit()

class Brick:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.visible = True

    def draw(self):
        if self.visible:
            pygame.draw.rect(screen, RED, self.rect)

# Initialize Pygame and create the screen
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")

# Create the paddle, ball, and bricks objects
paddle = Paddle(375, 550, 50, 10)
ball = Ball(400, 300, 10, 5, 5)

# Create a grid of bricks
brick_width = 80
brick_height = 20
bricks = []
for row in range(5):
    for col in range(10):
        brick = Brick(col * brick_width, row * brick_height + 50, brick_width, brick_height)
        bricks.append(brick)

# Game loop
running = True
clock = pygame.time.Clock()  # Create a clock object to control frame rate
fps = 60  # Desired frames per second

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle keyboard events
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.move_left()
    if keys[pygame.K_RIGHT]:
        paddle.move_right()

    # Update the screen
    screen.fill(BLACK)

    # Draw the paddle and ball
    paddle.draw()
    ball.draw()

    # Update the ball's position
    ball.update()

    # Check for collisions between the ball and the paddle
    if ball.rect.colliderect(paddle.rect):
        ball.speed_y *= -1

    # Check for collisions between the ball and the bricks
    for brick in bricks:
        if brick.visible and ball.rect.colliderect(brick.rect):
            ball.speed_y *= -1
            brick.visible = False

    # Draw the bricks
    for brick in bricks:
        brick.draw()

    pygame.display.flip()

    clock.tick(fps)  # Limit the frame rate to fps

# Quit Pygame
pygame.quit()
