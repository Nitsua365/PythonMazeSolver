import MazeGraph


class DijkstraGraph(MazeGraph):
    def __init__(self, maze):
        super().__init__(self, maze)

        for i in range(0, len(self.adjList)):
            for j in range(0, len(self.adjList[i])):
                
