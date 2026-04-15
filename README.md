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

Lifespan + rebirth
------------------
- Each square starts with `age = 0.0` and a random `life_span` between `30.0` and `180.0` seconds.
- During each update, the square's age increases by `dt`, so lifespan progression stays tied to real frame time.
- When `age >= life_span`, the square is marked for removal after the update loop finishes.
- Dead squares are removed safely using reversed index popping, then replaced with new squares so the total count stays constant.
- New squares get fresh random size, speed, position, color, and lifespan values.

Project structure
-----------------
- `main.py`: the complete simulation and rendering loop.
- `requirements.txt`: Python dependencies needed to run the project.
- `README.md`: setup notes, features, and project overview.
- `JOURNAL.md`: chronological log of development updates.
- `docs/code_explorer.html`: generated learning dashboard for the codebase.

```text
lab8-pygame/
├── .github/
│   ├── agents/
│   │   ├── code-explorer-template.html
│   │   ├── code-explorer.agent.md
│   │   └── journal-logger.agent.md
│   ├── hooks/
│   └── copilot-instructions.md
├── .venv/
├── docs/
│   └── code_explorer.html
├── .gitignore
├── copilot.usage.png
├── JOURNAL.md
├── main.py
├── MY_NOTES.md
├── prompts_history.md
├── README.md
├── REPORT.md
└── requirements.txt
```


