import math

class CellConnections:
    def __init__(self, cell_count):
        self.cells = [ [ 0 for i in range(cell_count) ] for j in range(cell_count) ]
    
    def Connect(self, index1, index2):
        self.cells[index1][index2] = 1
        self.cells[index2][index1] = 1
    
    def ComputeOptimalPath(self, index1, index2):
        pass
    
    def ComputeFloodFillDistance(self, index1, index2):
        pass

class CellInformation:
    def __init__(self, cell_index, connection_object, cell_information_list = [None for i in range(7)]):
        self.cell_index = cell_index 
        self.SetData(connection_object, cell_information_list)
        
    def SetData(self, connection_object, cell_information_list):
        self.cell_type = cell_information_list[0]
        self.resources = cell_information_list[1]
        self.my_ants = 0
        self.opp_ants = 0
        self.neighbors = cell_information_list[2:len(cell_information_list)]
        for i in range(len(self.neighbors)):
            connection_object.Connect(self.neighbors[i], self.cell_index)

cells_num = int(input())  # no. of cells
connection_object = CellConnections(cells_num)

cell_list = []  # list of CellInformation objects with cell information about current cells

for i in range(cells_num):
    # _type: 0 for empty, 1 for eggs, 2 for crystal
    # initial_resources: the initial amount of eggs/crystals on this cell
    # neigh_0: the index of the neighbouring cell for each direction
    cell_list.append( CellInformation( i, connection_object, [int(j) for j in input().split()] ) )

bases_num = int(input())  # no. of bases
my_base_indexes = [int(i) for i in input().split()]  # indexes of our bases
opp_base_indexes = [int(i) for i in input().split()]  # indexes of opponent bases

while True:
    for i in range(cells_num):
        # resources: the current amount of eggs/crystals on this cell
        # my_ants: the amount of your ants on this cell
        # opp_ants: the amount of opponent ants on this cell
        resources, my_ants, opp_ants = [int(j) for j in input().split()]
        cell_list[i].my_ants = my_ants
        cell_list[i].opp_ants = opp_ants
        cell_list[i].resources = resources

    print("WAIT")

    # WAIT | LINE <sourceIdx> <targetIdx> <strength> | BEACON <cellIdx> <strength> | MESSAGE <text>
