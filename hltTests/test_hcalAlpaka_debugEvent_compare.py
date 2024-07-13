#!/usr/bin/env python3
import ROOT
import sys

f0 = ROOT.TFile(sys.argv[1])
e0 = f0.Get('Events')

f1 = ROOT.TFile(sys.argv[2])
e1 = f1.Get('Events')
e0.AddFriend(e1,'alt')

hltHbhereco = 'HBHERecHitsSorted_hltHbhereco__HLTX.obj.obj'

energy = f'{hltHbhereco}.energy()'
detId = f'{hltHbhereco}.id_.id_'

scanFormat = 'colsize=30 precision=10'

scanVars = f'{energy}:alt.{energy}:{detId}:alt.{detId}'

scanSelec1 = f'{detId} != alt.{detId}' # && {energy}>0 && alt.{energy}>0'
print('-'*50)
print(' '*10, 'different DetIds')
print('-'*50)
e0.Scan(scanVars, scanSelec1, scanFormat)

scanSelec2 = f'({energy}-alt.{energy})>(0.0001*{energy}) && {detId}==alt.{detId}' # && {energy}>0 && alt.{energy}>0'
print('-'*50)
print(' '*10, 'different energy (same DetIds)')
print('-'*50)
e0.Scan(scanVars, scanSelec2, scanFormat)
