#!//Library/Frameworks/Python.framework/Versions/2.7/bin/python

from random import shuffle, seed
from sys import argv
from collections import deque
from uuid import uuid4 as uid
import copy

class Edge:
    def __init__(self, left, right):
        self.tag = str(uid()) 
        self.left = left
        self.right = right
        self.order = ""
        self.direction = ""

    def __str__(self):
        return "(" + str(self.left) + ", " + str(self.right) + ") " + self.direction + " " + str(self.order)

# Command line has two arguments: N (number of vertices per side) and
# d (degree).

if len(argv) == 1:
    print "Enter N, d:",
    params = raw_input().split()
    N = int(params[0])
    d = int(params[1])
else:
    N = int(argv[1])
    d = int(argv[2])

print N, d

# create a list with d of each node on the right side
right_sides = []
for right in range(N):
    for i in range(d):
        right_sides.append(N + right)
# seed(17)
shuffle(right_sides)
# REMOVE ME Todo
#right_sides = [12, 15, 11, 14, 13, 12, 8, 12, 9, 10, 15, 11, 8, 8, 13, 10, 15, 14, 9, 9, 10, 13, 14, 11]
print right_sides

incident = []
for i in range(2 * N):
    incident.append([])

i = 0
for left in range(N):
    for e in range(d):
        right = right_sides[i]
        edge = Edge(left, right)
        incident[left].append(edge)
        incident[right].append(edge)
        i += 1

# At this point, incident gives us the bipartite graph structure.
# Now find paths and direct edges.
degree = (2 * N) * [d]   # degree of untaken edges per vertex
# available = range(N)     # list of vertices on left with degree > 0


def eBFSExplore(incident, degree, root): 
  """
  * Make sure eBFS doesn't touch the real incident and degree.
  These should be copies, and output path of eBFS should be used to
  modify actual incident and degree. 
  
  * Retrace path by taking the largest ordered edges backwards?
  """

  exploreOrder = 1
  q = deque([root])
  while q: 
    print q 
    node = q.popleft()
    newEdges = [e for e in incident[node] if e.direction == ""] # Should really only exclude parent branch of edges taken to current node
    for e in newEdges: print e

    for e in newEdges:
      if node < N: # traversing L -> R
        # label edge L -> R
          e.direction = "L -> R"
          e.order = exploreOrder; exploreOrder += 1
          degree[e.right] -= 1 
          print e
        # stop if we make the node even degree AFTER visiting
          if degree[e.right] % 2 == 0:
            print "arrived at the right at an even degree node!  Retracing.."
            return eBFSRetrace(incident, root, e.right)
          else: 
            q.append(e.right)
      else: # traversing R -> L 
        # just make sure we aren't stuck before queuing node and labeling edge R -> L
        if degree[e.left] != 1: # if not stuck on left..
          e.direction = "R -> L"
          e.order = exploreOrder; exploreOrder += 1
          degree[e.left] -= 1
          q.append(e.left)
          print e
        else:
          print e, " :: would make me stuck.  Skip it."
  print "eBFS: ERROR - Reached end of queue with out finding a good path."

  
def eBFSRetrace(incident, root, end):
  node = end
  path = []
  while node != root:
    if node < N:
      edges = [e for e in incident[node] if e.direction == "R -> L"]
      prevEdge = edges[0]
      for e in edges:
        if e.order > prevEdge.order:
          prevEdge = e
      # incident[node].remove(prevEdge)
      print "RETRACE:",prevEdge
      path.insert(0,prevEdge)
      node = e.right     
    else:
      edges = [e for e in incident[node] if e.direction == "L -> R"]
      prevEdge = edges[0]
      for e in edges:
        if e.order > prevEdge.order:
          prevEdge = e
      # incident[node].remove(prevEdge)
      print "RETRACE:", prevEdge
      path.insert(0,prevEdge)
      node = e.left 

  return path

order = 1
times_stuck = 0

def eBFSUpdate(path, realIncident, realDegree):
  """
  path:         the path found in the bipartite graph
  realIncident: the REAL incident list
  realDegree:   the REAL degree list
  """
  for e in path:
    realDegree[e.left]  -= 1
    realDegree[e.right] -= 1
 
  global order 

  for es in realIncident:
    for e in es:
      for p in path:
        if e.tag == p.tag:
          e.direction = p.direction  
          e.order = 0 #order; order += 1

# Main eBFS Steps

for i in range(N):
  incidentCOPY = copy.deepcopy(incident)
  degreeCOPY   = copy.deepcopy(degree)
  path = eBFSExplore(incidentCOPY,degreeCOPY,i)
  eBFSUpdate(path, incident, degree)


# Print the result.    
for i in range(2 * N):
    print i,
    for e in incident[i]:
        print e, ";",
    print ""

# Check that all degrees are correctly computed.
for i in range(2 * N):
    this_degree = 0
    for e in incident[i]:
        if e.direction == "":
            this_degree += 1
    if this_degree != degree[i] or this_degree % 2 != 0:
        print "Degree error at vertex " + str(i) + ": actual degree = " + str(this_degree) + ", computed degree = " + str(degree[i])
    else:
        print "degree[" + str(i) + "] = " + str(degree[i])

