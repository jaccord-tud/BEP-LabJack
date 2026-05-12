set windows-shell := ["powershell", "-Command"]

# default: setup and loadcell
default:
    just setup
    just loadcell -gfd

# set up venv and install required packages
setup:
    python3 -m venv .venv
    .venv/bin/python -m pip install --upgrade pip
    .venv/bin/pip install -r requirements.txt

# clean up venv
clean:
    rm -rf .venv

# python interpreter
python:
    .venv/bin/python

# `read.py`: live loadcell readout
read ARGS="":
    .venv/bin/python src/read.py {{ARGS}}

# `loadcell.py`: advanced loadcell logging and graphing
loadcell ARGS="":
    .venv/bin/python src/loadcell.py {{ARGS}}

# `actuator.py`: control actuator
actuator ARGS="":
    .venv/bin/python src/actuator.py {{ARGS}}

# list available recipes
help:
    @just --list --unsorted
