#!/bin/bash -ex

hltConfigFromDB --configName /dev/CMSSW_15_1_0/HLT > hlt_full.py 

cat <<@EOF >> hlt_full.py
from HLTrigger.Configuration.common import *
# Replace specialized SoA Alpaka plugin type names with the generic plugin name,
# preserving all existing module parameters. This handles multiple representations
# that may appear in the menu (plain plugin name, plugin@library, fully-qualified).
def _replace_plugin_type_on_prod(prod, new_plugin_name):
    """
    Try multiple common attribute names that store the plugin/C++ type in the
    python description of a module and replace it with new_plugin_name.
    This keeps all other parameters unchanged.

    IMPORTANT: do NOT overwrite callable attributes (like the type_() method).
    Overwriting type_ with a cms.string would shadow the method and break
    dumpPython (TypeError: 'string' object is not callable). Instead prefer to
    set a non-callable backing attribute if present (e.g. _TypedParameterizable__type)
    or only update non-callable attributes (ComponentType, pluginType).
    """
    # Common attributes that might be used to indicate the C++ plugin/type
    possible_attrs = ['pluginType', 'ComponentType', 'type', 'type_']
    for attr in possible_attrs:
        if hasattr(prod, attr):
            current = getattr(prod, attr)
            # If the attribute is callable (e.g. the type_() accessor), don't overwrite it.
            if callable(current):
                continue
            try:
                # For regular cms.string-like attributes we assign a cms.string
                setattr(prod, attr, cms.string(new_plugin_name))
                return True
            except Exception:
                # if direct assignment fails, continue trying other attributes
                pass

    # Some Parameterizable objects encode their type in a private name.
    # This is the preferred place to set the plain Python string type name, because
    # it doesn't shadow the callable accessors used by dumpPython.
    try:
        # e.g. _TypedParameterizable__type is used internally in some objects
        if hasattr(prod, '_TypedParameterizable__type'):
            setattr(prod, '_TypedParameterizable__type', new_plugin_name)
            return True
    except Exception:
        pass

    return False

def customizeHLTReplaceSoAAlpakaPlugins(process):
    """
    For each instance in the menu of:
      - PixelTrackProducerFromSoAAlpakaPhase1
      - PixelTrackProducerFromSoAAlpakaPhase2
      - PixelTrackProducerFromSoAAlpakaHIonPhase1

    substitute its C++ plugin/type to:
      - PixelTrackProducerFromSoAAlpaka

    And similarly for rechit producers:
      - SiPixelRecHitFromSoAAlpakaPhase1
      - SiPixelRecHitFromSoAAlpakaPhase2
      - SiPixelRecHitFromSoAAlpakaHIonPhase1

    substitute to:
      - SiPixelRecHitFromSoAAlpaka

    All other parameters of the modules are left unchanged.
    """
    # mapping old base names -> new base name
    replacements = {
        'PixelTrackProducerFromSoAAlpakaPhase1': 'PixelTrackProducerFromSoAAlpaka',
        'PixelTrackProducerFromSoAAlpakaPhase2': 'PixelTrackProducerFromSoAAlpaka',
        'PixelTrackProducerFromSoAAlpakaHIonPhase1': 'PixelTrackProducerFromSoAAlpaka',
        'SiPixelRecHitFromSoAAlpakaPhase1': 'SiPixelRecHitFromSoAAlpaka',
        'SiPixelRecHitFromSoAAlpakaPhase2': 'SiPixelRecHitFromSoAAlpaka',
        'SiPixelRecHitFromSoAAlpakaHIonPhase1': 'SiPixelRecHitFromSoAAlpaka',
    }

    # for each old plugin name, consider multiple ways it can appear in the menu
    variants_suffixes = ['', '@alpaka', 'alpaka_serial_sync::']

    for old_base, new_base in replacements.items():
        # produce variants like 'OldName', 'OldName@alpaka', 'alpaka_serial_sync::OldName'
        variants = [old_base, old_base + '@alpaka', 'alpaka_serial_sync::' + old_base]
        for variant in variants:
            for prod in producers_by_type(process, variant):
                replaced = _replace_plugin_type_on_prod(prod, new_base)
                # If the direct attribute replacement failed, as a last resort try to
                # recreate the module with same parameters but new plugin type.
                if not replaced:
                    try:
                        # attempt to clone by creating a new EDProducer with same parameters
                        # This fallback only works if prod is a cms._Module and has pythonType/parameters.
                        params = {}
                        # collect parameters defined on the product
                        for p in prod.parameterNames_():
                            params[p] = getattr(prod, p)
                        # create a new cms.EDProducer with the new plugin name preserving parameters
                        new_mod = cms.EDProducer(new_base, **params)
                        # now replace the object in the process by name
                        # find the label(s) in the process that reference this prod object
                        for label, obj in list(process._Process__producers.items()):
                            if obj is prod:
                                setattr(process, label, new_mod)
                                break
                        for label, obj in list(process._Process__psets.items()):
                            if obj is prod:
                                setattr(process, label, new_mod)
                                break
                    except Exception:
                        # give up silently; don't break workflow
                        pass

    return process
    
process = customizeHLTReplaceSoAAlpakaPlugins(process)
@EOF
edmConfigDump hlt_full.py > hlt.py
