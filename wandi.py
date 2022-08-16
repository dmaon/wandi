from collections import deque
import numpy as np
import cv2

class Wandi():
    def __init__(self):
        self.row = self.col = 0
        self.image = None

    def wandi(self, image, node, **options):

        # Init
        minVal = [0,0,0]

        isGray = False
        if ("isGray" in options):
            isGray = bool(options["isGray"])

        if ("min" in options):
            if (isGray):
                minVal = options["min"]
            else:
                minVal = list(options["min"])

        if (isGray):
            maxVal = 255
            if ("max" in options):
                maxVal = options["max"]
        else:
            maxVal = [255,255,255]
            if ("max" in options):
                maxVal = list(options["max"])

        dynamicThr = False
        if ("dynamicThr" in options):
            dynamicThr = bool(options["dynamicThr"])

        ds = [0, 0]
        if (dynamicThr):
            ds = list(options["ds"])

        sample = ds[:]
        sample = sample[0]

        grid = image.copy()
        
        layerColor = int(255/2) 
        if (not(isGray)):
            layerColor = [245,135,66]
        
        counter = 0
        counterFill = 0

        # Initializing a queue
        q = deque()
        
        # Add node to the end of Q.
        q.append(node)
        
        # Continue looping until Q is exhausted.
        while (len(q) > 0):
            # Set n equal to the first element of Q and Remove first element from Q.
            n = q.popleft()

            x = n[0]
            y = n[1]

            counter += 1

            ds[1] += 1 # Count
            if (dynamicThr):
                
                if (isGray):
                    # ravesh baraasi hamsaye va entekhab hamsaye be onvane meyare jadid
                    if ( self.checkIntensity(grid[x][y], int(ds[0])-10, int(ds[0])+10) and self.checkIntensity(grid[x][y], int(sample)-50, int(sample)+50) ):
                        ds[0] = grid[x][y]
                        minVal = int(ds[0])-30
                        maxVal = int(ds[0])+30
                else:
                    # ravesh baraasi hamsaye va entekhab hamsaye be onvane meyare jadid
                    if (self.checkRGB(grid[x][y], self.changeRGB(ds[0], -10), self.changeRGB(ds[0], +10))) and (self.checkRGB(grid[x][y], self.changeRGB(sample, -50), self.changeRGB(sample, +50))):
                        ds[0] = grid[x][y]
                        minVal = self.changeRGB(ds[0], -30)
                        maxVal = self.changeRGB(ds[0], 30)


            # If n is Inside
            if (isGray and self.checkIntensity(grid[x][y], minVal, maxVal)) or (not(isGray) and self.checkRGB(grid[x][y], minVal, maxVal)):

                # Set the n 
                grid[x][y] = layerColor
                counterFill += 1

                if not(isGray):
                    # Add the node to the north of n to the end of Q.
                    if (list(grid[self.setLimit(x-1, 0, "lower")][y]) != layerColor) and (self.setLimit(x-1, 0, "lower"), y) not in q:
                        q.append((self.setLimit(x-1, 0, "lower"), y))

                    # Add the node to the east of n to the end of Q.
                    if (list(grid[x][self.setLimit(y+1, grid.shape[1]-1, "upper")]) != layerColor) and (x, self.setLimit(y+1, grid.shape[1]-1, "upper")) not in q:
                        q.append((x, self.setLimit(y+1, grid.shape[1]-1, "upper")))

                    # Add the node to the south of n to the end of Q.
                    if (list(grid[self.setLimit(x+1, grid.shape[0]-1, "upper")][y]) != layerColor) and (self.setLimit(x+1, grid.shape[0]-1, "upper"), y) not in q:
                        q.append((self.setLimit(x+1, grid.shape[0]-1, "upper"), y))

                    # Add the node to the west of n to the end of Q.
                    if (list(grid[x][self.setLimit(y-1, 0, "lower")]) != layerColor) and (x, self.setLimit(y-1, 0, "lower")) not in q:
                        q.append((x, self.setLimit(y-1, 0, "lower")))
                else:
                    # Add the node to the north of n to the end of Q.
                    if ((grid[self.setLimit(x-1, 0, "lower")][y]) != layerColor) and (self.setLimit(x-1, 0, "lower"), y) not in q:
                        q.append((self.setLimit(x-1, 0, "lower"), y))

                    # Add the node to the east of n to the end of Q.
                    if ((grid[x][self.setLimit(y+1, grid.shape[1]-1, "upper")]) != layerColor) and (x, self.setLimit(y+1, grid.shape[1]-1, "upper")) not in q:
                        q.append((x, self.setLimit(y+1, grid.shape[1]-1, "upper")))

                    # Add the node to the south of n to the end of Q.
                    if ((grid[self.setLimit(x+1, grid.shape[0]-1, "upper")][y]) != layerColor) and (self.setLimit(x+1, grid.shape[0]-1, "upper"), y) not in q:
                        q.append((self.setLimit(x+1, grid.shape[0]-1, "upper"), y))

                    # Add the node to the west of n to the end of Q.
                    if ((grid[x][self.setLimit(y-1, 0, "lower")]) != layerColor) and (x, self.setLimit(y-1, 0, "lower")) not in q:
                        q.append((x, self.setLimit(y-1, 0, "lower")))
        # Return
        return grid


    # Check color range
    def checkRGB(self, sample, minVal, maxVal):
        if (
            int(minVal[0]) <= int(sample[0]) and int(sample[0]) <= int(maxVal[0]) and
            int(minVal[1]) <= int(sample[1]) and int(sample[1]) <= int(maxVal[1]) and
            int(minVal[2]) <= int(sample[2]) and int(sample[2]) <= int(maxVal[2])
        ):
            return True
        return False


    # Check color range
    def checkIntensity(self, sample, minVal, maxVal):
        if (
            int(minVal) <= int(sample) and int(sample) <= int(maxVal)
        ):
            return True
        return False


    # set limit for values
    def setLimit(self, value, limit, type):
        if (type == "upper" and value > limit) or (type == "lower" and value < limit):
            value = limit
        return value
            

    # Get kernel and return lighter and darker color by BGR 
    def minMaxBGR(self, kernel):
        brightness = {}

        for item in kernel:
            for color in item:
                brightness[str(color)] = (color, self.intensity(color))
        
        brightness = dict(sorted(brightness.items(), key=lambda item: item[1][1], reverse=False))

        return brightness


    # Change color range
    def changeRGB(self, sample, value):
        arr = [int(sample[0])+int(value), int(sample[1])+int(value), int(sample[2])+int(value)]
        return arr


    # Get color intensity
    def intensity(self, color):
        return (((color[2] * 299) + (color[1] * 587) + (color[0] * 114)) / 1000)


    # Get 
    def getMin(self, val1, val2, minCheck=True):
        result = val1
        if (minCheck and (self.intensity(val2) < self.intensity(val1))) or (minCheck == False and (self.intensity(val2) > self.intensity(val1))):
            result = val2
        return result








# test = Wandi()
# test.x = 2
# test.y = 4
# print(test.get_xy())