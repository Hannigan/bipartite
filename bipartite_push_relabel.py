#!//Library/Frameworks/Python.framework/Versions/2.7/bin/python

from random import shuffle, seed, sample
from sys import argv

class Edge:
    def __init__(self, left, right, height=0):
        self.left = left
        self.right = right
        self.order = ""
        self.direction = ""
        self.capacity = 1
        self.flow = 0
        self.h = height 
    
    def e(self):
        self.flow - self.excess

    def __str__(self):
        return "(" + str(self.left) + ", " + str(self.right) + ") " 

# Command line has two arguments: N (number of vertices per side) and
# d (degree).

def create_regular_multigraph(N,d):
    # create a list with d of each node on the right side
    right_sides = []
    for right in range(N):
        for i in range(d):
            right_sides.append(N + right)
    # seed(17)
    shuffle(right_sides)
    print right_sides

    incident = []
    for i in range(2 * N):
        incident.append([])

    i = 0
    edges = []
    for left in range(N):
        for e in range(d):
            right = right_sides[i]
            edge = Edge(left, right)
            edges.append(edge)
            incident[left].append(edge)
            incident[right].append(edge)
            i += 1

    degree = (2 * N) * [d]   # degree of untaken edges per vertex
    return (incident, edges)


def push(u,v,f,cap,e):
    delta = min(e[u],cap[u][v] - f[u][v])
    print "Pushing " + str(delta) + " units of flow from " + str(u) + " -> " + str(v)    
    f[u][v] += delta
    f[v][u] = -f[u][v]
    e[u] -= delta
    e[v] += delta 
    return f,e


def relabel(u,cap,f,h):
    neighbors = [v for v in range(len(cap[u])) if cap[u][v] - f[u][v] > 0]
    neighbors.sort()
    lowest_neighbor = neighbors[0]
    for i in neighbors:
        if h[i] < h[lowest_neighbor]:
            lowest_neighbor = i 
    print "Relabeling " + str(u) + " from " + str(h[u]) + " to " + str(1+h[lowest_neighbor])
    h[u] = 1+h[lowest_neighbor]
    steps = len(neighbors)
    return h,steps 

def findPush(f,cap,e,h,N):
    for u in range(len(e)):
        if e[u] > 0:
            for v in range(2*N+2):
                if cap[u][v] - f[u][v] > 0 and h[u] == 1 + h[v]: 
                    return (u,v)
    return ("NO PUSH","NO PUSH")


def findRelabl(f,cap,e,h,N):
    for u in range(2*N): # don't consider sink and source
        #print [ h[u] <= h[v] for v in range(2*N+2) if cap[u][v] - f[u][v] > 0 ]
        #print e[u]
        if e[u] > 0 and all([ h[u] <= h[v] for v in range(2*N+2) if cap[u][v] - f[u][v] > 0]):
            return u
    return "NO RELABEL"
        

def main(doPrint = False):
    # Normal approach = 0, THC alternate approach = 1 
    if len(argv) == 1:
        print "Enter N, d:",
        params = raw_input().split()
        N = int(params[0])
        d = int(params[1])
        approach = int(params[2])
    else:
        N = int(argv[1])
        d = int(argv[2])
        approach = int(argv[3])

    print N, d
 
    (incident,edges) = create_regular_multigraph(N,d)

    
    if approach == 0: # Normal Approach
        # source is named 2N, sink is named 2N+1
        source_capacity = 1
        assert source_capacity <= d
        f = []
        cap = []
        for i in range(2*N+2):
            f.append((2*N+2)*[0])
            cap.append((2*N+2)*[0]) 
        for edge in edges:
            print edge.left, edge.right
            cap[edge.left][edge.right] += 1
        for left in range(N):
            cap[-2][left] = source_capacity 
        for right in range(N,2*N):
            cap[right][-1] = source_capacity
    
        #print "\nf[][] = " + str(f)
        print "\ncap[][] = " + str(cap)
    
        h = (2*N+2)*[0]
        h[-2] = N
        #print "\nh[] = " + str(h)
    
        e = (2*N+2)*[0]
        #print "\ne[] = " + str(e) 
    
        # Initialize Preflow
        for i in range(N):
            f[-2][i] = cap[-2][i]
            f[i][-2] = -cap[-2][i]
            e[i] = cap[-2][i]
            e[-2] -= cap[-2][i] 
    
    if approach == 1: # Alternate THC approach
        # source is named 2N, sink is named 2N+1
        f = []
        cap = []
        for i in range(2*N+2):
            f.append((2*N+2)*[0])
            cap.append((2*N+2)*[0]) 
        for edge in edges:
            print edge.left, edge.right
            cap[edge.left][edge.right] += 1
            f[edge.left][edge.right] += 1
            f[edge.right][edge.left] -= 1
        for left in range(N):
            cap[-2][left] = d 
            f[-2][left] = d
            f[left][-2] = -d
        for right in range(N,2*N):
            cap[right][-1] = 1
            f[right][-1] = 1
            f[-1][right] = -1
            
    
        print "\nf[][] = " + str(f)
        print "\ncap[][] = " + str(cap)
    
        h = (2*N+2)*[1]
        h[-2] = N
        h[-1] = 0 
        print "\nh[] = " + str(h)
    
        e = (2*N+2)*[0]
        e[-2] = -d*N
        e[-1] = N
        for i in range(N,2*N):
            e[i] = d-1
        print "\ne[] = " + str(e) 
    
    push_steps = 0 
    relabel_steps = 0
    while True:
        print ""
        (u,v) = findPush(f,cap,e,h,N) 
        if u != "NO PUSH":
            (f,e) = push(u,v,f,cap,e)
            if doPrint:
              print "f[][] = " + str(f)
              print "h[] = " + str(h)
              print "e[] = " + str(e) 
            push_steps += 1
            continue           
        u = findRelabl(f,cap,e,h,N)
        if u != "NO RELABEL": 
            h,steps = relabel(u,cap,f,h)
            if doPrint:
              print "f[][] = " + str(f)
              print "h[] = " + str(h)
              print "e[] = " + str(e) 
            relabel_steps += steps
            continue
        break
    
    # Print Results
    matching = {}
    for u in range(N):
        for v in range (N,2*N):
            if f[u][v] == 1: 
                matching[u] = v
                print "(" + str(u) + ", " + str(v) + ")"        
                
    # Check if matching is valid
    left = matching.keys()
    left.sort()
    assert left == range(N)
    right = [v for k,v in matching.iteritems()]
    right.sort()
    assert right == range(N,2*N)
      
    print "\nMatching is valid!\n" 
    print "Push Steps = " + str(push_steps) 
    print "Relabel Steps = " + str(relabel_steps)
    

if __name__ == "__main__":
  main()
