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

    def PathFinder(self, index_start, index_end, current_path=[]):
        for i in range(self.cell_count):
            if (
                self.cells[index_start][i] == 1
                and self.flood_fill_vector[i] > self.flood_fill_vector[index_start]
            ):
                path = current_path.copy()
                path.append(i)

                if i == index_end:
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
    EGG = 1
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

    def CellInfoUpdate(self, cell_frame_information):
        resources, my_ants, opp_ants = cell_frame_information
        self.resources = resources
        self.my_ants = my_ants
        self.opp_ants = opp_ants

        if resources == 0:
            self.cell_type = CellInformation.EMPTY


class AlgorithmBot:
    STATES = ("EGG", "CRYSTAL")
    TARGET_NUM = 2

    def __init__(self):
        self.InitializeCellInformation()
        self.InitializeBaseInformation()
        self.state = "EGG"

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

    def FindCellsOfType(self, cell_type):
        return [cell for cell in self.cell_list if cell.cell_type == cell_type]

    def FindDistance(self, index):
        return self.connection_object.ComputeFloodFillDistance(
            self.my_base_indexes[0], index
        )

    def FindClosestTargetsOfType(self, target_type, target_num):
        targets = self.FindCellsOfType(target_type)
        target_distances = np.array(
            [self.FindDistance(target.cell_index) for target in targets]
        )

        closest_targets = []

        for i in range(min(target_num, len(targets))):
            index = target_distances.argmin()
            closest_targets.append(targets[index].cell_index)
            target_distances[index] = target_distances.max() + 1

        return closest_targets

    def FrameUpdate(self):
        for i in range(self.cells_num):
            self.cell_list[i].CellInfoUpdate([int(j) for j in input().split()])

    def ChangeState(self, state):
        if state in self.STATES:
            self.state = state

    def Action(self):
        if len(self.FindCellsOfType(CellInformation.EGG)) == 0 and self.state == "EGG":
            self.ChangeState("CRYSTAL")

        if self.state == "EGG":
            target_type = CellInformation.EGG
        elif self.state == "CRYSTAL":
            target_type = CellInformation.CRYSTAL

        command = ""
        for index in self.FindClosestTargetsOfType(target_type, self.TARGET_NUM):
            command += f"LINE {self.my_base_indexes[0]} {index} {self.cell_list[index].resources};"
        print(command)


C = AlgorithmBot()

# game loop
while True:
    C.FrameUpdate()
    C.Action()
    # WAIT | LINE <sourceIdx> <targetIdx> <strength> | BEACON <cellIdx> <strength> | MESSAGE <text>
