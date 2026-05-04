# Exercise 1
For this exercise, I modified the square‑creation logic so the simulation starts with three fixed groups instead of random sizes
I now generate:
5 squares of size 25
10 squares of size 10
30 squares of size 4
I also recompute each square’s max_speed after forcing its size, so the movement still respects the size‑based speed rule.
# Exercise 2
I modified the rebirth logic so that when a square dies, the new square keeps the same size as the one it replaces.After creating the new square, I overwrite its size with the old size and recompute max_speed so the movement rules stay consistent.
# Exercise 3 
I replaced the bouncing logic with screen wrapping.
When a square moves past one edge of the screen, it reappears on the opposite side with the same velocity.This removes wall collisions and creates continuous movement across the screen.
# Exercise 4
I added a check_collision(a,b) function that uses pygame.Rect to detect overlap between two squares.Each square is converted into a rectangle using its position and size, and I return True when rectA.colliderect(rectB) is true.