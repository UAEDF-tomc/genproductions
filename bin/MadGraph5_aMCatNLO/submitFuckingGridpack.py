#!/bin/env python
import os, sys, time, glob

gridpack = sys.argv[1]
dir      = sys.argv[2]
os.system('qsub -v gridpack=' + gridpack + ',dir=' + dir + ' runTheFuckingGridpack.sh')
os.system('mkdir -p /user/' + os.environ['USER'] + '/temp')

while not os.path.isfile(gridpack + '.log'): time.sleep(100)

while True:
  if len(glob.glob('./' + gridpack + '.xz')) > 0: break
  os.system('qstat &> /user/' + os.environ['USER'] + '/temp/.qstat')
  time.sleep(60)
