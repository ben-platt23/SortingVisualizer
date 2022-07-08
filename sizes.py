# Author: Ben Platt
# Last Updated: 07/05/2022
# This program generates and returns a randomly sorted list of sizes for the drawn rectangles

import random


# Generate random list of 500 lengths of rectangles from 0 to whatever
def generateSizes():
    sizes = []
    sizeMin = 300
    sizeMax = 800
    stepSize = 4
    for i in range(sizeMin, sizeMax, stepSize):
        sizes.append(i+1)
    random.shuffle(sizes)
    return sizes
