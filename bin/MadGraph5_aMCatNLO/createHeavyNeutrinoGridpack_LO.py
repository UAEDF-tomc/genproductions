#!/usr/bin/env python

#
# Creates both the cards, prompt and displaced gridpack, and moves them to some public directory
#

import sys, os, fnmatch, shutil, math, numpy, time
type, mass, couplings, flavor = sys.argv[1:]
queue = 'cream02'
#queue = 'local'
dirac = False 
pre2017 = True 
copyToOfficialDir = True

path = './cards/production/2017/13TeV/exo_heavyNeutrino_LO/'

def intOrFloat(str):
  try:    return int(str)
  except: return float(str)

def createCards(path, mass, coupling, flavor, isPre2017, type, noZ):
  sys.path.append(path)
  from makeHeavyNeutrinoCards import makeHeavyNeutrinoCards
  cwd = os.getcwd()
  os.chdir(path)
  baseName = makeHeavyNeutrinoCards(intOrFloat(mass), float(coupling), flavor, isPre2017, type, noZ=noZ, dirac=dirac)
  os.chdir(cwd)
  return baseName

def findGridpack(dir, baseName):
  for file in os.listdir(dir):
    if fnmatch.fnmatch(file, baseName + '*.tar.xz'):
      return file
  return None

def copyToOfficial(gridpack):
  dest = '/user/' + os.environ['USER'] + '/public/production/official2/gridpacks' + ('Pre2017' if pre2017 else '') + '/' + gridpack
  try:    os.makedirs(os.path.dirname(dest))
  except: pass
  shutil.copyfile('/user/' + os.environ['USER'] + '/public/production/gridpacks2/displaced/' + gridpack, dest)

def createGridpack(path, mass, coupling, flavor, isPre2017, type, noZ):
  baseName = createCards(path, mass, coupling, flavor, isPre2017, type, noZ)
  gridpack = findGridpack('/user/tomc/public/production/gridpacks2/displaced', baseName)
  if gridpack:
    print gridpack + ' already exist, skipping'
    if copyToOfficialDir: copyToOfficial(gridpack)
    return None
  else:
    print 'Creating ' + baseName
  gridpack = findGridpack('.', baseName)
  if gridpack: return gridpack
  os.system('./gridpack_generation.sh ' + baseName + ' ' + path + '/' + baseName + ' ' + queue)
  time.sleep(10)
  gridpack = findGridpack('.', baseName)
  if gridpack: shutil.rmtree(gridpack.split('_slc')[0])
  return gridpack

if couplings=='all':
  if dirac and flavor=='tau':
    if intOrFloat(mass) == 1:    vs  = [4.66e-1]
    elif intOrFloat(mass) == 2:  vs  = [5.00e-2]
    elif intOrFloat(mass) == 3:  vs  = [1.35e-2]
    elif intOrFloat(mass) == 4:  vs  = [9.28e-3]
    elif intOrFloat(mass) == 5:  vs  = [9.04e-3]
    elif intOrFloat(mass) == 10: vs  = [1.52e-3]
  elif dirac:
    if intOrFloat(mass) == 10:   v2s = [1.15e-6]
    elif intOrFloat(mass) == 8:  v2s = [4.59e-6]
    elif intOrFloat(mass) == 6:  v2s = [8.20e-6]
    elif intOrFloat(mass) == 5:  v2s = [4.23e-6]
    elif intOrFloat(mass) == 4:  v2s = [1.69e-5]
    elif intOrFloat(mass) == 3:  v2s = [1.00e-4]
    elif intOrFloat(mass) == 2:  v2s = [1.23e-3, 2.47e-4]
    elif intOrFloat(mass) == 1:  v2s = [9.02e-2, 1.80e-2]
  elif flavor=='tau':
    if intOrFloat(mass) == 1:    vs  = [3.29e-1]
    elif intOrFloat(mass) == 2:  vs  = [3.53e-2]
    elif intOrFloat(mass) == 3:  vs  = [9.57e-3]
    elif intOrFloat(mass) == 4:  vs  = [6.56e-3]
    elif intOrFloat(mass) == 5:  vs  = [6.39e-3]
    elif intOrFloat(mass) == 10: vs  = [1.08e-3]
  else:
#    if   intOrFloat(mass) == 20: v2s = [3.74e-10, 7.48e-11]
#    elif intOrFloat(mass) == 15: v2s = [2.28e-9, 4.57e-10]
    if intOrFloat(mass) == 10:   v2s = [5.73e-7]
    elif intOrFloat(mass) == 8:  v2s = [2.29e-6]
    elif intOrFloat(mass) == 6:  v2s = [4.10e-6]
    elif intOrFloat(mass) == 5:  v2s = [2.12e-6]
    elif intOrFloat(mass) == 4:  v2s = [8.44e-6]
    elif intOrFloat(mass) == 3:  v2s = [5.01e-5]
    elif intOrFloat(mass) == 2:  v2s = [6.17e-4, 1.23e-4]
    elif intOrFloat(mass) == 1:  v2s = [4.51e-2, 9.02e-3]
  try:
    print vs
    couplings = vs
  except:
    print v2s
    couplings = [math.sqrt(v2) for v2 in v2s]
elif couplings=='allOld':
  v2s       = [5e-4, 3e-4, 2e-4, 1e-4, 7e-5, 5e-5, 3e-5, 2e-5, 1e-5, 8e-6, 6e-6]
  if   intOrFloat(mass) > 8: v2s = v2s[7:]
  elif intOrFloat(mass) > 7: v2s = v2s[6:]
  elif intOrFloat(mass) > 6: v2s = v2s[5:]
  elif intOrFloat(mass) > 5: v2s = v2s[4:]
  elif intOrFloat(mass) > 4: v2s = v2s[3:]
  elif intOrFloat(mass) > 3: v2s = v2s[2:]
  elif intOrFloat(mass) > 2: v2s = v2s[1:]
  print v2s
  couplings = [math.sqrt(v2) for v2 in v2s]
else:
  couplings = [couplings]

def logFilesOk(gridpack):
  try:
    with open(gridpack.split('LO')[0] + 'LO.log') as f:
      for line in f:
        if '+' in line: continue
        if 'tar: Error is not recoverable: exiting now' in line: return False
  except:
    pass
  return True

for coupling in couplings:
  while True:
    gridpack = createGridpack(path, mass, coupling, flavor, pre2017, type, False)
    if (not gridpack) or logFilesOk(gridpack): break
    if gridpack: shutil.move(gridpack, gridpack + '_problem')
  time.sleep(10)
  if gridpack:
    print gridpack + ' --> fixing for Madspin bug'
    os.system('./fixGridpack.sh ' + gridpack)
    print gridpack + ' --> prompt done'
    shutil.copyfile(gridpack, '/user/' + os.environ['USER'] + '/public/production/gridpacks2/prompt/' + gridpack)
    print gridpack + ' --> fixing for displaced'
    os.system('./fixGridpackForDisplacedLO.sh ' + gridpack)
    shutil.move(gridpack, '/user/' + os.environ['USER'] + '/public/production/gridpacks2/displaced/' + gridpack)
    print gridpack + ' --> displaced done'
    try:    os.remove(gridpack.split('LO')[0] + 'LO.log')
    except: pass

    if copyToOfficialDir: copyToOfficial(gridpack)
