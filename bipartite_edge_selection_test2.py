import bipartite_edge_selection as bes
import bipartite_edge_selection_improved as besi 
from bipartite_lib import get_args
from sys import argv

def mean(l):
    return float(sum(l)) / len(l)

def main(N, d, approach, freq):
  itr = 0
  max_unmatched = 0
  while True:
    itr += 1
    if itr % freq == 0: print "iteration #" + str(itr)

    if approach == 3:
      success,num_unmatched,matching,incident = besi.main(N,d)
    else:
      success,num_unmatched,matching,incident = bes.main(N,d,approach)
 
    assert success
    if num_unmatched > max_unmatched:
      for n in range(N):
        for e in incident[n]:
          print e
      print matching
      print "New max unmatched: " + str(num_unmatched)
      max_unmatched = num_unmatched
        
        
if __name__ == "__main__":
  print "Script that outputs the maximum amount of unmatched nodes encountered during run."
  
  # Lauren's w/ multi --> approach = 0
  # Lauren's w/o multi --> approach = 1
  # Random, stupid edge selection --> approach = 2
  (N,d,approach,freq) = get_args('N','d','approach','frequency')
  
  main(N,d,approach,freq)

