
class HeapPair:
    def __init__(self, nodeNdx, weight):
        self.index = nodeNdx
        self.weight = weight

    def __lt__(self, other):
        return self.weight < other.weight

    def __gt__(self, other):
        return self.weight > other.weight

class MazeNode:
    def __init__(self, coordinate, index, weight):
        self.coordinate = coordinate
        self.index = index
        self.weight = weight


    def __eq__(self, other):
        return self.coordinate[0] == other.coordinate[0] and \
               self.coordinate[1] == other.coordinate[1]

    def __str__(self):
        return "coordinate: (x: " + str(self.coordinate[0]) + ", y: " + str(self.coordinate[1]) + ") index: " + str(
            self.index)

    def __getitem__(self, item):
        if 2 > item >= 0:
            return self.coordinate[item]
        else:
            assert False

    def __hash__(self):
        return hash(str(self))