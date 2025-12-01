#!/usr/bin/env python3

import os
import sys
import FWCore.ParameterSet.Config as cms

def main():
    cmssw_base = os.environ.get("CMSSW_RELEASE_BASE")
    if not cmssw_base:
        print("ERROR: CMSSW_RELEASE_BASE not set")
        sys.exit(1)

    cfg_path = os.path.join(
        cmssw_base,
        "src/HLTrigger/Configuration/test/OnLine_HLT_GRun.py"
    )

    print(f"Loading {cfg_path}")

    namespace = {"cms": cms}

    with open(cfg_path) as f:
        exec(f.read(), namespace)

    process = namespace.get("process")
    if process is None:
        print("ERROR: process object not found")
        sys.exit(1)

    # --- Correct modules lookup ---
    # EDFilters live in process._Process__filters (dict: name -> module)
    filters = process._Process__filters

    matches = []
    for name, module in filters.items():
        if hasattr(module, "saveTags"):
            matches.append(name)

    # Write results
    logfile = "filters_with_saveTags.log"
    with open(logfile, "w") as out:
        for m in matches:
            out.write("fullname:"+m + "\n")

    print(f"Found {len(matches)} EDFilters with saveTags")
    print(f"Saved to {logfile}")

if __name__ == "__main__":
    main()
