class MazeNode:
    def __init__(self, coordinate, index):
        self.coordinate = coordinate
        self.index = index

    def __eq__(self, other):
        return self.coordinate[0] == other.coordinate[0] and \
               self.coordinate[1] == other.coordinate[1] and \
               self.index == other.index

    def __str__(self):
        return "coordinate: (x: " + str(self.coordinate[0]) + ", y: " + str(self.coordinate[1]) + ") index " + str(self.index)


class MazeGraph:
    def __init__(self, maze):
        self.adjList = []
        self.maze = maze
        self.DFSSearchStack = []
        self.DFSVisitedStack = []
        self.DFSFound = False
        self.edgeCount = 0

        self.adjList.append([MazeNode(maze.__getattribute__('startNodeLoc'), 0)])
        self.adjList.append([MazeNode(maze.__getattribute__('endNodeLoc'), 1)])

        nodeLengthItr = maze.__getattribute__('wallWidth')
        while nodeLengthItr < maze.__getattribute__('length'):
            nodeWidthItr = maze.__getattribute__('wallWidth')
            while nodeWidthItr < maze.__getattribute__('width'):

                if self.__isNode([nodeLengthItr, nodeWidthItr]) and \
                        self.adjList[0][0].__getattribute__('coordinate') != [nodeLengthItr, nodeWidthItr] and \
                        self.adjList[1][0].__getattribute__('coordinate') != [nodeLengthItr, nodeWidthItr]:
                    self.adjList.append([MazeNode([nodeLengthItr, nodeWidthItr], len(self.adjList))])

                nodeWidthItr += maze.__getattribute__('nodeSize') + maze.__getattribute__('wallWidth')

            nodeLengthItr += maze.__getattribute__('nodeSize') + maze.__getattribute__('wallWidth')

        for i in range(0, len(self.adjList)):
            for j in range(0, len(self.adjList)):
                if i != j and \
                        (self.adjList[i][0].__getattribute__('coordinate')[0] ==
                         self.adjList[j][0].__getattribute__('coordinate')[0] or
                         self.adjList[i][0].__getattribute__('coordinate')[1] ==
                         self.adjList[j][0].__getattribute__('coordinate')[1]) and not \
                        self.__isWallSeparated(self.adjList[i][0], self.adjList[j][0]) and not \
                        self.__isNodeSeparated(self.adjList[i][0], self.adjList[j][0]):
                    self.__addEdge(self.adjList[i][0], self.adjList[j][0])

        self.DFSVisitedStack = [False for i in range(len(self.adjList))]

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

    def DFS(self, mazeNode):

        self.DFSVisitedStack[mazeNode.__getattribute__('index')] = True
        self.DFSSearchStack.append(mazeNode)
        visitingNdx = mazeNode.__getattribute__('index')

        for i in range(0, len(self.adjList[visitingNdx])):
            if not self.DFSVisitedStack[self.adjList[visitingNdx][i].__getattribute__('index')]:
                if not self.adjList[1][0] == self.adjList[visitingNdx][i]:
                    self.DFS(self.adjList[visitingNdx][i])

        while len(self.DFSSearchStack) > 0 and self.__isDeadEnd(self.DFSSearchStack[len(self.DFSSearchStack) - 1]):
            self.DFSSearchStack.pop()


    def BFS(self):
        print("BFS")

    def Dijkstra(self):
        print("Do dijkstra")

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

        if mazeNode1.__getattribute__('coordinate')[0] == mazeNode2.__getattribute__('coordinate')[0]:
            xCoord = mazeNode1.__getattribute__('coordinate')[0]
            for i in range(0, len(self.adjList)):
                currCoord = self.adjList[i][0].__getattribute__('coordinate')
                if mazeNode1.__getattribute__('coordinate')[1] < mazeNode2.__getattribute__('coordinate')[1]:
                    if currCoord[0] == xCoord and currCoord[1] > mazeNode1.__getattribute__('coordinate')[1] and currCoord[1] < mazeNode2.__getattribute__('coordinate')[1]:
                        return True
                elif currCoord[0] == xCoord and currCoord[1] < mazeNode1.__getattribute__('coordinate')[1] and currCoord[1] > mazeNode2.__getattribute__('coordinate')[1]:
                    return True
        elif mazeNode1.__getattribute__('coordinate')[1] == mazeNode2.__getattribute__('coordinate')[1]:
            yCoord = mazeNode1.__getattribute__('coordinate')[1]
            for i in range(0, len(self.adjList)):
                currCoord = self.adjList[i][0].__getattribute__('coordinate')
                if mazeNode1.__getattribute__('coordinate')[0] < mazeNode2.__getattribute__('coordinate')[0]:
                    if currCoord[1] == yCoord and currCoord[0] > mazeNode1.__getattribute__('coordinate')[0] and currCoord[0] < mazeNode2.__getattribute__('coordinate')[0]:
                        return True
                elif currCoord[1] == yCoord and currCoord[0] < mazeNode1.__getattribute__('coordinate')[0] and currCoord[0] > mazeNode2.__getattribute__('coordinate')[0]:
                    return True

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
                if self.__getWalls([node1Coordinates[0], yAxisCounter])['down'] and yAxisCounter >= self.maze.__getattribute__('wallWidth'):
                    return True
                yAxisCounter += self.maze.__getattribute__('nodeSize') + self.maze.__getattribute__('wallWidth')

        elif node1Coordinates[1] == node2Coordinates[1]:

            greaterNode = node2Coordinates if node1Coordinates[0] < node2Coordinates[0] else node1Coordinates
            lesserNode = node1Coordinates if node1Coordinates != greaterNode else node2Coordinates
            xAxisCounter = lesserNode[0]

            while xAxisCounter < greaterNode[0]:
                if self.__getWalls([xAxisCounter, node1Coordinates[1]])['right'] and xAxisCounter >= self.maze.__getattribute__('wallWidth'):
                    return True
                xAxisCounter += self.maze.__getattribute__('nodeSize') + self.maze.__getattribute__('wallWidth')

        return False

    def __getWalls(self, node):
        image = self.maze.__getattribute__('image')
        leftIsWall = image[node[1]][node[0] - 1][0] == 0 and \
                     image[node[1]][node[0] - 1][1] == 0 and \
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

        upIsWall = image[node[1] - 1][node[0]][0] == 0 and \
                   image[node[1] - 1][node[0]][1] == 0 and \
                   image[node[1] - 1][node[0]][2] == 0

        return {'up' : upIsWall, 'down' : downIsWall, 'left' : leftIsWall, 'right' : rightIsWall}

    def __isNode(self, node):
        image = self.maze.__getattribute__('image')

        walls = self.__getWalls(node)

        isNode = (walls['left'] and walls['right'] and not walls['up'] and not walls['down']) or (walls['up'] and walls['down'] and not walls['left'] and not walls['right'])

        return not isNode
