import numpy as np
import matplotlib.pyplot as plt
import random

class Node:
    def __init__(self,idx):
        self.idx = idx
        self.x = np.random.uniform()
        self.y = np.random.uniform()
        self.p = 0.5 # Probability of having the new node in red color
        self.k = 1.0 # Coefficient of the cost of own effort
        self.f = 8.0 # Coefficient of the reward from own effort
        self.ownEffort = 10 #random.uniform(1.0,10.0)
        self.otherEffort = 10 #random.uniform(1.0,10.0)
        if random.random() < self.p:
            self.color = 'r' # Red = in need
            self.initiallyRed = True
        else:
            self.color = 'b' # Blue = not in need
            self.initiallyRed = False

    def calcReturn(self):
        return (-0.5*self.k*self.ownEffort**2 + self.f*self.ownEffort)

    def evalExpectation(self,numBluesAround):
        return numBluesAround * self.otherEffort

    def decideToHelp(self,numBluesAround):
        return (self.evalExpectation(numBluesAround) < self.calcReturn()) # True if we help

class World:
    def __init__(self,radius):
        self.dictofnodes = {}
        self.bluenodestocheck = {}
        self.currentidx=0
        self.radius = radius

    def createNewNode(self):
        NewNode = Node(self.currentidx)
        if NewNode.color == 'r':
            self.checkProximityRed(NewNode)
        for tuple in self.bluenodestocheck.items():
            # tuple[0] = idx , tuple[1] = node
            numBluesAround = self.checkProximityBlue(NewNode)
            if self.dictofnodes[tuple[0]].decideToHelp(numBluesAround):
                NewNode.color = 'b'
        self.bluenodestocheck = {}
        self.dictofnodes[self.currentidx] = NewNode
        self.currentidx += 1

    def checkProximityRed(self,node):
        # check surroundings
        for t in self.dictofnodes.items():
            distance = np.sqrt((t[1].x-node.x)**2+(t[1].y-node.y)**2)
            if (distance < self.radius and t[1].color == 'b'):
                self.bluenodestocheck[t[0]] = t[1]

    def checkProximityBlue(self,node):
        counter = 0.0
            # Evaluate expectation considering other blues
        for t in self.dictofnodes.items():
            distance = np.sqrt((t[1].x-node.x)**2+(t[1].y-node.y)**2)
            if (distance < self.radius and t[1].color == 'b'):
                counter += 1.0
        return counter # TODO Check if this is legal in python

def main():
    # Give parameters
    radius = 0.2 # The whole world is scaled between 0 and 1
    numNodes = 200
    world = World(radius)
    sumHelped = 0
    steptracker = []

    for i in range(numNodes):
        world.createNewNode()
        print("Generating node:", world.dictofnodes[i].idx)
        x = world.dictofnodes[i].x
        y = world.dictofnodes[i].y
        plot1 = plt.figure(1)
        plt.title("Red: Needs Help, Blue: Might consider to help")
        plt.xlim((0,1))
        plt.ylim((0,1))
        if world.dictofnodes[i].initiallyRed:
            plt.scatter(x, y, c = 'r')
            plt.pause(0.0005)
            if world.dictofnodes[i].color == 'b':
                plt.pause(0.0005)
                sumHelped += 1
        plt.scatter(x, y, c = world.dictofnodes[i].color)
        plt.pause(0.0005)
        steptracker.append((i,sumHelped))
        plot2 = plt.figure(2)
        plt.title("Course of conversion")
        plt.xlabel("Population")
        plt.ylabel("Conversions")
        plt.plot(*zip(*steptracker))
    plt.show()
    
if __name__ == '__main__':
    main()
