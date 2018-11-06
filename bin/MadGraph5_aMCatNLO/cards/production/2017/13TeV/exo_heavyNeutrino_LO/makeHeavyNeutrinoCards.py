#!/usr/bin/env python
import os, shutil

def replaceInCard(card, replacements):
  with open(card, 'r') as f:  data = f.read()
  for r in replacements:      data = data.replace(r[0], r[1])
  with open(card, 'w') as f:  f.write(data)

#
# Create heavyNeutrino cards for given parameters
# Returns baseName (useful when this function is called from other scripts) which can be used to find the cards i.e. as baseName/baseName_*.dat
# mass            - mass of the heavy neutrino particle
# coupling        - mixing parameter between the heavy neutrino and lepton
# flavours        - could be e, mu, tau, 2l (e+mu), 3l (e+mu+tau)
# isPre2017       - use older pdf's as used in Moriond17 campaign
# type            - trilepton (n1 --> llnu) or lljj (n1 --> ljj)
# oneFlavourDecay - also limit the decay to the specified flavor
# signFirstFlavor - specify the sign of the first lepton
# noZ             - avoid diagrams containing Z
#
def makeHeavyNeutrinoCards(mass, coupling, flavours, isPre2017=False, type='trilepton', oneFlavourDecay=False, signFirstFlavor=0, noZ=False):
  if signFirstFlavor==1:  sign = 'Plus'
  if signFirstFlavor==-1: sign = 'Min'
  else:                   sign = ''
  baseName = 'HeavyNeutrino_' + type + '_M-' + str(mass) + '_V-' + str(coupling) + '_' + flavours + ('_oneFlavorDecay' if oneFlavourDecay else '') + ('_noZ' if noZ else '') + ('_pre2017' if isPre2017 else '') + '_massiveAndCKM' + sign + '_LO'

  try:    os.makedirs(baseName)
  except: pass

  for card in ['madspin_card', 'extramodels', 'run_card', 'proc_card', 'customizecards']:
    try:    shutil.copyfile('templateCards/HeavyNeutrino_template_LO_' + card + '.dat', baseName + '/' + baseName + '_' + card + '.dat')
    except: pass

  replacements = [('MASS',     str(mass)),
                  ('COUPLING', str(coupling)),
                  ('FLAVOURS', flavours),
                  ('TYPE',     type),
                  ('EXTRA',    ('_oneFlavorDecay' if oneFlavourDecay else '') + ('_noZ' if noZ else '') + ('_pre2017' if isPre2017 else '') + '_massiveAndCKM'+sign)]

  if flavours == '2l':    replacements += [('l+ = e+ mu+ ta+', 'l+ = e+ mu+'), ('l- = e- mu- ta-', 'l- = e- mu-')]
  elif flavours == 'e':   replacements += [('l+ = e+ mu+ ta+', 'l+ = e+'),     ('l- = e- mu- ta-', 'l- = e-')]
  elif flavours == 'mu':  replacements += [('l+ = e+ mu+ ta+', 'l+ = mu+'),    ('l- = e- mu- ta-', 'l- = mu-')]
  elif flavours == 'tau': replacements += [('l+ = e+ mu+ ta+', 'l+ = ta+'),    ('l- = e- mu- ta-', 'l- = ta-')]

  if signFirstFlavor==1:  replacements += [('l = l+ l-', 'l = l+')]
  if signFirstFlavor==-1: replacements += [('l = l+ l-', 'l = l-')]

  if oneFlavourDecay:
    if flavours in ['2l']:           replacements += [('ldecay+ = e+ mu+ ta+', 'ldecay+ = e+ mu+'), ('ldecay- = e- mu- ta-', 'ldecay- = e- mu-')]
    if flavours in ['e']:            replacements += [('ldecay+ = e+ mu+ ta+', 'ldecay+ = e+'), ('ldecay- = e- mu- ta-', 'ldecay- = e-')]
    if flavours in ['mu']:           replacements += [('ldecay+ = e+ mu+ ta+', 'ldecay+ = mu+'), ('ldecay- = e- mu- ta-', 'ldecay- = mu-')]
  if flavours in ['3l', '2l', 'e']:  replacements += [('set param_card numixing 1 0.000000e+00', 'set param_card numixing 1 %E' % coupling)]
  if flavours in ['3l', '2l', 'mu']: replacements += [('set param_card numixing 4 0.000000e+00', 'set param_card numixing 4 %E' % coupling)]
  if flavours in ['3l', 'tau']:      replacements += [('set param_card numixing 7 0.000000e+00', 'set param_card numixing 7 %E' % coupling)]

  if isPre2017:
    replacements += [('$DEFAULT_PDF_SETS', '292200')]
    replacements += [('$DEFAULT_PDF_MEMBERS', '292201  =  PDF_set_min\n292302  =  PDF_set_max\nTrue')]

  if type=='lljj':
    replacements += [('n1 > ldecay ldecay v', 'n1 > ldecay j j')]
  if noZ:
    replacements += [('n1 > ldecay ldecay v', 'n1 > ldecay ldecay v / Z')]
    replacements += [('n1 > ldecay j j',      'n1 > ldecay j j / Z')]


  replaceInCard(baseName + '/' + baseName + '_run_card.dat',       replacements)
  replaceInCard(baseName + '/' + baseName + '_proc_card.dat',      replacements)
  replaceInCard(baseName + '/' + baseName + '_customizecards.dat', replacements)
  try:    replaceInCard(baseName + '/' + baseName + '_madspin_card.dat',   replacements)
  except: pass

  return baseName

#
# Use Example:
#
if __name__ == "__main__":
  import math
  def intOrFloat(str):
    try:    return int(str)
    except: return float(str)

  # Create grid in mass and couplings
  for mass in [2, 5, 8]:
    v2s       = [5e-4, 3e-4, 2e-4, 1e-4, 7e-5, 5e-5, 3e-5, 2e-5, 1e-5, 8e-6, 6e-6]
    if   intOrFloat(mass) > 8: v2s = v2s[7:]
    elif intOrFloat(mass) > 7: v2s = v2s[6:]
    elif intOrFloat(mass) > 6: v2s = v2s[5:]
    elif intOrFloat(mass) > 5: v2s = v2s[4:]
    elif intOrFloat(mass) > 4: v2s = v2s[3:]
    elif intOrFloat(mass) > 3: v2s = v2s[2:]
    elif intOrFloat(mass) > 2: v2s = v2s[1:]
    couplings = [math.sqrt(v2) for v2 in v2s]

    for coupling in couplings:
      for flavour in ['e', 'mu', 'tau']:
        makeHeavyNeutrinoCards(mass, coupling, flavour, isPre2017=False, type='trilepton')   # Note: for Moriond17 samples should put isPre2017 to True
        makeHeavyNeutrinoCards(mass, coupling, flavour, isPre2017=False, type='lljj')
