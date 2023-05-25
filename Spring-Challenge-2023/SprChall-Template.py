import math

cells_num = int(input())  # amount of hexagonal cells in this map

for i in range(cells_num):
    # _type: 0 for empty, 1 for eggs, 2 for crystal
    # initial_resources: the initial amount of eggs/crystals on this cell
    # neigh_0: the index of the neighbouring cell for each direction
    type, initial_resources, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5 = [
        int(j) for j in input().split()
    ]
number_of_bases = int(input())
for i in input().split():
    my_base_index = int(i)
for i in input().split():
    opp_base_index = int(i)


def cell_dist(cell):
    # finds the shortest path from the base to a cell
    # iterates through possible paths

    paths = []
    return min([len(path) for path in paths])


# game loop
while True:
    for i in range(cells_num):
        # resources: the current amount of eggs/crystals on this cell
        # my_ants: the amount of your ants on this cell
        # opp_ants: the amount of opponent ants on this cell
        resources, my_ants, opp_ants = [int(j) for j in input().split()]

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # WAIT | LINE <sourceIdx> <targetIdx> <strength> | BEACON <cellIdx> <strength> | MESSAGE <text>
    print("WAIT")
