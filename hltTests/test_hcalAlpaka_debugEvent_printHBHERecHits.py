#!/usr/bin/env python3
import os
import argparse
import glob
import ROOT

from DataFormats.FWLite import Runs, Events, Handle

def analyse_event(event, verbosity=0):

    if verbosity >= 0:
      print('-'*50)
      print('Run             =', event.eventAuxiliary().run())
      print('LuminosityBlock =', event.eventAuxiliary().luminosityBlock())
      print('Event           =', event.eventAuxiliary().event())
      print('-'*50)

    ## TriggerResults
    if verbosity >= 20:
      TriggerResultsInputTagLabel = 'TriggerResults'
      TriggerResultsHandle = Handle('edm::TriggerResults')
      event.getByLabel(TriggerResultsInputTagLabel, TriggerResultsHandle)
      TriggerResults = TriggerResultsHandle.product()
      triggerNames = event.object().triggerNames(TriggerResults).triggerNames()
      print('\nTriggerResults = "'+TriggerResultsInputTagLabel+'"'+f' [{len(triggerNames)} Paths]')

      if verbosity >= 1:
        print('')
        for triggerNameIdx, triggerName in enumerate(triggerNames):
          triggerNameIdxStr = '['+str(triggerNameIdx)+']'
          print(f'{triggerNameIdxStr:>6} | {int(TriggerResults.accept(triggerNameIdx))} | {str(triggerName)}')

    ## TriggerEvent
    if verbosity >= 30:
      hltTriggerSummaryInputTagLabel = 'hltTriggerSummaryAOD'
      hltTriggerSummaryHandle = Handle('trigger::TriggerEvent')
      event.getByLabel(hltTriggerSummaryInputTagLabel, hltTriggerSummaryHandle)
      hltTriggerSummary = hltTriggerSummaryHandle.product()
  
      trigProcessName = hltTriggerSummary.usedProcessName()
      trigSummarySizeFilters = hltTriggerSummary.sizeFilters()
      trigObjects = hltTriggerSummary.getObjects()

      print('\n'+'-'*20)
      print('\nTriggerEvent = "'+hltTriggerSummaryInputTagLabel+'::'+trigProcessName+'"'+f' [{trigSummarySizeFilters} Filters, {len(trigObjects)} TriggerObjects]')

      if verbosity >= 2:
        print('')
        for trigFilterIdx in range(trigSummarySizeFilters):
          trigFilterTag = hltTriggerSummary.filterTag(trigFilterIdx)
          trigFilterKeys = hltTriggerSummary.filterKeys(trigFilterIdx)
          trigFilterIds = hltTriggerSummary.filterIds(trigFilterIdx)
          trigFilterIdxStr = '['+str(trigFilterIdx)+']'

          if verbosity < 3:
            print(f'{trigFilterIdxStr:>7} {trigFilterTag.encode()} ({len(trigFilterKeys)} TriggerObjects)')
          else:
            print('')
            print(f'{trigFilterIdxStr:>7} {trigFilterTag.encode()} ({len(trigFilterKeys)} TriggerObjects)')
            for trigFilterKeyIdx, trigFilterKey in enumerate(trigFilterKeys):
              trigObj, trigObjId = trigObjects[trigFilterKey], trigFilterIds[trigFilterKeyIdx]
              trigObjStr = f'pt = {trigObj.pt(): >8.3f}, eta = {trigObj.eta(): >-6.3f}, phi = {trigObj.phi(): >-6.3f}, id = {trigObj.id(): >-3d}'
              trigFilterKeyStr = '['+str(trigFilterKey)+']'
              print(f'        {trigFilterKeyStr:>4} FilterId = {trigObjId: >-3d} : '+trigObjStr)

    ## HBHERecHits
    if verbosity >= 0:
      for hltHcalRecHitsLabel in [
        'hltHbhereco',
      ]:
        print('\n'+'-'*10)
        hltHcalRecHitsHandle = Handle('edm::SortedCollection<HBHERecHit,edm::StrictWeakOrdering<HBHERecHit> >')
        event.getByLabel(hltHcalRecHitsLabel, hltHcalRecHitsHandle)
        try:
          hltHcalRecHits = hltHcalRecHitsHandle.product()
          hltHcalRecHitsVars = []
          for hltHcalRecHit_idx in range(len(hltHcalRecHits)):
            hltHcalRecHit = hltHcalRecHits[hltHcalRecHit_idx]
            hltHcalRecHitsVars += [(hltHcalRecHit.id().rawId(), hltHcalRecHit.chi2(), hltHcalRecHit.energy(), hltHcalRecHit.eraw())]
          hltHcalRecHitsVars = sorted(hltHcalRecHitsVars, key=lambda x: x[0])
          for rh_id,rh_chi2,rh_e,rh_eraw in hltHcalRecHitsVars:
            print(f' {rh_id: >8d} {rh_chi2: >14.4f} {rh_e: >11.4f}')# {rh_eraw: >11.4f}')
        except:
          print(hltHcalRecHitsLabel, ': N/A')

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

   SHOW_EVERY = opts.every
   if SHOW_EVERY <= 0:
     print(log_prx+'invalid (non-positive) value for option "-e/--every" ('+str(SHOW_EVERY)+'), value will be changed to 100')
     SHOW_EVERY = 1e2

   if len(opts_unknown) > 0:
     raise RuntimeError(log_prx+'unrecognized command-line arguments: '+str(opts_unknown))

   ## histograms
   nEvtProcessed = 0

   for i_inpf in INPUT_FILES:

       if opts.verbosity >= 11:
         print(f'[input] {os.path.relpath(i_inpf)}')

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
   print(f'Events processed = {nEvtProcessed}')
