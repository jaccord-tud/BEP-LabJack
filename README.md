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
usage: loadcell.py [-h] [-g] [-f [PATH]] [-d] [-p PRECISION] [-c CHANNEL]
                   [-r RATE] [--v-min V_MIN] [--v-max V_MAX]

optional arguments:
  -h, --help            show this help message and exit
  -g, --graph           show live graph
  -f [PATH], --file [PATH]
                        save to CSV file (omit PATH for datetime-stamped
                        filename)
  -d, --detached        don't write data to stdout
  -p PRECISION, --precision PRECISION
                        decimal places (default: 4)
  -c CHANNEL, --channel CHANNEL
                        AIN channel (default: 0)
  -r RATE, --rate RATE  sample rate in Hz (default: 20.0)
  --v-min V_MIN         min voltage (default: 0.0)
  --v-max V_MAX         max voltage (default: 10.0)
```
