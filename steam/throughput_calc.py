#!/usr/bin/env python3
import sys

timingServer_throughput = float(sys.argv[1])

timingServer_extraOverhead_sec = 0.04

n_threads = 256

n_nodes = 200

extra_proc_power = 1.2

safety_margin = 0.9

throughput_corrected = n_threads / ((n_threads / timingServer_throughput) - timingServer_extraOverhead_sec)

full_hlt_throughput = timingServer_throughput * n_nodes * extra_proc_power * safety_margin / 1000.
full_hlt_throughput_corrected = throughput_corrected * n_nodes * extra_proc_power * safety_margin / 1000.

print(f'Throughput (Timing Server): {full_hlt_throughput:>8.1f} kHz')
print(f'Throughput (Corrected)    : {full_hlt_throughput_corrected:>8.1f} kHz')
