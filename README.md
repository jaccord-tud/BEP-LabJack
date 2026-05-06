# BEP LabJack

- Read, plot, and save loadcell measurements
- Control linear actuator

## Requirements

- Python 3.x
- LabJack drivers
    - Linux/macOS: Exodriver
    - Windows: UD Driver
- LabJackPython

## Setup (macOS)

1. Install Exodriver

```
$ brew install exodriver
```

2. Install required Python libraries

```
$ pip install -r requirements.txt
```

## Usage

```
$ python loadcell.py -h
usage: loadcell.py [-h] [-g] [-f] [-d]

optional arguments:
  -h, --help  show this help message and exit
  -g          show live graph
  -f          save to CSV file
  -d          detached: don't write data to stdout
```
