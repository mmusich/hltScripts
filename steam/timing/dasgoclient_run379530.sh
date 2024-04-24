#!/bin/bash

# Run 379530, LS 465-467

rm -f filelist_run379530.txt
touch filelist_run379530.txt

for lsNum in {465..467}; do
  for pdIdx in {0..7}; do
    cmd="file run=379530 lumi=${lsNum} dataset=/EphemeralHLTPhysics${pdIdx}/Run2024C-v1/RAW"
    echo ${cmd}
    dasgoclient -query "${cmd}" >> filelist_run379530.txt
  done; unset pdIdx
done; unset lsNum
