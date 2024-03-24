# Latest Instructions
https://gitlab.cern.ch/cms-tsg/steam/timing/-/blob/master/README.md
https://twiki.cern.ch/twiki/bin/viewauth/CMS/TriggerStudiesTiming

# Quick Setup
```bash
git clone https://"${USER}"@gitlab.cern.ch/cms-tsg/steam/timing.git
python3 -m venv venv
source venv/bin/activate
pip3 install -r timing/requirements.txt
python3 timing/submit.py --show
```
