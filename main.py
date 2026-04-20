"""
Socratic Pygame skeleton: moving squares

This file contains the full implementation with:
- size-based max speed
- jitter
- fleeing
- life span + rebirth
"""

import random
from typing import List, Dict, Tuple

import pygame

# Configuration constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
FLEE_STRENGTH = 200

NUM_SQUARES = 20
MIN_SIZE = 10
MAX_SIZE = 40
GLOBAL_MAX_SPEED = 300

JITTER_STRENGTH = 20
JITTER_INTERVAL = 0.2

# Life span in seconds
MIN_LIFE_SPAN = 30.0
MAX_LIFE_SPAN = 180.0


def init_pygame() -> Tuple["pygame.Surface", "pygame.time.Clock", "pygame.font.Font"]:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Lab8 – Moving Squares")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    return screen, clock, font


def create_square() -> Dict:
    size = random.randint(MIN_SIZE, MAX_SIZE)
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

    life_span = random.uniform(MIN_LIFE_SPAN, MAX_LIFE_SPAN)

    return {
        "x": x,
        "y": y,
        "vx": vx,
        "vy": vy,
        "size": size,
        "max_speed": max_speed,
        "time_since_jitter": 0.0,
        "color": color,
        "age": 0.0,
        "life_span": life_span,
    }


def create_squares() -> List[Dict]:
    squares: List[Dict] = []
    for _ in range(NUM_SQUARES):
        squares.append(create_square())
    return squares


def handle_events() -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return True
    return False


def distance(ax: float, ay: float, bx: float, by: float) -> float:
    dx = bx - ax
    dy = by - ay
    return (dx * dx + dy * dy) ** 0.5


def find_closest_big(square: Dict, squares: List[Dict]) -> Dict | None:
    closest = None
    closest_dist = float("inf")

    for other in squares:
        if other is square:
            continue
        if other["size"] <= square["size"]:
            continue

        d = distance(square["x"], square["y"], other["x"], other["y"])
        if d < closest_dist:
            closest_dist = d
            closest = other

    return closest

def find_closest_small(square: Dict, squares: List[Dict]) -> Dict | None:
    closest = None
    closest_dist = float("inf")

    for other in squares:
        if other is square:
            continue
        if other["size"] >= square["size"]:
            continue  

        d = distance(square["x"], square["y"], other["x"], other["y"])
        if d < closest_dist:
            closest_dist = d
            closest = other

    return closest


def compute_flee_vector(small: Dict, big: Dict) -> Tuple[float, float]:
    dx = small["x"] - big["x"]
    dy = small["y"] - big["y"]

    dist = (dx * dx + dy * dy) ** 0.5
    if dist == 0:
        return 0.0, 0.0

    nx = dx / dist
    ny = dy / dist

    fx = nx * FLEE_STRENGTH
    fy = ny * FLEE_STRENGTH
    return fx, fy

def compute_chase_vector(big: Dict, small: Dict) -> Tuple[float, float]:
    dx = small["x"] - big["x"]
    dy = small["y"] - big["y"]

    dist = (dx * dx + dy * dy) ** 0.5
    if dist == 0:
        return 0.0, 0.0

    nx = dx / dist
    ny = dy / dist

    fx = nx * FLEE_STRENGTH  
    fy = ny * FLEE_STRENGTH
    return fx, fy

def update_squares(squares: List[Dict], dt: float) -> None:
    dead_indices: List[int] = []

    for index, sq in enumerate(squares):
        # fleeing behavior
        closest_big = find_closest_big(sq, squares)
        if closest_big is not None:
            fx, fy = compute_flee_vector(sq, closest_big)
            sq["vx"] += fx * dt
            sq["vy"] += fy * dt

            speed = (sq["vx"] ** 2 + sq["vy"] ** 2) ** 0.5
            if speed > sq["max_speed"]:
                scale = sq["max_speed"] / speed
                sq["vx"] *= scale
                sq["vy"] *= scale
            # chasing behaviour
            closest_small = find_closest_small(sq, squares)
            if closest_small is not None:
                fx, fy = compute_chase_vector(sq, closest_small)
                sq["vx"] += fx * dt
                sq["vy"] += fy * dt

                speed = (sq["vx"] ** 2+ sq["vy"] ** 2) **0.5
                if speed > sq["max_speed"]:
                    scale = sq["max_speed"] / speed
                    sq["vx"] *= scale
                    sq["vy"] *= scale

        # jitter
        sq["time_since_jitter"] += dt
        if sq["time_since_jitter"] >= JITTER_INTERVAL:
            sq["time_since_jitter"] = 0.0
            sq["vx"] += random.uniform(-JITTER_STRENGTH, JITTER_STRENGTH)
            sq["vy"] += random.uniform(-JITTER_STRENGTH, JITTER_STRENGTH)

            speed = (sq["vx"] ** 2 + sq["vy"] ** 2) ** 0.5
            if speed > sq["max_speed"]:
                scale = sq["max_speed"] / speed
                sq["vx"] *= scale
                sq["vy"] *= scale

        # movement
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

        # life span/age update
        sq["age"] += dt
        if sq["age"] >= sq["life_span"]:
            dead_indices.append(index)

    # rebirth remove dead squares and create new ones
    for index in reversed(dead_indices):
        squares.pop(index)
        squares.append(create_square())


def draw_squares(screen: "pygame.Surface", squares: List[Dict], font: "pygame.font.Font", clock: "pygame.time.Clock") -> None:
    screen.fill((0, 0, 0))

    for sq in squares:
        size = sq["size"]

        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.rect(surf, sq["color"], (0, 0, size, size))

        rect = surf.get_rect(topleft=(sq["x"], sq["y"]))
        screen.blit(surf, rect)

    particle_count = len(squares)
    avg_x = sum(sq["x"] for sq in squares) / particle_count
    fps = int(clock.get_fps())

    text_surface = font.render(
        f"FPS: {fps}   Particles: {particle_count}   Avg X: {int(avg_x)}",
        True,
        (255, 255, 255),
    )
    screen.blit(text_surface, (10, 10))

    pygame.display.flip()


def run() -> None:
    screen, clock, font = init_pygame()
    squares = create_squares()

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        if handle_events():
            running = False
            continue

        update_squares(squares, dt)
        draw_squares(screen, squares, font, clock)

    pygame.quit()


if __name__ == "__main__":
    run()
