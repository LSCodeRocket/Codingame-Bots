import math

cells_num = int(input())  # no. of cells

cell_list = []  # list of tuples with cell info

for i in range(cells_num):
    # _type: 0 for empty, 1 for eggs, 2 for crystal
    # initial_resources: the initial amount of eggs/crystals on this cell
    # neigh_0: the index of the neighbouring cell for each direction
    cell_list.append(tuple([int(j) for j in input().split()]))

bases_num = int(input())  # no. of bases

my_base_indexes = [int(i) for i in input().split()]  # indexes of our bases
opp_base_indexes = [int(i) for i in input().split()]  # indexes of opponent bases

# game loop
while True:
    for i in range(cells_num):
        # resources: the current amount of eggs/crystals on this cell
        # my_ants: the amount of your ants on this cell
        # opp_ants: the amount of opponent ants on this cell
        resources, my_ants, opp_ants = [int(j) for j in input().split()]

        print("Commands")

    # WAIT | LINE <sourceIdx> <targetIdx> <strength> | BEACON <cellIdx> <strength> | MESSAGE <text>
