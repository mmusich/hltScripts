#!/bin/bash

cat <<@EOF > tmp.txt
370293:207:367006439
370293:194:334113735
370293:220:396761674
370293:207:365580932
370293:260:488436515
370293:200:348164653
370293:252:470807150
370293:211:375447299
370293:236:434278658
370293:237:436488122
370293:252:469996299
370293:240:445609979
370293:224:407832572
370293:225:409582518
370293:251:467913657
370293:261:489982122
370293:247:460307886
370293:217:390217376
370293:179:299216561
370293:200:348713776
370293:214:381999164
370293:217:390016919
370293:258:483622135
@EOF

NEVTMAX=$(cat tmp.txt | wc -l)

edmPickEvents.py "/EphemeralHLTPhysics0/Run2023D-v1/RAW" tmp.txt --runInteractive --maxEventsInteractive "${NEVTMAX}" --output eph0
edmPickEvents.py "/EphemeralHLTPhysics1/Run2023D-v1/RAW" tmp.txt --runInteractive --maxEventsInteractive "${NEVTMAX}" --output eph1
edmPickEvents.py "/EphemeralHLTPhysics2/Run2023D-v1/RAW" tmp.txt --runInteractive --maxEventsInteractive "${NEVTMAX}" --output eph2
edmPickEvents.py "/EphemeralHLTPhysics3/Run2023D-v1/RAW" tmp.txt --runInteractive --maxEventsInteractive "${NEVTMAX}" --output eph3
edmPickEvents.py "/EphemeralHLTPhysics4/Run2023D-v1/RAW" tmp.txt --runInteractive --maxEventsInteractive "${NEVTMAX}" --output eph4
edmPickEvents.py "/EphemeralHLTPhysics5/Run2023D-v1/RAW" tmp.txt --runInteractive --maxEventsInteractive "${NEVTMAX}" --output eph5
edmPickEvents.py "/EphemeralHLTPhysics6/Run2023D-v1/RAW" tmp.txt --runInteractive --maxEventsInteractive "${NEVTMAX}" --output eph6
edmPickEvents.py "/EphemeralHLTPhysics7/Run2023D-v1/RAW" tmp.txt --runInteractive --maxEventsInteractive "${NEVTMAX}" --output eph7
