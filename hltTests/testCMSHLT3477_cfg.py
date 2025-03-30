import FWCore.ParameterSet.Config as cms

process = cms.Process('TEST')

process.options.wantSummary = True

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = int( 1e4 )
process.MessageLogger.cerr.enableStatistics = False

process.source = cms.Source('EmptySource')

process.maxEvents.input = int( 1e5 )

process.PrescaleService = cms.Service("PrescaleService",
    lvl1Labels = cms.vstring( "A" ),
    lvl1DefaultLabel = cms.string( "A" ),
    forceDefault = cms.bool( True ),
    prescaleTable = cms.VPSet()
)

# Mock-up L1T menu.
# - 3 groups of algos (Standard, AXO, CICADA), 8 algos in total.
# - Path decision corresponds to prescale decision.
# - Different prescales applied to every Path.
prescalesDict = {
    'L1T_Standard_1': 61,
    'L1T_Standard_2': 67,

    'L1T_AXO_1': 71,
    'L1T_AXO_2': 73,
    'L1T_AXO_3': 79,

    'L1T_CICADA_1': 83,
    'L1T_CICADA_2': 89,
    'L1T_CICADA_3': 97,
}

for pathName in prescalesDict:
    process.PrescaleService.prescaleTable += [
        cms.PSet(
            pathName = cms.string( pathName ),
            prescales = cms.vuint32( prescalesDict[pathName] )
        ),
    ]
    prescaleModuleLabel = 'pre' + pathName.replace('_', '')
    setattr(process, prescaleModuleLabel, cms.EDFilter('HLTPrescaler'))
    setattr(process, pathName, cms.Path(getattr(process, prescaleModuleLabel)))

# TriggerResultsFilter expressions,
# using different combinations of the decisions of the mock-up L1T seeds
#  - Pure rates of the AXO and CICADA triggers are determined with 2 methods:
#    method #1 uses AND/NOT/OR and is assumed to return the correct results,
#    method #2 uses the MASKING operator to avoid explicit mentions of other triggers in the menu.
#  - The two methods are expected to give identical results.
#  - For both AXO and CICADA, a validation Path is included:
#    the Path is designed such that its decision for a given event
#    is "False" if method-1 and method-2 return different results;
#    it is expected that the decision of method-1 and method-2 will always be identical,
#    and so the validation Path should accept every event.
from HLTrigger.HLTfilters.triggerResultsFilter_cfi import triggerResultsFilter as _trigResFilter
_triggerResultsFilter = _trigResFilter.clone(
    usePathStatus = True,
    hltResults = '',
    l1tResults = '',
    throw = True
)

expressionsDict = {
    'All': 'L1T_*',
    'Standard': 'L1T_Standard_*',
    'AXO': 'L1T_AXO_*',
    'CICADA': 'L1T_CICADA_*',

    'PureRate_Method1_AXO': 'L1T_* AND NOT (L1T_Standard_* OR L1T_CICADA_*)',
    'PureRate_Method2_AXO': 'L1T_* AND NOT (L1T_* MASKING L1T_AXO_*)',
    'Validate_PureRate_AXO': 'NOT (PureRate_Method1_AXO XOR PureRate_Method2_AXO)',

    'PureRate_Method1_CICADA': 'L1T_* AND NOT (L1T_Standard_* OR L1T_AXO_*)',
    'PureRate_Method2_CICADA': 'L1T_* AND NOT (L1T_* MASKING L1T_CICADA_*)',
    'Validate_PureRate_CICADA': 'NOT (PureRate_Method1_CICADA XOR PureRate_Method2_CICADA)',
}

for pathName in expressionsDict:
    triggerResultsFilterModuleLabel = 'filter' + pathName.replace('_', '')
    setattr(process, triggerResultsFilterModuleLabel,
        _triggerResultsFilter.clone(triggerConditions = [expressionsDict[pathName]])
    )
    setattr(process, pathName, cms.Path(getattr(process, triggerResultsFilterModuleLabel)))
