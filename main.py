"""
Socratic Pygame skeleton: 10 moving squares (stubs only)

This file contains stub functions with TODOs and guiding questions
so you can implement the full behaviour step-by-step.

Keep changes minimal — implement one TODO at a time and run interactively.
"""

import random
from typing import List, Dict, Tuple

import pygame

# === SLIDE REQUIREMENTS ===
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

NUM_SQUARES = 100
MIN_SIZE = 10
MAX_SIZE = 40
GLOBAL_MAX_SPEED = 300

JITTER_STRENGTH = 20
JITTER_INTERVAL = 0.2


def init_pygame() -> Tuple["pygame.Surface", "pygame.time.Clock"]:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Lab8 – Moving Squares")
    clock = pygame.time.Clock()
    return screen, clock


def create_squares() -> List[Dict]:
    """Create squares with size, speed, and color."""
    squares = []
    for _ in range(NUM_SQUARES):
        size = random.randint(MIN_SIZE, MAX_SIZE)

        # max speed = f(size) (bigger = slower)
        max_speed = GLOBAL_MAX_SPEED * (MIN_SIZE / size)

        vx = random.uniform(-max_speed, max_speed)
        vy = random.uniform(-max_speed, max_speed)

        x = random.uniform(0, SCREEN_WIDTH - size)
        y = random.uniform(0, SCREEN_HEIGHT - size)

        color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255),
        )

        squares.append({
            "x": x,
            "y": y,
            "vx": vx,
            "vy": vy,
            "size": size,
            "max_speed": max_speed,
            "time_since_jitter": 0.0,
            "color": color,
        })
    return squares


def handle_events() -> bool:
    """Return True if user wants to quit."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return True
    return False


def update_squares(squares: List[Dict], dt: float) -> None:
    """Move squares, apply jitter, clamp speed, bounce."""
    for sq in squares:
        # === SLIDE FEATURE: JITTER ===
        sq["time_since_jitter"] += dt
        if sq["time_since_jitter"] >= JITTER_INTERVAL:
            sq["time_since_jitter"] = 0.0
            sq["vx"] += random.uniform(-JITTER_STRENGTH, JITTER_STRENGTH)
            sq["vy"] += random.uniform(-JITTER_STRENGTH, JITTER_STRENGTH)

            # clamp to max_speed
            speed = (sq["vx"]**2 + sq["vy"]**2) ** 0.5
            if speed > sq["max_speed"]:
                scale = sq["max_speed"] / speed
                sq["vx"] *= scale
                sq["vy"] *= scale

        # move
        sq["x"] += sq["vx"] * dt
        sq["y"] += sq["vy"] * dt

        size = sq["size"]

        # bounce left/right
        if sq["x"] < 0:
            sq["x"] = 0
            sq["vx"] *= -1
        elif sq["x"] + size > SCREEN_WIDTH:
            sq["x"] = SCREEN_WIDTH - size
            sq["vx"] *= -1

        # bounce top/bottom
        if sq["y"] < 0:
            sq["y"] = 0
            sq["vy"] *= -1
        elif sq["y"] + size > SCREEN_HEIGHT:
            sq["y"] = SCREEN_HEIGHT - size
            sq["vy"] *= -1


def draw_squares(screen: "pygame.Surface", squares: List[Dict]) -> None:
    """Draw squares using their individual sizes."""
    screen.fill((0, 0, 0))
    for sq in squares:
        rect = pygame.Rect(int(sq["x"]), int(sq["y"]), sq["size"], sq["size"])
        pygame.draw.rect(screen, sq["color"], rect)
    pygame.display.flip()


def run() -> None:
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
