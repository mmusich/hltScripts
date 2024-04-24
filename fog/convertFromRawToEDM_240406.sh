#!/bin/bash

for fff in $(ls /eos/cms/store/group/tsg/FOG/error_stream/run378*/*raw); do
  ddd=${fff/error_stream/error_stream_root}
  ddd=${ddd/raw/root}
  mkdir -p $(dirname ${ddd})
  cmsRun ../../../hltScripts/fog/convertFromRawToEDM.py ${fff} ${ddd}
done
unset fff
