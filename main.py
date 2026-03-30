"""
Socratic Pygame skeleton: 10 moving squares (stubs only)

This file contains stub functions with TODOs and guiding questions
so you can implement the full behaviour step-by-step.

Keep changes minimal — implement one TODO at a time and run interactively.
"""

import random
from typing import List, Dict, Tuple

import pygame

# Configuration constants (adjust when implementing)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SQUARE_SIZE = 30
NUM_SQUARES = 10
FPS = 60


def init_pygame() -> Tuple["pygame.Surface", "pygame.time.Clock"]:
    """Initialize pygame and return (screen, clock)."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Lab8 – Moving Squares")
    clock = pygame.time.Clock()
    return screen, clock


def create_squares() -> List[Dict]:
    """Return a list of square data structures."""
    squares: List[Dict] = []
    for _ in range(NUM_SQUARES):
        x = random.uniform(0, SCREEN_WIDTH - SQUARE_SIZE)
        y = random.uniform(0, SCREEN_HEIGHT - SQUARE_SIZE)
        # Small random velocities
        vx = random.uniform(-200, 200)
        vy = random.uniform(-200, 200)
        color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255),
        )
        squares.append({"x": x, "y": y, "vx": vx, "vy": vy, "color": color})
    return squares


def handle_events() -> bool:
    """Process pygame events and return True if the app should quit."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True
    return False


def update_squares(squares: List[Dict], dt: float) -> None:
    """Update square positions in-place using delta time `dt` (seconds)."""
    for sq in squares:
        sq["x"] += sq["vx"] * dt
        sq["y"] += sq["vy"] * dt

        # Bounce on left/right
        if sq["x"] < 0:
            sq["x"] = 0
            sq["vx"] *= -1
        elif sq["x"] + SQUARE_SIZE > SCREEN_WIDTH:
            sq["x"] = SCREEN_WIDTH - SQUARE_SIZE
            sq["vx"] *= -1

        # Bounce on top/bottom
        if sq["y"] < 0:
            sq["y"] = 0
            sq["vy"] *= -1
        elif sq["y"] + SQUARE_SIZE > SCREEN_HEIGHT:
            sq["y"] = SCREEN_HEIGHT - SQUARE_SIZE
            sq["vy"] *= -1


def draw_squares(screen: "pygame.Surface", squares: List[Dict]) -> None:
    """Draw all squares to the provided `screen` surface."""
    screen.fill((0, 0, 0))
    for sq in squares:
        rect = pygame.Rect(int(sq["x"]), int(sq["y"]), SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(screen, sq["color"], rect)
    pygame.display.flip()


def run() -> None:
    """Main entry: wire initialization, creation, main loop, and cleanup."""
    screen, clock = init_pygame()
    squares = create_squares()

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        if handle_events():
            running = False
            continue

        update_squares(squares, dt)
        draw_squares(screen, squares)

    pygame.quit()


if __name__ == "__main__":
    run()
