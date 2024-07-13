#!/bin/bash

cat <<@EOF > tmp.txt
381065:449:880739293
381065:449:881019838
381065:449:881085666
381065:450:883887053
381065:451:885604891
381065:453:889740949
381065:454:892153529
381065:457:899755459
381065:458:901422780
@EOF

NEVTMAX=$(cat tmp.txt | wc -l)

edmPickEvents.py "/EphemeralHLTPhysics0/Run2024E-v1/RAW" tmp.txt --runInteractive --maxEventsInteractive "${NEVTMAX}" --output eph0
edmPickEvents.py "/EphemeralHLTPhysics1/Run2024E-v1/RAW" tmp.txt --runInteractive --maxEventsInteractive "${NEVTMAX}" --output eph1
edmPickEvents.py "/EphemeralHLTPhysics2/Run2024E-v1/RAW" tmp.txt --runInteractive --maxEventsInteractive "${NEVTMAX}" --output eph2
edmPickEvents.py "/EphemeralHLTPhysics3/Run2024E-v1/RAW" tmp.txt --runInteractive --maxEventsInteractive "${NEVTMAX}" --output eph3
edmPickEvents.py "/EphemeralHLTPhysics4/Run2024E-v1/RAW" tmp.txt --runInteractive --maxEventsInteractive "${NEVTMAX}" --output eph4
edmPickEvents.py "/EphemeralHLTPhysics5/Run2024E-v1/RAW" tmp.txt --runInteractive --maxEventsInteractive "${NEVTMAX}" --output eph5
edmPickEvents.py "/EphemeralHLTPhysics6/Run2024E-v1/RAW" tmp.txt --runInteractive --maxEventsInteractive "${NEVTMAX}" --output eph6
edmPickEvents.py "/EphemeralHLTPhysics7/Run2024E-v1/RAW" tmp.txt --runInteractive --maxEventsInteractive "${NEVTMAX}" --output eph7
