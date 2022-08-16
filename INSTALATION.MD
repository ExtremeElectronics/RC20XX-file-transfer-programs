# Python instalation

As with most python programs, the issue is not with the programs, but getting a working set of python modules and paths

### All tools
These tools need python3.6 or greater. Currently there are some issues that appear under the GUI in Linux, I'm looking in to these.

All of the tools require the pyserial module, this is usually installed with pip or pip3
e.g. "pip3 install pyserial"

### Windows/X GUI tools
For these you will need tkinter, in windows this is provided along with the python package. 
In Linux you may have to add this to your OS as a installable "package" in your OS's package manager
e.g apt-get install python-tk 

For ffexplorer you will need the tkinterdnd2 package this is usually installed with pip or pip3
e.g. "pip3 install tkinterdnd2"

The ffsexplorer.py uses 'Courier' as fixed width font, Its helps formatting if this font is available in X. 

## Linux Permissions 
if you get a permission denied error when accessing the port, ensure the user is a member of the dialout group

## Apple MAC / IPAD 
Glad you asked, not a clue :) but I'm sure with a bit of python knoledge they are installable. 
If you have a method that works, please contact me and I'll add it here

## Raspberry PI and 32bit systems. 
installing tkinterdnd2 with pip, appears to load the 64 bit version, even if you have a 32bit OS and therefore won't run. I suspect this may be the same for other 32bit systems. This only affects ffsexplorer.py
Sorry no fix for this currently
