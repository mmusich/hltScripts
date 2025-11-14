#!/usr/bin/env python3
import os
import subprocess
import itertools
import tempfile

# ----------------------------------------------------------------------
# List of modifier combinations
# ----------------------------------------------------------------------

modifier_sets = [
    ["trackingLST"],
    ["trackingLST", "seedingLST"],
    ["singleIterPatatrack", "phase2CAExtension", "trackingLST"],
    ["singleIterPatatrack", "phase2CAExtension", "trackingLST", "seedingLST"],
    ["phase2CAExtension", "singleIterPatatrack", "trackingLST", "seedingLST",
     "trackingMkFitCommon", "hltTrackingMkFitInitialStep"],
]

# ----------------------------------------------------------------------
# Helper to generate filename-friendly tags
# ----------------------------------------------------------------------

def tag_from_modifiers(mods):
    return "_".join(mods)

# ----------------------------------------------------------------------
# Main loop
# ----------------------------------------------------------------------

for mods in modifier_sets:
    tag = tag_from_modifiers(mods)
    python_fname = f"hlt_{tag}.py"
    dump_fname   = f"dump_{tag}.py"
    html_out     = f"html_{tag}"

    print(f"\n=== Processing modifiers: {mods}")
    print(f"--> Python file: {python_fname}")
    print(f"--> Dump file:   {dump_fname}")
    print(f"--> HTML out:    {html_out}")

    # --------------------------------------------------------------
    # 1. Generate the python config
    # --------------------------------------------------------------

    with open(python_fname, "w") as f:
        f.write("import FWCore.ParameterSet.Config as cms\n\n")

        for mod in mods:
            f.write(f"from Configuration.ProcessModifiers.{mod}_cff import {mod}\n")

        # Build process line
        joined = ",".join(mods)
        f.write(f"\nprocess = cms.Process(\"HLT\", {joined})\n")
        f.write("process.load(\"HLTrigger.Configuration.HLT_75e33_cff\")\n")

    # --------------------------------------------------------------
    # 2. Run edmConfigDump
    # --------------------------------------------------------------

    print(f"    Running edmConfigDump for {python_fname} ...")
    with open(dump_fname, "w") as dumpfile:
        subprocess.run(["edmConfigDump", python_fname], stdout=dumpfile, check=True)

    # --------------------------------------------------------------
    # 3. Run py2html_refactor.py
    # --------------------------------------------------------------

    print(f"    Converting dump with py2html_refactor.py ...")
    subprocess.run([
        "python3",
        "py2html_refactor.py",
        "-i", dump_fname,
        "-o", html_out
    ], check=True)

    print(f" Done: {html_out}")

print("\nALL DONE.")
