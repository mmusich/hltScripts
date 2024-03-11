#!/usr/bin/env python3
import csv

# copy-paste PS tables from OMS to spreadsheet (incl. PS-column names in first row)
# then export L1T and HLT spreadsheets to CSV files

colNames = []

l1tDict = {}
with open('l1t.csv', newline='') as l1tfile:
    l1treader = csv.reader(l1tfile, delimiter=',')
    for row in l1treader:
        if colNames:
          l1tDict[row[1]] = row[2:]
        else:
          colNames = row[2:]

colPairs = [[colIdx-1, colIdx] for colIdx in range(1, len(colNames))]

colPairs += [[colNames.index('2p0E34'), colNames.index('1p8E34')]]
colPairs += [[colNames.index('2p0E34'), colNames.index('2p0E34_OnlyMuons')]]
colPairs += [[colNames.index('2p0E34'), colNames.index('2p0E34_NoMuShower')]]
colPairs += [[colNames.index('2p0E34'), colNames.index('2p0E34_NoEcalTiming')]]

for colIdx0,colIdx1 in colPairs:
    l1tSeedsDiff = []
    for l1tSeed in l1tDict:
        if l1tDict[l1tSeed][colIdx0] != l1tDict[l1tSeed][colIdx1]:
            l1tSeedsDiff += [f'  {l1tSeed} ({l1tDict[l1tSeed][colIdx0]} -> {l1tDict[l1tSeed][colIdx1]})']
    print(f'Columns: {colNames[colIdx0]} vs {colNames[colIdx1]}')
    for l1tSeedStr in l1tSeedsDiff:
        print(l1tSeedStr)

#hltDict = {}
#with open('hlt.csv', newline='') as hltfile:
#    hltreader = csv.reader(hltfile, delimiter=',')
#    for row in hltreader:
#        try: int(row[2])
#        except: continue
#        hltDict[row[1]] = row[2:]
#
#for colIdx,colName in enumerate(colNames):
#    print(f'Checking column: {colName}')
#    for colIdx2,colName2 in range(colIdx+1,len(colNames)):
#        colName2 = colNames[colIdx2]
#        isSame = True
#        if colIdx2 == colIdx:
#            continue
#        for l1tAlgo in l1tDict:
#            if l1tDict[l1tAlgo][colIdx] != l1tDict[l1tAlgo][colIdx2]:
#                isSame = False
#                break
#        for hltPath in hltDict:
#            if hltDict[hltPath][colIdx] != hltDict[hltPath][colIdx2]:
#                isSame = False
#                break
#        if isSame:
#            print(f' {colName2: <20} is the same as {colName: <20}')
