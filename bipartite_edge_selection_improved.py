#!//Library/Frameworks/Python.framework/Versions/2.7/bin/python

from random import shuffle, seed, sample
from sys import argv
from pprint import pprint
from sets import Set
from itertools import permutations
from bipartite_lib import Edge, create_regular_multigraph, knockout_multi_edges, get_args 


def main(N,d,doPrint = False,shortRun=False):

    incident,degree = create_regular_multigraph(N,d)
    incident,degree = knockout_multi_edges(incident,degree)
    
    if doPrint:
        print "Initial Edges:"
        for i in range(N):
            for e in incident[i]:
                print e 
    
        print "degree[] = " + str(degree)

    matching = {}
   
    cur = 0
    for i in range(2*N):
        if degree[i] < degree[cur]:
            cur = i 
 
# Main Loop
# TODO change left to cur, right to match 
    if shortRun: iteration = 0
    while len(matching) < N and cur != -1:    
        if shortRun:
          iteration+=1
          if iteration == 20:
            break
        edges = [e for e in incident[cur] if e.status == "on"]
        if cur < N:
            neighbors = [e.right for e in edges]
        else:
            neighbors = [e.left for e in edges]
        neighbors.sort()
        if doPrint:
            print degree
            print ""
            print "cur = " + str(cur) #DEBUG
            print "Valid remaing edges incident on #" + str(cur) + ":"#DEBUG 
            for e in edges: #DEBUG
                print "  " + str(e)
    
        if not neighbors: # This logic shouldn't be necesary
            if doPrint: print "ERROR: NODE #" + str(cur) + " IS DISCONNECTED."
            matching[cur] = -1

        else:
            # find min degree neighbor
            min_degree = neighbors[0]
            for i in neighbors:
                if doPrint: print "  degree[" + str(i) + "] = " + str(degree[i]) #DEBUG
                if degree[i] < degree[min_degree]:
                    min_degree = i
            match = min_degree

            # update matching
            if cur < N:
                matching[cur] = match
                e = [e for e in edges if e.right == match][0]
                e.matched = True 
            else:
                matching[match] = cur
                e = [e for e in edges if e.left == match][0]
                e.matched = True

            # remove edges
            for e in edges:
                e.status = "off"
            for i in neighbors:
                degree[i] -= 1 
            degree[cur] = 0

            match_edges = [e for e in incident[match] if e.status == "on"]
            if match < N:
                match_neighbors = [e.right for e in match_edges]
            else:
                match_neighbors = [e.left for e in match_edges]
            for e in match_edges:
                e.status = "off"
            for i in match_neighbors:
                degree[i] -= 1
            degree[match] = 0
             
        min_degree = -1 
        for i in range(2*N):
            if degree[i] != 0:
                min_degree = i
                break 
        
        if min_degree != -1:  
            for i in range(2*N):
                if degree[i] < degree[min_degree] and degree[i] != 0:
                    min_degree = i

        cur = min_degree
        
    # Check if matching is valid and print result
    if doPrint: print(matching)
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
    assert N - len(pure_matching) == len(unmatched)
    if doPrint: print str(len(unmatched)) + " unmatched nodes."

    return (success,len(unmatched),matching,incident)
         
               

if __name__ == "__main__":
  N,d = get_args('N','d')  
  main(N,d,True)
