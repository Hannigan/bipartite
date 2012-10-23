#!//Library/Frameworks/Python.framework/Versions/2.7/bin/python

from random import shuffle, seed, sample
from sys import argv
from pprint import pprint
from sets import Set
from itertools import permutations

class Edge:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.order = ""
        self.direction = ""
        self.status = "on"

    def __str__(self):
        return "(" + str(self.left) + ", " + str(self.right) + ") " + self.status

# Command line has two arguments: N (number of vertices per side) and
# d (degree).

#

def create_all_right_sides(N,d):
    # create a list with d of each node on the right side
    right_sides = []
    for right in range(N):
        for i in range(d):
            right_sides.append(N + right)

    perms = permutations(right_sides)

    #graphs = Set([]) 
    #for p in perms:
    #  graphs.add( tuple([ tuple(sorted(p[i*d:i*d+d])) for i in range(N) ]) )

    graphs = []
    for p in perms:
      graphs.append( tuple([ tuple(sorted(p[i*d:i*d+d])) for i in range(N) ]) )

    graphs = Set(graphs)

    all_right_sides = []
    for g in graphs:
      out = ()
      for i in g:
        out += i
      all_right_sides.append(list(out))

    return all_right_sides


def create_regular_multigraph(N,d,doPrint = False):
    right_sides = []
    # create a list with d of each node on the right side
    for right in range(N):
        for i in range(d):
            right_sides.append(N + right)
    # seed(17)
    shuffle(right_sides)
    if doPrint: print right_sides

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
     
    degree = (2 * N) * [d]   # degree of untaken edges per vertex
    return (incident, degree)

def main(N,d,approach,doPrint = False):

    (incident,degree) = create_regular_multigraph(N,d)

    for i in range(2*N):
        edges = incident[i]
        for edge in edges:
            if i < N:
                if len([e for e in edges if e.right == edge.right and e.status == "on"]) > 1:
                    edge.status = "off" 
                    degree[edge.left] -= 1
                    degree[edge.right] -= 1
            else:
                if len([e for e in edges if e.left == edge.left and e.status == "on"]) > 1:
                    edge.status = "off" 
                    degree[edge.left] -= 1
                    degree[edge.right] -= 1
        incident[i] = edges
    
    if doPrint:
        print "Initial Edges:"
        for i in range(N):
            for e in incident[i]:
                print e 
    
        print "degree[] = " + str(degree)

    matching = {}
   
# for all approaches, set the left to the min degree node on left 
#   (for random approach, left = 0 always)
    left = 0
    for i in range(N):
        if degree[i] < degree[left]:
            left = i 
 
# Main Loop 
    while len(matching) < N and left != -1:    
        edges = [e for e in incident[left] if e.status == "on"]
        neighbors = [e.right for e in edges]
        neighbors.sort()
        if doPrint:
            print ""
            print "left = " + str(left) #DEBUG
            print "Valid remaing edges incident on #" + str(left) + ":"#DEBUG 
            for e in edges: #DEBUG
                print "  " + str(e)
    
        if not neighbors:
            if doPrint: print "ERROR: NODE #" + str(left) + " IS DISCONNECTED."
            matching[left] = -1 

        else:
            # find min degree neighbor on right
            if approach == 0 or approach == 1 or approach == 3:
                min_degree = neighbors[0]
                for i in neighbors:
                    if doPrint: print "  degree[" + str(i) + "] = " + str(degree[i]) #DEBUG
                    if degree[i] < degree[min_degree]:
                        min_degree = i
                right = min_degree
            if approach == 2:
                right = sample(neighbors,1)[0] 
             
            if doPrint: print "right = " + str(right) 
            # record matching, remove edges, update degrees
            matching[left] = right
            if doPrint: print "MATCH: " + str(left) + " --> " + str(right)
            for e in edges: 
                e.status = "off"    
            for i in neighbors:
                degree[i] -= 1
    
            degree[left] = 0
    
            # check if we are done
            # matched_left = matching.keys()
            # matched_left.sort()
            # 
            # matched_right = [v for k,v in matching.iteritems()]
            # matched_right.sort()

            # if matched_left == range(N) and matched_right == range(N,2*N):
            #     match_status = "valid"
            #     # check if matching is valid
            #     for i in range(N):
            #         neighbors = [e.right for e in incident[i]]
            #         if matching[i] not in neighbors:
            #             print "ERROR: Matching invalid. (" + str(i) + ", " + str(matching[i]) + ")"
            #             match_status = "invalid"
            #     print "matching is " + match_status
            #     print matching
            #     break 
    
        # find a node to start from on the left
        edges = [e for e in incident[right] if e.status == "on"]
        neighbors = [e.left for e in edges]
        neighbors.sort()
        if approach == 0 or approach == 1: 
            if neighbors: # if right is connected, go to min degree neighbor on left
                if doPrint:
                    print "Edges available from #" + str(right) + ":"
                    for e in edges: #DEBUG
                        print "  " + str(e)   
                min_degree = neighbors[0]
                for i in neighbors:
                    if degree[i] < degree[min_degree]:
                        min_degree = i
                left = min_degree
                
                for e in edges:
                    e.status = "off"
                for i in neighbors:
                    degree[i] -= 1 
                degree[right] = 0
    
            else: # right is not connected, so just start from lowest unmatched node on left
                left = -1 
                for i in range(N):
                    if i not in matching:
                        left = i
                        if doPrint: print "#" + str(right) + " is no longer connected.  Next unmatched node on left is " + str(left) + "."
                        break
                if left == -1:
                    if doPrint: print "ERROR: all nodes have been visited"


        elif approach == 2:
            for e in edges:
                e.status = "off"
            for i in neighbors:
                degree[i] -= 1 
            degree[right] = 0
            left = -1 
            for i in range(N):
                if i not in matching:
                    left = i
                    if doPrint: print "#" + str(right) + " is no longer connected.  Next unmatched node on left is " + str(left) + "."
                    break
      

        elif approach == 3:
            for e in edges:
                e.status = "off"
            for i in neighbors:
                degree[i] -= 1 
            degree[right] = 0

            min_degree = -1 
            for i in range(N):
                if degree[i] != 0:
                    min_degree = i
                    break 
            
            if min_degree != -1:  
                for i in neighbors:
                    if degree[i] < degree[min_degree] and degree[i] != 0:
                        min_degree = i

            left = min_degree
            
        else:
            assert False 

    # Check if matching is valid and print result
    if doPrint: print(matching)
    if approach == 3:
      unmatched = [i for i in range(N) if i not in matching.keys()] 
      for i in unmatched:
        matching[i] = -1
    keys = sorted(matching.keys())  
    pure_matching = dict([(k,v) for k,v in matching.iteritems() if v != -1])
    assert all([0 <= k and k<N for k in pure_matching.keys()]) 
    assert all([N <= v and v<2*N for v in [v for k,v in pure_matching.iteritems()]])
    for k in pure_matching.keys():
        neighbors = [e.right for e in incident[k]]
        assert pure_matching[k] in neighbors
    if len(pure_matching) != len(Set([v for k,v in pure_matching.iteritems()])):
        success = False
        if doPrint: print "Matching is INVALID"  
    else:
        success = True
        if doPrint: print "Matching is VALID."
    unmatched = [k for k,v in matching.iteritems() if v == -1]
    if doPrint: print str(len(unmatched)) + " unmatched nodes."

    return (success,len(unmatched),matching,incident)
         
               

if __name__ == "__main__":
    if len(argv) == 1:
        # Lauren's w/ multi --> approach = 0
        # Lauren's w/o multi --> approach =1
        # Random, stupid edge selection --> approach = 2
        print "Enter N, d, approach:",
        params = raw_input().split()
        N = int(params[0])
        d = int(params[1])
        approach = int(params[2])
    else:
        N = int(argv[1])
        d = int(argv[2])
        approach = int(argv[3])
    print N, d, approach
    main(N,d,approach)
