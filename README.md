# VVjjSemileptonic-NanoSkim
nanoAOD skiming code for VVjj Semileptonic VBS studies

## Code setup

```bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
cmsrel CMSSW_10_2_22
cd CMSSW_10_2_22/src
cmsenv
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
cd PhysicsTools/NanoAODTools
git checkout 079c9e18c14c9d71ffe6d0cc4b42f15d97c29efc
cd -
git clone https://github.com/singh-ramanpreet/VVjjSemileptonic-NanoSkim.git VVjjSemileptonic/NanoSkim
scram b
```


## Interactive running

```
voms-proxy-init -voms cms --valid 192:00
scripts/post_proc.py -i <input root file> -y <year, 2016, 2017 or 2018> -t <mc or data> -n <number of events, 0 for all> -p <prefetch input file yes or no> -o <Optional, output filename>
```

example with MC:
```
scripts/post_proc.py -i root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv7/WWW_4F_DiLeptonFilter_TuneCUETP8M1_13TeV-amcatnlo-pythia8/NANOAODSIM/PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/110000/14F2B4F9-20E2-E347-93BB-7FF7210A13FA.root  -y 2016 -t mc -n 1000 -p no -o test
```
The input root file was found with:
```
dasgoclient -query="file dataset=/WWW_4F_DiLeptonFilter_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM"
```
from the list in ```inputs/sample_list_v7_2016_campaign.dat```

NB: the ```-o``` option is currently hardcoded to taking the same as the input.

### Condor job submission

```bash
# setup proxy
voms-proxy-init -voms cms --valid 192:00
```

#### Submission script arguments,
```bash
cd VVjjSemileptonic/NanoSkim/submit
submit_condor.sh <input dataset list file> <year> <true/false whether input file is custom nanoaod> <output directory>
```

##### Example,
(enter a new line in the list file!)

```bash
submit_condor.sh ../inputs/sample_list_v7_2016_campaign.dat 2016 false /eos/uscms/store/...
```

My example
```
submit_condor.sh testinput.dat 2016 false /eos/uscms/store/user/izoi/VBS_nanoskim/
```
