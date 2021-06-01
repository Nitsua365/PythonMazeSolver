import math

class Maze:
    def __init__(self, MazeImage):
        self.image = MazeImage
        self.length = MazeImage.shape[1]
        self.width = MazeImage.shape[0]
        self.wallWidth = self.length
        wallThicknessProbeInterval = math.floor(self.length / 10)
        i = wallThicknessProbeInterval
        while i < self.length:
            countWallPixelDensity = 0
            while i < self.length and countWallPixelDensity < math.floor(self.width / 2) and self.image[countWallPixelDensity][i][0] == 0 and self.image[countWallPixelDensity][i][1] == 0 and self.image[countWallPixelDensity][i][2] == 0:
                countWallPixelDensity += 1

            if countWallPixelDensity < self.wallWidth and countWallPixelDensity != 0:
                self.wallWidth = countWallPixelDensity

            i += wallThicknessProbeInterval

        self.nodeSize = 0

        self.startLocArray = []
        for i in range(0, self.wallWidth):
            for j in range(0, self.length):

                if self.image[i][j][0] == 255 and self.image[i][j][1] == 255 and self.image[i][j][2] == 255:
                    self.image[i][j][0] == 255
                    self.image[i][j][1] == 0
                    self.image[i][j][2] = 0
                    self.startLocArray.append([i, j])

                    if i == 0:
                        self.nodeSize += 1

        self.startNodeLoc = [self.startLocArray[0][1], self.startLocArray[0][0] + self.wallWidth]

        self.endLocArray = []
        for i in range(0, self.wallWidth):
            for j in range(0, self.length):
                if self.image[(self.width - 1) - i][j][0] == 255 and self.image[(self.width - 1) - i][j][1] == 255 and self.image[(self.width - 1) - i][j][2] == 255:
                    self.image[(self.width - 1) - i][j][0] == 255
                    self.image[(self.width - 1) - i][j][1] == 0
                    self.image[(self.width - 1) - i][j][2] = 0
                    self.endLocArray.append([(self.width - 1) - i, j])

        self.endNodeLoc = [self.endLocArray[0][1], self.endLocArray[0][0] - self.wallWidth - self.nodeSize + 1]

    def __str__(self):
        mazeString = "Maze Stats:\nwidth: " + str(self.width) + "\nlength: " + str(self.length) + "\nmazeShape: " + str(self.image.shape)
        return (mazeString)