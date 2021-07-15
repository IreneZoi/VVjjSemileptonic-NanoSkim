#!/usr/bin/env python
import os
import sys
import argparse

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *
from VVjjSemileptonic.NanoSkim.wvAnalysisModule import *
from VVjjSemileptonic.NanoSkim.JetSFMaker import *

parser = argparse.ArgumentParser()

parser.add_argument("-i", type=str, default="",
                    help="input root file, default=%(default)s")

parser.add_argument("-y", type=int, default=2016,
                    help="input file year, default=%(default)s")

parser.add_argument("-t", type=str, default="mc",
                    help="'mc' or else it's data, default=%(default)s")

parser.add_argument("-n", type=int, default=0,
                    help="number of entries, 0 -> all, default=%(default)s")

parser.add_argument("-o", type=str, default="",
                    help="output hist file, same as input if empty, default=%(default)s")

parser.add_argument("-p", type=str, default="no",
                    help="prefetch root file or not, Ture if 'yes' else False, default=%(default)s")

args = parser.parse_args()

input_file = args.i
year = args.y
is_mc = True if args.t == "mc" else False
max_entries = args.n
output_file = os.path.basename(input_file)
prefetch = True if args.p == "yes" else False

print("===> INPUT FILE: " + input_file)
print("===> YEAR: " + str(year))
print("===> IS MC: " + str(is_mc))
print("===> MAX ENTRIES: " + str(max_entries))
print("===> OUTPUT FILE: " + output_file)
print("===> DO PREFETCH: " + str(prefetch))

#input_file = "root://cms-xrd-global.cern.ch//store/data/Run2018A/SingleMuon/NANOAOD/Nano25Oct2019-v1/20000/D03C6AE0-73AD-A940-B8CA-779A621D4853.root"

#input_file = "root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv7/DYJetsToLL_M-50_HT-70to100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/110000/03C532D0-DB79-1F44-AC0C-65A3270BB19C.root"


if year == 2016:
    json_filename="Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt"
    btag_era="Legacy2016"
    btag_sf_filename="DeepCSV_2016LegacySF_V1.csv"

elif year == 2017:
    json_filename="Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt"
    btag_era="2017"
    btag_sf_filename="DeepCSV_94XSF_V5_B_F.csv"

elif year == 2018:
    json_filename="Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt"
    btag_era="2018"
    btag_sf_filename="DeepCSV_102XSF_V2.csv"

else:
    print("===> Incorrect Year: " + year)
    print("===> Exiting")
    sys.exit()

print("===> JSON File: " + json_filename)
print("===> BTAG ERA: " + btag_era)
print("===> BTAG SF FILE: " + btag_sf_filename)

json_filename = os.environ['CMSSW_BASE'] + "/src/VVjjSemileptonic/NanoSkim/data/" + json_filename

# btag SF module
if is_mc:
    btagSF_ = btagSFProducer(btag_era, algo="deepcsv",
                             selectedWPs=['L','M','T','shape_corr'],
                             sfFileName=btag_sf_filename)
    btagSF_.inputFilePath = os.environ['CMSSW_BASE'] + "/src/VVjjSemileptonic/NanoSkim/data/btag/"
    btagSF = lambda: btagSF_

# PUID SF
if is_mc:
    puidSF = lambda: JetSFMaker(str(year))

jetmetCorrector = createJMECorrector(isMC=is_mc, dataYear=year, jesUncert="Merged", jetType = "AK4PFchs")
fatJetCorrector = createJMECorrector(isMC=is_mc, dataYear=year, jesUncert="Merged", jetType = "AK8PFPuppi")

if not is_mc:
    p = PostProcessor(".", [input_file], None, None,
                      [wvAnalysisModule(), jetmetCorrector(), fatJetCorrector()],
                      provenance=False, fwkJobReport=False, jsonInput=json_filename,
                      maxEntries=max_entries, haddFileName=output_file, prefetch=prefetch)

else:
    p = PostProcessor(".", [input_file], None, None,
                      [wvAnalysisModule(), jetmetCorrector(), fatJetCorrector(), btagSF(), puidSF()],
                      provenance=True, fwkJobReport=False,
                      maxEntries=max_entries, haddFileName=output_file, prefetch=prefetch)

p.run()
print "DONE"
