#!/bin/bash
source ~/.virtualenvs/venv/bin/activate
nohup python main.py > log.txt 2>&1 &

