import FWCore.ParameterSet.Config as cms
def customiseForHepmc(process):
  process.VtxSmeared.src = 'source'
  process.genParticles.src = 'source'
  return(process)
