# Installation

To install, clone the repo and install with

> pip install -e .

Or you can do

> pip install git+https://github.com/tddesjardins/romcom_time

# Usage

To convert times, at the command line type:

> tcomm {time} {time_system}

where `{time}` is a string of particular format and `{time_system}` is one of:
- EASTERN
- UTC
- DOY
- MET 
DOY is day of year and MET is mission elapsed time since launch. The EASTERN option naturally updates with daylight savings time. Before November 1, 2026 02:00 AM it will be EDT and then it will transition to EST.

The format of `{time}` depends on the input:
- EASTERN & UTC = ISOT string (e.g., YYYY-MM-DDTHH:MM:SS)
- DOY = DDD/HH:MM:SS
- MET = D.DD, i.e., a floating point number of days

Example: 

> tcomm 257/05:00:00 DOY

Returns:
```
EASTERN (EDT): 2026-09-14T01:00:00
UTC: 2026-09-14T05:00:00
MET: 14.73
DOY (UTC): 257/05:00:00
```