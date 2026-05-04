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
# Exercise 5
I detect collisions between squares using check_collision().When two squares collide, the larger one eats the smaller.The eaten square is removed and respawned with the same sizeI collect eaten indices separately and merge them with the normal death list before respawning to avoid index errors.
# Exercise 6
I extended the eating behavior so that when a larger square eats a smaller one, the larger squaregrows.  I increase its size by 1 and recompute `max_speed` so that bigger squares move more slowly.  The eaten square is still respawned with the same size as before, following the rules from Exercise 2.
# Exercise 7
I added a trail feature so each square leaves a visible trace of its past movement. I store recent positions in a list called trail and draw them using pygame.draw.lines(). This creates smooth, colorful paths showing each square’s trajectory.
# Exercise 8
I added a global variable TEST_MODE_ON to enable a diagnostic mode that checks whether squares move at their correct speed. 
When active, the program calculates each square’s actual velocity magnitude and compares it to its max_speed. If the square exceeds its limit, a warning is printed. 
This test validates that the speed‑clamping logic works correctly.
# Exercise 9
I added a visual arrow to each square to show its movement direction. 
The arrow starts at the square’s center and points in the direction of its velocity vector. Its length is scaled so it remains readable. This helps visualize motion and debugging behaviors..


