# Architecture

This project is a single-module Pygame simulation. The entire runtime lives in [main.py](../main.py), and the behavior is organized around a small set of helper functions plus one main game loop.

## Module Dependency Graph

```mermaid
graph LR
    A["main.py"] --> B["pygame"]
    A --> C["random"]
    A --> D["typing"]
```

`main.py` depends on `pygame` for windowing, timing, drawing, and event handling; `random` for square initialization and jitter; and `typing` for function signatures.

## Runtime Flow

```mermaid
flowchart TD
    A["Program start"] --> B["run()"]
    B --> C["init_pygame()"]
    C --> D["create_squares()"]
    D --> E["Main loop"]
    E --> F["clock.tick(FPS)"]
    F --> G["handle_events()"]
    G --> H{ "Quit requested?" }
    H -- "Yes" --> I["pygame.quit()"]
    H -- "No" --> J["update_squares(squares, dt)"]
    J --> K["draw_squares(screen, squares, font, clock)"]
    K --> E
```

The loop is frame driven. Each iteration gets `dt`, processes events, updates the square list, renders the scene, and repeats until quit.

## Function-Level Call Graph

```mermaid
graph TD
    A["run()"] --> B["init_pygame()"]
    A --> C["create_squares()"]
    A --> D["handle_events()"]
    A --> E["update_squares(squares, dt)"]
    A --> F["draw_squares(screen, squares, font, clock)"]

    C --> G["create_square()"]

    E --> H["find_closest_small(square, squares)"]
    E --> I["find_closest_big(square, squares)"]
    E --> J["compute_chase_vector(big, small)"]
    E --> K["compute_flee_vector(small, big)"]

    H --> L["distance(ax, ay, bx, by)"]
    I --> L
    J --> L
    K --> L
```

`run()` orchestrates the whole application. `update_squares()` is the core physics and lifecycle function. `draw_squares()` is the rendering and HUD function.

## Primary Sequence

```mermaid
sequenceDiagram
    participant R as "run()"
    participant C as "Clock"
    participant E as "handle_events()"
    participant U as "update_squares()"
    participant D as "draw_squares()"
    participant L as "Lifecycle"

    R->>R: initialize screen, clock, font, and squares
    loop every frame
        R->>C: clock.tick(FPS)
        C-->>R: dt
        R->>E: poll events
        alt quit or escape pressed
            E-->>R: True
            R->>R: stop loop
        else keep running
            E-->>R: False
            R->>U: update all squares
            loop each square
                U->>U: find closest small square
                alt smaller square exists
                    U->>U: apply chase force
                end
                U->>U: find closest big square
                alt bigger square exists
                    U->>U: apply flee force
                    U->>U: clamp velocity to max_speed
                end
                U->>U: apply jitter when timer reaches interval
                U->>U: move square by velocity * dt
                U->>U: bounce off window edges
                U->>U: add dt to age
                alt age >= life_span
                    U->>L: mark square for rebirth
                end
            end
            U-->>R: updated squares
            R->>D: render squares and HUD text
            D-->>R: frame displayed
        end
    end
```

This sequence mirrors the real control flow in [main.py](../main.py): event handling happens before simulation, the simulation mutates square state in place, and rendering happens after updates.

## Data Flow Notes

`squares` is the main mutable data structure. It is created once in `create_squares()`, updated in place by `update_squares()`, and read by `draw_squares()`.

`dt` comes from `clock.tick(FPS) / 1000.0` and scales velocity changes, jitter timing, movement, and age progression.

Square rebirth uses reverse-index removal so the list is not corrupted while iterating.

## Key Functions

`init_pygame()` sets up the window, clock, and font.

`create_square()` builds one square with random size, speed, position, color, and lifespan.

`create_squares()` creates the initial population.

`handle_events()` exits on `QUIT` or `ESC`.

`find_closest_small()` and `find_closest_big()` scan the list to locate the nearest smaller or larger square.

`compute_chase_vector()` and `compute_flee_vector()` turn relative positions into normalized steering vectors.

`update_squares()` applies steering, jitter, movement, bouncing, aging, and rebirth.

`draw_squares()` renders the squares and overlays FPS, particle count, and average X.

`run()` owns the application loop.

## Assumptions

The documentation reflects the current `main.py` only. There are no additional Python modules in the repository, so the architecture is intentionally flat and single-file.