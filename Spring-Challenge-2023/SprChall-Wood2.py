import math
import sys
import numpy as np

DEBUG_FLAG = True


def DebugLog(message):
    if DEBUG_FLAG:
        print(message, file=sys.stderr)


class CellConnections:
    def __init__(self, cell_count):
        self.cell_count = cell_count
        self.flood_fill_vector = [-1 for i in range(self.cell_count)]
        self.cells = [[0 for i in range(cell_count)] for j in range(cell_count)]

    def Connect(self, index1, index2):
        self.cells[index1][index2] = 1
        self.cells[index2][index1] = 1

    def CellIsWorthPathing(self, index_start, current_index):
        ARE_THE_CELLS_CONNECTED = self.cells[index_start][current_index] == 1
        IS_CURRENT_FLOODFILL_VALUE_GREATER = self.flood_fill_vector[current_index] > self.flood_fill_vector[index_start]

        return ARE_THE_CELLS_CONNECTED and IS_CURRENT_FLOODFILL_VALUE_GREATER

    def HasPathEnded(self, current_path_index, index_end):
        return current_path_index == index_end

    def PathFinder(self, index_start, index_end, current_path = []):
        for i in range(self.cell_count):
            if self.CellIsWorthPathing(index_start, i):
                path = current_path.copy()
                path.append(i)

                if self.HasPathEnded(i, index_end):
                    return path

                result_path = self.PathFinder(i, index_end, path)
                if result_path[-1] == index_end:
                    return result_path
        return [-1]

    def ComputeOptimalPath(self, index1, index2):
        path = self.PathFinder(index1, index2)
        return path

    def ComputeFloodFillDistance(self, index1, index2):
        if index1 == index2:
            return 0

        self.flood_fill_vector = [-1 for i in range(self.cell_count)]
        self.flood_fill_vector[index1] = 0

        self.ComputeNeighbors(0, index1)

        return self.flood_fill_vector[index2] + 1

    def ChooseCellsToFlood(self, cells_to_flood, index, targetindex):
        if self.cells[index][targetindex] == 1:
            if (
                self.flood_fill_vector[targetindex] > self.flood_fill_vector[index]
                or self.flood_fill_vector[targetindex] == -1
            ):
                cells_to_flood.append(targetindex)

                self.flood_fill_vector[targetindex] = self.flood_fill_vector[index] + 1

    def ComputeNeighbors(self, current_value, index):
        cells_to_flood = []
        for i in range(self.cell_count):
            self.ChooseCellsToFlood(cells_to_flood, index, i)

        for i in range(len(cells_to_flood)):
            self.ComputeNeighbors(current_value + 1, cells_to_flood[i])


class CellInformation:
    EMPTY = 0
    EGGS = 1
    CRYSTAL = 2

    def __init__(
        self,
        cell_index,
        connection_object,
        cell_information_list=[None for i in range(7)],
    ):
        self.cell_index = cell_index
        self.SetData(connection_object, cell_information_list)

    def SetData(self, connection_object, cell_information_list):
        self.cell_type = cell_information_list[0]
        self.resources = cell_information_list[1]
        self.my_ants = 0
        self.opp_ants = 0
        self.neighbors = cell_information_list[2:]
        self.ConnectToNeighbors(connection_object)

    def ConnectToNeighbors(self, connection_object):
        for i in range(len(self.neighbors)):
            if self.neighbors[i] != -1:
                connection_object.Connect(self.neighbors[i], self.cell_index)

    def FrameUpdate(self, cell_frame_information):
        resources, my_ants, opp_ants = cell_frame_information
        self.resources = resources
        self.my_ants = my_ants
        self.opp_ants = opp_ants

        if resources == 0:
            self.cell_type = CellInformation.EMPTY


class AlgorithmBot:
    def __init__(self):
        self.InitializeCellInformation()
        self.InitializeBaseInformation()
        self.InitializeControllerVariables()

    def InitializeControllerVariables(self):
        self.distances = []

    def InitializeBaseInformation(self):
        self.bases_num = int(input())  # no. of bases
        self.my_base_indexes = [int(i) for i in input().split()]  # indexes of our bases
        self.opp_base_indexes = [
            int(i) for i in input().split()
        ]  # indexes of opponent bases

    def InitializeCellInformation(self):
        self.cells_num = int(input())  # no. of cells
        self.connection_object = CellConnections(self.cells_num)
        self.cell_list = (
            []
        )  # list of CellInformation objects with cell information about current cells
        for i in range(self.cells_num):
            given_cell_info = [int(j) for j in input().split()]
            self.cell_list.append(
                CellInformation(i, self.connection_object, given_cell_info)
            )

    def RecordDistances(self, index):
        if (
            self.cell_list[index].cell_type == CellInformation.CRYSTAL
            and self.cell_list[index].resources != 0
            and index != self.my_base_indexes
        ):
            self.distances.append(
                self.connection_object.ComputeFloodFillDistance(
                    self.my_base_indexes[0], index
                )
            )
        else:
            self.distances.append(math.inf)

    def ChooseTwoTargetsBasedOnDistances(self):
        distances = self.distances.copy()
        first_index = np.array(distances).argmin()
        distances.remove(distances[first_index])

        second_index = np.array(distances).argmin()

        if first_index <= second_index:
            second_index += 1

        if self.cell_list[second_index].resources == 0:
            second_index = -1

        return (first_index, second_index)

    def FrameUpdate(self):
        self.distances = []
        for i in range(self.cells_num):
            self.cell_list[i].FrameUpdate([int(j) for j in input().split()])
            self.RecordDistances(i)

    def Action(self):
        first_index, second_index = self.ChooseTwoTargetsBasedOnDistances()
        if second_index != -1:
            print(
                f"LINE {self.my_base_indexes[0]} {first_index} {self.cell_list[first_index].resources}; LINE {self.my_base_indexes[0]} {second_index} {self.cell_list[second_index].resources}"
            )
        else:
            print(
                f"LINE {self.my_base_indexes[0]} {first_index} {self.cell_list[first_index].resources}"
            )


C = AlgorithmBot()

# game loop
while True:
    C.FrameUpdate()
    C.Action()
    # WAIT | LINE <sourceIdx> <targetIdx> <strength> | BEACON <cellIdx> <strength> | MESSAGE <text>
