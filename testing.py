import numpy as np
import sys

#read input file and return seperated data of given inputs

### CHANGE FILE INPUT WHEN DONE TESTING ###

def readInputFile():

    with open("inputFile2.txt", "r") as inputFile:

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
                    

        #read number of sensor observations as int
        numberObservations = int(inputFile.readline())

        #create ordered list of observation strings
        observationList = []
        for i in range(numberObservations):
            
            s = (str(inputFile.readline())).strip()
            observationList.append(s)
            
        
        #read and write sensor error rate as float
        errorRate = float(inputFile.readline())
        
    return(mapData, stateSpace, observationList, errorRate, mapSize)

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

def initialProbability(stateSpace):

    numTraversablePoints = len(stateSpace)
    startingProbability = 1/numTraversablePoints
    return startingProbability

#SEQUENCE OF OBSERVATIONS - Number of observations taken (observation list - size T)


#TRANSITION MATRIX - K x K matrix of probability that each point will move to another point in one move eg 1000 obs 100 prob will move North, 1100 50 prob move North 50 prob move south
    
#EMISSION MATRIX - K x N matrix. made specificallt for each position

#take in two binary numbers and count inconsistent bits
def countMismatchBits(s1,s2):
    count = 0
    for i in range(4):
        if s1[i] != s2[i]:
            count += 1
    
    return count
    

#take map, current state and observation and return number of incorect bits 
def getIncorrectValues(mapData, state, observation):

    x,y = state
    N = str(int(mapData[x-1,y]))
    S = str(int(mapData[x+1,y]))
    W = str(int(mapData[x,y-1]))
    E = str(int(mapData[x,y+1]))

    neighboursString = N + S + W + E

    return countMismatchBits(neighboursString,observation)
   
#take inputs and create KxT emisson matrix, then return
def createEmissionMatrix(mapData, stateSpace, observationList, errorRate,K,T):

    ER = errorRate

    emissionMatrix = np.zeros([K,T])

    i = 0
    j = 0

    for state in stateSpace:

        for observation in observationList:
            dit = getIncorrectValues(mapData,state,observation)
            emissionMatrix[i,j] = pow(1-ER,4-dit) * pow(ER, dit)
            j += 1
        j = 0    
        i += 1 
            
    return emissionMatrix

#transition matrix
def createTransitionMatrix(K, stateSpace, mapData):
    transitionMatrix = np.zeros([K,K])

    #iterate over transition matrix

    for i in stateSpace:
        for j in stateSpace:
            
            #if not comparing to itself
            if i != j:

                x,y = j
                #check neighbour values
                N = int(mapData[x-1,y])
                S = int(mapData[x+1,y])
                W = int(mapData[x,y-1])
                E = int(mapData[x,y+1])

                #total neightbours
                neighbours = 4-N-S-W-E

                if neighbours == 0:
                    prob = 0
                #split probability between neighbours
                else:
                    prob = 1/neighbours
                
                # set neighbours value in table to 
                if N == 0:
                    transitionMatrix[x,y-1] = prob
                if S ==0:
                    transitionMatrix[x,y+1] = prob
                if W == 0:
                    transitionMatrix[x-1,y] = prob
                if E == 0:
                    transitionMatrix[x+1,y] = prob

    return transitionMatrix
 
def viterbiFowardAlgorithm(mapData,stateSpace,observationList,errorRate):

    K = len(stateSpace)
    T = len(observationList)

    Em = createEmissionMatrix(mapData,stateSpace,observationList,errorRate,K,T)
    Tm = createTransitionMatrix(K,stateSpace,mapData)

    trellisMatrix = np.zeros([K,T])

    for i in range(K):
        trellisMatrix[i,0] = initialProbability(stateSpace) * Em[i,1] ## CHECK NUMS

    for j in range(1,T):

        for i in range(K):

            trellisCol = trellisMatrix[:,j-1]
            TransCol = Tm[:,i]
            PriorProb = trellisCol*TransCol
            trellisMatrix[i,j] = np.max(PriorProb) * Em[i,j]
    
            

    return(trellisMatrix)


#main file

#read input
mapData, stateSpace, observationList, errorRate, mapSize= readInputFile()

#pad border with 1s (CHECK IF NEEDED)
paddedMapData = np.pad(mapData, (1,1), mode='constant', constant_values=(1,1))

#create trellis matrix using input data
trellisMatrix = viterbiFowardAlgorithm(paddedMapData,stateSpace,observationList,errorRate)

numberObservations = len(observationList)

outputMap = np.zeros(mapSize)

maps= []

for obsRow in range(numberObservations):
    outputMap = np.zeros(mapSize)
    trellisCount = 0
    for i in range(mapSize[0]):
        
        for j in range(mapSize[1]):

            if mapData[i,j] == 0:
                outputMap[i,j] = trellisMatrix[trellisCount, obsRow]
                trellisCount += 1
    
    maps.append(outputMap)

np.savez("output.npz", *maps)
             





