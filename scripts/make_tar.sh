#!/bin/bash

cmssw=$(basename $CMSSW_BASE)

rm -f ${cmssw}.tgz

tar --exclude-vcs -zcf ${cmssw}.tgz -C $CMSSW_BASE/.. \
    ${cmssw}/lib \
    ${cmssw}/bin \
    ${cmssw}/python \
    ${cmssw}/config \
    ${cmssw}/.SCRAM \
    ${cmssw}/src \
    --exclude=${cmssw}.tgz \
    --exclude="*condor_logs*"
