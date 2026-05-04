"""
Socratic Pygame skeleton: moving squares

This file contains the full implementation with:
- size-based max speed
- jitter
- fleeing
- life span + rebirth
"""

import random
from typing import List, Dict, Tuple, TypedDict

import pygame

# REFACTORING STEP 1: Define Square type for clarity
# WHY: TypedDict documents the exact shape of square data.
#      This helps beginners understand what fields exist,
#      and typos in key names get caught by linters.
# CONCEPT: Type annotations + data contracts = safer, more readable code
class Square(TypedDict):
    """Square entity with position, velocity, size, steering, and lifecycle data."""
    x: float
    y: float
    vx: float
    vy: float
    size: int
    max_speed: float
    time_since_jitter: float
    color: Tuple[int, int, int]
    age: float
    life_span: float

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


def create_square() -> Square:
    """Create a new square with random properties.
    
    REFACTORING: Return type is now Square (TypedDict) instead of Dict.
    WHY: This makes the function contract explicit and type-safe.
    """
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

# Exercise 1: A mix of squares
def create_squares() -> List[Square]:
    squares: List[Square] = []

    ### 5 squares of size 25###
    for _ in range(5):
        sq = create_square()
        sq["size"] = 25
        sq["max_speed"] = GLOBAL_MAX_SPEED * (MIN_SIZE / 25)
        squares.append(sq)

    # 10 squares of size 10
    for _ in range(10):
        sq = create_square()
        sq["size"] = 10
        sq["max_speed"] = GLOBAL_MAX_SPEED * (MIN_SIZE / 10)
        squares.append(sq)

    # 30 squares of size 4
    for _ in range(30):
        sq = create_square()
        sq["size"] = 4
        sq["max_speed"] = GLOBAL_MAX_SPEED * (MIN_SIZE / 4)
        squares.append(sq)

    return squares


def handle_events() -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return True
    return False


def distance(ax: float, ay: float, bx: float, by: float) -> float:
    """Euclidean distance between two 2D points.
    
    Used for nearest-neighbor lookups during steering behavior.
    """
    dx = bx - ax
    dy = by - ay
    return (dx * dx + dy * dy) ** 0.5


# REFACTORING STEP 2: Extract speed clamping into a helper.
# WHY: Duplication is reduced from appearing in two places (flee, jitter)
#      to one centralized function. Easier to maintain, test, and modify.
# CONCEPT: DRY principle (Don't Repeat Yourself) = better maintainability.
def clamp_speed(square: Square) -> None:
    """Limit square velocity to its max_speed.
    
    If speed exceeds max_speed, scale both vx and vy proportionally.
    This preserves direction while respecting the speed limit.
    """
    speed = (square["vx"] ** 2 + square["vy"] ** 2) ** 0.5
    if speed > square["max_speed"]:
        # Avoid division by zero
        if speed == 0:
            return
        scale = square["max_speed"] / speed
        square["vx"] *= scale
        square["vy"] *= scale


# REFACTORING STEP 3: Extract update behaviors into focused helpers.
# WHY: Breaking update_squares() into smaller functions improves readability
#      and makes each behavior testable in isolation.
# CONCEPT: Separation of concerns = each function has one job.
def apply_chase(square: Square, squares: List[Square], dt: float) -> None:
    """Apply chase force if a smaller square exists nearby.
    
    Bigger squares hunt smaller ones by computing a force toward the
    nearest smaller square and accumulating it into velocity.
    """
    closest_small = find_closest_small(square, squares)
    if closest_small is not None:
        force_x, force_y = compute_chase_vector(square, closest_small)
        square["vx"] += force_x * dt
        square["vy"] += force_y * dt


def apply_flee(square: Square, squares: List[Square], dt: float) -> None:
    """Apply flee force if a larger square exists nearby.
    
    Smaller squares run away by computing a force away from the
    nearest larger square. After applying the force, we clamp speed.
    """
    closest_big = find_closest_big(square, squares)
    if closest_big is not None:
        force_x, force_y = compute_flee_vector(square, closest_big)
        square["vx"] += force_x * dt
        square["vy"] += force_y * dt
        # After adding force, ensure we don't exceed max speed
        clamp_speed(square)


def apply_jitter(square: Square, dt: float) -> None:
    """Apply random velocity perturbation on a timer.
    
    Every JITTER_INTERVAL seconds, add random noise to velocity
    to prevent perfectly straight, predictable motion.
    """
    square["time_since_jitter"] += dt
    if square["time_since_jitter"] >= JITTER_INTERVAL:
        square["time_since_jitter"] = 0.0
        square["vx"] += random.uniform(-JITTER_STRENGTH, JITTER_STRENGTH)
        square["vy"] += random.uniform(-JITTER_STRENGTH, JITTER_STRENGTH)
        # After adding jitter, ensure speed doesn't exceed max
        clamp_speed(square)

# Exercise 3 : Screen Wrapping
def move_and_bounce(square: Square, dt: float) -> None:
    """Update position with screen wrapping instead of bouncing."""
    square["x"] += square["vx"] * dt
    square["y"] += square["vy"] * dt
    size = square["size"]

    # Wrap horizontally
    if square["x"] + size < 0:
        square["x"] = SCREEN_WIDTH
    elif square["x"] > SCREEN_WIDTH:
        square["x"] = -size

    # Wrap vertically
    if square["y"] + size < 0:
        square["y"] = SCREEN_HEIGHT
    elif square["y"] > SCREEN_HEIGHT:
        square["y"] = -size



def update_age_and_collect_dead(square: Square, dt: float, index: int, dead_indices: List[int]) -> None:
    """Increment age and mark for removal if lifespan exceeded.
    
    Each square has a random lifespan. When age >= life_span,
    the square is marked for rebirth (removal and replacement).
    """
    square["age"] += dt
    if square["age"] >= square["life_span"]:
        dead_indices.append(index)


def find_closest_big(square: Square, squares: List[Square]) -> Square | None:
    """Find nearest square larger than the given square.
    
    REFACTORING: Signatures now use Square type instead of Dict.
    WHY: Type safety ensures callers pass the right data structure.
    """
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


def find_closest_small(square: Square, squares: List[Square]) -> Square | None:
    """Find nearest square smaller than the given square.
    
    REFACTORING: Signatures now use Square type instead of Dict.
    WHY: Type safety ensures callers pass the right data structure.
    """
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


def compute_flee_vector(small: Square, big: Square) -> Tuple[float, float]:
    """Compute escape force: normalized direction away from threat, scaled by FLEE_STRENGTH.
    
    REFACTORING STEP 4: Renamed fx/fy to force_x/force_y (shown below).
    WHY: Variable names should describe their purpose, not just be abbreviations.
    CONCEPT: Self-documenting code reduces bugs and cognitive load.
    """
    dx = small["x"] - big["x"]
    dy = small["y"] - big["y"]

    dist = (dx * dx + dy * dy) ** 0.5
    if dist == 0:
        return 0.0, 0.0

    # Normalize direction vector: divide by distance to get unit vector
    nx = dx / dist
    ny = dy / dist

    # Scale by flee strength to get final force magnitude
    force_x = nx * FLEE_STRENGTH
    force_y = ny * FLEE_STRENGTH
    return force_x, force_y


def compute_chase_vector(big: Square, small: Square) -> Tuple[float, float]:
    """Compute pursuit force: normalized direction toward prey, scaled by FLEE_STRENGTH.
    
    REFACTORING STEP 4: Renamed fx/fy to force_x/force_y (shown below).
    WHY: Variable names should describe their purpose, not just be abbreviations.
    CONCEPT: Self-documenting code reduces bugs and cognitive load.
    """
    dx = small["x"] - big["x"]
    dy = small["y"] - big["y"]

    dist = (dx * dx + dy * dy) ** 0.5
    if dist == 0:
        return 0.0, 0.0

    # Normalize direction vector: divide by distance to get unit vector
    nx = dx / dist
    ny = dy / dist

    # Scale by flee strength (same magnitude as flee force, just opposite direction)
    force_x = nx * FLEE_STRENGTH
    force_y = ny * FLEE_STRENGTH
    return force_x, force_y

# Exercise 4: Collision Detection
def check_collision(a: Square, b: Square) -> bool:
#Return True if two squares overlap using pygame.Rect collision
    rect_a = pygame.Rect(a["x"], a["y"], a["size"], a["size"])
    rect_b = pygame.Rect(b["x"], b["y"], b["size"], b["size"])
    return rect_a.colliderect(rect_b)


def update_squares(squares: List[Square], dt: float) -> None:
    """Update all squares for one frame.
    
    REFACTORING STEP 3: This function now delegates to focused helpers.
    WHY: Separation of concerns makes the flow clear and each behavior testable.
    CONCEPT: Orchestrator pattern = main function coordinates, helpers do work.
    
    Execution order (preserved from original):
    1. Apply chase force (if larger prey nearby)
    2. Apply flee force (if larger threat nearby)
    3. Apply jitter (random velocity kicks)
    4. Update position and bounce
    5. Age and mark for rebirth
    6. Rebirth dead squares
    """
    dead_indices: List[int] = []

    for index, sq in enumerate(squares):
        # STEP 1: Chase behavior
        apply_chase(sq, squares, dt)

        # STEP 2: Flee behavior
        apply_flee(sq, squares, dt)

        # STEP 3: Jitter (random perturbation)
        apply_jitter(sq, dt)

        # STEP 4: Movement and collision
        move_and_bounce(sq, dt)

        # STEP 5: Lifecycle management
        update_age_and_collect_dead(sq, dt, index, dead_indices)

    # STEP 6: Rebirth dead squares
    # REFACTORING STEP 6: Keep rebirth explicit and documented.
    # WHY: Reverse iteration prevents index corruption during removal.
    # CONCEPT: Safe list mutation with reverse-index popping (mutation safety).
    # Exercise 2:Same size respawn
    for index in reversed(dead_indices):
        old_size = squares[index]["size"]
        squares.pop(index)
        new_sq = create_square()
        new_sq["size"] = old_size
        new_sq["max_speed"] = GLOBAL_MAX_SPEED * (MIN_SIZE / old_size)
        squares.append(new_sq)




def draw_squares(screen: "pygame.Surface", squares: List[Square], font: "pygame.font.Font", clock: "pygame.time.Clock") -> None:
    """Render all squares and HUD diagnostics to screen.
    
    REFACTORING STEP 5: Added defensive check for zero particle count.
    WHY: Prevents ZeroDivisionError if particle_count becomes 0.
         This is defensive programming: handle edge cases gracefully.
    CONCEPT: Input/state validation = robust, crash-resistant code.
    """
    screen.fill((0, 0, 0))

    for sq in squares:
        size = sq["size"]

        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.rect(surf, sq["color"], (0, 0, size, size))

        rect = surf.get_rect(topleft=(sq["x"], sq["y"]))
        screen.blit(surf, rect)

    particle_count = len(squares)
    # REFACTORING STEP 5: Guard against division by zero
    avg_x = 0.0 if particle_count == 0 else sum(sq["x"] for sq in squares) / particle_count
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
