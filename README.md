# faam-wxrx
Processing for the FAAM Weather Radar.

This package provides software to decode the raw ARINC708 data recorded on the FAAM wxrx machine.
These are typically files of the form XXXXX.tmp, which contain the data, and <fltnum>.log, which
provides a file size log used to produce a timestamp for the data.

## Dependencies
This code requires the `faam_data` and `vocal` libraries to be installed, along with `tqdm`.

## Usage
```
faam_wxrx.py [-h] --tmpfile tmpfile [tmpfile ...] --logfile logfile --corefile corefile 
             [--output-dir output_dir]

Process raw WxRx data from the FAAM aircraft.

options:
  -h, --help            show this help message and exit
  --tmpfile tmpfile [tmpfile ...], -t tmpfile [tmpfile ...]
                        One or more raw ARINC 708 tmp file(s)
  --logfile logfile, -l logfile
                        The log file
  --corefile corefile, -c corefile
                        The FAAM (1hz) core file
  --output-dir output_dir, -o output_dir
                        The output directory
```
