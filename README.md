# lab8-pygame

Simple Pygame simulation of colorful moving squares.

What it does
-----------
- Shows 20 colorful squares that move, bounce, and interact on screen.
- Each square has a random size, speed, direction, and color.

Key behaviors
-------------
- **Size-based speed:** Smaller squares can move faster than larger ones (max speed is scaled by size).
- **Fleeing:** Each square detects the nearest bigger square and accelerates away from it, producing separation behavior.
- **Jitter:** Every ~0.2 seconds each square receives a small random velocity kick to avoid perfectly straight motion.
- **Bouncing:** Squares stay inside the window by reflecting their velocity when they hit edges.
- **Diagnostics:** The app draws FPS, particle count (number of squares), and the average X position of all squares.

Setup
-----
1. Create and activate a virtual environment (Windows PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

Running
-------

Run the app:

```bash
python main.py
```

Notes & tuning
--------------
- Default uses 20 squares; change the constant in `main.py` to experiment.
- Jitter interval and magnitude, flee strength, and max-speed scaling are tunable parameters in `main.py`.
- Setting `FPS = 0` runs the loop without a frame limiter: CPU usage will spike and animation timing may become unstable. Prefer `30` or `60` for smooth, predictable results.

Why this setup works
--------------------
- Size-based speed keeps motion visually balanced.
- Fleeing makes objects respond to each other, producing emergent movement.
- Jitter prevents perfectly deterministic trajectories and makes the simulation feel alive.
- Bouncing keeps objects onscreen for continuous interaction.

Files of interest
-----------------
- `main.py`: simulation code and tunable parameters.
- `requirements.txt`: project dependencies.


