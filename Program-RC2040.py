import serial
import io
import time
import base64
import sys
import argparse
import os.path
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
        usage="%(prog)s [PORT] [Address] [filepath]...",
        description="Program Ram/ROM directly on RC2040."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version=f"{parser.prog} version 1.0.0"
    )
    parser.add_argument('-debug', help="Set Debug", action='store_true')

    parser.add_argument('port', help="Com or TTY port with an RC20XX attached")
    parser.add_argument('Address', help="Base address for bin transfer in HEX (0-65535")
    parser.add_argument('filepath', help="local BIN file to save to the Address in RAM/ROM on the RC2040")

    return parser


parser = init_argparse()
args = parser.parse_args()

debug = args.debug
RCxxSerial.debug = debug

totalsize = 0

serialport = args.port
if serialport == "": serialport = "COM1"

Address = int(args.Address, 16)  # convert to decimal

filepath = args.filepath
filename = os.path.basename(filepath)
if debug: print(filepath, filename)

if filename == "": sys.exit(1)

if os.path.isfile(filepath) == False:
    print("File doesn't Exist ", filepath)
    sys.exit(1)

if (Address<0 or Address>65535):
    print("Address Out of range ", Address)
    sys.exit(1)

# Time the transfer
start = time.time()

# Do Copy to
if debug: print("Sending to RCxxSerial")
totalsize = RCxxSerial.DoProgram(serialport, Speed, StartToken, filepath, Address)

end = time.time()
print(filepath + " Sent")
print("%d Bytes sent  " % totalsize)





