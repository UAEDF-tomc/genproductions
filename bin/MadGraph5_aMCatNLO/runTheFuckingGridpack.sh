#!/bin/bash
cd /user/tomc/heavyNeutrino/CMSSW_8_0_28_patch1/src/
source $VO_CMS_SW_DIR/cmsset_default.sh
eval `scram runtime -sh`
cd /user/tomc/madgraph/oldSetup/genproductions/bin/MadGraph5_aMCatNLO
qstat(){
  if [ -z "$1" ]; then 
    cat /user/$USER/temp/.qstat | grep $USER
  else 
    cat /user/$USER/temp/.qstat | grep $1
  fi
}
source ./gridpack_generation.sh $gridpack $dir cream02
