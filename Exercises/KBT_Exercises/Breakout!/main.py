import pygame as pyg
import sys

# Initialize Pygame
pyg.init()

# Screen settings
SCREEN_W = 960
SCREEN_H = 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Platform settings
PLATFORM_W = 100
PLATFORM_H = 20
PLATFORM_SPEED = 7

# Ball settings
BALL_RADIUS = 10
BALL_SPEED = 3.0  # General speed variable
BALL_DIR_X = 1    # Direction: 1 = right, -1 = left
BALL_DIR_Y = -1   # Direction: -1 = up, 1 = down
SPEED_INCREMENT = 1.02  # Increase speed by 2% after each block hit

# Block settings
BLOCK_ROWS = 6
BLOCK_COLS = 12
BLOCK_OFFSET_TOP = 50
BLOCK_H = 30
BLOCK_W = SCREEN_W / BLOCK_COLS

# Create screen
screen = pyg.display.set_mode((SCREEN_W, SCREEN_H))
pyg.display.set_caption("Breakout! - by Kaan")

# Initial positions
platform_x = SCREEN_W / 2 - PLATFORM_W / 2
platform_y = SCREEN_H - PLATFORM_H * 3
ball_x = SCREEN_W / 2
ball_y = SCREEN_H / 2

# Create blocks
blocks = []
for row in range(BLOCK_ROWS):
    for col in range(BLOCK_COLS):
        x = col * BLOCK_W
        y = row * BLOCK_H + BLOCK_OFFSET_TOP
        blocks.append(pyg.Rect(x, y, BLOCK_W, BLOCK_H))

clock = pyg.time.Clock()
running = True

while running:
    clock.tick(60)

    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            running = False

    # Key controls
    keys = pyg.key.get_pressed()
    if keys[pyg.K_a]:
        platform_x -= PLATFORM_SPEED
    if keys[pyg.K_d]:
        platform_x += PLATFORM_SPEED

    # Keep platform inside screen
    platform_x = max(0, min(platform_x, SCREEN_W - PLATFORM_W))

    # Move ball using speed and direction
    ball_x += BALL_DIR_X * BALL_SPEED
    ball_y += BALL_DIR_Y * BALL_SPEED

    # Bounce off walls
    if ball_x - BALL_RADIUS <= 0:
        BALL_DIR_X = 1
    if ball_x + BALL_RADIUS >= SCREEN_W:
        BALL_DIR_X = -1
    if ball_y - BALL_RADIUS <= 0:
        BALL_DIR_Y = 1

    # Bounce off platform
    if (platform_y <= ball_y + BALL_RADIUS <= platform_y + PLATFORM_H and
        platform_x <= ball_x <= platform_x + PLATFORM_W and BALL_DIR_Y > 0):
        BALL_DIR_Y = -1

    # Check collision with blocks
    ball_rect = pyg.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
    hit_index = ball_rect.collidelist(blocks)
    if hit_index != -1:
        del blocks[hit_index]
        BALL_DIR_Y *= -1  # Reverse vertical direction
        BALL_SPEED *= SPEED_INCREMENT  # Increase speed slightly

    # Game over if ball falls below screen
    if ball_y - BALL_RADIUS > SCREEN_H:
        print("Game Over!")
        running = False

    # Draw everything
    screen.fill(WHITE)
    pyg.draw.rect(screen, BLACK, (platform_x, platform_y, PLATFORM_W, PLATFORM_H))
    pyg.draw.circle(screen, RED, (int(ball_x), int(ball_y)), BALL_RADIUS)

    # Draw blocks with outlines
    for block in blocks:
        pyg.draw.rect(screen, BLUE, block)
        pyg.draw.rect(screen, BLACK, block, 1)

    pyg.display.flip()

pyg.quit()
sys.exit()