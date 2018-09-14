import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *
from Configuration.Generator.Pythia8PowhegEmissionVetoSettings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
                         maxEventsToPrint = cms.untracked.int32(1),
                         pythiaPylistVerbosity = cms.untracked.int32(1),
                         filterEfficiency = cms.untracked.double(1.0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         comEnergy = cms.double(13000.),
                         emissionVeto1 = cms.untracked.PSet(),
                         EV1_nFinal = cms.int32(2),
                         EV1_nFinalMode = cms.int32(2),
                         EV1_vetoOn = cms.bool(True),
                         EV1_maxVetoCount = cms.int32(10),
                         EV1_pThardMode = cms.int32(1),
                         EV1_pTempMode = cms.int32(0),
                         EV1_emittedMode = cms.int32(0),
                         EV1_pTdefMode = cms.int32(1),
                         EV1_MPIvetoOn = cms.bool(False),
                         EV1_QEDvetoMode = cms.int32(1),
                         PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CUEP8M1SettingsBlock,
        processParameters = cms.vstring(
            'POWHEG:nFinal = 2',   ## Number of final state particles
                                   ## (BEFORE THE DECAYS) in the LHE
                                   ## other than emitted extra parton
            '23:mMin = 0.05',      
	    	'24:mMin = 0.05',      
            '25:m0 = 125.0',
            '25:onMode = off',
			'25:onIfMatch = 5 -5', #Higgs decays only to bb pair
            #PSweights
            'UncertaintyBands:doVariations = on',
            # 3 sets of variations for ISR&FSR up/down
            # Reduced sqrt(2)/(1/sqrt(2)), Default 2/0.5 and Conservative 4/0.25 variations
                    'UncertaintyBands:List = {\
            isrRedHi isr:muRfac=0.707,fsrRedHi fsr:muRfac=0.707,isrRedLo isr:muRfac=1.414,fsrRedLo fsr:muRfac=1.414,\
            isrDefHi isr:muRfac=0.5, fsrDefHi fsr:muRfac=0.5,isrDefLo isr:muRfac=2.0,fsrDefLo fsr:muRfac=2.0,\
            isrConHi isr:muRfac=0.25, fsrConHi fsr:muRfac=0.25,isrConLo isr:muRfac=4.0,fsrConLo fsr:muRfac=4.0}',

            'UncertaintyBands:MPIshowers = on',
            'UncertaintyBands:overSampleFSR = 10.0',
            'UncertaintyBands:overSampleISR = 10.0',
            'UncertaintyBands:FSRpTmin2Fac = 20',
            'UncertaintyBands:ISRpTmin2Fac = 1'
          ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters'
                                    )
        )
                         )

ProductionFilterSequence = cms.Sequence(generator)
