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
    
    def FindNonEmptyCellsOfType(self, cell_type):
        return [cell for cell in self.cell_list if cell.cell_type == cell_type and cell.resources != 0]
        

    def FindClosestTargetsOfType(self, target_type, target_num):
        targets = self.FindCellsOfType(target_type)
        target_distances = np.array(
            [
                self.connection_object.ComputeFloodFillDistance(
                    self.my_base_indexes[0], target.cell_index
                )
                for target in targets
            ]
        )

        closest_targets = []

        for i in range(min(target_num, len(targets))):
            index = target_distances.argmin()
            closest_targets.append(targets[index].cell_index)
            target_distances[index] = target_distances.max() + 1

        return closest_targets

    def FindClosestNonEmptyTargetsOfType(self, target_type, target_num):
        targets = self.FindNonEmptyCellsOfType(target_type)
        target_distances = np.array(
            [self.FindDistance(target.cell_index) for target in targets]
        )

        closest_targets = []

        for i in range(min(target_num, len(targets))):
            index = target_distances.argmin()
            closest_targets.append(targets[index].cell_index)
            target_distances[index] = target_distances.max() + 1

        return closest_targets

    def MoveToTargets(self, targets):
        print(
            *[
                f"LINE {self.my_base_indexes[0]} {target} {self.cell_list[target].resources};"
                for target in targets
            ]
        )

    def FrameUpdate(self):
        for i in range(self.cells_num):
            self.cell_list[i].CellInfoUpdate([int(j) for j in input().split()])

    def FindThreeTargets(self):
        closest_eggs = self.FindClosestTargetsOfType(CellInformation.EGG, 2)
        number_of_crystals = 3 - len(closest_eggs)
        closest_crystals = self.FindClosestTargetsOfType(
            CellInformation.CRYSTAL, number_of_crystals
        )
        targets = [
            *[egg for egg in closest_eggs],
            *[crystal for crystal in closest_crystals],
        ]
        return targets

    def FindThreeNonEmptyTargets(self):
        closest_eggs = self.FindClosestNonEmptyTargetsOfType(CellInformation.EGG, 2)
        closest_crystals = self.FindClosestNonEmptyTargetsOfType(CellInformation.CRYSTAL, 3)
        targets = [
            *[closest_eggs[i] for i in closest_eggs],
            *[closest_crystals[i] for i in 3 - len(closest_eggs)],
        ]
        return targets

    def FindThreeLineDistance(self, indexes):
        return sum(
            [
                self.connection_object.ComputeFloodFillDistance(
                    self.my_base_indexes[0], index
                )
                for index in indexes
            ]
        )

    def FindTwoLineDistances(self, indexes):
        two_line_distances = []
        two_line_references = []
        for i in range(len(indexes)):
            current_indexes = indexes.copy()
            current_indexes.remove(indexes[i])

            connected_distance_forward = (
                self.connection_object.ComputeFloodFillDistance(
                    self.my_base_indexes[0], current_indexes[0]
                )
                + self.connection_object.ComputeFloodFillDistance(
                    current_indexes[0], current_indexes[1]
                )
            )
            connected_distance_backward = (
                self.connection_object.ComputeFloodFillDistance(
                    self.my_base_indexes[0], current_indexes[1]
                )
                + self.connection_object.ComputeFloodFillDistance(
                    current_indexes[1], current_indexes[0]
                )
            )
            two_line_references.append([current_indexes, i])
            two_line_distances.append(connected_distance_forward)
            two_line_references.append([current_indexes.reverse(), i])
            two_line_distances.append(connected_distance_backward)

        return (two_line_references, two_line_distances)

    def FindOneLineDistances(self, indexes):
        one_line_distances = []
        one_line_references = []
        for i in range(len(indexes)):
            subtracted_index = indexes.copy()
            subtracted_index.remove(subtracted_index[i])

            for j in range(len(subtracted_index)):
                final_index = subtracted_index.copy()
                final_index.remove(final_index[j])
                final_index = final_index[0]

                distance = self.connection_object.ComputeFloodFillDistance(
                    self.my_base_indexes[0], indexes[i]
                )
                distance += self.connection_object.ComputeFloodFillDistance(
                    indexes[i], subtracted_index[j]
                )
                distance += self.connection_object.ComputeFloodFillDistance(
                    subtracted_index[j], final_index
                )

                one_line_references.append([indexes[i], subtracted_index[j], final_index])
                one_line_distances.append(distance)

        return (one_line_references, one_line_distances)

    def MoveToAndFromSelectCells(self, paths_and_weights):
        print(
            *[
                f"LINE {path_and_weight[0][0]} {path_and_weight[0][1]} {path_and_weight[1]};"
                for path_and_weight in paths_and_weights
            ]
        )
        
    def MoveWithIndependentPaths(self, indexes):
        self.MoveToTargets(indexes)
        

    def GetCellResources(self, cell):
        return self.cell_list[cell].resources

    def MoveWithTwoLinePath(self, best_two_line_path):
        dual_line = best_two_line_path[0].copy()
        dual_line.insert(0, self.my_base_indexes[0])

        independent_index = best_two_line_path[1]
        paths_and_weights = [] 
        max_resources = max([self.GetCellResources(dual_line[i+1]) for i in range(2)])
        
        for i in range(2):
            paths_and_weights.append([[dual_line[i], dual_line[i+1]], max_resources])

        paths_and_weights.append([ [self.my_base_indexes[0], independent_index ], self.GetCellResources(independent_index)])

        self.MoveToAndFromSelectCells(paths_and_weights)

    def MoveWithOneLinePath(self, best_one_line_path):
        triple_line = best_one_line_path[0].copy()
        triple_line.insert(0, self.my_base_indexes[0])
        
        paths_and_weights = [] 
        max_resources = max([self.GetCellResources(triple_line[i+1]) for i in range(3)])
        
        for i in range(3):
            paths_and_weights.append([[triple_line[i], triple_line[i+1]], max_resources])

        self.MoveToAndFromSelectCells(paths_and_weights)
        
    def ChooseOptimalGraph(self, indexes, independent_distance, two_line_reference_arrays, one_line_reference_arrays):
        two_line_references, two_line_distances = two_line_reference_arrays
        one_line_references, one_line_distances = one_line_reference_arrays

        minimum_distance_type = np.array([independent_distance, min(two_line_distances), min(one_line_distances)]).argmin()

        if minimum_distance_type == 0:
            self.MoveWithIndependentPaths(indexes)

        elif minimum_distance_type == 1:
            best_two_line_path = two_line_references[np.array(two_line_distances).argmin()]
            self.MoveWithTwoLinePath(best_two_line_path)
        
        else:
            best_one_line_path = one_line_references[np.array(one_line_distances).argmin()]
            self.MoveWithOneLinePath(best_one_line_path)
            

    def DecideTargetIndexesBasedOnNumber(self, crystal_indexes, egg_indexes):
        if len(egg_indexes) >= 2:
            return [crystal_indexes[0], egg_indexes[0], egg_indexes[1]]
        
        elif len(egg_indexes) == 1:
            if len(crystal_indexes) > 1:
                return [crystal_indexes[0], crystal_indexes[1], egg_indexes[0]]
            else:
                return [crystal_indexes[0], crystal_indexes[1], egg_indexes[0]]
        else:
            if len(crystal_indexes) >= 2:
                return [crystal_indexes[0], crystal_indexes[1]]
            else:
                return [crystal_indexes[0]]

    def NormalThreeIndexPath(self, indexes):
        independent_distance = self.FindThreeLineDistance(indexes)
        two_line_distances = self.FindTwoLineDistances(indexes)
        one_line_distances = self.FindOneLineDistances(indexes)
        self.ChooseOptimalGraph(indexes, independent_distance, two_line_distances, one_line_distances)

    def AbnormalTwoIndexPath(self, indexes):
        self.MoveToTargets(indexes)

    def FindDistance(self, cell):
        return self.connection_object.ComputeFloodFillDistance(self.my_base_indexes[0], cell)

    def Action(self):
        crystal_indexes = self.FindClosestNonEmptyTargetsOfType(CellInformation.CRYSTAL, 2)
        egg_indexes = self.FindClosestNonEmptyTargetsOfType(CellInformation.EGG, 2)
        indexes = self.DecideTargetIndexesBasedOnNumber(crystal_indexes, egg_indexes)
        if len(indexes) == 3:
            self.NormalThreeIndexPath(indexes)
        elif len(indexes) == 2:
            self.AbnormalTwoIndexPath(indexes)
        else:
            self.MoveToTargets(indexes)

C = AlgorithmBot()

# game loop
while True:
    C.FrameUpdate()
    C.Action()
    # WAIT | LINE <sourceIdx> <targetIdx> <strength> | BEACON <cellIdx> <strength> | MESSAGE <text>
