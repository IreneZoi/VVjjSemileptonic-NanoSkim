#!/bin/bash

cmssw_path=${1}
input_file=${2}
year=${3}
eos_output_dir=${4}

#determine output name from input file
output=$(basename ${input_file})

# Get cmssw tar
cmssw=$(basename ${cmssw_path})
xrdcp ${cmssw_path} ${cmssw}

source /cvmfs/cms.cern.ch/cmsset_default.sh

tar -xf ${cmssw}
rm ${cmssw}
cd ${cmssw%.tgz}/src/

scramv1 b ProjectRename
eval `scram runtime -sh`

type=$(python -c "import ROOT;
f=ROOT.TFile.Open('$input_file');
t=f.Get('Runs');
print('mc' if t.GetBranchStatus('genEventSumw') else 'data')")

post_proc.py -i ${input_file} -y ${year} -t ${type} -n 0 -p yes

echo "===> copying output root file to eos ..." 

xrdfs root://cmseos.fnal.gov/ mkdir -p ${eos_output_dir}
xrdcp -f ${output} root://cmseos.fnal.gov/${eos_output_dir}/${output}

cd ${_CONDOR_SCRATCH_DIR}
rm -rf *
