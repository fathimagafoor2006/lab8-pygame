# Overview

This project is a single-file Pygame simulation in `main.py` where squares move, flee/chase, jitter, bounce on walls, age, and respawn.

The code is already functional and readable at a basic level, but it can be improved with small beginner-friendly changes:
- clearer naming and type definitions for square data
- reduced duplicated logic (especially speed clamping)
- safer edge-case handling (like division by zero when there are zero squares)
- cleaner structure inside `update_squares()`

The goal is to keep the same behavior while making the code easier to understand, test, and extend.

# Refactoring Goals

- Improve readability with clearer names and smaller helper functions.
- Reduce duplication in repeated velocity-clamping math.
- Improve maintainability of square state by defining a clearer data shape.
- Keep logic order explicit in `update_squares()`.
- Add small defensive checks for edge cases.
- Preserve current gameplay behavior.

# Step-by-Step Refactoring Plan

## Step 1: Define a clearer square type

What to do:
- Introduce a `TypedDict` named `Square` (or a simple `dataclass` if preferred) to document required keys like `x`, `y`, `vx`, `vy`, `size`, `max_speed`, `time_since_jitter`, `color`, `age`, and `life_span`.
- Update function signatures from broad `Dict` to `Square` and `List[Square]`.

Why this helps:
- Beginners can quickly see what data a square contains.
- Typos in keys become easier to catch with editor/type-checker support.

Inline comment requirement for final code:
- Add short comments near the new type explaining:
  - what changed: a formal square structure was introduced
  - why it helps: clearer contract and fewer key mistakes
  - concept highlighted: type annotations and data modeling

Optional before/after snippet:

Before:
```python
def create_square() -> Dict:
```

After:
```python
class Square(TypedDict):
    ...

def create_square() -> Square:
```

## Step 2: Extract speed clamping into one helper

What to do:
- Create a helper like `clamp_speed(square: Square) -> None`.
- Move duplicated `speed` and `scale` logic from fleeing and jitter sections into this helper.
- Call it after any velocity change that might exceed `max_speed`.

Why this helps:
- Removes duplication.
- Makes behavior consistent everywhere speed is limited.
- Easier for beginners to modify speed rules in one place.

Inline comment requirement for final code:
- Add concise comments in/near `clamp_speed` explaining:
  - what changed: repeated clamp code was centralized
  - why it helps: avoids inconsistent edits and improves readability
  - concept highlighted: DRY (Don't Repeat Yourself)

Optional before/after snippet:

Before:
```python
speed = (sq["vx"] ** 2 + sq["vy"] ** 2) ** 0.5
if speed > sq["max_speed"]:
    scale = sq["max_speed"] / speed
    sq["vx"] *= scale
    sq["vy"] *= scale
```

After:
```python
clamp_speed(sq)
```

## Step 3: Split update_squares into tiny behavior helpers

What to do:
- Keep `update_squares()` as coordinator, but extract small helpers such as:
  - `apply_chase(square, squares, dt)`
  - `apply_flee(square, squares, dt)`
  - `apply_jitter(square, dt)`
  - `move_and_bounce(square, dt)`
  - `update_age_and_collect_dead(square, dt, index, dead_indices)`
- Preserve the current behavior order exactly.

Why this helps:
- The main update loop becomes easier to read line-by-line.
- Each helper has one job, making debugging easier for first-year students.

Inline comment requirement for final code:
- Add short comments before helper calls in `update_squares()` explaining:
  - what changed: behavior blocks were extracted
  - why it helps: clearer sequencing and easier debugging
  - concept highlighted: separation of concerns

Optional before/after snippet:

Before:
```python
# large mixed block in update_squares
```

After:
```python
apply_chase(sq, squares, dt)
apply_flee(sq, squares, dt)
apply_jitter(sq, dt)
move_and_bounce(sq, dt)
```

## Step 4: Improve naming clarity for steering vectors

What to do:
- Rename `fx`/`fy` to clearer names such as `force_x`/`force_y` (or `steer_x`/`steer_y`).
- Keep formulas unchanged.

Why this helps:
- New learners understand variable purpose faster.
- Makes vector math less cryptic.

Inline comment requirement for final code:
- Add brief comments where names were clarified explaining:
  - what changed: variable names now describe intent
  - why it helps: improves readability
  - concept highlighted: self-documenting code

## Step 5: Add a safe guard for average X calculation

What to do:
- In `draw_squares()`, avoid dividing by zero if `particle_count == 0`.
- Use a simple conditional default (`avg_x = 0.0` when no squares exist).

Why this helps:
- Prevents runtime crash in edge cases (for example, if constants are changed).
- Teaches defensive programming.

Inline comment requirement for final code:
- Add a short comment near the guard explaining:
  - what changed: zero-count check added
  - why it helps: avoids `ZeroDivisionError`
  - concept highlighted: input/state validation

Optional before/after snippet:

Before:
```python
avg_x = sum(sq["x"] for sq in squares) / particle_count
```

After:
```python
avg_x = 0.0 if particle_count == 0 else sum(sq["x"] for sq in squares) / particle_count
```

## Step 6: Keep rebirth logic explicit and documented

What to do:
- Keep reversed-index removal logic as-is (it is correct), but make it explicit with helper naming or concise comments.
- Optionally extract to `rebirth_dead_squares(squares, dead_indices)`.

Why this helps:
- Preserves correct list-mutation behavior.
- Makes a subtle algorithm easier for beginners to trust and reuse.

Inline comment requirement for final code:
- Add short comments explaining:
  - what changed: rebirth logic isolated/documented
  - why it helps: safe list mutation during removals
  - concept highlighted: mutation safety with reverse iteration

## Step 7: Light cleanup pass (format and consistency)

What to do:
- Standardize small style issues (spacing, consistent local variable names).
- Keep constants and behavior unchanged.
- Ensure all function signatures keep type hints.

Why this helps:
- Cleaner style reduces cognitive load.
- Consistent code is easier to maintain in team projects.

Inline comment requirement for final code:
- Add comments only where behavior might not be obvious.
- Keep comments concise and beginner-friendly.

# Final Output Requirements (Mandatory)

When this plan is executed, the output MUST:
- Contain only the refactored code.
- Include inline comments that explain:
  - what changed
  - why the change improves readability/maintainability/correctness
  - relevant programming concepts
- Keep all explanations concise and beginner-friendly.
- Preserve current behavior and structure as much as possible.

# Key Concepts for Students

- Type annotations and data contracts (`TypedDict`/structured state).
- DRY principle by extracting duplicated logic.
- Separation of concerns through small helper functions.
- Defensive programming with edge-case checks.
- Safe list mutation using reverse-index removal.
- Self-documenting code via meaningful names.

# Safety Notes

- Refactor in small steps and run the program after each step.
- Do not change gameplay constants while refactoring.
- Keep function behavior and execution order unchanged, especially inside `update_squares()`.
- Verify that fleeing, chasing, jitter, bounce, and rebirth still happen in the same order.
- Confirm HUD still displays FPS, particle count, and average X correctly.
