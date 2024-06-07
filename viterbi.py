import numpy as np
import sys

#read input file and return seperated data of given inputs

### CHANGE FILE INPUT WHEN DONE TESTING ###

def readInputFile():

    with open("inputFile.txt", "r") as inputFile:

        #write map size to tuple
        mapSize = tuple(map(int,inputFile.readline().split()))
        
        #make numpy array of zeros and input X points as 1 and count x points. Also add points to stateSpace array
        mapData = np.zeros(mapSize)

        stateSpace = []

        for i in range(mapSize[0]):
            elements = inputFile.readline().split()

            for j in range(mapSize[1]):
                if elements[j] == "X":
                    mapData[i,j] = 1
                else:
                    stateSpace.append([i,j])
                    
        #pad border with 1s (CHECK IF NEEDED)
        #mapData = np.pad(mapData, (1,1), mode='constant', constant_values=(1,1))

        #read number of sensor observations as int
        numberObservations = int(inputFile.readline())

        #create ordered list of observation strings
        observationList = []
        for i in range(numberObservations):
            observationList.append(inputFile.readline().split())
        
        #read and write sensor error rate as float
        errorRate = float(inputFile.readline())
        
    return(mapSize,mapData, stateSpace, observationList, errorRate)

#print test
a,b,c,d,e,f = readInputFile()
print(c)
print(len(c))


#OBSERVATION SPACE - Any possible observation eg 0000 0011 1101 ect - N = 4^2 observation possibilites

#STATE SPACE - Any traversable (not 0) space on the map. K is size of state space
#created when reading file - index starts at 0

#ARRAY OF INIT PROBS - array displaying probability each point could be the starting point. each traversable point has equal probability 1/k, non traversable have prob 0
#Getting probability array, look into incresing accuracy of Floating points

def initialProbabilitiesArray(mapSize,stateSpace):
    
    numTraversablePoints = len(stateSpace)
    
    startingProbability = 1/numTraversablePoints
    IPArray = np.zeros(mapSize)

    for i in stateSpace:
        x,y = i
        IPArray[x,y] = startingProbability

    return IPArray

#SEQUENCE OF OBSERVATIONS - Number of observations taken (observation list - size T)


#TRANSITION MATRIX - K x K matrix of probability that each point will move to another point in one move eg 1000 obs 100 prob will move North, 1100 50 prob move North 50 prob move south

def transitionMatrix(stateSpace, mapData):
    t
    
#EMISSION MATRIX - K x N matrix. made specificallt for each position

def viterbiFowardAlgorithm(stateSpace, initialProbabilitiesArray, observationList):

    K = len(stateSpace)
    T = len(observationList)

    trellisMatrix = np.zeros(K,T)
    
    for i in K:
        trellisMatrix[i,1] = 