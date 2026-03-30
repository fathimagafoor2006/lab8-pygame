# lab8-pygame

Simple Pygame exercise: display 10 squares moving randomly on the screen.

Setup
-----
1. Create and activate the virtual environment (Windows PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Or (cmd.exe):

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

On Unix/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies (after activation):

```bash
pip install -r requirements.txt
```

Running
-------

Run the app with:

```bash
python main.py
```

Notes
-----
- A `.venv` was created and `pygame` installed.
- `requirements.txt` was generated from the venv.
- `main.py` currently contains a Socratic skeleton with TODOs to implement behavior.

Features Implemented
--------------------

The following features were implemented from scratch in `main.py`:

- **Size-based max speed:** Each square's maximum speed scales with its size. Larger squares move slower, smaller squares move faster. This makes motion feel more natural because larger objects cover more screen area per update and therefore should move more slowly.

- **Random jitter:** Small random velocity perturbations are applied each frame to each square. This introduces subtle, non-linear motion and prevents perfectly smooth paths, producing a more organic, jittery movement.

- **Rotation:** Squares are rendered with rotation applied so each sprite can spin while it moves. Rotation is computed per-square and updated independently from translation.

- **FPS experiment (FPS = 0):** The app supports experimenting with the frame rate. Setting the target FPS to `0` disables the fixed-frame delay, causing the main loop to run as fast as possible.

What happens when FPS is set to 0
--------------------------------

When you set FPS to `0`, the loop does not wait between frames — it continually processes events, updates, and draws as quickly as the CPU allows. Consequences:

- **CPU usage spikes:** With no sleep or delay, the program spends almost all CPU time running the main loop, often driving one or more cores to near 100% usage.
- **Unstable animation timing:** Frame-to-frame timing becomes entirely dependent on how fast the machine can run the loop. This can produce inconsistent motion speeds and jitter because movement updates typically assume a stable delta-time or a fixed-step update.
- **Higher power draw and heat:** Continuous full utilization increases power consumption and may cause thermal throttling on some machines.

Why CPU usage increases
-----------------------

Most game loops use a frame limiter (e.g., `clock.tick(FPS)` in Pygame) to pause the loop long enough to match the target FPS. When `FPS > 0`, the loop yields time back to the OS each frame, keeping CPU usage moderate. Setting `FPS = 0` removes that pause, so the loop never yields and runs continuously, causing high CPU usage.

Recommendations
---------------

- Use a moderate FPS (e.g., `30` or `60`) for smooth animation and reasonable CPU usage.
- If you need heavy CPU work per frame, consider using a fixed timestep with frame skipping or moving expensive work to separate threads/processes.

