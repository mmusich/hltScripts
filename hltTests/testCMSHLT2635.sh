#!/bin/bash

hltConfigFromDB --configName /users/missirol/test/dev/CMSSW_13_0_0/CMSHLT_2635/Test03/HLT > diele0.py

cp diele0.py diele1.py
cat <<@EOF >> diele1.py

elenames = [
  'Ele4',
  'Ele4p5',
  'Ele5',
  'Ele5p5',
  'Ele6',
  'Ele6p5',
  'Ele7',
  'Ele7p5',
  'Ele8',
  'Ele8p5',
  'Ele9',
  'Ele9p5',
  'Ele10',
]

for foo in elenames:
  s1 = getattr(process, 'hltDouble'+foo+'eta1p22PMmMax6MassFilter').dumpPython()
  s2 = getattr(process, 'hltDouble'+foo+'eta1p22DZPMmMax6MassFilter').dumpPython()
  s3 = getattr(process, 'hltDouble'+foo+'eta1p22ValidHits10PMmMax6MassFilter').dumpPython()
  print(foo, s1 == s2, s1 == s3)
  if s1 != s2 or s1 != s3:
    raise RuntimeError(foo)
@EOF

python3 diele1.py

elenames=(
  Ele4
  Ele4p5
  Ele5
  Ele5p5
  Ele6
  Ele6p5
  Ele7
  Ele7p5
  Ele8
  Ele8p5
  Ele9
  Ele9p5
  Ele10
)

cp diele0.py diele11.py
for foo in "${elenames[@]}"; do
  echo "1 ${foo}"
  sed -i "s|hltDouble${foo}eta1p22DZPMmMax6MassFilter|hltDouble${foo}eta1p22PMmMax6MassFilter|g" diele11.py
  sed -i "s|hltDouble${foo}eta1p22ValidHits10PMmMax6MassFilter|hltDouble${foo}eta1p22PMmMax6MassFilter|g" diele11.py
done
unset foo

edmConfigDump diele11.py > diele11_dump.py

###########################################

cp diele0.py diele2.py
cat <<@EOF >> diele2.py

rmPaths = set()

del process.HLTEndSequence

for pathName in process.paths_():
  if '___XXX___' not in pathName:
    rmPaths.add(pathName)

for rmPath in rmPaths:
  process.__delattr__(rmPath)
@EOF

for foo in "${elenames[@]}"; do
  echo "2 ${foo}"
  cp diele2.py diele_"${foo}".py
  sed -i "s|___XXX___|${foo}_|g" diele_"${foo}".py
  edmConfigDump --prune diele_"${foo}".py > diele_"${foo}"_dump.py
  cp diele_"${foo}"_dump.py diele_"${foo}"_toEle4_dump.py
  sed -i "s|${foo}eta|Ele4eta|g" diele_"${foo}"_toEle4_dump.py
  sed -i "s|${foo}_|Ele4_|g" diele_"${foo}"_toEle4_dump.py
  diff diele_Ele4_dump.py diele_"${foo}"_toEle4_dump.py
  rm -rf diele_"${foo}".py
done
unset foo
