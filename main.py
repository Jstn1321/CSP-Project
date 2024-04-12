#import all librarys
import matplotlib.pyplot as plt
import numpy as np
import random
import math
from gooey import Gooey, GooeyParser

#I used matplotlib for the graph and "gooey" for the gui.

#define GUI and ask for user input
@Gooey(program_name = "Traveling Salesman Problem", header_bg_color = "#017bfe")
def main():
    #define variables
    x = []
    y = []
    constX = []
    constY = []
    diff = []
    constDiff = []
    totalDistance = 0
    finalX = []
    finalY = []

    #Used https://www.youtube.com/watch?v=Szi8OgdWDWY to learn how to use the gooey library

    #ask for user input
    parser = GooeyParser()
    parser.add_argument("numPoints", action = "store", help = "How many random points would you like?", metavar = "Number of Points")
    parser.add_argument("minimum", action = "store", help = "Minimum range of possible points.", metavar = "Minimum range of Points")
    parser.add_argument("maximum", action="store", help="Maximum range of possible points", metavar="Maximum range of possible Points")
    group = parser.add_mutually_exclusive_group("Type of Algorithm")
    group.add_argument("--Random", action = "store_true", help = "Randomly Draws Lines to Random Points *REQUIRED TO PICK ONE*")
    group.add_argument("--Shortest", action="store_true", help="Finds the Shortest Distance Between Each Point *REQUIRED TO PICK ONE*")
    parser.add_argument("--pickStarting", action = "store_true", help = "Would you like to choose the starting point?", metavar = "Custom Starting Point?")
    parser.add_argument("--UserStarting", action="store", help="What is your custom starting points (index)? Leave blank if not applicable",metavar="Custom Start Point")
    args = parser.parse_args()

    #check if any varibles are empty and if they are give them a value so no error
    if args.UserStarting is None:
        args.UserStarting = 0
    if args.Random is None:
        args.Random = False
    if args.Shortest is None:
        args.Shortest = True

    #create a function to make random points given a min and a max
    def randomPoints(min, max):
        x = random.randint(min, max)
        y = random.randint(min, max)
        newpoint = [x, y]
        return newpoint

    #create a function that makes points according to user input
    def makeNewPoints(numberOfPoints):
        for o in range(numberOfPoints):
            plotPoints = (randomPoints(int(args.minimum), int(args.maximum)))
            if plotPoints[0] in x:
                numberOfPoints += 1
            if plotPoints[1] in y:
                numberOfPoints += 1
            else:
                x.append(plotPoints[0])
                y.append(plotPoints[1])
                constX.append(plotPoints[0])
                constY.append(plotPoints[1])

    #make random points and set the startpoint always equal to the first x and y pair of the list
    makeNewPoints(int(args.numPoints))
    startPoint = [x[0], y[0]]

    #if the user wants their own starting point then move their start point to the first index of the list
    if args.pickStarting == True:
        userStartValX = x[int(args.UserStarting)]
        userStartValY = y[int(args.UserStarting)]
        del x[int(args.UserStarting)]
        del y[int(args.UserStarting)]
        x.insert(0, userStartValX)
        y.insert(0, userStartValY)

    print("The start point is")
    print(startPoint)

    #function that uses the equation to find the distance between 2 x and y coordinates
    def distBetPoint(firstPoint, secondPoint):
        disX = (secondPoint[0] - firstPoint[0]) ** 2
        disY = (secondPoint[1] - firstPoint[1]) ** 2
        sum = disX + disY
        adistance = math.sqrt(sum)
        return adistance

    #function that compares the distance of the starting point to all other points in the x,y list
    def disAllPoints(startPoint, t):
        nextPoint = [x[t], y[t]]
        distance = distBetPoint(startPoint, nextPoint)
        return distance

    #finds the smallest index of a list
    def findSmallest(list):
        smallest = min(list)
        smallestIndex = list.index(smallest)
        return smallestIndex

    #first check if they want to use the "Shortest algorithm"
    if args.Shortest is True:
        #set final x and final y equal to the first term of the x, y list OR the start point
        finalX = [x[0]]
        finalY = [y[0]]
        #find the smallest distance between each and every point
        for k in range(0, len(x) - 1):
            for l in range(1, len(x)):
                #adds all distances to a list
                diff.append(disAllPoints(startPoint, l))
                constDiff.append(disAllPoints(startPoint, l))
            #find the smallest distance between points
            smallIndex = findSmallest(diff)
            smallDiffValue = diff[smallIndex]
            #finds the total distance
            totalDistance = totalDistance + smallDiffValue
            smallValueX = x[smallIndex + 1]
            finalX.append(smallValueX)
            smallValueY = y[smallIndex + 1]
            finalY.append(smallValueY)
            #organize list to map the line to the shortest point
            del x[0]
            del y[0]
            del x[smallIndex]
            del y[smallIndex]
            x.insert(0, smallValueX)
            y.insert(0, smallValueY)
            #reset startpoint
            startPoint = [x[0], y[0]]
            diff = []
        #finalX.append(constX[0])
        #finalY.append(constY[0])

    #check if the user wants a random algorithm
    if args.Random is True:
        #decalre final x and y as nothing
        finalX = []
        finalY = []
        #randomly organize the x and y list
        for j in range(0, len(x)):
            randIndex = random.randint(0, len(x) - 1)
            randXVal = x[randIndex]
            randYVal = y[randIndex]
            finalX.append(randXVal)
            finalY.append(randYVal)
            del x[randIndex]
            del y[randIndex]

        #finalX.append(constX[0])
        #finalY.append(constY[0])

        #find the distance of all the random points
        for p in range(0, len(finalX) - 1):
            if p + 1 > len(finalX):
                break
            else:
                distance = distBetPoint([finalX[p], finalY[p]], [finalX[p + 1], finalY[p + 1]])
                totalDistance = totalDistance + distance

        #reset x and y values

        x = constX
        y = constY


    print("TOTAL DISTANCE OF THE PATH IS:")
    print(totalDistance)
    print(constX)
    print(constY)


    #plot all points
    xpoints = np.array(finalX)
    ypoints = np.array(finalY)
    plt.plot(xpoints, ypoints, marker='o')
    plt.show()

main()

