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
        usage="%(prog)s [PORT] ...",
        description="EXIT Serial File Mode on RC2040."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument('-debug', help="Set Debug", action='store_true')
    
    parser.add_argument('port', help="Com or TTY port with an RC20XX attached")
    return parser

#Get Command line
parser = init_argparse()
args = parser.parse_args()

debug = args.debug

serialport = args.port
if serialport == "": serialport = "COM1"
# close port
RCxxSerial.DoExit(serialport, Speed)

print("EXIT")



