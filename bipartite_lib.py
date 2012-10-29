#!//Library/Frameworks/Python.framework/Versions/2.7/bin/python

from random import shuffle, seed, sample
from sys import argv, stdout
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
        self.matched = False

    def __str__(self):
        return "(" + str(self.left) + ", " + str(self.right) + ") " + self.status


def create_all_right_sides(N,d):
    print "WARNING: create_all_right_sides is incredibly inefficient, use small params. N=5,d=2 max."
    # create a list with d of each node on the right side
    right_sides = []
    for right in range(N):
        for i in range(d):
            right_sides.append(N + right)

    perms = permutations(right_sides)

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


def knockout_multi_edges(incident, degree):
    N = len(incident)/2
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
    return incident,degree

def get_args(*names):
    assert len(names) == len(Set(names))
    if len(argv) == 1:
        stdout.write("Enter "),
        for n in names:
          stdout.write(n)
          if n == names[-1]: stdout.write(': ')
          else: stdout.write(', ')
        params = raw_input().split()
    else:
        params = argv[1:]
    assert len(params) == len(names) # too many or too few arguments inputted on command line
    params = tuple([ int(n) for n in params ])
    return params
