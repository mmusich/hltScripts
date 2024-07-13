#!/bin/bash

for name in Legacy CUDA AlpakaSerialSync AlpakaGPU; do
  for nnn in {00..09}; do
    ./test_hcalAlpaka_debugEvent_printHBHERecHits.py -v 10 \
      -i hltSingleEle8_try${nnn}_${name}.root \
       > hltSingleEle8_try${nnn}_${name}.txt 2> /dev/null
    echo "========================================"
    echo "${name} (${nnn} vs 00)"
    echo "========================================"
    diff -q hltSingleEle8_try00_${name}.txt hltSingleEle8_try${nnn}_${name}.txt
  done
  unset nnn
done
unset name

runComparison(){
  echo "========================================"
  echo "$1 vs $2"
  echo "========================================"
  hltDiff -o hltSingleEle8_try00_"${1}".root -n hltSingleEle8_try00_"${2}".root 2> /dev/null
  diff    -q hltSingleEle8_try00_"${1}".txt     hltSingleEle8_try00_"${2}".txt
}

runComparison Legacy AlpakaSerialSync
runComparison AlpakaSerialSync AlpakaGPU
runComparison CUDA AlpakaGPU
