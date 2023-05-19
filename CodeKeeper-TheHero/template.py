import sys
import math

# Make the hero reach the exit of the maze alive.


# game loop
while True:
    # x: x position of the hero
    # y: y position of the hero
    # health: current health points
    # score: current score
    # charges_hammer: how many times the hammer can be used
    # charges_scythe: how many times the scythe can be used
    # charges_bow: how many times the bow can be used
    x, y, health, score, charges_hammer, charges_scythe, charges_bow = [int(i) for i in input().split()]
    visible_entities = int(input())  # the number of visible entities
    for i in range(visible_entities):
        # ex: x position of the entity
        # ey: y position of the entity
        # etype: the type of the entity
        # evalue: value associated with the entity
        ex, ey, etype, evalue = [int(j) for j in input().split()]

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # MOVE x y [message] | ATTACK weapon x y [message]
    print("MOVE 6 8 Let's go!")
