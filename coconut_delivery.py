#!/usr/bin/python3

import sys
import os.path

# Small class to hold JetStream data
class JetStream:
    def __init__(self, start, end, energy):
        self.__start = start
        self.__end = end
        self.__energy = energy

        self.predecessor = None
        self.pathEnergy = sys.maxsize

    def getStart(self): return self.__start
    def getEnd(self): return  self.__end
    def getEnergy(self): return self.__energy

    def __str__(self):
        return (self.__start, self.__end, self.__energy, self.pathEnergy).__str__()

    def __repr__(self):
        return (self.__start, self.__end, self.__energy, self.pathEnergy).__str__()

class CoconutDelivery:
    """
    The Coconut Delivery problem can be characterized as a single pair,
    shortest path problem on a directed, acyclic graph.
    This problem can be solved in several different ways.
    Here is an implementation using a simple BFS-like traversal
    and also using Dijkstra
    """

    def __init__(self, pathsFile):
        self.pathsFile = pathsFile
        self.jetStreamList = []
        self.adjacencyList = { }
        self.defaultPathCost = 0
        self.lastMile = 0
        self.minEnergy = sys.maxsize
        self.minPath = None
        self.firstJetStreams = []

    def findShortestPath(self):
        """ Find the shortest path using the jet stream file given"""

        if not self._readPathsFile():
            return False

        #self._bfsMethod()
        self._dijkstra()

        # Print the results
        print(self.minEnergy)
        print(self.minPath)

        return True

    def _dijkstra(self):
        """Implementation of Dijkstra's algorithm using a sorted list of nodes
        to compute a shortest path between a pair of nodes"""

        # Choose a source
        source = self.firstJetStreams[0]

        # Create our priority queue of pathLength
        self.jetStreamList.sort(key=lambda x: x.pathEnergy, reverse=True)

        while len(self.jetStreamList) > 0:
            node = self.jetStreamList.pop()
            i = node.getEnd()
            nodeEnergy = node.pathEnergy

            # Increment the energy cost until we encounter another jetstream
            while i not in self.adjacencyList and i < self.lastMile:
                i += 1
                nodeEnergy += self.defaultPathCost

            # Check and see if we've reached the goal
            if i == self.lastMile:
                self._storePath(node)
                self.minEnergy = nodeEnergy;
                return
                
            for childNode in self.adjacencyList[i]:
                newLength = nodeEnergy + childNode.getEnergy()

                # If the computed path energy is smaller, store it and store
                # the new predecessor
                if newLength < childNode.pathEnergy:
                    childNode.pathEnergy = newLength
                    childNode.predecessor = node

            # Keep our priority queue sorted
            self.jetStreamList.sort(key=lambda x: x.pathEnergy, reverse=True)
        
    def _bfsMethod(self):
        """Implement a shortest path between a pair of nodes using BFS
        concepts"""

        # initialize our energy and the node state for a BFS
        # however we want to visit every edge, so don't mark anything as visited
        nodeStack = list(self.firstJetStreams)

        while len(nodeStack) > 0:
            node = nodeStack.pop()

            i = node.getEnd()
            nodeEnergy = node.pathEnergy

            # Increment the energy cost until we encounter another jetstream
            while i not in self.adjacencyList and i < self.lastMile:
                i += 1
                nodeEnergy += self.defaultPathCost

            if i == self.lastMile:
                # We've reached our goal!
                self._storePath(node)
                self.minEnergy = nodeEnergy;
                return

            # Do a breadth-first search
            for childNode in self.adjacencyList[i]:
                newLength = nodeEnergy + childNode.getEnergy()

                # If the computed path energy is smaller, store it and store
                # the new predecessor
                if newLength < childNode.pathEnergy:
                    childNode.pathEnergy = newLength
                    childNode.predecessor = node

                    # Check for the end condition
                    if childNode.getEnd() == self.lastMile:
                        if childNode.pathEnergy < self.minEnergy:
                            self._storePath(childNode)
                            self.minEnergy = childNode.pathEnergy
                    elif childNode.pathEnergy > self.minEnergy:
                        # No need to continue, we are beyond the minimum so
                        # far
                        continue
                    else:
                        # Enqueue the next node to visit
                        nodeStack.append(childNode)
        
    def _storePath(self, lastNode):
        # Follow the predecessor chain (from the end) and store in
        # self.minPath
        self.minPath = []
        while lastNode:
            self.minPath.insert(0, (lastNode.getStart(), lastNode.getEnd()))
            lastNode = lastNode.predecessor

    def _readPathsFile(self):
        """Read and parse the given paths file"""

        minStart = sys.maxsize
        try:
            if not os.path.exists(self.pathsFile):
                raise Exception('The paths file (%s) does not exist' % self.pathsFile)

            with open(self.pathsFile) as fileObj:
                lineNum = 0
                for line in fileObj:
                    data = line.split(' ')

                    if lineNum == 0:
                        # The first line should be a default path cost integer
                        if len(data) > 0:
                            self.defaultPathCost = int(data[0])
                        else:
                            raise Exception('The first line of the paths file is malformed')
                    else:
                        # Subsequent lines should have 3 integers, the start
                        # mile, end mile, and energy to traverse that distance
                        start = int(data[0])
                        end = int(data[1])
                        energy = int(data[2])

                        jetStream = JetStream(start, end, energy)

                        # default the path energy to the maximum it could be
                        jetStream.pathEnergy = start * self.defaultPathCost + energy

                        # Add the JetStream to an adjacency list
                        # representation by start mile
                        if start not in self.adjacencyList:
                            self.adjacencyList[start] = [ ]
                        self.adjacencyList[start].append(jetStream)

                        # Store the last mile marker
                        self.lastMile = max(self.lastMile, end)

                        # Add it to a full list of jetStreams (needed for
                        # Dijkstra's algorithm
                        self.jetStreamList.append(jetStream)

                        # Store the first jet streams we have to have a proper
                        # starting point
                        if start < minStart:
                            self.firstJetStreams = []
                            self.firstJetStreams.append(jetStream)
                            minStart = start
                        elif start <= minStart:
                            self.firstJetStreams.append(jetStream)

                    lineNum += 1
        except Exception as e:
            print('Error reading paths file')
            print(e)
            return False
        
        return True
                            
if __name__ == '__main__':
    # Default to some common file names or allow the file to be input on the
    # command line
    if len(sys.argv) < 2:
        if os.path.exists('flight_paths'):
            delivery = CoconutDelivery('flight_paths')
        elif os.path.exists('flight_paths.txt'):
            delivery = CoconutDelivery('flight_paths.txt')
        else:
            print('Usage: %s <paths_file>' % sys.argv[0])
            sys.exit(1)
    else:
        delivery = CoconutDelivery(sys.argv[1])

    if not delivery.findShortestPath():
        sys.exit(2)
