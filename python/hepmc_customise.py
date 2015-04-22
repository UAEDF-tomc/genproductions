import FWCore.ParameterSet.Config as cms
def customiseForHepmc(process):
  process.VtxSmeared.src = 'source'
  process.genParticles.src = 'source'
  process.g4SimHits.HepMCProductLabel = 'source'
  process.g4SimHits.Generator.HepMCProductLabel = 'source'
  return(process)
