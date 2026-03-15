#!/bin/bash

cd /root/to-do-list

git fetch origin
git reset --hard origin/main
git clean -fd

source .venv/bin/activate
pip install -r requirements.txt

sudo systemctl restart todo