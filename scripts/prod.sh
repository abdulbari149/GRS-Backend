#!/bin/sh
echo "Running production build"
# use pm2 to start python flask app
source env/bin/activate
pip install -r requirements.txt
# run app.py with pm2
pm2 start app.py --interpreter=env/bin/python3 --name="grs" 