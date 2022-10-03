#!/bin/bash

mkdir -p venv/
pushd venv/
python3 -m venv .
popd
source venv/bin/activate
pip install -r requirements.txt
python monitor.py
