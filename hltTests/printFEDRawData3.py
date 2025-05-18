#!/usr/bin/env python3
import os
import argparse
import glob
import ROOT

from DataFormats.FWLite import Runs, Events, Handle

### Event Analysis
def getRawData(label):
  handle = Handle('FEDRawDataCollection')
  event.getByLabel(label, handle)
  return handle.product()

def analyse_event(event, eventSizeDict, verbosity=0):

#    print('-'*50)
#    print('Run             =', event.eventAuxiliary().run())
#    print('LuminosityBlock =', event.eventAuxiliary().luminosityBlock())
#    print('Event           =', event.eventAuxiliary().event())
#    print('-'*50)

    rawData1 = getRawData('rawDataCollector::LHC')

    for fedId in range(4096+1):
        f1 = rawData1.FEDData(fedId)
        s1 = f1.size()

        eventSizeDict['Total'] += s1

        eventSizeDict[fedId] += s1

### main
if __name__ == '__main__':
   ### args
   parser = argparse.ArgumentParser()

   parser.add_argument('-i', '--inputs', dest='inputs', required=True, nargs='+', default=None,
                       help='path to input .root file(s)')

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

   evtSizeDict = {'Total': 0.}
   for fedId in range(4096+1):
       evtSizeDict[fedId] = 0.

   nEvtProcessed = 0
   for i_inpf in INPUT_FILES:
       if opts.verbosity >= 10:
         print('[input]', os.path.relpath(i_inpf))

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

#         if (not (eventIndex % SHOW_EVERY)) and (eventIndex > 0):
#           print('-'*10)
#           print('Event #'+str(eventIndex))

         analyse_event(event=event, eventSizeDict=evtSizeDict, verbosity=opts.verbosity)
         nEvtProcessed += 1
         eventIndex += 1

   print('='*30)
   print('Events processed =', nEvtProcessed)

   for foo in range(4096+1):
       frac = evtSizeDict[foo] / nEvtProcessed #/ 1024. / 1024.
       print(f'{foo: <20} {frac:>10.2f}')
