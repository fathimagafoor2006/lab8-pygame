## WHAT MY PROGRAM DOES ##
My program shows 20 colorful squares moving around the screen.
each squre has a random size,speed and direction.
they bounce of the wall ,move around their own and try to run away from bigger squares

## HOW THE SPEED WORKS ## 
Small square moves faster than big ones
I calculate their max speed like this 
small size --- fast and big size -- slow

## HOW FLEEING WORKS ##
Each square looks for the closest square that is bigger than it.
if it finds one, it moves away from it
the idea is find the bigger square, figure out the direction away from it and push the small square in that direction 
this makes the small squares run away from the big ones

## JITTER ##
Every 0.2 seconds, each squre gets a tiny random push
this stops them from moving in perfect straight lines and makes  the motion looks more alive

## MOVEMENT+BOUNCING ##
Squares move based on their velocity,if they hit a wall,they bounce back by flipping their direction

## DRAWING ##
Each square is drawn as simple colored rectangle
i also show FPS, number of squares,average x position

## WHY THIS WORKS ##
fleeing makes the square react to each other
jitter adds randomness
speed limits keep things under control
bouncing keeps everything inside the screen
So,everything together creates the simulation

## LIFESPAN+REBIRTH FEATURE ##

To implement this feature, I added two new attributes to each square: age and life_span. The life_span is a random value between 30 and 180 seconds. Each square starts with age = 0.
During each update, I increment the age using the delta time (dt). When a square’s age becomes greater than or equal to its life span, I mark it as dead.
After updating all squares, I remove the dead ones and immediately create new squares to replace them. The new squares get a new random position, speed, color, and life span. This keeps the total number of squares constant and simulates a cycle of life, death, and rebirth.

## REVIEW BY COPILOT ##
I asked Copilot to double check just the lifespan + rebirth part.and it confirmed that
age is updated correctly using dt, squares are removed safely using reversed index popping, and new squares are spawned without list mutation issues. The only edge cases it identified were normal real time simulation behaviors, such as a one frame delay before death and possible mass rebirth after a large dt spike, which do not affect correctness

## WHAT I LEARNED ##

I asked copilot few questions to make sure my life span and rebirth feature was working the way i intented

# How i tested that rebirth works
i temporarily set the lifespan to something very small like 1 second so i could see squares dying and respawning quickly.rebirth works as the square count always stays the same;new squares should restart with age 0 and fresh lifespan.Big dt spikes can make many squares die at once, but the logic still stays stable.
# How could i visualize which squares are about to die
I can compute a ratio: age/life_span and a small life bar
If i want smoother behavior during dt spikes, I can clamp dt or use fixed step updates.
# Code structure
My rebirth logic is correct, but I could move it into a helper function to make the code cleaner.
# Interaction with fleeing and jitter
Lifespan works fine with fleeing and jitter squares die at the end of the frame, which is normal.
## CHASING FEATURE ##
I added a new behavior where Bigger squares chase smaller squares(predator-pray effect)
# How chasing works
Each square looks for the closest smaller square.
If it finds one, it moves toward it.only squares that are bigger than others will chase.small squares never chase they only flee.
# How I implemented it
I added two new helper functions:
one to find the closest smaller square and one to compute the chase direction
Inside update_squares(), I apply the chasing force before the fleeing force so both behaviors work independently.
## Why chasing improves the simulation
Big squares behave like predators
Small squares behave like prey
Movement becomes more dynamic and interesting
Fleeing + chasing + jitter together create natural‑looking motion
This feature adds a new layer of interaction and makes the whole system feel more intentional and alive.
# What i learned
I learned how to make bigger squares move toward smaller ones by finding the closest smaller square and pushing the velocity in that direction. I also learned that chasing and fleeing both work correctly as long as they are checked separately. Adding chasing made the movement look more interesting and helped me understand how combining simple rules can create more complex behavior
# Copilot interaction
To make sure my chasing feature was working correctly, I asked Copilot a few questions about my code. I checked things like whether my chasing logic made sense, whether it conflicted with the fleeing behavior, and how I could make the chasing movement smoother. Copilot explained how chasing and fleeing should be kept separate, and it also gave suggestions for making the motion feel more natural, such as using a smaller chase strength or adding a detection range. This helped me understand how different forces interact in my simulation and how small changes can make the movement look more realistic

