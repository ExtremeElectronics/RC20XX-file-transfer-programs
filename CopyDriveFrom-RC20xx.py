import base64
import argparse
import time
import serial
import io
import sys
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
Speed = 115200


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [PORT] [DRIVE] ...",
        description="copy CPM Drive on RC20XX to local directory."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version=f"{parser.prog} version 1.0.0"
    )
    parser.add_argument('-debug', help="Set Debug",action='store_true')
    
    parser.add_argument('port', help="Com or TTY port with an RC20XX attached")
    parser.add_argument('drive', help="CPM Drive on the Attached RC20XX")
    parser.add_argument('directory', help="Local Directory to save files into")
    
    return parser


def DoExec(cmd):
    stream = os.popen(cmd)
    output = stream.read()
    if debug:print(cmd)
    print(output)


# Get Command line
parser = init_argparse()
args = parser.parse_args()

debug = args.debug

serialport = args.port
if serialport == "": serialport="COM1"

drive=args.drive.upper()
if drive == "": drive = "A"

path=args.directory
if not os.path.isdir(path):
    print("Path does not exist")
    sys.exit(1)


b64ls=RCxxSerial.DoLS(serialport, Speed, StartToken, drive)

if debug: print("b64", b64ls)

#decode message
try:
    message_bytes = base64.b64decode(b64ls)
except:
    print("decode failed ",b64ls)
    sys.exit(1)
  
# print it

directory = message_bytes.decode('utf_8')

filenames = RCxxSerial.DirectoryToFilenames(directory)
      
db = " "
if debug: db = " -d "
    
for file in filenames:
    print(path, file)
    pathfile = os.path.join(path, file)
    pythonpath = sys.executable
    cmd = pythonpath +" CopyFrom-RC20xx.py " + serialport + db + drive + " " + pathfile
    DoExec(cmd)
    time.sleep(0.1)    

