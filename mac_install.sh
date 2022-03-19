#!/bin/bash

python3 -m venv ./venv
source venv/bin/activate
python --version
pip install uvicorn
pip install pip-tools
pip install -r requirements.txt
pip install -r src/api/requirements.txt


#cd src/frontend
#nvm use 16.13.2
#npm install
#cd ../..