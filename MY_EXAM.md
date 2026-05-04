# Exercise 1
For this exercise, I modified the square‑creation logic so the simulation starts with three fixed groups instead of random sizes
I now generate:
5 squares of size 25
10 squares of size 10
30 squares of size 4
I also recompute each square’s max_speed after forcing its size, so the movement still respects the size‑based speed rule.
# Exercise 2
I modified the rebirth logic so that when a square dies, the new square keeps the same size as the one it replaces.After creating the new square, I overwrite its size with the old size and recompute max_speed so the movement rules stay consistent.
