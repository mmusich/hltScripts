#!/bin/bash

wfs=(
  standard
  highstats
  pileup
  generator
  extendedgen
  production
  ged
  cleanedupgrade
  gpu
  2017
  2026
  machine
  premix
  nano
)

for wf in "${wfs[@]}"; do

  echo "${wf}"

  runTheMatrix.py -nel all -w "${wf}" > wf_"${wf}".txt

#  grep -inr relval2023 wf_${wf}.txt | grep -v _2023_ | grep -v _2024_ | grep -v _hlt_relval > wf_${wf}_test1.txt
#  grep -inr relval2022 wf_${wf}.txt | grep -v _2022_ > wf_${wf}_test2.txt

done
unset wf
