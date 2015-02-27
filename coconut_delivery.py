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
        self.fake = False

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
    """

    def __init__(self, pathsFile):
        self.pathsFile = pathsFile
        self.adjacencyList = { }
        self.defaultPathCost = 0
        self.lastMile = 0
        self.minEnergy = sys.maxsize
        self.minPath = None
        self.firstJetStreams = []

    def findShortestPath(self):
        if not self._readPathsFile():
            return False

        self._bfsMethod()

        # Print the results
        print(self.minEnergy)
        print(self.minPath)

        return True

    def _bfsMethod(self):
        # initialize our energy and the node state for a BFS
        # however we want to visit every edge, so don't mark anything as visited
        nodeStack = list(self.firstJetStreams)

        while len(nodeStack) > 0:
            node = nodeStack.pop()

            if node.getEnd() in self.adjacencyList:
                # There are jet streams end at this node
                for childNode in self.adjacencyList[node.getEnd()]:
                    if (node.pathEnergy + childNode.getEnergy()) < childNode.pathEnergy:
                        childNode.pathEnergy = node.pathEnergy + childNode.getEnergy()

                        if node.fake:
                            childNode.predecessor = node.predecessor
                        else:
                            childNode.predecessor = node
                        
                        if childNode.getEnd() == self.lastMile:
                            if childNode.pathEnergy < self.minEnergy:
                                self.storePath(childNode)
                                self.minEnergy = childNode.pathEnergy
                        elif childNode.pathEnergy > self.minEnergy:
                            # No need to continue, we are beyond the minimum so
                            # far
                            continue
                        else:
                            nodeStack.append(childNode)
            else:
                # Add a next node with a length of 1
                # This could be optimized by storing a pointer to the next
                # valid jet stream
                fakeNode = JetStream(node.getEnd(), node.getEnd() + 1, self.defaultPathCost)
                fakeNode.fake = True
                fakeNode.pathEnergy = node.pathEnergy + self.defaultPathCost

                # if the node we are looking at is 'fake', then use its
                # predecessor, since that's a jet stream we need to track
                if node.fake:
                    fakeNode.predecessor = node.predecessor
                else:
                    fakeNode.predecessor = node

                if fakeNode.getEnd() == self.lastMile:
                    if fakeNode.pathEnergy < self.minEnergy:
                        self.storePath(fakeNode.predecessor)
                        self.minEnergy = fakeNode.pathEnergy
                elif fakeNode.pathEnergy > self.minEnergy:
                    # No need to continue, we are beyond the minimum so
                    # far
                    continue
                else:
                    nodeStack.append(fakeNode)
        
    def storePath(self, lastNode):
        self.minPath = []
        while lastNode:
            self.minPath.insert(0, (lastNode.getStart(), lastNode.getEnd()))
            lastNode = lastNode.predecessor

    def _readPathsFile(self):
        minStart = sys.maxsize
        try:
            if not os.path.exists(self.pathsFile):
                raise Exception('The paths file does not exist')

            with open(self.pathsFile) as fileObj:
                lineNum = 0
                for line in fileObj:
                    data = line.split(' ')

                    if lineNum == 0:
                        # This should be a single entry
                        if len(data) > 0:
                            self.defaultPathCost = int(data[0])
                        else:
                            raise Exception('The first line of the paths file is malformed')
                    else:
                        # Subsequent lines should have 3 integers
                        start = int(data[0])
                        end = int(data[1])
                        energy = int(data[2])

                        jetStream = JetStream(start, end, energy)
                        # default the path energy to the maximum it could be
                        jetStream.pathEnergy = start * self.defaultPathCost + energy

                        # Add the edge to the adjacencyList with its energy
                        if start not in self.adjacencyList:
                            self.adjacencyList[start] = [ ]
                        self.adjacencyList[start].append(jetStream)

                        # Store the last mile marker
                        self.lastMile = max(self.lastMile, end)

                        # Store the first jet streams we have
                        if start < minStart:
                            self.firstJetStreams = []
                            self.firstJetStreams.append(jetStream)
                            minStart = start
                        elif start <= minStart:
                            self.firstJetStreams.append(jetStream)

                    lineNum += 1

            #print('Flight Paths Loaded')
        except Exception as e:
            print('Error reading paths file')
            print(e)
            return False
        
        return True
                            

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: %s <paths_file>')
    else:
        delivery = CoconutDelivery(sys.argv[1])
        delivery.findShortestPath()


    
    
    
