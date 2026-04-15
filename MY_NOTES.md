## WHAT MY PROGRAM DOES
My program shows 20 colorful squares moving around the screen.
each squre has a random size,speed and direction.
they bounce of the wall ,move around their own and try to run away from bigger squares

## HOW THE SPEED WORKS 
Small square moves faster than big ones
I calculate their max speed like this 
small size --- fast and big size -- slow

## HOW FLEEING WORKS
Each square looks for the closest square that is bigger than it.
if it finds one, it moves away from it
the idea is find the bigger square, figure out the direction away from it and push the small square in that direction 
this makes the small squares run away from the big ones

## JITTER 
Every 0.2 seconds, each squre gets a tiny random push
this stops them from moving in perfect straight lines and makes  the motion looks more alive

## MOVEMENT+BOUNCING
Squares move based on their velocity,if they hit a wall,they bounce back by flipping their direction

## DRAWING
Each square is drawn as simple colored rectangle
i also show FPS, number of squares,average x position

## WHY THIS WORKS
fleeing makes the square react to each other
jitter adds randomness
speed limits keep things under control
bouncing keeps everything inside the screen
So,everything together creates the simulation

## LIFESPAN+REBIRTH FEATURE

To implement this feature, I added two new attributes to each square: age and life_span. The life_span is a random value between 30 and 180 seconds. Each square starts with age = 0.
During each update, I increment the age using the delta time (dt). When a square’s age becomes greater than or equal to its life span, I mark it as dead.
After updating all squares, I remove the dead ones and immediately create new squares to replace them. The new squares get a new random position, speed, color, and life span. This keeps the total number of squares constant and simulates a cycle of life, death, and rebirth.


