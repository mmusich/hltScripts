
```bash
for fff in $(ls /eos/cms/store/group/tsg/FOG/error_stream_root/run380360/*root); do
  foo=${fff/.root/}
  bar=$(basename $foo)
  ../../../hltScripts/crashes/test_run380360.sh file:$fff $bar
done
unset fff foo bar
```
