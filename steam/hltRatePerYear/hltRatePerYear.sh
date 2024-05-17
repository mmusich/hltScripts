#!/bin/bash

jobLabel=231217_12h17h_

# timestamp: start
date

# Fills selected in Sanu's latest plots
./hltRatePerYear.py -y 2016 -f 5257 -o "${jobLabel}"_2016_5257.json
./hltRatePerYear.py -y 2017 -f 6325 -o "${jobLabel}"_2017_6325.json
./hltRatePerYear.py -y 2018 -f 7321 -o "${jobLabel}"_2018_7321.json
./hltRatePerYear.py -y 2022 -f 8489 -o "${jobLabel}"_2022_8489.json
./hltRatePerYear.py -y 2023 -f 9045 -o "${jobLabel}"_2023_9045.json

# The Top-10 Fills of every year ranked by "-s".
# Notes.
#  - Use '-s "peak_lumi"' to rank Fills by highest peak instantaneous luminosity.
#  - Option "-n N" denotes the number of selected Fills
#    (the top-N Fills ranked by highest "-s")

# The 10 Fills of every year with the largest delivered integrated luminosity
./hltRatePerYear.py --fill-hours-min 11 --fill-hours-max 17 -n 10 -y 2015 2016 2017 2018 2022 2023 \
  -o "${jobLabel}"_byDeliLumi.json -s "delivered_lumi"

# The 10 Fills of every year with the highest peak instantaneous luminosity
./hltRatePerYear.py --fill-hours-min 11 --fill-hours-max 17 -n 10 -y 2015 2016 2017 2018 2022 2023 \
  -o "${jobLabel}"_byPeakLumi.json -s "peak_lumi"

# timestamp: finish
date
