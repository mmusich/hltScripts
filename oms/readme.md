```bash
git clone https://gitlab.cern.ch/cmsoms/oms-api-client.git
cd oms-api-client
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
python3 -m pip install -r requirements.txt
export PYTHONPATH="${HOME}"/.local/lib/python3.6/site-packages/:${PYTHONPATH}
python3 setup.py install --user
cd ..
```

```bash
source oms-api-client/venv/bin/activate
export PYTHONPATH="${HOME}"/.local/lib/python3.6/site-packages/:${PYTHONPATH}
```
