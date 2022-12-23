#!/usr/bin/env python3
'''
./showL1TMuonShowers.py -i $(xrootd_server cern)/store/data/Run2022F/Muon/AOD/PromptReco-v1/000/361/957/00000/1cb14e07-d436-4150-8891-a62c1e53e8fe.root -v 10 -n -1 > data.txt

./showL1TMuonShowers.py -i $(xrootd_server cern)/store/mc/Run3Summer22DRPremix/HTo2LongLivedTo4b_MH-1000_MFF-450_CTau-100000mm_TuneCP5_13p6TeV_pythia8/AODSIM/124X_mcRun3_2022_realistic_v12-v2/2810000/8f27aed2-f136-41f6-b40e-54e6b0092015.root -v 10 -n -1 > mc.txt
'''
import os
import argparse
import glob
import ROOT

from DataFormats.FWLite import Runs, Events, Handle

### Utilities
def colored_text(txt, keys=[]):
    return txt
#    _tmp_out = ''
#    for _i_tmp in keys:
#        _tmp_out += '\033['+_i_tmp+'m'
#    _tmp_out += txt
#    if len(keys) > 0: _tmp_out += '\033[0m'
#    return _tmp_out

### Event Analysis
def getMuonShowers(label):
  handle = Handle('BXVector<l1t::MuonShower>')
  event.getByLabel(label, handle)
  return handle.product()

def analyse_event(event, verbosity=0):

    runNumber = event.eventAuxiliary().run()
    lumiBlockNumber = event.eventAuxiliary().luminosityBlock()
    eventNumber = event.eventAuxiliary().event()

#    if not (runNumber == 361957 and lumiBlockNumber == 222 and eventNumber == 354121384):
#      return

    print('-'*50)
    print('Run             =', runNumber)
    print('LuminosityBlock =', lumiBlockNumber)
    print('Event           =', eventNumber)
    print('-'*50)

    muShBxColl = getMuonShowers('gtStage2Digis:MuonShower')

    for bx in range(muShBxColl.getFirstBX(), muShBxColl.getLastBX() + 1):
      print(f'(bx = {bx:d})')
      for mush_idx in range(muShBxColl.size(bx)):
        mush = muShBxColl.at(bx, mush_idx)
        print(f'  [{mush_idx:d}]')
        print(f'    pt   = {mush.pt()}')
        print(f'    eta  = {mush.eta()}')
        print(f'    phi  = {mush.phi()}')
        print(f'    mass = {mush.mass()}')
        print(f'    musOutOfTime0 = {mush.musOutOfTime0()}')
        print(f'    musOutOfTime1 = {mush.musOutOfTime1()}')
        print(f'    isOneNominalInTime = {mush.isOneNominalInTime()}')
        print(f'    isOneTightInTime   = {mush.isOneTightInTime()}')
        print(f'    longLived          = {mush.longLived()}')
        print(f'    hwEta              = {mush.hwEta()}')
        print(f'    hwIso              = {mush.hwIso()}')
        print(f'    hwPhi              = {mush.hwPhi()}')
        print(f'    hwPt               = {mush.hwPt()}')
        print(f'    hwQual             = {mush.hwQual()}')
        print(f'    numberOfDaughters  = {mush.numberOfDaughters()}')

#    if verbosity >= 0:
#      TriggerResultsInputTagLabel = 'TriggerResults'
#      TriggerResultsHandle = Handle('edm::TriggerResults')
#      event.getByLabel(TriggerResultsInputTagLabel, TriggerResultsHandle)
#      TriggerResults = TriggerResultsHandle.product()
#      triggerNames = event.object().triggerNames(TriggerResults).triggerNames()
#      print('\nTriggerResults = "'+TriggerResultsInputTagLabel+'"'+f' [{len(triggerNames)} Paths]')
#
#      if verbosity >= 1:
#        print('')
#        for triggerNameIdx, triggerName in enumerate(triggerNames):
#          triggerNameIdxStr = '['+str(triggerNameIdx)+']'
#          print(f'{triggerNameIdxStr:>6} | {int(TriggerResults.accept(triggerNameIdx))} | {str(triggerName)}')
#
#    hltTriggerSummaryInputTagLabel = 'hltTriggerSummaryAOD'
#    hltTriggerSummaryHandle = Handle('trigger::TriggerEvent')
#    event.getByLabel(hltTriggerSummaryInputTagLabel, hltTriggerSummaryHandle)
#    hltTriggerSummary = hltTriggerSummaryHandle.product()
#
#    trigProcessName = hltTriggerSummary.usedProcessName()
#    trigSummarySizeFilters = hltTriggerSummary.sizeFilters()
#    trigObjects = hltTriggerSummary.getObjects()
#
#    if verbosity >= 0:
#      print('\n'+'-'*20)
#      print('\nTriggerEvent = "'+hltTriggerSummaryInputTagLabel+'::'+trigProcessName+'"'+f' [{trigSummarySizeFilters} Filters, {len(trigObjects)} TriggerObjects]')
#
#      if verbosity >= 2:
#        print('')
#        for trigFilterIdx in range(trigSummarySizeFilters):
#          trigFilterTag = hltTriggerSummary.filterTag(trigFilterIdx)
#          trigFilterKeys = hltTriggerSummary.filterKeys(trigFilterIdx)
#          trigFilterIds = hltTriggerSummary.filterIds(trigFilterIdx)
#          trigFilterIdxStr = '['+str(trigFilterIdx)+']'
#
#          if verbosity < 3:
#            print(f'{trigFilterIdxStr:>7} {trigFilterTag.encode()} ({len(trigFilterKeys)} TriggerObjects)')
#          else:
#            print('')
#            print(f'{trigFilterIdxStr:>7} {trigFilterTag.encode()} ({len(trigFilterKeys)} TriggerObjects)')
#            for trigFilterKeyIdx, trigFilterKey in enumerate(trigFilterKeys):
#              trigObj, trigObjId = trigObjects[trigFilterKey], trigFilterIds[trigFilterKeyIdx]
#              trigObjStr = f'pt = {trigObj.pt(): >8.3f}, eta = {trigObj.eta(): >-6.3f}, phi = {trigObj.phi(): >-6.3f}, id = {trigObj.id(): >-3d}'
#              trigFilterKeyStr = '['+str(trigFilterKey)+']'
#              print(f'        {trigFilterKeyStr:>4} FilterId = {trigObjId: >-3d} : '+trigObjStr)

### main
if __name__ == '__main__':
   ### args
   parser = argparse.ArgumentParser()

   parser.add_argument('-i', '--inputs', dest='inputs', required=True, nargs='+', default=None,
                       help='path to input .root file(s)')

#   parser.add_argument('-o', '--output', dest='output', action='store', default=None,
#                       help='path to output .root file')

   parser.add_argument('-e', '--every', dest='every', action='store', type=int, default=1e2,
                       help='show progress of processing every N events')

   parser.add_argument('-s', '--skipEvents', dest='skipEvents', action='store', type=int, default=0,
                       help='index of first event to be processed (inclusive)')

   parser.add_argument('-n', '--maxEvents', dest='maxEvents', action='store', type=int, default=-1,
                       help='maximum number of events to be processed (inclusive)')

   parser.add_argument('-v', '--verbosity', dest='verbosity', action='store', type=int, default=0,
                       help='level of verbosity')

   opts, opts_unknown = parser.parse_known_args()

   log_prx = os.path.basename(__file__)+' -- '

   ### args validation
   INPUT_FILES = []
   for i_inpf in opts.inputs:
     i_inpf_ls = glob.glob(i_inpf)
     if len(i_inpf_ls) == 0:
       i_inpf_ls = [i_inpf]
     for i_inpf_2 in i_inpf_ls:
       i_inpfile = os.path.abspath(os.path.realpath(i_inpf_2)) if os.path.isfile(i_inpf_2) else i_inpf_2
       INPUT_FILES += [i_inpfile]

   INPUT_FILES = sorted(list(set(INPUT_FILES)))

   if len(INPUT_FILES) == 0:
     raise RuntimeError(log_prx+'empty list of input files [-i]')

#   if (opts.output is not None) and os.path.exists(opts.output):
#     raise RuntimeError(log_prx+'target path to output .root file already exists [-o]: '+opts.output)

   SHOW_EVERY = opts.every
   if SHOW_EVERY <= 0:
     print(log_prx+'invalid (non-positive) value for option "-e/--every" ('+str(SHOW_EVERY)+'), value will be changed to 100')
     SHOW_EVERY = 1e2

   if len(opts_unknown) > 0:
     raise RuntimeError(log_prx+'unrecognized command-line arguments: '+str(opts_unknown))

   ## histograms
   nEvtProcessed = 0

   for i_inpf in INPUT_FILES:

       if opts.verbosity >= 10:
         print(colored_text('[input]', ['1','94']), os.path.relpath(i_inpf))

       try:
         events = Events(i_inpf)
       except:
         print(log_prx+'target TFile does not contain a TTree named "Events" (file will be ignored) [-t]: '+i_inpf)
         continue

       skipEvents = 0 if opts.skipEvents < 0 else opts.skipEvents

       eventIndex = 0
       for event in events:
         if (eventIndex < skipEvents) or ((opts.maxEvents >= 0) and (nEvtProcessed >= opts.maxEvents)):
           continue

         if (not (eventIndex % SHOW_EVERY)) and (eventIndex > 0):
           print('-'*10)
           print('Event #'+str(eventIndex))

         analyse_event(event=event, verbosity=opts.verbosity)
         nEvtProcessed += 1
         eventIndex += 1

   print('='*30)
   print(colored_text('Events processed =', ['1']), nEvtProcessed)
