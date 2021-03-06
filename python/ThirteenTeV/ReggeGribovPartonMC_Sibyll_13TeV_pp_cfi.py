import FWCore.ParameterSet.Config as cms

from GeneratorInterface.ReggeGribovPartonMCInterface.ReggeGribovPartonMC_AdvancedParameters_cfi import *

generator = cms.EDFilter("ReggeGribovPartonMCGeneratorFilter",
                    ReggeGribovPartonMCAdvancedParameters,
                    beammomentum = cms.double(6500),
                    targetmomentum = cms.double(-6500),
                    beamid = cms.int32(1),
                    targetid = cms.int32(1),
                    model = cms.int32(6),
                    crossSection = cms.untracked.double(79610000000.0),
                    filterEfficiency = cms.untracked.double(1.0)
                    )


configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.1 $'),
    name = cms.untracked.string('$Source: /local/reps/CMSSW/CMSSW/GeneratorInterface/ReggeGribovPartonMCInterface/python/ReggeGribovPartonMC_Sibyll_13TeV_pp_cfi.py,v $'),
    annotation = cms.untracked.string('ReggeGribovMC generator')
    )
