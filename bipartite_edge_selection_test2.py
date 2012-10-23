import bipartite_edge_selection as bes
from sys import argv

def mean(l):
    return float(sum(l)) / len(l)

def main(N, d, approach):
  i = 0
  max_unmatched = 0
  while True:
    i += 1
    print "iteration #" + str(i)
    success,num_unmatched,matching,incident = bes.main(N,d,approach)
    assert success
    if num_unmatched > max_unmatched:
      for i in range(N):
        for e in incident[i]:
          print e
      print matching
      print "New max unmatched: " + str(num_unmatched)
      max_unmatched = num_unmatched
        
        
if __name__ == "__main__":
  print "Script that outputs the maximum amount of unmatched nodes encountered during run."
  
  if len(argv) == 1:
      # Lauren's w/ multi --> approach = 0
      # Lauren's w/o multi --> approach = 1
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
  main(N,d,approach)

