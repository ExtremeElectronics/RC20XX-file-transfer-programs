import serial
import io
import time
import base64
import sys
import argparse
import os.path
import RCxxSerial

StartToken = "&&&-magic-XXX"
Speed=115200

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [PORT] [DRIVE] [filepath]...",
        description="Copy file to CPM Drive on RC20XX."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument('-debug', help="Set Debug",action='store_true')
    
    parser.add_argument('port', help="Com or TTY port with an RC20XX attached")
    parser.add_argument('drive', help="CPM Drive on the Attached RC20XX")
    parser.add_argument('filepath', help="local CPM file and file to save on the Attached RC20XX")
    
    return parser

parser = init_argparse()
args = parser.parse_args()

debug=args.debug
RCxxSerial.debug=debug

bufsize=(4*1024) #needs to be EXACTLY 4096  else cpmWrite fails

zork=96000
totalsize=0

serialport=args.port 
if serialport=="": serialport="COM1"

drive=args.drive.upper()
if drive=="": drive="A"

filepath=args.filepath
filename=os.path.basename(filepath)
if debug: print(filepath,filename)

if filename=="":sys.exit(1)
if len(filename)>12:
    print("filename needs to be 8.3 formatted")
    sys.exit(1)

#Time the transfer
start = time.time()

#Do Copy to

totalsize=RCxxSerial.DoCopyTo(serialport,Speed,StartToken,drive,filepath,filename,bufsize)

end = time.time()
print (filepath+" Sent")
bps=totalsize/(end-start)
print("%d Bytes in %0.3f Seconds, %0.0f B/s (%0.3f Z/s) " %(totalsize,end-start,bps,bps/zork))
      





