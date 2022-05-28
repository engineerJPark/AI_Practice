import time
from NQueens import *

def testRandomStarts(alg, reps, sizeList):
    """Run this on hillClimb, stochHillClimb, and simAnnealing only.
    Takes in a function name for one of the local search functions.
    It also has optional inputs for a number of repetitions and list
    of sizes to test. It runs reps tests for each size, and prints the results."""
    allResults = {}
    for siz in sizeList:
        print("testing size", siz)
        allResults[siz] = []
        print("..........processing.............")
        #input으로 받은 reps 만큼 loop
        for rep in range(reps):
            startState = NQueens(siz)
            startTime = time.time()
            result = alg(startState, False)
            endTime = time.time()
            result = list(result)
            result.append(endTime-startTime)
            allResults[siz].append(result)
    print("==================================")
    print("Running tests on", alg)
    for siz in sizeList:
        print("---------------")
        print("Test results for size ", siz)
        runs = allResults[siz]
        for i in range(len(runs)):
            [lastVal, maxVal, count, deltaTime] = runs[i]
            print("Test ", i+1, ": value = ", lastVal, "out of", maxVal, "count = ", count, " time = {:.5f}".format(deltaTime))

# todo:
def testVaryingPops(alg, popSize, reps, sizeList):
    """Run this on beam search and GA only. Takes in a function name for one
    of the local search functions, and a population size. It
    also has an optional input a number of repetitions. This runs the given
    algorithm with the specified population size. Does
    run reps tests and prints the results."""
    allResults = {}
    for siz in sizeList:
        print("testing size", siz)
        print("...........processing.............")
        allResults[siz] = []
        for rep in range(reps):
            startTime = time.time()
            result = alg(siz, False, popSize)
            endTime = time.time()
            result = list(result)
            result.append(endTime-startTime)
            allResults[siz].append(result)
    print("==================================")
    print("Running tests on", alg)
    for siz in sizeList:
        print("---------------")
        print("Size =", siz)
        runs = allResults[siz]
        for i in range(len(runs)):
            [lastVal, maxVal, count, deltaTime] = runs[i]
            print("Test", i+1, ": value =", lastVal, "out of", maxVal, "count =", count, "time = {:.5f}".format(deltaTime))
           
            

