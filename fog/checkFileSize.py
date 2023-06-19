import os
import glob
import sys
# python3 -i list_size.py "/eos/cms/tier0/store/data/*/*/RAW/*/*/368/489/*/*.root"
# python3 -i list_size.py "/eos/cms/store/t0streamer/Data/*/*/368/489/*"
ret = sorted([(file_i, os.stat(file_i).st_size) for file_i in glob.glob(sys.argv[1])], key=lambda a: a[1])
