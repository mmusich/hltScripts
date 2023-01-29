#!/usr/bin/env python3
"""
TMPURL=https://cmssdt.cern.ch/SDT/jenkins-artifacts/pull-request-integration/PR-9fbb71/30232/runTheMatrix-results
auth-get-sso-cookie -o .tmp_ssocookie.txt -u "${TMPURL}"
wget --load-cookies .tmp_ssocookie.txt -r -np -nH -A .log "${TMPURL}"
rm -f .tmp_ssocookie.txt

mkdir base
TMPURL=https://cmssdt.cern.ch/SDT/jenkins-artifacts/ib-baseline-tests/CMSSW_13_0_X_2023-01-28-1100/el8_amd64_gcc11/-GenuineIntel/matrix-results
auth-get-sso-cookie -o .tmp_ssocookie.txt -u "${TMPURL}"
wget --load-cookies .tmp_ssocookie.txt -r -np -nH -A .log "${TMPURL}"
rm -f .tmp_ssocookie.txt
cd ..

./checkMatrixLogs.py
"""
import os
import glob

def dirname(fpath):
  return '/'.join(os.path.abspath(fpath).split('/')[:-2])

def filename(fpath):
  return '/'.join(os.path.abspath(fpath).split('/')[-2:])

if __name__ == '__main__':

  f2_dir = 'base/SDT/jenkins-artifacts/ib-baseline-tests/CMSSW_13_0_X_2023-01-28-1100/el8_amd64_gcc11/-GenuineIntel/matrix-results'

  f1 = glob.glob('SDT/jenkins-artifacts/pull-request-integration/PR-9fbb71/30232/runTheMatrix-results/*/step*log')
  f2 = glob.glob(f2_dir+'/*/step*log')

  tot_diff = 0

  for file1_i in f1:
    f1_d = dirname(file1_i)
    f1_f = filename(file1_i)

    file2_i = f2_dir+'/'+f1_f

    if file2_i not in f2:
      raise RuntimeError(file2_i)

    l1 = open(file1_i).readlines()
    l2 = open(file2_i).readlines()

    if len(l1) != len(l2):
      print(f'{len(l1): >10d} {len(l2): >10d} {f1_f}')

    tot_diff += len(l1) - len(l2)

  print(tot_diff)
