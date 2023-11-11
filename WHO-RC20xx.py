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
        usage="%(prog)s [PORT] ...",
        description="Return System Name for RC20XX."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version=f"{parser.prog} version 1.0.0"
    )
    parser.add_argument('-debug', help="Set Debug",action='store_true')
    
    parser.add_argument('port', help="Com or TTY port with an RC20XX attached")
 
    return parser


def DoExec(cmd):
    stream = os.popen(cmd)
    output = stream.read()
    print(cmd)
    print(output)

#Get Command line
parser = init_argparse()
args = parser.parse_args()

debug=args.debug

serialport = args.port
if serialport == "": serialport = "COM1"

# Do the WHO 
who = RCxxSerial.DoWho(serialport,Speed,StartToken)

# print it
print("WHO:", who)

