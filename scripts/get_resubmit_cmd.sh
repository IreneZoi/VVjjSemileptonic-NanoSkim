#!/bin/bash

ref_jdl=$1
file_size_check=${2:-false}

temp_file="test_condor"

echo ""
echo "Just doing the dry run in temp file \"$temp_file\""
echo ""
condor_submit $ref_jdl --dry-run $temp_file

proc_ids=($(grep "ProcId=" $temp_file | cut -d '=' -f2))
out_dir=($(grep "Args=" $temp_file | cut -d '=' -f2- | cut -d '"' -f2 | cut -d ' ' -f2))
out_file=($(grep "Args=" $temp_file | cut -d '=' -f2- | cut -d '"' -f2 | cut -d ' ' -f1 | rev | cut -d '/' -f1 | rev))

resubmit_list=""

for ((i=0;i<${#proc_ids[@]};++i))
do
  #echo ${proc_ids[i]}
  file_exists=$(eos root://cmseos.fnal.gov ls ${out_dir[i]}/${out_file[i]/.root/_SkimHadd.root} &> /dev/null && echo true || echo false)

  # in bytes
  if $file_size_check
  then
    file_size=$(eos root://cmseos.fnal.gov stat ${out_dir[i]}/${out_file[i]/.root/_SkimHadd.root} | grep -Eo "Size: ([0-9]+)" | cut -d ' ' -f2 )
  fi

  if $file_exists && $file_size_check
  then
    if (( $file_size < 1001 ))
    then
      echo "procId: ${proc_ids[i]} file exists, but small file size of $file_size"
      echo "adding to the re-submit list"
      resubmit_list+="${proc_ids[i]},"
    fi
  fi

  if ! $file_exists
  then
    echo "procId: ${proc_ids[i]} file does not exists"
    echo "adding to the re-submit list"
    resubmit_list+="${proc_ids[i]},"
  fi
done

resubmit_list=${resubmit_list%,}
echo ""
echo "now resubmit using"
echo ""
echo "condor_submit $ref_jdl noop_job=\\!stringListMember\\(\\\"\\\$\\(ProcId\\)\\\",\\\"${resubmit_list[@]}\\\"\\)"

rm $temp_file

exit
