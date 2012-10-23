import bipartite_edge_selection as bes

def mean(l):
    return float(sum(l)) / len(l)

def main(Ns, ds, num_trials, statistic, approach, filename):
  doPrintd = False
  if len(Ns) == 1: doPrintd = True

  filename = "output/" + filename
  f = open(filename,"w")
  for N in Ns:
    print "N = " + str(N)
    for d in ds:
      if doPrintd: print d
      trials = num_trials*[0]      
      for i in range(num_trials):
        success,unmatched,matching,incident = bes.main(N,d,approach)
        assert success
        if unmatched > 0:
          for i in range(N):
            for e in incident[i]:
              print e 
          print matching
        trials[i] = unmatched 
      result = statistic(trials)
      f.write(str(result))
      if d == ds[-1]:
        f.write("\n")
      else:
        f.write(",")
  f.close()
        
        
if __name__ == "__main__":
  #main([x*2-1 for x in range(1,51)], [x*2-1 for x in range(1,51)], 50, max, 1, "N=1,3,..,99_d=1,3,..,99_trials=50")
  #main([x*2-1 for x in range(1,11)], [x*2-1 for x in range(1,11)], 50, max, 1, "test")
  #main([x*2-1 for x in range(1,51)], [5], 1000, max, 2, "N=1,3,..,99_d=5_trials=1000_approach=2")
  #main([99], [x*2-1 for x in range(1,51)], 1000, max, 2, "N=99_d=1,3,..,99_trials=1000_approach=2")
  #main([x*2-1 for x in range(1,51)], [5], 1000, max, 1, "N=1,,..,99_d=5_trials=1000_approach=1")
  #main([99], [x*2-1 for x in range(1,51)], 1000, max, 1, "N=99_d=1,3,..,99_trials=1000_approach=1")
  #main([x*4-3 for x in range(1,22)], [5], 1000, mean, 2, "N=1,5,..,81_d=5_trials=1000_approach=2_stat=mean")
  #main([99], [x*4-3 for x in range(1,22)], 1000, mean, 2, "N=99_d=1,5,..,81_trials=1000_approach=2_stat=mean")
  #main([x*4-3 for x in range(1,22)], [5], 1000, max, 2, "N=1,5,..,81_d=5_trials=1000_approach=2_stat=max")
  #main([99], [x*4-3 for x in range(1,22)], 1000, max, 2, "N=99_d=1,5,..,81_trials=1000_approach=2_stat=max")
  main([6],[3],10000000,max,1,"out")

