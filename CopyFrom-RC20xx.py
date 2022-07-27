import serial
import io
import time
import base64
import sys
import argparse
import os
import RCxxSerial


#     ________________________________
#    /                                |
#   /       RC20xx  FFS tools         |
#  /         Derek Woodroffe          |
# |  O        Extreme Kits            |
# |     Kits at extkits.uk/RC2040     |
# |               2022                |
# |___________________________________|
#   | | | | | | | | | | | | | | | | |

# https://github.com/ExtremeElectronics/RC20XX-file-transfer-programs

StartToken = "&&&-magic-XXX"
Speed=115200

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [PORT] [DRIVE] [filepath] ...",
        description="Copy file from CPM Drive on RC20XX."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument('-debug', help="Set Debug",action='store_true')
    

    parser.add_argument('port', help="Com or TTY port with an RC20XX attached")
    parser.add_argument('drive', help="CPM Drive on the Attached RC20XX")
    parser.add_argument('filepath', help="local file path to save the file to")
    
    return parser

parser = init_argparse()
args = parser.parse_args()

debug=args.debug
RCxxSerial.debug=debug

zork=96000
totalsize=0

serialport=args.port
if serialport=="": serialport="COM1"

drive=args.drive.upper()
if drive=="": drive="A"

filepath=args.filepath
filename=os.path.basename(filepath)

if debug:print(filepath,filename)

if filename=="":
    print ("Filename can't be empty")
    sys.exit(1)
    
if len(filename)>12:
    print ("Filename must be 8.3 formatted")
    sys.exit(1)

start = time.time()

#Do Copy From
b64from=RCxxSerial.DoCopyFrom(serialport,Speed,StartToken,drive,filename)

if debug :print("b64",b64ls)

try:
  message_bytes = base64.b64decode(b64from)
except:
  print("base 64 decode failed ",b64from)
  sys.exit(1)

end = time.time()
if debug:print(message_bytes.decode('utf_8'))
  
if len(message_bytes)<2:
    print ("File empty Save aborted")
    sys.exit(1)

localfile = open(filepath, "wb")
localfile.write(message_bytes)
localfile.close()
totalsize=len(message_bytes)

print (filepath+" Saved")
bps=totalsize/(end-start)
print("%d Bytes in %0.3f Seconds, %0.0f B/s (%0.3f Z/s) " %(totalsize,end-start,bps,bps/zork))
 

if debug: print("in ",end-start);

