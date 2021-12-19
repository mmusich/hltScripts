#!/usr/bin/env python3
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
def analyse_event(event, verbosity=0):

    if verbosity >= 0:
      print('-'*50)
      print('Run             =', event.eventAuxiliary().run())
      print('LuminosityBlock =', event.eventAuxiliary().luminosityBlock())
      print('Event           =', event.eventAuxiliary().event())
      print('-'*50)

    if verbosity >= 0:
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

    hltTriggerSummaryInputTagLabel = 'hltTriggerSummaryAOD'
    hltTriggerSummaryHandle = Handle('trigger::TriggerEvent')
    event.getByLabel(hltTriggerSummaryInputTagLabel, hltTriggerSummaryHandle)
    hltTriggerSummary = hltTriggerSummaryHandle.product()

    trigProcessName = hltTriggerSummary.usedProcessName()
    trigSummarySizeFilters = hltTriggerSummary.sizeFilters()
    trigObjects = hltTriggerSummary.getObjects()

    if verbosity >= 0:
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

    if verbosity >= 0:
      for hltRecoTracksLabel in [
        'hltMergedTracks',
        'hltDoubletRecoveryPFlowCtfWithMaterialTracksForBTag',
        'hltDoubletRecoveryPFlowCtfWithMaterialTracksTauReg',
        'hltDoubletRecoveryPFlowTrackSelectionHighPurityForBTag',
        'hltDoubletRecoveryPFlowTrackSelectionHighPurityTauReg',
        'hltDoubletRecoveryTrackSelectionHighPurityDisplacedJpsiReg',
        'hltDoubletRecoveryTrackSelectionHighPurityDisplacedJpsiRegDoubleTrk',
        'hltDoubletRecoveryTrackSelectionHighPurityDisplacedNRReg',
        'hltDoubletRecoveryTrackSelectionHighPurityDisplacedPsiPrimeReg',
        'hltDoubletRecoveryTrackSelectionHighPurityDisplacedTau3muNoL1MassReg',
        'hltIter0IterL3FromL1MuonTrackSelectionHighPurity',
        'hltIter0IterL3FromL1MuonTrackSelectionHighPurityNoVtx',
        'hltIter0IterL3FromL1MuonTrackSelectionHighPurityOpenMu',
        'hltIter0IterL3MuonCtfWithMaterialTracks',
        'hltIter0IterL3MuonCtfWithMaterialTracksNoVtx',
        'hltIter0IterL3MuonCtfWithMaterialTracksOpenMu',
        'hltIter0IterL3MuonTrackSelectionHighPurity',
        'hltIter0IterL3MuonTrackSelectionHighPurityNoVtx',
        'hltIter0IterL3MuonTrackSelectionHighPurityOpenMu',
        'hltIter0L3MuonCtfWithMaterialTracks',
        'hltIter0L3MuonCtfWithMaterialTracksNoVtx',
        'hltIter0L3MuonTrackSelectionHighPurity',
        'hltIter0L3MuonTrackSelectionHighPurityNoVtx',
        'hltIter0PFlowCtfWithMaterialTracks',
        'hltIter0PFlowCtfWithMaterialTracksForBTag',
        'hltIter0PFlowCtfWithMaterialTracksTauReg',
        'hltIter0PFlowTrackSelectionHighPurityForBTag',
        'hltIter0PFlowTrackSelectionHighPurityTauReg',
        'hltIter1DisplacedJpsiCtfWithMaterialTracks',
        'hltIter1DisplacedJpsiCtfWithMaterialTracksDoubleTrk',
        'hltIter1DisplacedJpsiMerged',
        'hltIter1DisplacedJpsiMergedDoubleTrk',
        'hltIter1DisplacedJpsiTrackSelectionHighPurity',
        'hltIterL3MuonsFromL2NoVtx',
        'hltIterL3MuonsFromL2OpenMu',
        'hltIterL3OIL3Muons',
        'hltIterL3OIL3MuonsNoVtx',
        'hltIterL3OIL3MuonsOpenMu',
        'hltIterL3OIMuCtfWithMaterialTracks',
        'hltIterL3OIMuCtfWithMaterialTracksNoVtx',
        'hltIterL3OIMuCtfWithMaterialTracksOpenMu',
        'hltIterL3OIMuonTrackSelectionHighPurity',
        'hltIterL3OIMuonTrackSelectionHighPurityNoVtx',
        'hltIterL3OIMuonTrackSelectionHighPurityOpenMu',
        'hltL2CosmicMuons',
        'hltL2Muons',
        'hltL2MuonsAllBx',
        'hltL2MuonsOpenMu',
        'hltL2SelectorForL3IO',
        'hltL2SelectorForL3IONoVtx',
        'hltL2SelectorForL3IOOpenMu',
        'hltL3Muons',
        'hltL3MuonsIOHit',
        'hltL3MuonsIterL3IO',
        'hltL3MuonsIterL3IONoVtx',
        'hltL3MuonsIterL3IOOpenMu',
        'hltL3MuonsIterL3OI',
        'hltTripletRecoveryCtfWithMaterialTracksDisplacedJpsiRegDoubleTrk',
        'hltTripletRecoveryCtfWithMaterialTracksDisplacedNRReg',
        'hltTripletRecoveryCtfWithMaterialTracksDisplacedPsiPrimeReg',
        'hltTripletRecoveryCtfWithMaterialTracksDisplacedTau3muNoL1MassReg',
        'hltTripletRecoveryCtfWithMaterialTracksDisplacedTau3muReg',
        'hltTripletRecoveryMergedDisplacedJpsiReg',
        'hltTripletRecoveryMergedDisplacedJpsiRegDoubleTrk',
        'hltTripletRecoveryMergedDisplacedNRMuMuReg',
        'hltTripletRecoveryMergedDisplacedPsiPrimeReg',
        'hltTripletRecoveryMergedDisplacedTau3muNoL1MassReg',

        'hltMergedTracksPPOnAA',
        'hltL2MuonsPPOnAA',
#        'hltL3MuonsIOHit',
#        'hltL3MuonsIOHit:L2Seeded',

        'hltFullIter0CtfWithMaterialTracksPPOnAAForDmeson',
        'hltFullIter1CtfWithMaterialTracksPPOnAAForDmeson',
        'hltFullIter2CtfWithMaterialTracksPPOnAAForDmeson',
        'hltFullIter3CtfWithMaterialTracksPPOnAA',
        'hltFullIter4CtfWithMaterialTracksPPOnAA',
        'hltFullIter5CtfWithMaterialTracksPPOnAA',
        'hltFullIter6CtfWithMaterialTracksPPOnAA',
        'hltFullIter7CtfWithMaterialTracksPPOnAA',
        'hltFullIter8CtfWithMaterialTracksPPOnAA',
        'hltFullIter9CtfWithMaterialTracksPPOnAA',
        'hltFullIter10CtfWithMaterialTracksPPOnAA',

        'hltFullIter9CtfWithMaterialTracksPPOnAAForLowPt',
        'hltFullIterativeTrackingMergedPPOnAAForBTag',
        'hltFullIterativeTrackingMergedPPOnAAForDmeson',
        'hltFullIterativeTrackingMergedPPOnAAForDmesonNoIter10',
        'hltFullIterativeTrackingMergedPPOnAAForLowPt',
        'hltGoodHighPurityFullTracksForDmeson',
        'hltGoodHighPurityFullTracksForDmesonNoIter10',
        'hltGoodHighPurityFullTracksForHighPt',
        'hltGoodHighPurityFullTracksForHighPtNoIter10',
        'hltGoodHighPurityFullTracksForLowMultiplicity',
        'hltHIPixelTracksForTrackTrigger',
        'hltHIPixelTracksFromTripletsForTrackTrigger',
        'hltHIPixelTracksMergedForTrackTrigger',
        'hltIter0ElectronsCtfWithMaterialTracks',
        'hltIter0ElectronsTrackSelectionHighPurity',
        'hltIter0IterL3FromL1MuonCtfWithMaterialTracksPPOnAA',
        'hltIter0IterL3FromL1MuonTrackSelectionHighPurityPPOnAA',
        'hltIter0IterL3MuonCtfWithMaterialTracksPPOnAA',
        'hltIter0IterL3MuonTrackSelectionHighPurityPPOnAA',
        'hltIter1ElectronsCtfWithMaterialTracks',
        'hltIter1ElectronsPixelTracks',
        'hltIter1ElectronsTrackSelectionHighPurity',
        'hltIter1ElectronsTrackSelectionHighPurityLoose',
        'hltIter1ElectronsTrackSelectionHighPurityTight',
        'hltIter1ForElectronsMerged',
        'hltIter1MergedPPOnAA',
        'hltIter2ElectronsCtfWithMaterialTracks',
        'hltIter2ElectronsTrackSelectionHighPurity',
        'hltIter2ForElectronsMerged',
      ]:
        print('\n'+'-'*10)
        hltRecoTracksHandle = Handle('std::vector<reco::Track>')
        event.getByLabel(hltRecoTracksLabel, hltRecoTracksHandle)
        try:
          hltRecoTracks = hltRecoTracksHandle.product()
          for hltRecoTrack_idx in range(len(hltRecoTracks)):
            hltRecoTrack = hltRecoTracks[hltRecoTrack_idx]
            print(hltRecoTracksLabel+' #{:d}'.format(hltRecoTrack_idx), hltRecoTrack.pt(), hltRecoTrack.eta(), hltRecoTrack.phi())
        except:
          print(hltRecoTracksLabel, ': N/A')

      for hltRecoPixelSeedsLabel in [
        'hltFullIter0PixelSeedsPPOnAAForDmeson',
      ]:
        print('\n'+'-'*10)
        hltRecoPixelSeedsHandle = Handle('std::vector<TrajectorySeed>')
        event.getByLabel(hltRecoPixelSeedsLabel, hltRecoPixelSeedsHandle)
        try:
          hltRecoPixelSeeds = hltRecoPixelSeedsHandle.product()
          for hltRecoPixelSeed_idx in range(len(hltRecoPixelSeeds)):
            hltRecoPixelSeed = hltRecoPixelSeeds[hltRecoPixelSeed_idx]
            print(hltRecoPixelSeedsLabel+' #{:d}'.format(hltRecoPixelSeed_idx),
              hltRecoPixelSeed.nHits(), hltRecoPixelSeed.direction(), hltRecoPixelSeed.recHits())
        except:
          print(hltRecoPixelSeedsLabel, ': N/A')

      for hltRecoPixelSeedsLabel in [
        'hltFullIter0PixelHitQuadrupletsPPOnAAForDmeson',
      ]:
        print('\n'+'-'*10)
        hltRecoPixelSeedsHandle = Handle('std::vector<TrajectorySeed>')
        event.getByLabel(hltRecoPixelSeedsLabel, hltRecoPixelSeedsHandle)
        try:
          hltRecoPixelSeeds = hltRecoPixelSeedsHandle.product()
          for hltRecoPixelSeed_idx in range(len(hltRecoPixelSeeds)):
            hltRecoPixelSeed = hltRecoPixelSeeds[hltRecoPixelSeed_idx]
            print(hltRecoPixelSeedsLabel+' #{:d}'.format(hltRecoPixelSeed_idx),
              hltRecoPixelSeed.nHits(), hltRecoPixelSeed.direction(), hltRecoPixelSeed.recHits())
        except:
          print(hltRecoPixelSeedsLabel, ': N/A')



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
