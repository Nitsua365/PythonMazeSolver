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

        self.adjList.append([MazeNode(maze.__getattribute__('startNodeLoc'), 0)])
        self.adjList.append([MazeNode(maze.__getattribute__('endNodeLoc'), 1)])


        nodeWidthItr = maze.__getattribute__('wallWidth')
        while nodeWidthItr < maze.__getattribute__('width'):
            nodeLengthItr = maze.__getattribute__('wallWidth')
            while nodeLengthItr < maze.__getattribute__('length'):

                if self.__isNode([nodeWidthItr, nodeLengthItr]) and \
                        self.adjList[0][0].__getattribute__('coordinate') != [nodeLengthItr, nodeWidthItr] and \
                        self.adjList[1][0].__getattribute__('coordinate') != [nodeLengthItr, nodeWidthItr]:
                    self.adjList.append([MazeNode([nodeLengthItr, nodeWidthItr], len(self.adjList))])

                nodeLengthItr += maze.__getattribute__('nodeSize') + maze.__getattribute__('wallWidth')

            nodeWidthItr += maze.__getattribute__('nodeSize') + maze.__getattribute__('wallWidth')

        for i in range(0, len(self.adjList)):
            for j in range(0, len(self.adjList)):
                if i != j and \
                        (self.adjList[i][0].__getattribute__('coordinate')[0] ==
                         self.adjList[j][0].__getattribute__('coordinate')[0] or
                         self.adjList[i][0].__getattribute__('coordinate')[1] ==
                         self.adjList[j][0].__getattribute__('coordinate')[1]) and not \
                        self.__isWallSeparated(self.adjList[i][0], self.adjList[j][0]) and not \
                        self.__isNodeSeparated(self.adjList[i][0], self.adjList[j][0]):
                    self.addEdge(self.adjList[i][0], self.adjList[j][0])

        self.DFSVisitedStack = [False for i in range(len(self.adjList))]

        for i in range(0, len(self.adjList)):
            for j in range(0, len(self.adjList[i])):
                print(self.adjList[i][j].__str__())
            print()

    def addEdge(self, node1, node2):
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


    def __isDeadEnd(self, mazeNode):
        visitingNdx = mazeNode.__getattribute__('index')
        for i in range(0, len(self.adjList[visitingNdx])):
            if not self.DFSVisitedStack[self.adjList[visitingNdx][i].__getattribute__('index')]:
                return False

        return True


    def drawNode(self, mazeNode):
        image = self.maze.__getattribute__('image')
        coordinate = mazeNode.__getattribute__('coordinate')
        for i in range(coordinate[0], coordinate[0] + self.maze.__getattribute__('nodeSize')):
            for j in range(coordinate[1], coordinate[1] + self.maze.__getattribute__('nodeSize')):
                image[j][i][0] = 50
                image[j][i][1] = 50
                image[j][i][2] = 255

    def BFS(self):
        print("BFS")

    def Dijkstra(self):
        print("Do dijkstra")

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

        if mazeNode1.__getattribute__('coordinate')[0] == mazeNode2.__getattribute__('coordinate')[0]:
            if mazeNode1.__getattribute__('coordinate')[1] < mazeNode2.__getattribute__('coordinate')[1]:
                node1Coordinates = mazeNode1.__getattribute__('coordinate')
                node2Coordinates = mazeNode2.__getattribute__('coordinate')
                yAxisCounter = node1Coordinates[1]
                while yAxisCounter <= node2Coordinates[1]:
                    if yAxisCounter != node1Coordinates[1] and yAxisCounter > self.maze.__getattribute__('wallWidth') and \
                            image[yAxisCounter - 1][node1Coordinates[0]][0] == 0 and \
                            image[yAxisCounter - 1][node1Coordinates[0]][1] == 0 and \
                            image[yAxisCounter - 1][node1Coordinates[0]][2] == 0:
                        return True

                    yAxisCounter += self.maze.__getattribute__('nodeSize') + self.maze.__getattribute__('wallWidth')
            else:
                node1Coordinates = mazeNode1.__getattribute__('coordinate')
                node2Coordinates = mazeNode2.__getattribute__('coordinate')
                yAxisCounter = node1Coordinates[1]
                while yAxisCounter <= node1Coordinates[1]:
                    if yAxisCounter > self.maze.__getattribute__('wallWidth') and \
                            image[yAxisCounter - 1][node2Coordinates[0]][0] == 0 and \
                            image[yAxisCounter - 1][node2Coordinates[0]][1] == 0 and \
                            image[yAxisCounter - 1][node2Coordinates[0]][2] == 0:
                        return True

                    yAxisCounter += self.maze.__getattribute__('nodeSize') + self.maze.__getattribute__('wallWidth')
        elif mazeNode1.__getattribute__('coordinate')[1] == mazeNode2.__getattribute__('coordinate')[1]:
            if mazeNode1.__getattribute__('coordinate')[0] < mazeNode2.__getattribute__('coordinate')[0]:
                node1Coordinates = mazeNode1.__getattribute__('coordinate')
                node2Coordinates = mazeNode2.__getattribute__('coordinate')
                xAxisCounter = node1Coordinates[0]
                while xAxisCounter <= node2Coordinates[0]:
                    if xAxisCounter != node1Coordinates[0] and xAxisCounter > self.maze.__getattribute__('wallWidth') and \
                            image[node1Coordinates[1]][xAxisCounter - 1][0] == 0 and \
                            image[node1Coordinates[1]][xAxisCounter - 1][
                                1] == 0 and image[node1Coordinates[1]][xAxisCounter - 1][2] == 0:
                        return True

                    xAxisCounter += self.maze.__getattribute__('nodeSize') + self.maze.__getattribute__('wallWidth')

            else:
                node1Coordinates = mazeNode1.__getattribute__('coordinate')
                node2Coordinates = mazeNode2.__getattribute__('coordinate')
                xAxisCounter = node2Coordinates[0]
                while xAxisCounter <= node1Coordinates[0]:
                    if xAxisCounter > self.maze.__getattribute__('wallWidth') and \
                            image[node2Coordinates[1]][xAxisCounter - 1][0] == 0 and \
                            image[node2Coordinates[1]][xAxisCounter - 1][
                                1] == 0 and image[node1Coordinates[1]][xAxisCounter - 1][2] == 0:
                        return True

                    xAxisCounter += self.maze.__getattribute__('nodeSize') + self.maze.__getattribute__('wallWidth')

        return False

    def __isNode(self, node):
        image = self.maze.__getattribute__('image')
        leftIsWall = image[node[0]][node[1] - 1][0] == 0 and \
                     image[node[0]][node[1] - 1][1] == 0 and \
                     image[node[0]][node[1] - 1][2] == 0

        rightIsWall = image[node[0]][node[1] + self.maze.__getattribute__('nodeSize') + 1][0] == 0 and \
                      image[node[0]][node[1] + self.maze.__getattribute__('nodeSize') + 1][1] == 0 and \
                      image[node[0]][node[1] + self.maze.__getattribute__('nodeSize') + 1][2] == 0

        downIsWall = \
        image[node[0] + self.maze.__getattribute__('nodeSize') + self.maze.__getattribute__('wallWidth') - 1][node[1]][
            0] == 0 and \
        image[node[0] + self.maze.__getattribute__('nodeSize') + self.maze.__getattribute__('wallWidth') - 1][node[1]][
            1] == 0 and \
        image[node[0] + self.maze.__getattribute__('nodeSize') + self.maze.__getattribute__('wallWidth') - 1][node[1]][
            2] == 0

        upIsWall = image[node[0] - 1][node[1]][0] == 0 and \
                   image[node[0] - 1][node[1]][1] == 0 and \
                   image[node[0] - 1][node[1]][2] == 0

        if (leftIsWall and rightIsWall and not upIsWall and not downIsWall) or (upIsWall and downIsWall and not leftIsWall and not rightIsWall):
            return False
        else:
            return True
