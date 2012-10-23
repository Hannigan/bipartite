import bipartite_edge_selection as bes
from sys import argv

        
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

  max_unmatched = 0
  i = 0
  for right_sides in bes.create_all_right_sides(N,d):
      i += 1
      success,unmatched,matching,incident = bes.main(N,d,approach, right_sides = right_sides) 
      if i % 100000: print i 
      if unmatched > max_unmatched:
        print ""
        for i in range(N):
          for e in incident[i]:
            print e
        print matching
        print "Max Unmatched = " + str(unmatched)

