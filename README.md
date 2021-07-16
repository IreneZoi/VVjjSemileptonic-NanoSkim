# VVjjSemileptonic-NanoSkim
nanoAOD skiming code for VVjj Semileptonic VBS studies

## Code setup

```bash
cmsrel CMSSW_10_2_22
cd CMSSW_10_2_22/src
cmsenv
git clone git@github.com:cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
cd PhysicsTools/NanoAODTools
git checkout 079c9e18c14c9d71ffe6d0cc4b42f15d97c29efc
cd -
git clone git@github.com:singh-ramanpreet/VVjjSemileptonic-NanoSkim.git VVjjSemileptonic/NanoSkim
scram b
```


## Interactive running

```
post_proc.py -i <input root file> -y <year, 2016, 2017 or 2018> -t <mc or data> -n <number of events, 0 for all> -p <prefetch input file yes or no> -o <Optional, output filename>
```
   
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
```bash
submit_condor.sh ../inputs/sample_list_v7_2016_campaign.dat 2016 false /eos/uscms/store/...
```
