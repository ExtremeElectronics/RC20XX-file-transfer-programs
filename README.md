# RC20XX-file-transfer-programs
Python programs to transfer CPM files to/from PC to RC2040 and RC2014 with an XK SD card interface.

Transfer / delete/ list files via the serial port (or usb serial port) 

The port needs to be the COM port connected to the RC20xx, the program needs exclusive access to this port, no other serial program must be running
On Windoes machines the com port will be of the form COMxx 
On Linux machines the port will be obvious to anyone that uses linux :) ( something like tty1, I haven't tried this yet)

In all cases the file path is for the machine running the python program. 
The filename part of the filepath will be used as the CPM file name when the file is transferred

Drive letters are from A to P and are required for all programs except EXIT

The SD card must be using an img style CPM image and you will need to add the img diskdefs to your SD card from https://github.com/ExtremeElectronics/RC2040/blob/main/DiskDefs/RC2040img_diskdefs.txt to a file called diskdefs (no extension)

## RM-RC20xx.py
Removes a file on the host CMP system 
Takes COM port CPM Drive letter and CPM filename

## CopyFrom-RC20xx.py
Copy Filename From the RC20xx to your host 
Takes COM port CPM Drive letter and a destination path/filename
The filename will be the same in the host and CPM Source file system.
The path is only used on the host.

## CopyTo-RC20xx.py
Copy Filename To the RC20xx from your host 
Takes COM port CPM Drive letter and a destination path/filename
The filename will be the same in the Source CPM file system and host 
the path is only used on the host.

## LS-RC20xx.py
Lists a directory on the CPM Filesystem 
Takes COM port CPM Drive letter

## EXIT-RC20xx.py
Sends a code to release the RC2040 from serial file mode. (not needed on the RC2014)
