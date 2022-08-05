# RC20XX Fast File Serial transfer programs
Python programs to transfer CPM files to/from PC to RC2040 (https://github.com/ExtremeElectronics/RC2040) and RC2014 SD Card interface(https://github.com/ExtremeElectronics/Pico-SD--IDE-interface--for-Rc2014) with an XK SD card interface.

Transfer / delete/ list / cat files via the serial port (or usb serial port) 

## Your RC20xx needs to reliably boot into and run CP/M before trying to use these tools

The port needs to be the COM port connected to the RC20xx, the program needs exclusive access to this port, no other serial program must be running.
On Windows machines the com port will be of the form COMxx 
On Linux machines the port will be similar to /dev/ttyAMA0 (USB on a pi) , /dev/tty0 or /dev/ttyS0  

In all cases the file path is for the machine running the python program. 
The filename part of the filepath will be used as the CPM file name when the file is transferred

Drive letters are from A to P and are required for all programs except EXIT

The SD card must be using an img style CPM image and you will need to add the img diskdefs to your SD card from https://github.com/ExtremeElectronics/RC2040/blob/main/DiskDefs/RC2040img_diskdefs.txt to a file called diskdefs (no extension)

You need to update your Pico to the latest RC2040 software, currently found in the main (until I make a release)

The SD card must have a valid DiskDef File
### DISKDEF WARNING ###
The diskdefs file must have lines terminated in LF ONLY, don't copy/paste the file into an editor then save, it may change them to CRLF's 
Download and Save as RAW

## Python instalation

These scripts need python3.6 or greater and you may also need to add in the pyserial module "pip install pyserial"
and the tkinterdnd2 module for the ffsexplorer "pip install tkinterdnd2"

# GUI Programs

## ffsexplorer.py
A GUI to try to tie everything following together. Probably the easyest one to start with now.
Connect by selecting a com port (top right)
Select the drive with the CPM Dive dropdown
Drop files to the black and green directory display to upload files to your RC20xx
Select files in the directory display and click on the buttons on the left to Erase, Copy slected files to a directory on your computer.
Disconnect to detach from the com port (and exit from file transfer on an RC2040) 

## Port Monitor
Monitors Serial ports and displays current ports attached, and any newly connected ports are highlighted.

# CLI Progams
These are for your own automation. be carefull with the options, they are currently not agressivly checked for sanity. 

## RM-RC20xx.py
Removes a file on the host CMP system 
Arguments of COM port CPM Drive letter and CPM filename required

## CopyFrom-RC20xx.py
Copy Filename From the RC20xx to your host 
Arguments of  COM port , CPM Drive letter and a destination path/filename required
The filename will be the same in the host and CPM Source file system.
The path is only used on the host.

## CopyTo-RC20xx.py
Copy Filename To the RC20xx from your host 
Arguments of COM port , CPM Drive letter and a destination path/filename required
The filename will be the same in the Source CPM file system and host 
the path is only used on the host.

## LS-RC20xx.py
Lists a directory on the CPM Filesystem 
Arguments of COM port and CPM Drive letter required

## EXIT-RC2040.py
Sends a code to release the RC2040 from serial file mode. (not needed on the RC2014)
Argument, needs com port only 

## WHO-RC20xx.py
Returns RC2040 or RC2014 depending on the device the COM port is connected to
Argument, needs com port only 

# Transfer Speed
CopyTo and CopyFrom give an idea of transfer speed. 
around 15Kb/s (0.16 Z/s)* should be doable for CopyTo 
and 52Kb/s (0.53 Z/s)* for CopyFrom

*Zorks a second, where 1 ZORK=96K

Non Transfer Programs.

# WATCH-RC2040.py
Sets a memory watch on an RC2040 ONLY
Arguments, needs com port and Hex Watch Address
