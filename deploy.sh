#!/bin/bash
cd /root/to-do-list
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart todo