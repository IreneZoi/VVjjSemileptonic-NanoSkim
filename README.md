# nanoAOD_vvVBS
nanoAOD skiming code for vv semi-leptonic VBS studies

## Code setup

1. Step: 1: Get CMSSW release

   ```bash
   cmsrel CMSSW_10_2_22
   cd CMSSW_10_2_22/src
   cmsenv
   ```
   
2. Step: 2: Get nanoAODTools

   ```bash
   git clone git@github.com:cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
   cd PhysicsTools/NanoAODTools
   git checkout 079c9e18c14c9d71ffe6d0cc4b42f15d97c29efc
   cd -
   ```
   
3. Step: 3: Get analysis repository

   ```bash
   git clone git@github.com:singh-ramanpreet/VVjjSemileptonic-NanoSkim.git VVjjSemileptonic/NanoSkim
   scram b
   ```

4. Step: 4: interactive running

   ```bash
   python VVjjSemileptonic/NanoSkim/scripts/post_proc.py
   ```
   
5. batch job submission.
    ```bash
    cd $CMSSW_BASE/src/PhysicsTools/NanoAODTools/python/postprocessing/analysis/nanoAOD_vvVBS
    # Edit condor_setup.py, then
    python condor_setup.py
    # Set proxy before submitting the condor jobs.
    voms-proxy-init -voms cms --valid 200:00
    condor_submit <Files-created-from-above-command>.jdl
    ```


