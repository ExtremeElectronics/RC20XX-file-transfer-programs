# RC20XX-file-transfer-programs
Python programs to transfer CPM files to/from PC to RC2040 and RC2014

Transfer / delete/ list files via the serial port (or usb serial port) 

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
