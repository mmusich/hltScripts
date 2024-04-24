#!/bin/bash

filePattern=/eos/cms/tier0/store/data/Run2024C/EphemeralHLTPhysics*/RAW/v*/*/379/866/*/*.root

for file_i in $(ls ${filePattern}); do
  echo "${file_i}"
  edmLumisInFiles.py "${file_i}"
  echo "-----------------------"
done
unset file_i

# grep -B 1 '126, 126' list.txt
