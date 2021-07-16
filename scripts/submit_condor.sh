#!/bin/bash

input_dataset_list=${1}
year=${2}
custom_eos=${3:-false}
output_eos_dir=${4:-"/eos/uscms/store/user/lnujj/VVjj_aQGC/nanoAOD_skim/Run2016_v7_test"}

cmssw=$(basename $CMSSW_BASE)
cmssw_eos_path="root://cmseos.fnal.gov/${output_eos_dir}/${cmssw}.tgz"

# Logs dir
mkdir -p condor_logs

# make tar send to eos
make_tar.sh
eos root://cmseos.fnal.gov mkdir -p ${output_eos_dir}
xrdcp -f ${cmssw}.tgz ${cmssw_eos_path}

while read -r line
do
  [[ "${line}" == "#"* ]] && continue

  dataset=$(echo ${line} | cut -d '/' -f2)
  [[ "${line}" =~ .*/Run201[6-8].* ]] && dataset=${dataset}_$(echo ${line} | cut -d '/' -f3 | cut -d '-' -f1)
  mkdir -p condor_logs/${dataset}

  if $custom_eos
  then
    list_of_files=($(eos root://cmseos.fnal.gov find -name "*.root" /store/group/lnujj/VVjj_aQGC/custom_nanoAOD/${line}))
    xrd_redirector="root://cmseos.fnal.gov"
  else
    list_of_files=($(dasgoclient --query="file dataset=${line}"))
    xrd_redirector="root://cms-xrd-global.cern.ch/"
  fi

  for input_file in "${list_of_files[@]}"
  do
    # check if already proccessed
    output_file_location=${output_eos_dir}/${dataset}/$(basename ${input_file})
    output_exists=$(eos root://cmseos.fnal.gov ls ${output_file_location} &> /dev/null && echo true || echo false)

    $output_exists && continue

    condor_submit \
      universe=vanilla \
      executable=$(which run_skim.sh) \
      transfer_input=True \
      transfer_output=True \
      stream_error=True \
      stream_output=True \
      log_filename="condor_logs/${dataset}/$(basename ${input_file})" \
      log="/dev/null" \
      output="\$(log_filename).out" \
      error="\$(log_filename).err" \
      transfer_input_files="$(which run_skim.sh)" \
      transfer_output_files="\"\"" \
      -append "arguments = ${cmssw_eos_path} ${xrd_redirector}/${input_file} ${year} ${output_eos_dir}/${dataset}" \
      -append "queue" \
      /dev/null
  done
done < ${input_dataset_list}

exit
