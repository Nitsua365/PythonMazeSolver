import time
from math import floor
import heapq
from EdgesAndNodes import HeapPair, MazeNode, DijkstraEdge


def binSearchbyXandY(key, searchList, searchType):
    lo = 0
    hi = len(searchList) - 1
    isX = int(False if searchType == "X" or searchType == "x" else True)

    while lo <= hi:
        mid = floor((hi + lo) / 2)

        if searchList[mid][0][isX] < key:
            lo = mid + 1
        elif searchList[mid][0][isX] > key:
            hi = mid - 1
        else:
            return mid


class MazeGraph:
    def __init__(self, maze):
        self.adjList = []
        self.maze = maze
        self.DFSSearchStack = []
        self.DFSVisitedStack = []
        self.edgeCount = 0
        self.BFSQueue = []
        self.BFSVisited = []
        self.BFSBacktrack = {}
        self.startNode = []
        self.endNode = []

        # find all valid edges and populate adj list
        nodeLengthItr = maze.__getattribute__('wallWidth')

        while nodeLengthItr < maze.__getattribute__('length'):

            nodeWidthItr = maze.__getattribute__('wallWidth')

            while nodeWidthItr < maze.__getattribute__('width'):

                if self.__isNode([nodeLengthItr, nodeWidthItr]) or \
                        [nodeLengthItr, nodeWidthItr] == maze.__getattribute__('startNodeLoc') or \
                        [nodeLengthItr, nodeWidthItr] == maze.__getattribute__('endNodeLoc'):
                    self.adjList.append([MazeNode([nodeLengthItr, nodeWidthItr], len(self.adjList))])

                if [nodeLengthItr, nodeWidthItr] == maze.__getattribute__('startNodeLoc'):
                    self.startNode = MazeNode([nodeLengthItr, nodeWidthItr], len(self.adjList))

                if [nodeLengthItr, nodeWidthItr] == maze.__getattribute__('endNodeLoc'):
                    self.endNode = MazeNode([nodeLengthItr, nodeWidthItr], len(self.adjList))

                nodeWidthItr += maze.__getattribute__('nodeSize') + maze.__getattribute__('wallWidth')

            nodeLengthItr += maze.__getattribute__('nodeSize') + maze.__getattribute__('wallWidth')

        # add all edges with same X coordinates
        nodeLengthItr = maze.__getattribute__('wallWidth')
        while nodeLengthItr < maze.__getattribute__('length'):

            Xindex = binSearchbyXandY(nodeLengthItr, self.adjList, "X")

            foundRight = foundLeft = False

            startNdx = endNdx = Xindex

            for j in range(1, len(self.adjList)):

                if (j + Xindex) < len(self.adjList) and self.adjList[j + Xindex][0][0] == nodeLengthItr:
                    endNdx = j + Xindex
                else:
                    foundRight = True

                if (Xindex - j) >= 0 and self.adjList[Xindex - j][0][0] == nodeLengthItr:
                    startNdx = Xindex - j
                else:
                    foundLeft = True

                if foundRight and foundLeft:
                    endNdx += 1
                    break

            for i in range(startNdx, endNdx):
                for j in range(startNdx, endNdx):
                    if i != j and \
                            self.adjList[i][0][0] == self.adjList[j][0][0] and not \
                            self.__isWallSeparated(self.adjList[i][0], self.adjList[j][0]) and not \
                            self.__isNodeSeparated(self.adjList[i][0], self.adjList[j][0]):
                        self.__addEdge(self.adjList[i][0], self.adjList[j][0])

            nodeLengthItr += maze.__getattribute__('nodeSize') + maze.__getattribute__('wallWidth')

        # sort values by Y coordinates
        self.adjList.sort(key=lambda MazeNode: MazeNode[0][1])

        for i in range(0, len(self.adjList)):
            self.adjList[i][0].__setattr__('index', i)
            if self.adjList[i][0] == self.startNode:
                self.startNode = MazeNode(self.startNode.__getattribute__('coordinate'), i)

            if self.adjList[i][0] == self.endNode:
                self.endNode = MazeNode(self.endNode.__getattribute__('coordinate'), i)

        # add all edges with same Y coordinates
        nodeWidthItr = maze.__getattribute__('wallWidth')
        while nodeWidthItr < maze.__getattribute__('width'):

            Yindex = binSearchbyXandY(nodeWidthItr, self.adjList, "Y")

            foundRight = foundLeft = False

            startNdx = endNdx = Yindex

            for j in range(1, len(self.adjList)):

                if (j + Yindex) < len(self.adjList) and self.adjList[j + Yindex][0][1] == nodeWidthItr:
                    endNdx = j + Yindex
                else:
                    foundRight = True

                if (Yindex - j) >= 0 and self.adjList[Yindex - j][0][1] == nodeWidthItr:
                    startNdx = Yindex - j
                else:
                    foundLeft = True

                if foundRight and foundLeft:
                    endNdx += 1
                    break

            for i in range(startNdx, endNdx):
                for j in range(startNdx, endNdx):
                    if i != j and \
                            self.adjList[i][0][1] == self.adjList[j][0][1] and not \
                            self.__isWallSeparated(self.adjList[i][0], self.adjList[j][0]) and not \
                            self.__isNodeSeparated(self.adjList[i][0], self.adjList[j][0]):
                        self.__addEdge(self.adjList[i][0], self.adjList[j][0])

            nodeWidthItr += maze.__getattribute__('nodeSize') + maze.__getattribute__('wallWidth')

        # for i in range(0, len(self.adjList)):
        #     for j in range(0, len(self.adjList)):
        #         if i != j and \
        #                 (self.adjList[i][0][0] == self.adjList[j][0][0] or
        #                  self.adjList[i][0][1] == self.adjList[j][0][1]) and not \
        #                 self.__isWallSeparated(self.adjList[i][0], self.adjList[j][0]) and not \
        #                 self.__isNodeSeparated(self.adjList[i][0], self.adjList[j][0]):
        #             self.__addEdge(self.adjList[i][0], self.adjList[j][0])

        self.DFSVisitedStack = [False for i in range(len(self.adjList))]
        self.BFSVisited = [False for i in range(len(self.adjList))]

        for i in self.adjList:
            self.edgeCount += (len(i) - 1)

        print("Adjacency List: [x, y]")
        self.printAdjList()

    def printAdjList(self):
        for i in range(0, len(self.adjList)):
            print("[", end='')
            for j in range(0, len(self.adjList[i])):
                if j == 0:
                    print(str(self.adjList[i][j].__getattribute__('coordinate')) + "]", end='')
                else:
                    print(" -> " + str(self.adjList[i][j].__getattribute__('coordinate')), end='')
            print()

    def __addEdge(self, node1, node2):
        self.adjList[node1.__getattribute__('index')].append(node2)

    def DFS(self):
        self.__DFSHelper(self.startNode)
        self.DFSSearchStack.append(self.endNode)

    def __DFSHelper(self, mazeNode):
        self.DFSVisitedStack[mazeNode.__getattribute__('index')] = True
        self.DFSSearchStack.append(mazeNode)
        visitingNdx = mazeNode.__getattribute__('index')

        for i in range(1, len(self.adjList[visitingNdx])):
            if not self.DFSVisitedStack[self.adjList[visitingNdx][i].__getattribute__('index')]:
                if not self.maze.__getattribute__('endNodeLoc') == self.adjList[visitingNdx][i].__getattribute__(
                        'coordinate'):
                    self.__DFSHelper(self.adjList[visitingNdx][i])

        while len(self.DFSSearchStack) > 0 and self.__isDeadEnd(
                self.DFSSearchStack[len(self.DFSSearchStack) - 1]) and not \
                self.endNode == self.DFSSearchStack[len(self.DFSSearchStack) - 1]:
            self.DFSSearchStack.pop()

    def BFS(self):

        self.BFSQueue.append(self.startNode)
        self.BFSBacktrack[self.startNode] = self.startNode

        while len(self.BFSQueue) > 0 and not self.endNode == self.BFSQueue[0]:

            visitingNode = self.BFSQueue[0]
            visitingNodeNdx = visitingNode.__getattribute__('index')

            for i in range(1, len(self.adjList[visitingNodeNdx])):

                neighbor = self.adjList[visitingNodeNdx][i]

                if not neighbor in self.BFSBacktrack:
                    self.BFSQueue.append(neighbor)
                    self.BFSBacktrack[neighbor] = visitingNode

            self.BFSQueue.pop(0)

    def Dijkstra(self):
        shortestPath = [10000000000 for i in range(0, len(self.adjList))]

        heap = []

        shortestPath[self.startNode.__getattribute__('index')] = 0

        heapq.heappush(heap, HeapPair(self.startNode.__getattribute__('index'), 0))

        while len(heap) > 0:

            minItem = heapq.heappop(heap)
            minItemNdx = minItem.__getattribute__('index')

            for i in self.adjList[minItemNdx]:

                j = i.__getattribute__('index')

                if (shortestPath[minItemNdx] + shortestPath[j]) < shortestPath[i.__getattribute__('index')]:
                    shortestPath[i.__getattribute__('index')] = j + shortestPath[minItemNdx]
                    heapq.heappush(heap, HeapPair(shortestPath[i.__getattribute__('index')], j))


        return shortestPath


    def drawNode(self, mazeNode):
        image = self.maze.__getattribute__('image')
        for i in range(mazeNode[0], mazeNode[0] + self.maze.__getattribute__('nodeSize')):
            for j in range(mazeNode[1], mazeNode[1] + self.maze.__getattribute__('nodeSize')):
                image[j][i][0] = 50
                image[j][i][1] = 50
                image[j][i][2] = 255

    def __isDeadEnd(self, mazeNode):
        visitingNdx = mazeNode.__getattribute__('index')
        for i in range(0, len(self.adjList[visitingNdx])):
            if not self.DFSVisitedStack[self.adjList[visitingNdx][i].__getattribute__('index')]:
                return False

        return True

    def __isNodeSeparated(self, mazeNode1, mazeNode2):
        image = self.maze.__getattribute__('image')

        if mazeNode1[0] == mazeNode2[0]:
            largerY = mazeNode1[1] if mazeNode1[1] > mazeNode2[1] else mazeNode2[1]
            smallerY = mazeNode2[1] if mazeNode1[1] > mazeNode2[1] else mazeNode1[1]
            xVal = mazeNode1[0]

            smallerY += self.maze.__getattribute__('nodeSize') + self.maze.__getattribute__('wallWidth')

            while smallerY < largerY:

                if self.__isNode([xVal, smallerY]):
                    return True

                smallerY += self.maze.__getattribute__('nodeSize') + self.maze.__getattribute__('wallWidth')

        elif mazeNode1[1] == mazeNode2[1]:
            largerX = mazeNode1[0] if mazeNode1[0] > mazeNode2[0] else mazeNode2[0]
            smallerX = mazeNode2[0] if mazeNode1[0] > mazeNode2[0] else mazeNode1[0]
            yVal = mazeNode1[1]

            smallerX += self.maze.__getattribute__('nodeSize') + self.maze.__getattribute__('wallWidth')

            while smallerX < largerX:

                if self.__isNode([smallerX, yVal]):
                    return True

                smallerX += self.maze.__getattribute__('nodeSize') + self.maze.__getattribute__('wallWidth')

        return False

    def __isWallSeparated(self, mazeNode1, mazeNode2):

        image = self.maze.__getattribute__('image')

        node1Coordinates = mazeNode1.__getattribute__('coordinate')
        node2Coordinates = mazeNode2.__getattribute__('coordinate')

        if node1Coordinates[0] == node2Coordinates[0]:

            greaterNode = node2Coordinates if node1Coordinates[1] < node2Coordinates[1] else node1Coordinates
            lesserNode = node1Coordinates if node1Coordinates != greaterNode else node2Coordinates
            yAxisCounter = lesserNode[1]

            while yAxisCounter < greaterNode[1]:
                if self.__getWalls([node1Coordinates[0], yAxisCounter])[
                    'down'] and yAxisCounter >= self.maze.__getattribute__('wallWidth'):
                    return True
                yAxisCounter += self.maze.__getattribute__('nodeSize') + self.maze.__getattribute__('wallWidth')

        elif node1Coordinates[1] == node2Coordinates[1]:

            greaterNode = node2Coordinates if node1Coordinates[0] < node2Coordinates[0] else node1Coordinates
            lesserNode = node1Coordinates if node1Coordinates != greaterNode else node2Coordinates
            xAxisCounter = lesserNode[0]

            while xAxisCounter < greaterNode[0]:
                if self.__getWalls([xAxisCounter, node1Coordinates[1]])[
                    'right'] and xAxisCounter >= self.maze.__getattribute__('wallWidth'):
                    return True
                xAxisCounter += self.maze.__getattribute__('nodeSize') + self.maze.__getattribute__('wallWidth')

        return False

    def __getWalls(self, node):
        image = self.maze.__getattribute__('image')
        leftIsWall = image[node[1]][node[0] - 1][0] == 0 and image[node[1]][node[0] - 1][1] == 0 and \
                     image[node[1]][node[0] - 1][2] == 0

        rightIsWall = image[node[1]][node[0] + self.maze.__getattribute__('nodeSize') + 1][0] == 0 and \
                      image[node[1]][node[0] + self.maze.__getattribute__('nodeSize') + 1][1] == 0 and \
                      image[node[1]][node[0] + self.maze.__getattribute__('nodeSize') + 1][2] == 0

        downIsWall = \
            image[node[1] + self.maze.__getattribute__('nodeSize') + self.maze.__getattribute__('wallWidth') - 1][
                node[0]][
                0] == 0 and \
            image[node[1] + self.maze.__getattribute__('nodeSize') + self.maze.__getattribute__('wallWidth') - 1][
                node[0]][
                1] == 0 and \
            image[node[1] + self.maze.__getattribute__('nodeSize') + self.maze.__getattribute__('wallWidth') - 1][
                node[0]][
                2] == 0

        upIsWall = image[node[1] - 1][node[0]][0] == 0 and image[node[1] - 1][node[0]][1] == 0 and \
                   image[node[1] - 1][node[0]][2] == 0

        return {'up': upIsWall, 'down': downIsWall, 'left': leftIsWall, 'right': rightIsWall}

    def __isNode(self, node):
        image = self.maze.__getattribute__('image')

        walls = self.__getWalls(node)

        isNode = (walls['left'] and walls['right'] and not walls['up'] and not walls['down']) or (
                walls['up'] and walls['down'] and not walls['left'] and not walls['right'])

        return not isNode
