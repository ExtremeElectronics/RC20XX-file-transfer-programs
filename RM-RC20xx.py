import serial
import io
import time
import base64
import sys
import argparse
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
        description="Remove CPM File on RC20XX."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version=f"{parser.prog} version 1.0.0"
    )
    parser.add_argument('-debug', help="Set Debug",action='store_true')

    parser.add_argument('port', help="Com or TTY port with an RC20XX attached")
    parser.add_argument('drive', help="CPM Drive on the Attached RC20XX")
    parser.add_argument('filename', help=" CPM file to delete on the Attached RC20XX")
    
    return parser

parser = init_argparse()
args = parser.parse_args()

debug=args.debug
RCxxSerial.debug=debug

serialport = args.port
if serialport == "": serialport="COM1"
drive = args.drive.upper()
if drive == "": drive="A"

filename=args.filename

if filename == "":
    print("Filename can't be empty")
    sys.exit(1)
    
if len(filename) > 12:
    print("Filename must be 8.3 formatted")
    sys.exit(1)

#Do RM
RCxxSerial.DoRM(serialport, Speed, StartToken, drive, filename)

print("Removed", filename)


